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

Cerco la documentazione di Umbraco e trovo che i collegamenti a DB sono impostati all'interno del file Web.config, e la stringa identificativa è "umbracoDbDMS". Quindi eseguo un grep sul file di config:

```
cat Web.config | grep umbracoDbDMS
```

Trovo la stringa di riferimento e scopro che un file di backup del DB è salvato dentro il file *Umbraco.sdf*. Lo rintraccio all'interno della cartella *App_Data*, faccio un cat, strings ed head. Tramite il comando *head* trovo un po di stringhe interessanti ma confuse. Quindi devio il flusso su un file dump_pwd.txt, quindi scremo e trovo:

```                                                                                                    
admin@htb.local
b8be16afba8c314ad33d812f22a04991b90e2aaa
{"hashAlgorithm":"SHA1"}
smith@htb.local
8+xXICbPe7m5NQ22HfcGlg==RF9OLinww9rd2PmaKUpLteR6vesD2MtFaBKe1zL5SXA=
{"hashAlgorithm":"HMACSHA256"}
```

Rompo l'hash di admin (essendo uno sha1 risulta rompibile) con CrackStation (o John):
```
baconandcheese
```
Faccio quindi il login nell'apposito tab:
```
10.10.10.180/umbraco/#/login
```
