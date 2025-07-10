---
title: "Speechy"
description: "Le projet Speechy permet d'enregistrer la voix et de faire une transcription de ce qui a été dit ainsi qu'un résumé avec les points clés abordés."
pubDate: "22 Apr 2024"
lang: "fr"
heroImage: "/portfolio/projects/speechy/speechy.webp"
badge: "PERSONNEL"
tags: ["Azure", "IA", "LLM", "Nuxt", "TypeScript"]
---

Ce projet est encore en cours de développement.

## Liens
Le projet est disponible sur GitHub : 
* [Front-end](https://github.com/IssamSisbane/speechy-frontend)
* [Back-end](https://github.com/IssamSisbane/speechy-backend)

[Voir la version hébergée](https://speechy.snzprojects.tech/)

## Besoin
Ce projet a été mené durant mon temps libre pour mes propres besoins. Au cours de mon cursus en alternance, j'ai découvert un élément très important dans mon travail : **la prise de notes**. En effet, en tant qu'alternant, j'avais de longues périodes sans école et inversement de longues périodes sans entreprise. Ainsi, quand je revenais à l'école ou en entreprise, je me suis très vite rendu compte qu'il était impossible de me rappeler de tout ce que j'avais fait et de ce sur quoi je travaillais.

J'ai donc commencé à **prendre des notes** et à **documenter** tout ce que je faisais et tout ce que j'apprenais, que ce soit à l'école ou au travail. J'ai commencé en utilisant Google Docs et je suis ensuite passé sur Notion, que j'utilise toujours d'ailleurs. Cependant, après quelques années, je me suis rendu compte que lorsque je terminais une réunion par exemple et que je mettais en forme mes notes, j'omettais certaines choses car je voulais à la fois étoffer mais aussi reformuler mes notes. Je perdais donc un peu d'informations.

Puis un jour, j'ai essayé un outil sur internet qui permettait de faire une **transcription** de ce que je disais et cela m'a permis de ne rien omettre de la réunion que je venais d'avoir. De plus, j'ai trouvé cette façon de faire utile lorsque je réfléchis à un projet par exemple. Cela étant dit, il me fallait une **plateforme personnelle** pour faire cela et la connecter à ma notion (où je garde toutes mes traces écrites).

## Objectifs
L'objectif est donc de créer un site web qui permet de faire une transcription de l'enregistrement vocal et de fournir un résumé ainsi que les points clés de cet enregistrement.

Un autre objectif était d'utiliser de l'IA dans un projet réel afin de découvrir la puissance de ces outils.

## Méthodologie
J'ai commencé par développer une POC qui fonctionne et j'améliorerai ce dernier au fur et à mesure de mes besoins.

## Technologies Utilisées
Je suis encore en pleine réflexion. En effet, j'ai commencé une **POC** en utilisant Whisper d'OpenAI et GPT pour résumer et avoir les points clés. Cependant, je me suis rendu compte qu'en termes de coût, cela allait très vite devenir cher.

Je me suis ensuite tourné vers les modèles open source plus légers que je pouvais faire tourner en local (pour le traitement après transcription). Cela marchait (un peu moins bien que Whisper certes car les modèles sont plus légers) et m'évitait de payer énormément pour rien. Cependant, je veux pouvoir utiliser ce projet n'importe où sans forcément faire tourner un LLM sur chaque PC que je veux utiliser.

Ainsi, je commence à réfléchir à faire héberger ce modèle sur Azure. Cela me fera économiser beaucoup d'argent par rapport à utiliser une LLM via l'API d'OpenAI par exemple. De plus, je pourrais utiliser des fonctions afin de limiter encore plus les coûts.

* `Azure`
* `Nuxt`
* `Typescript`
* `Azure Functions`
* `Azure Static Apps`
* `Azure Key Vault`
* `Whisper`
* `Gpt-3.5-turbo`

## **Architecture**
![speechy-architecture](/portfolio/projects/speechy/speechy-architecture.png)

## Résultats
Le projet fonctionne bien, je peux enregistrer ma voix ou ajouter directement un fichier audio. Ce dernier va ensuite être envoyé à mon backend (Azure Function) puis enfin à OpenAI pour obtenir la transcription. Avec la transcription, on renvoie cette fois-ci à GPT-3.5-Turbo pour obtenir un résumé et les points clés abordés. 

J'ai décidé d'utiliser GPT-3.5-Turbo plutôt que GPT-4 pour limiter les coûts d'autant plus que pour une tâche si simple ce n'était pas vraiment nécessaire d'avoir un modèle plus performant.

## Tâches Restantes
Le projet est actuellement fonctionnel mais il peut encore être amélioré. En effet, il faudrait :

* **Code :**
    * Ajouter une limite à la durée d'un enregistrement pour limiter l'utilisation de tokens au maximum.
    * Vérifier les fichiers ajoutés et leur format avant de les envoyer à OpenAI.
    * Améliorer les sorties d'erreur.
    * Ajouter un chronomètre qui permet de connaître la durée de l'enregistrement.
    * Ajout de tests
    
* **Architecture :**
    * Ajouter une base de données pour garder une trace des dernières transcriptions.
    * Ajouter la connexion à Notion et l'envoi des données dans une page Notion.
    * Permettre la configuration de la solution pour l'utilisation par d'autres personnes.
    * Trouver une alternative moins chère à l'API d'OpenAI.

## Conclusion
Je suis fier d'avoir pu réaliser ce projet, ce n'était pas très difficile puisque j'utilise l'API d'OpenAI qui est très facile à utiliser. Le projet fonctionne assez bien et correspond à mes besoins mais j'aimerais l'améliorer encore plus.
