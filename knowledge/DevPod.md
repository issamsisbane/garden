Implementation open source de [[Dev Containers]].

On utilise des providers qui permettent de lancer un container via docker ou sur kubernetes ou directement de creer une machine virtuelle dans le cloud.

DevPod prend en charge de base les dotfiles. On peut fournir un fichier setup qui permet d'initialiser notre conteneur avec notre config.

On peut ensuite utiliser devpods qui va lancer un server vscode qu'on peut acceder depuis notre navigateur ou simplement ne rien mettre dans ide pour utiliser simplement vim.

Premiere commande à faire : 

``` bash
devpod add provider docker
```

Ensuite il suffit de créer un fichier `.devcontainers/devcontainers.json`

On lance : 
``` bash
devpod up . --ide none --dotfiles git@github.com:issamsisbane/dotfile-demo
```

et on ssh dans le conteneur : 
```
devpod ssh conteneur-name
```

On peut mettre le ide par defaut : 
```
devpod ide use none
```

On peut ajouter aussi nos dotfiles de manière globale : 
```
devpod context set-options -o DOTFILE_URL=git@github.com:issamsisbane/dotfile-demo.git
```

