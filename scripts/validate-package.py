#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Confere a coerência do pacote jusmanizer.

  · mesma versão em SKILL.md (metadata.version), .claude-plugin/plugin.json,
    .cursor-plugin/plugin.json e scripts/jusmanizer.py (VERSAO); o README é para o advogado
    e não carrega versão;
  · padrões numerados sem lacuna (### J01 … ### Jnn) no SKILL.md; a contagem vem dos títulos;
  · README com cada padrão uma vez, e contagem de padrões e de grupos igual à do SKILL.md;
  · toda referência Jnn do SKILL.md, do README e do AGENTS.md aponta para padrão existente;
  · SKILL.md com até 5.500 palavras, porque ele é lido inteiro a cada uso;
  · manifestos de plugin com a primeira frase da descrição do SKILL.md;
  · nenhuma risca (travessão ou meia-risca) na prosa do SKILL.md fora de linha de exemplo
    (que começa por `>`), de tabela (`|`), de frontmatter e de trecho em código;
  · manifestos com nome `jusmanizer`; o do Claude aponta skills ["./"], o do Cursor omite
    `skills` para carregar o SKILL.md da raiz.

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
LIMITE_PALAVRAS = 5500
falhas = []


def ler(rel):
    with open(os.path.join(RAIZ, rel), encoding="utf-8") as f:
        return f.read()


def ler_json(rel):
    try:
        return json.loads(ler(rel))
    except json.JSONDecodeError as erro:
        sys.exit(f"FALHAS:\n  - JSON inválido em {rel}: {erro}")


skill = ler("SKILL.md")
readme = ler("README.md")
agents = ler("AGENTS.md")
plugin = ler_json(".claude-plugin/plugin.json")
market = ler_json(".claude-plugin/marketplace.json")
cursor = ler_json(".cursor-plugin/plugin.json")
mod = ler("scripts/jusmanizer.py")

frontmatter = re.match(r"^---\n(.*?)\n---\n", skill, re.S)
yaml = frontmatter.group(1) if frontmatter else ""

# Versão
v_skill = re.search(r'^\s*version:\s*"([^"]+)"', yaml, re.M)
v_mod = re.search(r'^VERSAO = "([^"]+)"', mod, re.M)
versoes = {v_skill and v_skill.group(1), plugin.get("version"), cursor.get("version"),
           v_mod and v_mod.group(1)}
if len(versoes) != 1 or None in versoes:
    falhas.append("versões divergem entre SKILL.md, plugin.json do Claude e do Cursor e "
                  f"jusmanizer.py: {versoes}")
if re.search(r"^version:", yaml, re.M):
    falhas.append("SKILL.md: a versão fica em metadata.version, não no nível superior")

# Padrões e grupos
nums = [int(m) for m in re.findall(r"^### J(\d{2})\b", skill, re.M)]
total = len(nums)
if total == 0 or nums != list(range(1, total + 1)):
    falhas.append(f"padrões J01..Jnn sem lacuna esperados no SKILL.md; achado {nums}")
grupos = re.findall(r"^## ([A-Z])\. ", skill, re.M)
if grupos != [chr(ord("A") + i) for i in range(len(grupos))]:
    falhas.append(f"grupos do SKILL.md devem seguir A, B, C… sem lacuna; achado {grupos}")

nums_readme = sorted(int(m) for m in re.findall(r"^\| J(\d{2}) \|", readme, re.M))
if nums_readme != list(range(1, total + 1)):
    falhas.append(f"README deve listar J01..J{total:02} uma vez cada; achado {nums_readme}")
if f"## As {total} regras" not in readme:
    falhas.append(f"README: título da lista deve ser 'As {total} regras'")
extenso = {5: "cinco", 6: "seis", 7: "sete", 8: "oito"}.get(len(grupos), str(len(grupos)))
if f"**{total} padrões de revisão**" not in readme or f"**{extenso} grupos**" not in readme:
    falhas.append(f"README: a abertura deve dizer {total} padrões em {extenso} grupos")

# Referências Jnn: um renumerar pode deixá-las apontando para o nada.
for nome, texto in (("SKILL.md", skill), ("README.md", readme), ("AGENTS.md", agents)):
    fora = sorted({int(n) for n in re.findall(r"\bJ(\d{2})\b", texto)} - set(range(1, total + 1)))
    if fora:
        falhas.append(f"{nome} cita padrão inexistente: {['J%02d' % n for n in fora]}")

# Tamanho: cada palavra do SKILL.md é lida a cada uso.
palavras = len(skill.split())
if palavras > LIMITE_PALAVRAS:
    falhas.append(f"SKILL.md tem {palavras} palavras; o teto é {LIMITE_PALAVRAS}")

# Descrição: os manifestos usam a primeira frase da descrição do SKILL.md.
bloco = re.search(r"^description: \|\n((?:  .*\n)+)", yaml + "\n", re.M)
descricao = " ".join(bloco.group(1).split()) if bloco else ""
primeira = descricao.split(". ")[0].rstrip(".") + "." if descricao else ""
descricoes = {plugin.get("description"), cursor.get("description"),
              *(p.get("description") for p in market.get("plugins", []))}
if not primeira or descricoes != {primeira}:
    falhas.append("manifestos devem trazer a primeira frase da descrição do SKILL.md: "
                  f"{sorted(map(str, descricoes))}")

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

# Manifestos
if plugin.get("name") != "jusmanizer" or plugin.get("skills") != ["./"]:
    falhas.append("plugin.json: name deve ser 'jusmanizer' e skills ['./']")
if cursor.get("name") != "jusmanizer" or "skills" in cursor:
    falhas.append(".cursor-plugin/plugin.json: name 'jusmanizer' e sem 'skills'")
if market.get("name") != "jusmanizer" or not any(
        p.get("name") == "jusmanizer" for p in market.get("plugins", [])):
    falhas.append("marketplace.json: name e plugins[].name devem ser 'jusmanizer'")
if not re.search(r"^name:\s*jusmanizer\s*$", yaml, re.M):
    falhas.append("SKILL.md: frontmatter name deve ser jusmanizer")
for rel in ("LICENSE", "AGENTS.md", "agents/openai.yaml", "scripts/test_jusmanizer.py"):
    if not os.path.exists(os.path.join(RAIZ, rel)):
        falhas.append(f"arquivo obrigatório ausente: {rel}")

if falhas:
    print("FALHAS:\n  - " + "\n  - ".join(falhas))
else:
    print(f"OK: pacote coerente, v{v_skill.group(1)}, {total} padrões em {len(grupos)} grupos, "
          f"{palavras} palavras")
sys.exit(1 if falhas else 0)
