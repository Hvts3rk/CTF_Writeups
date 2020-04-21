## Information Gathering

Fase iniziale di IG ha rivelato un servizio sulla porta 22 e sulla 80. Visito la pagina in ascolto sulla porta 80 e trovo un servizio per l'image uploading. 

Tramite dirbuster scopro le pagine upload.php e login.php. Visito la upload form ma non riesco ad accedere perché devo essere loggato. Quindi passo al form di login.

Giro per il sitoweb alla ricerca di credenziali ma non ne trovo. Quindi provo con una basica sqli utile a superare l'authentication schema:

```
username: 1' OR True; --
password: abcabcabc
```

(NOTA: a FE c'è un filtro caratteri. Per bypassarlo modifico la richiesta con Burp) Riesco così a loggarmi ed accedo direttamente al form di image upload.

## Web Exploitation

Arrivato al form di upload capisco che devo caricare una web shell in php, uso b374k. Adesso devo capire come caricarla bypassando tutti i controlli di sicurezza. Alla fine, ci sono riuscito effettuando: 

* Creo png da 1px
* Rinomino il png in image.php.png
* Carico l'immagine tramite l'uploader, quindi con Burp intercetto la richiesta ed aggiungo in coda il codice sorgente di __b374k
* Visito il path dov'è collocata la risorsa (http://magic/images/uploads/a.php.png) 

Ed ecco che mi ritrovo davanti la webshell! 

```
########### ########### ########### ###########
Alternativa: usare msfvenom per generare una meterpreter_reverse_tcp, quindi stabilire un handler su msfconsole in ascolto sulla porta stabilita. Quindi aprire una shell, renderla interattiva con bash -i, quindi:

www-data@ubuntu:/var/www/Magic/images/uploads$ 
########### ########### ########### ###########
```
## Privilege Escalation

### www-data -> Theseus

Navigo nelle directory del webserver e rintraccio le credenziali di connessione al db:
```
private static $dbUsername = 'theseus';
private static $dbUserPassword = 'i[...]s';
```
