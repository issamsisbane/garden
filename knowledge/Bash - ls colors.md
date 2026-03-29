J'ai ces couleurs que je n'aime pas : 
![[Pasted image 20250810153004.png]]

Pour les changer il faut : 
```
 dircolors -p > ~/.dircolors
```

Puis modifier le fichier pour modifier la couleurs : 
![[Pasted image 20250810153313.png]]
Enrengistrer les modifs avec :
```
eval "$(dircolors ~/.dircolors)"
```

On peut le mettre dans le bashrc directement.