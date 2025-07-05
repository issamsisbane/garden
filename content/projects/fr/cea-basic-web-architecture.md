---
title: "Concevoir une Architecture Web Basique"
description: "Ce projet vise à créer une architecture de base pour une application web."
lang: "fr"
pubDate: "Sept 09 2024"
heroImage: "/portfolio/projects/cea-basic-web-architecture/cea-basic-web-architecture-cover.webp"
badge: "PERSONNEL"
tags: ["Cloud", "Architecture", "Cloud Engineer Academy"]
---

## Objectif du Projet

L'objectif ici est de concevoir une infrastructure cloud qui supporte une application web, tout en assurant une haute disponibilité, une tolérance aux pannes et une bonne scalabilité.

## Vue d’Ensemble de l’Architecture

![Week2_Architecture_basic.png](/portfolio/projects/cea-basic-web-architecture/Week2_Architecture_basic.png)

1. **Pare-feu (Firewall)** :  
   Premier élément de mon architecture, le pare-feu agit comme une couche de sécurité. Il filtre les requêtes entrantes selon des règles définies, autorisant uniquement le trafic légitime, ce qui permet de protéger l'infra contre les attaques potentielles.

2. **Load Balancer (Équilibreur de Charge)** :  
   Une fois le trafic passé par le pare-feu, il est dirigé vers un load balancer. Son rôle est de répartir les requêtes entre les ressources disponibles les plus efficaces, pour garantir performance et équilibre. J'en déploie plusieurs pour gérer les pics de trafic et assurer la redondance en cas de panne.

3. **Redondance Géographique** :  
   J'ai conçu l'architecture pour qu'elle s'étende sur deux régions géographiques. En cas d'indisponibilité d'une région, l'autre prend le relais. En plus, ça permet de router les utilisateurs vers la région la plus proche, ce qui améliore les temps de réponse.

4. **Clusters dans Chaque Région** :
   
   - **Cluster Haute Disponibilité** : Ce cluster contient les ressources principales pour faire tourner l'app web. Il gère le trafic normal avec de bonnes perfs.
   - **Cluster de Secours (Standby)** : Ce cluster est là en backup. Si le cluster principal rencontre un souci, celui-ci prend le relais pour assurer la continuité de service.

5. **Composants de l’Application** :

   - **Frontend** : Hébergé dans un subnet public pour être accessible aux utilisateurs. Il gère l’interface et les requêtes côté client.
   - **Backend** : Composé d’APIs et de bases de données, il tourne dans un subnet privé pour renforcer la sécurité. En l’isolant du public, on réduit la surface d’attaque et on protège les données sensibles.

## Stratégies de Scalabilité pour la Haute Dispo et la Tolérance aux Pannes

Chaque composant est dimensionné selon ses besoins pour garantir perfs et résilience :


| Composant                         | Type de Scalabilité | Raisons                                                                                                                                                        |
| --------------------------------- | -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Frontend (CDN)**                | Scalabilité Horizontale | Facile d’ajouter des serveurs, ce qui améliore la tolérance aux pannes.                                                                                         |
| **Backend (Serveurs d’App)**      | Scalabilité Horizontale | Plusieurs serveurs backend permettent de traiter plus de requêtes en parallèle.                                                                                 |
| **Load Balancer**                 | Scalabilité Horizontale | Plusieurs load balancers = meilleure répartition du trafic + redondance.                                                                                       |
| **Pare-feu**                      | Scalabilité Horizontale | Plus de pare-feux = plus de trafic géré, tout en gardant une bonne sécurité.                                                                                   |
| **Base de Données (SQL)**         | Scalabilité Verticale   | Les bases relationnelles sont souvent scalées verticalement car le horizontal est plus complexe à gérer (cohérence des données, synchro…).                     |

---

## Résumé des Choix d’Architecture

- **Scalabilité Horizontale** pour la majorité des composants : plus facile à gérer, meilleure perf et tolérance aux pannes.
- **Redondance Géographique** pour encaisser les pannes régionales et router automatiquement le trafic vers la région dispo.
- **Clusters** dans chaque région pour basculer sur du secours si les ressources principales tombent.
- **Scalabilité Verticale** pour la base SQL, pour augmenter sa capacité sans se prendre la tête avec plusieurs instances.

En bref, cette archi est conçue pour être dispo, scalable et sécurisée – parfaite pour une app web solide.