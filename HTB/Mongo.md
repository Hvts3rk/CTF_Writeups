## Information Gathering

Si comincia con la fase iniziale di Informazion Gathering, con un classico port scan di nmap. Scopro aperte solo la porta 80 e 443 all'interno dell'host 10.10.10.163.

Richiedendo la porta 80 non trovo nulla di interessante, richiedendo la porta 443 (in http) invece mi comunica che il servizio è operato tramite SSL. Quindi richiedo: https://10.10.10.163, scoprendo così un errore al certificato. Lo leggo e scopro nel campo CN un valore interessante: all'interno dell'host sono presenti due VM: mango (la principale) ed anche il servizio "staging-order.mango.htb/".

Ovviamente provando a visitare la macchina indicata non viene rilevata, quindi inserisco dentro il file di hosts il redirect personalizzato: 
```
10.10.10.162 staging-order.mango.htb.
```
Ed ecco rilevato un form di login.

## Web Exploitation

Per associazione, il nome della macchina "Mango" ovviamene mi suona come il nome del DB "Mongo" quindi dopo un po di ricerche trovo questo exploit per l' [Username e Password Enumeration in MongoDB](https://github.com/an0nlk/Nosql-MongoDB-injection-username-password-enumeration/blob/master/nosqli-user-pass-enum.py) che banalmente fa:

* 
*
*

Tramite l'exploit trovo i seguenti dati:
```
admin:h3mXK8RhU~f{]f5H
mango:t9KcS3>!0B#2
