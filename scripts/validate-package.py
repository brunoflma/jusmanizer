#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Confere a coerência do pacote jusmanizer.

  · mesma versão em SKILL.md (metadata.version), .claude-plugin/plugin.json e
    scripts/jusmanizer.py (VERSAO); o README é para o advogado e não carrega versão;
  · 32 padrões numerados sem lacuna (### J01 … ### J32) no SKILL.md;
  · nenhuma risca (travessão ou meia-risca) na prosa do SKILL.md fora de linha de exemplo
    (que começa por `>`), de tabela (`|`), de frontmatter e de trecho em código;
  · manifestos com nome `jusmanizer` e skills ["./"].

Exit 1 se algo divergir. Uso: python scripts/validate-package.py
"""
import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
falhas = []


def ler(rel):
    with open(os.path.join(RAIZ, rel), encoding="utf-8") as f:
        return f.read()


skill = ler("SKILL.md")
readme = ler("README.md")
plugin = json.loads(ler(".claude-plugin/plugin.json"))
market = json.loads(ler(".claude-plugin/marketplace.json"))
mod = ler("scripts/jusmanizer.py")

v_skill = re.search(r'^\s*version:\s*"([^"]+)"', skill, re.M)
v_mod = re.search(r'^VERSAO = "([^"]+)"', mod, re.M)
versoes = {v_skill and v_skill.group(1), plugin.get("version"), v_mod and v_mod.group(1)}
if len(versoes) != 1 or None in versoes:
    falhas.append(f"versões divergem entre SKILL.md, plugin.json e jusmanizer.py: {versoes}")

nums = [int(m) for m in re.findall(r"^### J(\d{2})\b", skill, re.M)]
if nums != list(range(1, 33)):
    falhas.append(f"padrões J01..J32 sem lacuna esperados no SKILL.md; achado {nums}")

# Prosa do SKILL.md sem risca. Pula frontmatter, linha de exemplo (`>`), tabela (`|`), bloco
# de código (```) e trecho em código inline (`…`), onde a risca é o objeto e não o vício.
em_frontmatter = False
em_codigo = False
for n, linha in enumerate(skill.splitlines(), 1):
    if n == 1 and linha.strip() == "---":
        em_frontmatter = True
        continue
    if em_frontmatter:
        if linha.strip() == "---":
            em_frontmatter = False
        continue
    if linha.strip().startswith("```"):
        em_codigo = not em_codigo
        continue
    if em_codigo or linha.startswith(">") or linha.startswith("|"):
        continue
    limpa = re.sub(r"`[^`]*`", "", linha)
    if "—" in limpa or "–" in limpa:
        falhas.append(f"SKILL.md:{n} tem risca na prosa (fora de exemplo): {linha.strip()[:70]}")

if plugin.get("name") != "jusmanizer" or plugin.get("skills") != ["./"]:
    falhas.append("plugin.json: name deve ser 'jusmanizer' e skills ['./']")
if market.get("name") != "jusmanizer" or not any(
        p.get("name") == "jusmanizer" for p in market.get("plugins", [])):
    falhas.append("marketplace.json: name e plugins[].name devem ser 'jusmanizer'")
if not re.search(r"^name:\s*jusmanizer\s*$", skill, re.M):
    falhas.append("SKILL.md: frontmatter name deve ser jusmanizer")
for rel in ("LICENSE", "AGENTS.md", "agents/openai.yaml", "scripts/test_jusmanizer.py"):
    if not os.path.exists(os.path.join(RAIZ, rel)):
        falhas.append(f"arquivo obrigatório ausente: {rel}")

print("OK: pacote coerente" if not falhas else "FALHAS:\n  - " + "\n  - ".join(falhas))
sys.exit(1 if falhas else 0)
