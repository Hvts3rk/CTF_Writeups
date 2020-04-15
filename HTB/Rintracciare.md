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
