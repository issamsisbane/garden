---
title: "Park IT !"
description: "Le projet Park It! est une solution IoT innovante visant à simplifier le stationnement. Avec des capteurs intelligents et une application conviviale, il offre une expérience de stationnement optimisée."
lang: "fr"
pubDate: "24 janv. 2024"
heroImage: "/portfolio/projects/parkit/parkit_img.webp"
badge: "SCOLAIRE"
tags: ["Arduino", "FreeRtos", "Express", "TypeScript", "React Native"]
---
## **Liens**
* [L'API du projet](https://github.com/IssamSisbane/parkit-api)


## **Description**

Le projet Parking Connect, également connu sous le nom de "Park It!", est une solution innovante visant à relever les défis du stationnement urbain dans les métropoles animées. Il exploite l'Internet des objets (IoT) pour créer un système de stationnement intelligent qui améliore l'expérience de stationnement à la fois pour les conducteurs et les exploitants de parkings.

## **Objectifs**

L'objectif principal du projet est de concevoir et développer une solution de stationnement connectée qui optimise l'utilisation de l'espace de stationnement et fournit des informations sur la disponibilité en temps réel aux utilisateurs. De plus, le projet vise à rationaliser le processus de réservation, à améliorer l'expérience utilisateur grâce à une application mobile, et à intégrer différentes technologies IoT pour un fonctionnement sans faille.

## **Méthodologie**

Ce projet a été réalisé en groupe avec deux autres étudiants. J'étais en charge du backend et des communications. Le projet suit une approche globale, commençant par la conceptualisation et la conception, suivie par le développement et la mise en œuvre. L'équipe a adopté une méthodologie itérative, permettant un affinement continu et une adaptation aux défis rencontrés pendant le cycle de vie du projet. La collaboration et la communication entre les membres de l'équipe étaient essentielles pour une gestion efficace du projet et la résolution de problèmes.

## **Technologies Utilisées**

Le projet Parking Connect utilise une gamme de technologies pour atteindre ses objectifs :

* `React Native` : pour développer l'interface de l'application mobile.
* `Node.js & Express.js` : pour construire le backend de l'API.
* `MongoDB` : pour stocker et gérer les données liées au stationnement.
* `FreeRTOS & ESP32` : pour l'infrastructure IoT basée sur microcontrôleur.
* Protocole `MQTT` : pour la communication entre l'API et les appareils ESP32.
* `Expo` : pour le développement et le déploiement simplifiés de l'application mobile.
* `Swagger/OpenAPI` : pour documenter et définir les points de terminaison de l'API.
* Diverses dépendances pour les composants frontend, backend et IoT.

## **Architecture**

L'architecture du système Parking Connect comprend trois composants principaux :

**Application Mobile :** Développée avec React Native et Expo, l'application mobile offre aux utilisateurs des fonctionnalités telles que la réservation de stationnement, la disponibilité en temps réel et la gestion de compte.

**Backend de l'API :** Construit avec Node.js et Express.js, l'API sert d'intermédiaire entre l'application mobile et la base de données. Elle gère les requêtes, communique avec la base de données MongoDB, et interagit avec les appareils ESP32 via MQTT.

**Infrastructure IoT :** Implémentée avec FreeRTOS et des microcontrôleurs ESP32, l'infrastructure IoT comprend des capteurs, des actionneurs et des modules de communication déployés dans des espaces de stationnement physiques. Ces appareils interagissent avec l'API pour fournir des données en temps réel et contrôler les opérations de stationnement.

## **Résultats**

Le projet a livré avec succès une preuve de concept démontrant les fonctionnalités de base du système de stationnement intelligent. Les utilisateurs peuvent accéder à des informations sur la disponibilité en temps réel des places de stationnement, effectuer des réservations via l'application mobile, et interagir avec l'infrastructure physique de stationnement. Malgré les contraintes matérielles et budgétaires, le projet a atteint ses objectifs principaux et a jeté les bases pour des améliorations futures et une évolutivité.

## **Perspectives d'améliorations**

En tant qu'étudiants, nous avions des contraintes de matériel et de budget pour ce projet. Malgré cela, nous avons réalisé un proof of concept satisfaisant. Toutefois, certains aspects pourraient être améliorés.

Premièrement, le design aurait pu être plus réaliste, mais nous étions limités par le matériel disponible.

Deuxièmement, l'intervention d'un administrateur est nécessaire pour configurer le parking, ce qui pourrait être simplifié avec une interface web dédiée.

Nous avons également ajouté un système de statistiques, mais une interface spécifique pour les propriétaires du parking aurait été préférable, offrant des graphiques personnalisables pour les entrées, les réservations, et l'occupation des places.

Enfin, il faudrait ajouter des tests au code.


## **Conclusion**

Le projet Parking Connect représente une intégration réussie de l'IoT, du développement d'applications mobiles et de l'infrastructure backend pour relever les défis du stationnement urbain. Malgré les contraintes, le projet a livré une solution fonctionnelle qui améliore la commodité et l'efficacité du stationnement. À l'avenir, il existe un potentiel pour d'autres améliorations, y compris des outils administratifs, des améliorations de l'expérience utilisateur et une évolutivité pour des déploiements plus importants.
