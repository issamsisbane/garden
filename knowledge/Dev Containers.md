[[Dev Containers - Podman]]
[[Dev Containers - Slow operations]]

C'est une extension VS Code qui permet de créer un container de développement. Cela permet de générer un container avec tous les outils nécessaires pour un certain projets et d'éviter de jouer avec différentes version installé sur le pc de développement. 

Par exemple si on a une application Node JS 18 et une application Node JS 22, on aura pas besoin de changer de version sur notre pc de développement mais seulement d'avoir un container spécifique pour chaque projet avec la bonne version de node.

# Usage

il suffit de faire `ctrl`+`shift`+`p`et de chercher DevContainers puis => Créer configuration file puis de suivre les instructions. 

Une fois configurer, il suffit de faire relancer dans un conteneur pour utiliser notre configuration et notre projet dans un conteneur.

[Developing inside a Container using Visual Studio Code Remote Development](https://code.visualstudio.com/docs/devcontainers/containers)

# To Know

[[Dev Containers - Slow operations]]

# Configuration

## Podman

J'ai essayer de faire une configuration pour utiliser podman plutôt que docker pour devcontainers. Mais ça n'a pas fonctionné. Le container ne s'ouvre jamais. 

J'avais modifié ces deux champs pour matcher avec podman :

![[Pasted image 20250323215147.png]]

Je suis finalement revenu sur docker. 