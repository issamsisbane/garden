# Methode Sed

Commenter des lignes sélectionnés via le visual mode : 
```
s/^/# /
```

Décommenter des lignes sélectionnés via le visual mode : 
```
s/^# //
```

# Methode Norm 

Pour commenter un ensemble de lignes séléctionné en visual mode :

```
norm I#
```

Pour décommenter un ensemble de lignes séléctionné en visual mode :

```
norm ^x
```