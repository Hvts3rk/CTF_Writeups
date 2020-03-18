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
