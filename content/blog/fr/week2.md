---
title: "Améliorer mes compétences Cloud - Semaine 2 - Git et Architecture Cloud"
description: "Semaine 2 pour améliorer mes compétences Cloud."
lang: "fr"
pubDate: "Sept 13 2024"
heroImage: "/portfolio/blog/week2/week2.drawio.png"
badge: "Améliorer mes compétences Cloud"
tags: ["Cloud", "GIT", "Cloud Engineer Academy", "Architecture"]
---

*Le **deuxième module** de l'Académie portait sur **Git** et l'**Architecture Cloud**. C'était un excellent mélange de concepts rafraîchissants avec lesquels j'étais déjà familier et de la découverte de **nouvelles perspectives** que je n'avais pas explorées auparavant.*

*J'ai eu l'occasion de **revoir certaines choses** que je connaissais déjà, tout en approfondissant ma compréhension dans certains domaines. Ce module s'est concentré sur l'utilisation efficace de **Git** dans les environnements cloud et a mis en évidence les éléments clés de l'**architecture cloud**, garantissant des solutions évolutives, sécurisées et efficaces.*

*Comme je l'ai mentionné précédemment, je viens d'un parcours en **cloud computing** et en **ingénierie logicielle**, donc tout au long de mon parcours d'apprentissage, je marquerai les nouveaux concepts avec le hashtag **#nouveau**. Cela permettra de mettre en évidence ce qui est nouveau pour moi et d'offrir aux lecteurs une idée plus claire de l'endroit où ils pourraient trouver une valeur ajoutée, qu'ils revisitent des concepts familiers ou qu'ils rencontrent de nouveaux éléments.*

*Restez à l'écoute, car je continue à documenter mon processus d'apprentissage et à partager les points à retenir de chaque module !*

---

1 - **Contrôle de version** <br/>
2 - **Architecture Cloud** <br/>
3 - **Conception de système** <br/>
4 - **Console AWS** <br/>
5 - **Projet | Concevoir une architecture de base pour un projet d'application web** <br/>

---

# Contrôle de version

Une petite introduction à GIT, à quoi cela sert avec création d'un repo github et utilisation de commande très basique tel que :

``` bash
git init
```

``` bash
git checkout -b dev
```

C'est très important d'utiliser des versions control car ...

# Architecture Cloud

L'**architecture cloud** fait référence à la structure et aux composants impliqués dans la fourniture de services de cloud computing. Elle comprend le **frontend**, le **backend**, l'**infrastructure cloud** et la **mise en réseau**, qui fonctionnent ensemble pour fournir des solutions évolutives, sécurisées et fiables pour l'exécution d'applications dans le cloud.

---

### Composants clés de l'architecture cloud :

1.  **Frontend** :  
    La partie du système orientée utilisateur, qui comprend l'**interface utilisateur** (UI) et la **logique côté client**. Elle gère les interactions de l'utilisateur et envoie des requêtes au backend. Son but est d'offrir une expérience conviviale.
    
2.  **Backend** :  
    L'infrastructure côté serveur qui traite les requêtes des utilisateurs et gère les données. Il se compose de **bases de données** et de **serveurs** qui garantissent l'intégrité des données et gèrent la logique métier.
    
3.  **Cloud** :  
    L'infrastructure physique et virtuelle qui stocke et gère les données et les applications. Il peut être **public**, **privé** ou **hybride**, selon la façon dont les ressources sont gérées. Les plateformes cloud comme **AWS**, **Azure** ou **Google Cloud** fournissent des services évolutifs.
    
4.  **Réseau** :  
    Assure la connectivité entre le frontend et le backend en facilitant le **transfert de données** et en permettant la communication entre les composants cloud. Un réseau fiable garantit une **faible latence**, une **haute disponibilité** et des **connexions sécurisées**.
    

---

### Couches de l'architecture cloud :

1.  **Applications et services** :  
    Cette couche comprend les applications et les services avec lesquels les utilisateurs interagissent, tels que les applications web et mobiles.
    
2.  **Couche de virtualisation** :  
    Crée des représentations virtuelles des ressources informatiques (par exemple, serveurs, stockage) et permet une **mise à l'échelle dynamique** des ressources.
    
3.  **Couche matérielle** :  
    L'infrastructure physique (serveurs, stockage, équipements réseau) qui prend en charge le cloud, située dans les centres de données. C'est l'épine dorsale des services cloud.
    

---

### Bonnes pratiques en matière d'architecture cloud :

1.  **Évolutivité** :  
    L'architecture doit prendre en charge la **mise à l'échelle verticale** (ajout de ressources à une seule machine) et la **mise à l'échelle horizontale** (ajout de machines supplémentaires pour gérer la charge). Cela garantit que le système peut croître avec la demande des utilisateurs.
    
2.  **Sécurité** :  
    La mise en œuvre de bonnes pratiques telles que le **chiffrement des données**, l'**authentification multifacteur (MFA)** et le **contrôle d'accès basé sur les rôles (RBAC)** garantit que le système est protégé contre les menaces et est conforme aux réglementations telles que le **RGPD**.
    
3.  **Fiabilité** :  
    S'assurer que le système peut gérer les pannes et récupérer rapidement en utilisant la **redondance**, les **systèmes de résilience** et les **plans de reprise après sinistre**.
    
4.  **Performance** :  
    Optimiser le système pour réduire la latence et améliorer les temps de réponse grâce à l'**équilibrage de la charge** et à une allocation efficace des ressources.
    
5.  **Rentabilité** :  
    Utiliser l'**allocation de ressources à la demande** et l'**auto-scaling** pour garantir une infrastructure cloud rentable sans compromettre les performances ou l'évolutivité.
    

---

### Rôles dans l'architecture cloud :

-   Les **architectes cloud** conçoivent les solutions cloud globales, en garantissant l'évolutivité, la sécurité et l'efficacité.
-   Les **ingénieurs cloud** construisent, mettent en œuvre et maintiennent l'architecture, en assurant un fonctionnement sans problème.

Ensemble, ils s'assurent que les systèmes cloud sont évolutifs, fiables, sécurisés et rentables.

# Conception de système

La **conception de système** est le processus de création de systèmes **évolutifs**, **fiables** et **efficaces**. Elle implique d'examiner attentivement chaque couche, de l'**infrastructure** et du **matériel** aux **logiciels** et au **flux de données**, afin de garantir que les systèmes peuvent gérer les demandes croissantes tout en maintenant les performances et la fiabilité.

La **conception de système** est essentielle pour créer des applications et des services qui peuvent **évoluer**, rester **disponibles** et gérer les **pannes** efficacement. En suivant les meilleures pratiques telles que l'**équilibrage de la charge**, en assurant une **haute disponibilité** et en mettant en œuvre une **architecture évolutive**, les systèmes peuvent répondre aux demandes croissantes sans compromettre les performances.

L'**architecte cloud** est responsable de la conception du système, tandis que les **ingénieurs cloud** construisent et mettent en œuvre l'architecture pour s'assurer qu'elle répond aux exigences de l'entreprise en matière d'**évolutivité**, de **fiabilité**, de **performance** et de **rentabilité**.

---

## Processus de conception de système

Pour construire un système robuste, un processus de conception clair doit être suivi. Ce processus comprend :

-   **Exigences** : Comprendre les exigences commerciales et techniques, telles que les performances, les demandes des utilisateurs et les fonctionnalités spécifiques.
-   **Architecture** : Définir la structure globale, y compris la façon dont les composants interagissent et comment les données circulent entre eux.
-   **Composants** : Identifier les principaux composants du système (par exemple, serveurs, bases de données, API).
-   **Données** : Gérer la façon dont les données sont stockées, traitées et récupérées.
-   **Interface** : Définir la façon dont les utilisateurs interagissent avec le système (par exemple, via des applications frontend ou des API).
-   **Sécurité** : S'assurer que le système est protégé contre les accès non autorisés et les vulnérabilités.

---

## Backend vs Frontend

Dans la conception de système, il est essentiel de faire la distinction entre le **backend** et le **frontend** :

-   **Frontend** : Il s'agit de la **partie du système orientée utilisateur**, comprenant les pages web, les applications mobiles et les interfaces utilisateur. Il gère l'**interaction utilisateur** et envoie des requêtes au backend.
-   **Backend** : Il s'agit de la partie **côté serveur** du système qui traite les requêtes des utilisateurs, gère les bases de données et gère la logique de l'application.

Les deux couches doivent fonctionner de manière transparente pour garantir aux utilisateurs une expérience fluide et efficace.

![user_client.png](/portfolio/blog/week2/user_client.png)

---

## Mise à l'échelle dans la conception de système

La **mise à l'échelle** fait référence à la capacité du système à **gérer des charges croissantes**. Il existe deux principaux types de mise à l'échelle :

![horizontal_vertical_sclaing.png](/portfolio/blog/week2/horizontal_vertical_sclaing.png)

### Mise à l'échelle verticale

La **mise à l'échelle verticale** implique d'**augmenter la puissance de traitement** d'une seule machine. Cela se fait en mettant à niveau le matériel du serveur pour le rendre plus puissant, par exemple en ajoutant plus de CPU, de RAM ou de stockage.

-   **Avantages** : Simple à mettre en œuvre, pas besoin de modifier l'architecture de l'application.
-   **Limitations** : Il y a une **limite à la quantité que vous pouvez mettre à l'échelle verticalement** (limitations matérielles), et cela peut devenir très **coûteux**.

### Mise à l'échelle horizontale

La **mise à l'échelle horizontale** implique d'ajouter **plusieurs instances de serveurs** pour gérer la demande croissante. Au lieu de mettre à niveau un seul serveur, vous ajoutez plus de serveurs pour répartir la charge de travail.

-   **Avantages** : Potentiel de **croissance illimité**, meilleure distribution du trafic et tolérance aux pannes.
-   **Limitations** : Nécessite une architecture plus complexe, telle que l'équilibrage de la charge et la gestion de plusieurs serveurs.

La mise à l'échelle horizontale est généralement plus **rentable** et **évolutive** à long terme.

---

## Équilibrage de la charge

Un **équilibreur de charge** est un composant essentiel de la conception de système, en particulier pour les systèmes évolutifs et fiables. Il **distribue le trafic entrant** sur plusieurs serveurs backend, garantissant qu'aucun serveur unique n'est submergé par trop de requêtes.

### Principaux avantages de l'équilibrage de la charge :

-   **Évolutivité** : Permet au backend d'évoluer en ajoutant plus de serveurs à mesure que la demande augmente.
-   **Réduction des temps d'arrêt** : Si un serveur tombe en panne, l'équilibreur de charge redirige le trafic vers des serveurs en bon état.
-   **Amélioration des performances** : Répartit la charge de travail uniformément sur les serveurs, évitant ainsi les goulots d'étranglement.
-   **Déchargement SSL** : Peut gérer le déchiffrement et le chiffrement SSL, réduisant ainsi la charge de travail sur les serveurs backend.
-   **Contrôles de santé** : Vérifie régulièrement l'état des serveurs backend pour s'assurer qu'ils sont opérationnels.
-   **Persistance de session** : Garantit que les sessions des utilisateurs sont maintenues sur plusieurs serveurs backend, améliorant ainsi l'expérience utilisateur.

---

## Haute disponibilité

La **haute disponibilité** est la capacité d'un système à **rester opérationnel** et **accessible** malgré les pannes. Elle garantit que le système a un **temps d'arrêt minimal** et est toujours disponible pour les utilisateurs.

### Composants de la haute disponibilité :

-   **Équilibreur de charge** : Assure une distribution continue du trafic, même en cas de pannes de serveur.
-   **Redondance** : Avoir **plusieurs instances** de composants critiques afin que si l'un d'eux tombe en panne, d'autres prennent le relais.
-   **Processus de basculement** : Bascule automatiquement vers des systèmes de sauvegarde en cas de panne.
-   **Contrôles de santé** : Surveillance constante des composants du système pour s'assurer qu'ils sont opérationnels.

La haute disponibilité améliore la **continuité des activités**, renforce la **confiance** des utilisateurs et maximise le **temps de fonctionnement**.

---

## Tolérance aux pannes

La **tolérance aux pannes** est la capacité d'un système à **continuer à fonctionner** même si certains de ses composants tombent en panne. Elle implique de concevoir des systèmes capables de gérer les pannes matérielles, logicielles ou réseau sans provoquer d'**interruption** du service.

### Techniques de tolérance aux pannes :

-   **Clusters de secours** : Au cas où l'ensemble du cluster à haute disponibilité tomberait en panne, un **cluster de secours** peut prendre le relais, garantissant que le système continue de fonctionner.
-   **Redondance** : Plusieurs sauvegardes pour les composants critiques garantissent qu'il y a toujours un repli.
-   **Basculement** : Similaire à la haute disponibilité, mais avec davantage l'accent sur le fonctionnement continu, même en cas de pannes multiples.

### Principales différences entre la tolérance aux pannes et la haute disponibilité :

-   La **tolérance aux pannes** garantit un **fonctionnement continu** avec un temps d'arrêt nul, même en cas de pannes.
-   La **haute disponibilité** minimise les temps d'arrêt, mais peut nécessiter un certain temps de récupération en cas de pannes.

La tolérance aux pannes et la haute disponibilité sont toutes deux cruciales pour garantir la **fiabilité du système** et la confiance des utilisateurs.

# Console AWS

J'ai pu utiliser la console aws pour la première fois pour :

### Créer un nouvel utilisateur IAM

### Ajouter une politique à l'utilisateur

### Créer un bucket s3

### Ajouter un fichier au bucket

## Projet : Concevoir une architecture de base pour une application web

Enfin, il y avait un projet. Vous pouvez le trouver ici

![Week2_Architecture_basic.png](/portfolio/blog/week2/Week2_Architecture_basic.png)

### Objectif du projet :

L'objectif de ce projet est de concevoir une infrastructure cloud qui prend en charge une application web, en garantissant une haute disponibilité, une tolérance aux pannes et une évolutivité.

### Aperçu de l'architecture :

1.  **Pare-feu** :  
    Le premier composant de mon architecture est le pare-feu. Il agit comme une couche de sécurité qui filtre les requêtes entrantes en fonction de règles prédéfinies. Seul le trafic légitime est autorisé à passer, protégeant ainsi l'infrastructure contre les attaques potentielles.
    
2.  **Équilibreur de charge** :  
    Une fois que le trafic a franchi le pare-feu, il est dirigé vers l'équilibreur de charge. Le rôle de l'équilibreur de charge est de distribuer les requêtes sur les ressources disponibles les plus efficaces, garantissant ainsi un trafic équilibré et des performances optimales. Je déploie plusieurs équilibreurs de charge pour gérer l'augmentation du trafic et assurer la redondance en cas de panne de l'un d'eux.
    
3.  **Redondance géographique** :  
    J'ai conçu l'architecture pour qu'elle s'étende sur deux régions géographiques. Cela permet une reprise après sinistre si une région devient indisponible. De plus, le trafic entrant peut être acheminé vers la région la plus proche en fonction de l'emplacement de l'utilisateur, ce qui améliore le temps de réponse.
    
4.  **Clusters dans chaque région** :
    
    -   **Cluster à haute disponibilité** : Ce cluster contient les principales ressources nécessaires pour exécuter l'application web. Il gère les opérations normales et est conçu pour des performances élevées.
    -   **Cluster de secours** : Le cluster de secours sert de sauvegarde. Si le cluster à haute disponibilité subit une panne dans la même région, le cluster de secours prend le relais, assurant ainsi la continuité.
5.  **Composants de l'application** :
    
    -   **Frontend** : Le frontend de l'application web réside dans un sous-réseau public, ce qui le rend accessible aux utilisateurs. Il fournit l'interface utilisateur et gère les requêtes côté client.
    -   **Backend** : Le backend, composé d'API et de bases de données, est hébergé dans un sous-réseau privé pour renforcer la sécurité. En isolant le backend de l'accès public, je réduis la surface d'attaque et protège les données sensibles.

### Stratégies de mise à l'échelle pour la haute disponibilité et la tolérance aux pannes :

Chaque composant de l'architecture est mis à l'échelle en fonction de sa fonction et de ses besoins pour assurer la performance et la résilience :

| Composant                         | Type de mise à l'échelle | Raison                                                                                                                                                                                                                            |
| --------------------------------- | ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Frontend (CDN)**                | Mise à l'échelle horizontale | La mise à l'échelle horizontale facilite l'ajout de serveurs supplémentaires, offrant ainsi une meilleure tolérance aux pannes.                                                                                                   |
| **Backend (Serveurs d'applications)** | Mise à l'échelle horizontale | Plusieurs serveurs backend garantissent que davantage de requêtes utilisateur peuvent être traitées simultanément.                                                                                                         |
| **Équilibreur de charge**                 | Mise à l'échelle horizontale | Plusieurs équilibreurs de charge distribuent le trafic plus efficacement et offrent une redondance.                                                                                                                            |
| **Pare-feu**                      | Mise à l'échelle horizontale | La mise à l'échelle horizontale garantit que davantage de trafic peut être traité et que le système reste sécurisé.                                                                                                              |
| **Base de données (SQL)**                | Mise à l'échelle verticale   | Pour les bases de données relationnelles, la mise à l'échelle verticale est souvent utilisée car il est plus complexe de mettre à l'échelle horizontalement et de maintenir la cohérence des données sur plusieurs instances. |

---

### Résumé des choix de conception :

-   La **mise à l'échelle horizontale** est choisie pour la plupart des composants car elle offre une meilleure tolérance aux pannes, de meilleures performances et une facilité de mise à l'échelle en ajoutant plus de serveurs.
-   La **redondance géographique** garantit que le système peut gérer les pannes régionales, en acheminant automatiquement le trafic vers la région disponible la plus proche.
-   Les **clusters** sont utilisés dans chaque région pour fournir des capacités de basculement, garantissant que si un ensemble de ressources tombe en panne, le cluster de secours prend le relais sans affecter les utilisateurs.
-   La **mise à l'échelle verticale** est appliquée à la base de données relationnelle pour améliorer la capacité sans la complexité de la gestion de plusieurs instances de base de données.

Cette architecture est conçue pour être hautement disponible, évolutive et sécurisée, ce qui la rend bien adaptée pour prendre en charge une application web robuste.