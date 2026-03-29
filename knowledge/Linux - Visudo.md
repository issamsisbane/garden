Si on ne veut pas toujours avoir à mettre le mot de passe quand on fait un sudo. On peut pour un utilisateur le desactiver. 


> [!ATTENTION] Risque
> Il faut ajouter dans visudo, à la fin du fichier
> ```
> user ALL=(ALL) NOPASSWD:ALL
>```
>On peut aussi restreindre a certaines commandes :
>```
>monuser ALL=(ALL) NOPASSWD: /usr/sbin/shutdown
>```

