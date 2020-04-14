## Information Gathering

Si comincia con la fase iniziale di Informazion Gathering, con un classico port scan di nmap. Scopro aperte solo la porta 80 e 443 all'interno dell'host 10.10.10.163.

Richiedendo la porta 80 non trovo nulla di interessante, richiedendo la porta 443 (in http) invece mi comunica che il servizio è operato tramite SSL. Quindi richiedo: https://10.10.10.163, scoprendo così un errore al certificato. Lo leggo e scopro nel campo CN un valore interessante: all'interno dell'host sono presenti due VM: mango (la principale) ed anche il servizio "staging-order.mango.htb/".

Ovviamente provando a visitare la macchina indicata non viene rilevata, quindi inserisco dentro il file di hosts il redirect personalizzato: 
```
10.10.10.162 staging-order.mango.htb.
```
Ed ecco rilevato un form di login.

## Web Exploitation

Per associazione, il nome della macchina "Mango" ovviamene mi suona come il nome del DB "Mongo". Mongo è un tipo di DB non-relazionare (quindi non produce strutture dati ma produce JSON).Trattandosi di un DB NoSQL sfrutto le regex per fare Injection con query del tipo:
```
username[$regex]:^<CHAR>.*&password[$ne]:1&login:login
```

Dopo un po di ricerche trovo questo exploit per l' [Username e Password Enumeration in MongoDB](https://github.com/an0nlk/Nosql-MongoDB-injection-username-password-enumeration/blob/master/nosqli-user-pass-enum.py) che banalmente fa quello enunciato precedentemente ma tutto automatizzato:

```
nosqli-user-pass-enum.py -u http://HOST/# -up username -pp password -ep <CHOOSE> -op login:login -m POST
```

Tramite l'exploit trovo i seguenti dati:

```
admin:h3[...]5H
mango:t9[...]#2
```

Provo quindi a collegarmi al tab di login con le creds trovate ma non succede nulla.

Quindi provo a collegarmi in ssh con le creds trovate e trovo efficace la seguente combinazione:
```
mango:h3[...]5H
```
Rintraccio l'user flag dentro la cartella dell'utenza "admin" ma non ho i permessi per aprirla.

## Privilege Escalation

### User1

Cerco qualche password salvata ma non trovo nulla. Ad un certo punto penso che la seconda password trova in DB possa servire a qualcosa quindi banalmente faccio:
```
su admin
```

Inserisco la seconda password (t9[...]#2) ed eccomi entrato in sessione con l'utenza Admin! Apro l'user flag!

### Root
