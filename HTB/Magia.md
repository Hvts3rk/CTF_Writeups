## Information Gathering

Fase iniziale di IG ha rivelato un servizio sulla porta 22 e sulla 80. Visito la pagina in ascolto sulla porta 80 e trovo un servizio per l'image uploading. 

Tramite dirbuster scopro le pagine upload.php e login.php. Visito la upload form ma non riesco ad accedere perché devo essere loggato. Quindi passo al form di login.

Giro per il sitoweb alla ricerca di credenziali ma non ne trovo. Quindi provo con una basica sqli utile a superare l'authentication schema:

```
username: 1' OR True; --
password: abcabcabc
```

(NOTA: a FE c'è un filtro caratteri. Per bypassarlo modifico la richiesta con Burp) Riesco così a loggarmi ed accedo direttamente al form di image upload.
