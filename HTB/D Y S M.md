Inizio con la verifica del file "getme", mi ispira più fiducia. Vedo che la main function è una funzione sostanzialmente vuota. Esploro le stringhe con:

- r2 -z getme

e scopro una seconda funzione più popolata che stampa a video una serie di byte in or esclusivo con 0x29a.
Scrivo un piccolo exploit in python che mi faccia tutto questo lavoro in locale:


  struct = [SECRET_ARRAY_BYTE]

  flag = ""

  for v in struct:
        flag+=chr(v^0x29a)

  print "[!] FLAG: " + flag


Vedo che la stringa tuttavia continua ad essere cifrata. 
Si tratta di una cifratura basilare con shift di 13. Calcolo il decifrato ed ecco il flag in chiaro. 
