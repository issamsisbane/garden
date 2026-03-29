On peut rediriger les erreurs pour ne pas les voirs dans la sortie courant avec 
```
2>/dev/null
```

utile pour find par exemple : 
```
find / -name "-" 2>/dev/null
```