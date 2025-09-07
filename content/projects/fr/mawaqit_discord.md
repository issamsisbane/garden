---
title: "Mawaqit Discord Notify"
description: "Un bot discord permettant d'envoyé des notifications à des heures précises de la journée récupérées à l'aide du scraping d'un siteweb."
lang: "fr"
pubDate: "Apr 8 2024"
heroImage: "/portfolio/projects/mawaqit_discord/mawaqit.webp"
badge: "PERSONNEL"
tags: ["Cloud", "Azure", "Cron", "Docker", "Javascript", "Scraping"]
---

## **Liens**

- [Le projet](https://github.com/IssamSisbane/mawaqit-discord-notify)
- [MAWAQIT](https://mawaqit.net/fr/)

## **Besoin**

Il existe une application appelée MAWAQIT qui permet d'obtenir les horaires de prières pour une mosquée donnée, parmi d'autres fonctionnalités. J'apprécie beaucoup cette application et l'utilise au quotidien. 

Cependant, j'ai un petit souci avec son fonctionnement. Il est possible de configurer des notifications pour être averti lors de l'heure d'une prière, mais ces notifications sont uniquement sonores et ne peuvent être émises que sur mon téléphone Android. Parfois, je travaille sur mon ordinateur et je ne touche donc pas à mon téléphone pendant un certain temps. 

J'avais trouvé une solution en ouvrant une page web MAWAQIT qui émettait un petit bip à chaque prière, mais cela posait problème lorsque j'avais déjà du son sur mon ordinateur ou lorsque je n'avais pas mes écouteurs branchés. J'avais donc besoin d'un système me permettant de recevoir des notifications à la fois sur mon ordinateur et sur mon téléphone.

## **Objectifs**

L'objectif de ce projet est donc de mettre en place un système permettant d'envoyer des notifications à l'heure de chaque prière, chaque jour.

## **Méthodologie**

Le but est d'envoyer des notifications cinq fois par jour à des horaires changeants quotidiennement. Pour cela, plusieurs problèmes doivent être résolus :

1. Récupérer les heures de prières pour un jour donné.
2. Envoyer des notifications lors de l'heure d'une des prières récupérées.
3. Assurer que cela s'exécute tous les jours.

J'ai commencé par le premier problème. J'aurais pu utiliser n'importe quelle API pour cela, mais je voulais vraiment les données de MAWAQIT pour avoir les horaires de prières précises des mosquées proches. J'ai donc analysé le site MAWAQIT et j'ai réalisé que tout était déjà chargé via la page (appel d'une page php). Ainsi, la solution pour récupérer les horaires était de scraper directement le site. J'ai mis cela en place en utilisant Node.js et Puppeteer, ce qui m'a permis d'obtenir un script pour récupérer les horaires de prières de toute la journée.

La prochaine étape était d'envoyer des notifications à chaque moment de prière. Pour cela, j'ai eu l'idée d'utiliser Discord. J'utilise Discord depuis un bon nombre d'années et j'ai toujours voulu tester le développement d'un bot, mais je n'avais pas encore eu de raison de le faire. Ma solution a donc été de créer un bot qui enverrait un message dans le canal de mon serveur privé. Cela me permettrait d'avoir les notifications à la fois sur mon ordinateur et sur mon téléphone. C'était idéal. J'ai entrepris mes recherches pour créer un bot Discord et j'ai finalement utilisé la librairie DiscordJs. Très simplement, j'ai pu envoyer un message via un bot dans un canal spécifique.

Il manquait finalement la dernière étape permettant de faire cela tous les jours. Ma première idée était de mettre ce code dans une fonction Azure, mais le code n'était pas adapté. Actuellement, le code récupère les horaires de prières puis attend chaque prière pour envoyer des notifications, ce qui nécessiterait que le code tourne toute la journée pour fonctionner. J'ai donc opté pour des conteneurs. J'ai pensé aux conteneurs job qui permettraient d'être exécutés tous les jours, mais j'ai réalisé qu'ils ont apparemment un temps limité maximal et que les faire tourner toute la journée n'est apparemment pas possible ou coûterait trop cher. 

J'ai donc choisi d'utiliser des conteneurs simples en utilisant Azure Container Instance. Je me suis dit que j'allais utiliser une logique app pour lancer le conteneur chaque jour, mais ce n'est pas possible. Avec une logique app, on ne peut gérer qu'un groupe de conteneurs et pas un conteneur unique. Je ne voulais pas créer de groupe de conteneurs juste pour ce petit projet. J'ai donc trouvé une solution, soit de créer un cron directement dans Node qui s'exécuterait tous les jours de lui-même. Ainsi, il me suffirait de lancer le conteneur et de le laisser tourner.

## **Technologies Utilisées**

- `Azure`
- `Azure Key Vault`
- `Azure Container Instances`
- `CosmosDB`
- `Node.js`
- `Javascript`

## **Architecture**

![mawaqit_discord_architecture.drawio.png](/portfolio/projects/mawaqit_discord/mawaqit_discord_architecture.png)

## **Résultats**

Ainsi, tout fonctionne très bien et correspond à mes besoins. Je suis très content d'avoir pu réaliser ce petit projet qui ne m'a pris que très peu de temps et qui me trottait dans la tête depuis longtemps.

## **Améliorations Possibles**

Le projet est fonctionnel et personnalisable grâce aux variables d'environnement, notamment pour choisir sa mosquée et le canal Discord de destination des messages. Cependant, j'aimerais développer une véritable application dédiée sans passer par Discord, qui serait une application de notification générale pour tous les appareils et permettrait de recevoir des rappels, notamment sur ce que j'ai à faire durant ma journée...

## **Conclusion**

J'ai vraiment apprécié la réalisation de ce petit projet. Je n'ai eu que très peu de problèmes, mais je trouve très intéressant de travailler sur des problématiques qui me concernent car je peux identifier très clairement les besoins et donc adapter les solutions au mieux.
