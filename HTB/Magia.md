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

Provo a collegarmi via ssh con le credenziali trovate ma la coppia kpub e kpriv non è riconosciuta. Quindi utilizzo le creds per accedere al db. Tuttavia, tramite:
```
mysql -u theseus -p Magic
```
Non riesco a collegarmi quindi uso mysqldump rintracciato fra i binary a mia disposizione.

Effettuo così il dump delle vere credenziali di Theseus.

Ultimo step prima dell'user flag è spawnare una tty shell (considerando che via ssh non ne ho accesso):
```
python3 -c "__import__('pty').spawn('/bin/bash')"
(unico comando funzionante fra tutti i metodi!)
```

Per mantenere la persistenza appendo la mia kpub dentro al file .ssh/authorized_keys, riuscendo così finalmente ad accedere via ssh usando la mia kpriv! 

### Theseus -> Root

Dopo essermi collegato in SSH mi sposto in /tmp e carico un po di script, LSE.sh, LE.sh e li lancio. Quello che emerge è veramente poco. Dopo ore di analisi noto un binario con SUID: sysinfo. 

Analizzo il binario con:

```
strings sysinfo
```
e noto che vengono richiamata diversi binari esterni. Ne scelgo uno, free. 

Quindi l'idea di base è di creare un binario finto clone di "free" in cui gli do il comando "cat /root/root.txt". Quindi, una volta lanciato sysinfo, avendo alterato la variabile globale PATH, lui andrà ad eseguire quel binario da me creato. In sostanza questo si traduce nei seguenti comandi:

```
PATH=.:$PATH

touch free

echo "cat /root/root.txt" > free

chmod +x free

sysinfo

```

Questo è quanto! 🍾
