## Information Gathering

Come qualsiasi CTF comincio con una prima analisi superficiale:

```
nmap -sV -A -T4 10.10.10.180
```
Scopro come servizi attivi, un webserver in ascolto sulla porta 80 ed un mount demon sulla porta 2049, puntante su */site_backups*.

A questo punto navigo un po nel sito web, trovo un form autenticativo per la parte di backoffice. Provo con delle credenziali basilari ma non succede nulla. Vedo se magari sono hardcoded nel BE, quindi monto il disco che è in ascolto in locale:

```
mount -t nfs 10.10.10.180:/site_backups /tmp/remote_htb/
```
