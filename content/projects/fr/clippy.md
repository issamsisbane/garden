---
title: "Clippy"
description: "Une plateforme web permettant le partage d'informations de manière éphémère, suivant le modèle de Pastebin."
lang: "fr"
pubDate: "Feb 15 2024"
heroImage: "/portfolio/projects/clippy/clippy.jpg"
badge: "PERSONNEL"
tags: ["Cloud", "Azure", "Nuxt", "CosmosDB", "Typescript"]
---

## **Liens**
Le projet est disponible via github : 
* [Front-end](https://github.com/IssamSisbane/clippy-frontend)
* [Back-end](https://github.com/IssamSisbane/clippy-backend)

[La version hebergée](https://clippy.snzprojects.tech/)

## **Besoin**
Ce projet a été mené durant mon temps libre pour mes propres besoins. Il m'arrivait d'avoir besoin d'un plateforme pour copier coller simplement et rapidement des informations entre deux appareils. Lorsque j'utilise deux appareils qui m'appartienent comme mon téléphone et mon pc je passe par un serveur privée discord qui me sert de presse-papiers. Seulement, parfois un des deux appareils ne m'appartenait pas et je ne pouvais donc utiliser cette méthode. Il existe des alternatives sur le marché sous la forme de siteweb cependant les url généré pour sont assez indigeste et peu pratique a copier coller a la main sur un navigateur.

## **Objectifs**
Ainsi, l'objectif de ce projet est de mettre un place un site web qui permet le partage d'information de manière éphémere via des urls simple à copier coller.


## **Methodologie**
J'ai commencer par définir ce que je voulais dans mon application, puis j'ai fait un schéma de l'architecture que j'allais mettre en place. Enfin, j'ai commencer à coder et à itérer sur ce code au fur et à mesure.

## **Technologies Utilisées**
Backend :
* `Azure`
* `Azure Function`
* `Azure Blob Storage`
* `CosmosDB`
* `Azure Key Vault`
* `Typescript`

Frontend :
* `Nuxt`
* `Nuxt-ui`
* `Typescript`

## **Architecture**
![clippy-architecture](/portfolio/projects/clippy/clippy-architecture.webp)


## **Résultats**
Ayant une certaine expérience avec les technologies d'Azure et javascript ce projet fut assez simple à mettre en place et à utiliser. Finalement, il est possible de créer un 'clip' qui peut être soit du texte soit un fichier. Il est aussi possible de décider du temps de la validité du clip. Enfin, après création un chemin pour le clip est généré et ce dernier correpond à un nom d'animal. Ainsi, il suffit juste de taper l'url du site suivi du chemin du clip pour y accèder. La suppression se fait automatiquement chaque jour et l'accès au clip est interdite si la durée de validité a expiré mais qu'il n'a pas encore été supprimé.

## **Améliorations Possibles**
Le projet est fonctionnel mais il pourrait encore être amélioré. En effet, il faudrait mettre en place une sécurité plus robuste pour les fichiers, ajouter une vérification pour être sûr qu'il sont de taille acceptable et surtout sans risques. 

De plus, l'interface peu encore être vraiment amélioré notamment le coté responsive.

Finalement, il faudrait ajouter des tests.
 
## **Conclusion**
J'ai bien aimé ce projet car j'ai pu travailler avec technologies que j'aime tout particuilièrement. Enfin, j'ai pu mobiliser de nombreuses compétences que j'ai acquises au sein du même projet.
