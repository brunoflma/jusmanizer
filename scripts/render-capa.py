"""Fotografa docs/capa.html e grava a capa do README e a imagem de compartilhamento.

A capa reusa o site.css e a marcação do destaque do site, então as duas peças não divergem.
Usa um Edge ou Chrome já instalado, sem janela (--headless --screenshot); nada é baixado.

Uso: python scripts/render-capa.py
"""

import functools
import http.server
import re
import shutil
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SAIDAS = (DOCS / "cover.png", DOCS / "assets/social-preview.png")
LARGURA, ALTURA = 1280, 640
# Ordem de tentativa. O Chrome vem primeiro: medido em 11/11/2026, o `--screenshot` do Edge 157
# sai com código 0 sem gravar a imagem.
NAVEGADORES = (
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "google-chrome", "chromium", "chrome",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "msedge",
)


def navegadores():
    vistos = []
    for candidato in NAVEGADORES:
        caminho = shutil.which(candidato) or (candidato if Path(candidato).is_file() else None)
        if caminho and caminho not in vistos:
            vistos.append(caminho)
    if not vistos:
        sys.exit("Nenhum Chrome ou Edge encontrado para fotografar a capa.")
    return vistos


def atualizar_contagem():
    """A capa diz quantas regras e grupos há; o número vem do SKILL.md."""
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    regras = len(re.findall(r"(?m)^### J\d{2} ", skill))
    grupos = len(re.findall(r"(?m)^## [A-Z]\. ", skill))
    capa = DOCS / "capa.html"
    html = capa.read_text(encoding="utf-8")
    html = re.sub(r'<strong id="regras">\d+</strong>', f'<strong id="regras">{regras}</strong>', html)
    html = re.sub(r'<strong id="grupos">\d+</strong>', f'<strong id="grupos">{grupos}</strong>', html)
    capa.write_text(html, encoding="utf-8", newline="")
    return regras, grupos


def servir():
    class Silencioso(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

    handler = functools.partial(Silencioso, directory=str(DOCS))
    servidor = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    return servidor


def fotografar(url, destino):
    """Grava `destino` com o primeiro navegador que de fato gravar. O arquivo antigo sai antes,
    para que uma falha silenciosa não deixe a capa velha passar por nova."""
    destino.unlink(missing_ok=True)
    for exe in navegadores():
        with tempfile.TemporaryDirectory() as perfil:
            subprocess.run([
                exe, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--mute-audio",
                "--no-first-run", "--no-default-browser-check", f"--user-data-dir={perfil}",
                "--force-device-scale-factor=1", f"--window-size={LARGURA},{ALTURA}",
                "--virtual-time-budget=4000", f"--screenshot={destino}", url,
            ], capture_output=True, timeout=120)
        if destino.is_file() and destino.stat().st_size > 0:
            return
        print(f"{Path(exe).name} não gravou a imagem; tentando o próximo navegador.")
    sys.exit(f"Nenhum navegador gravou {destino.name}.")


def main():
    regras, grupos = atualizar_contagem()
    servidor = servir()
    try:
        url = f"http://127.0.0.1:{servidor.server_address[1]}/capa.html"
        for destino in SAIDAS:
            fotografar(url, destino)
            dados = destino.read_bytes()
            assert dados[:8] == b"\x89PNG\r\n\x1a\n", destino
            largura = int.from_bytes(dados[16:20], "big")
            altura = int.from_bytes(dados[20:24], "big")
            print(f"{destino.relative_to(ROOT)}: {largura} x {altura}, {regras} regras em {grupos} grupos")
    finally:
        servidor.shutdown()


if __name__ == "__main__":
    main()
