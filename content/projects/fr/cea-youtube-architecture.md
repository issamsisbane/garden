---
title: "Concevoir une Architecture pour YouTube"
description: "Ce projet vise à concevoir une architecture pour quelques-unes des fonctionnalités les plus utilisées de YouTube."
lang: "fr"
pubDate: "Sept 16 2024"
heroImage: "/portfolio/projects/cea-youtube-architecture/youtube.webp"
badge: "PERSONNEL"
tags: ["Cloud", "Architecture", "Cloud Engineer Academy"]
---

1 — **Besoins** </br>
2 — **Uploader une Vidéo** </br>
3 — **Rechercher et Regarder des Vidéos** </br>
4 — **Composants Clés du Système** </br>
5 — **Points de Vigilance** </br>
6 — **Conclusion** </br>

---

## 1 - Besoins

Avant de se lancer dans la conception de l’architecture, il est essentiel de bien comprendre les **fonctionnalités** de l’application, et de poser les **besoins techniques**.

Les fonctionnalités clés :

- **Uploader des vidéos**
- **Rechercher des vidéos**
- **Regarder des vidéos**
- **Filtrer les contenus adultes**

Les exigences techniques pour l’architecture :

- **Scalabilité** : Le système doit gérer des millions d’utilisateurs et de vidéos uploadées en même temps.
- **Résilience** : Il doit être tolérant aux pannes et rester disponible 24/7.
- **Efficacité des coûts** : Il faut optimiser l’usage des ressources pour un bon équilibre coût/performance.
- **Sécurité** : Les données doivent être stockées de manière sécurisée et les accès non autorisés bloqués.

---
## 2 - Upload d’une Vidéo

![](/portfolio/projects/cea-youtube-architecture/youtube_upload_video_architecture.gif)

### 1. **Accès à YouTube**

Les **créateurs de contenu** (YouTubers) accèdent à YouTube via leur **navigateur**, en utilisant HTTPS pour garantir une communication sécurisée.

### 2. **Mise en ligne de la vidéo**

#### **Données Vidéo**

La première étape consiste à transférer la **vidéo elle-même**.

- Les YouTubers uploadent souvent des vidéos en très haute résolution (par exemple, en 4K).
- Comme la vidéo est une **donnée non structurée**, qui nécessite **scalabilité** et **durabilité**, le mieux est d’utiliser du **stockage objet** (comme **Amazon S3**). C’est économique grâce à son modèle **pay-as-you-go** (tu paies uniquement ce que tu stockes), donc parfait pour gérer de très gros volumes de fichiers vidéo.

#### **Métadonnées**

Les métadonnées contiennent des infos comme le titre de la vidéo, sa description, les tags, etc. C’est une **donnée structurée** qui a besoin d’un stockage rapide et scalable.

- Un système relationnel (type **MySQL**) risque d’avoir du mal à suivre à l’échelle de YouTube, car il scale **verticalement**, ce qui peut vite coûter cher et devenir un goulot d’étranglement.
- À la place, on préfère utiliser une **base NoSQL** (comme **Cassandra** ou **DynamoDB**) qui scale **horizontalement**, répartissant la charge sur plusieurs serveurs → bien plus adapté à un gros volume de métadonnées.

### 3. **Traitement Vidéo**

Une fois la vidéo uploadée, YouTube la traite en :

- La convertissant en plusieurs **résolutions** (240p, 360p, 720p, 1080p, 4K…), pour qu’elle soit lisible sur n’importe quel appareil et avec tout type de connexion.
- Ce boulot peut être géré par des **microservices**, des **serveurs dédiés** ou des **fonctions serverless** pour l'encodage/transcodage → objectif : que tout le monde puisse la lire correctement.

### 4. **Analyse du Contenu**

En parallèle du traitement, une **analyse automatique** est lancée pour vérifier si la vidéo respecte les règles de YouTube.

- Le système analyse la vidéo **frame par frame** pour détecter des contenus inappropriés.
- Si une anomalie est détectée, les **métadonnées** sont mises à jour pour **restreindre** ou **bloquer** l’accès à la vidéo.

### 5. **Stockage Optimisé**

Une fois traitée, chaque version de la vidéo (en différentes résolutions) est stockée dans un **autre système de stockage objet**, optimisé pour le streaming.

- Des **fonctions serverless** (type **AWS Lambda**) peuvent automatiser le déplacement des vidéos vers la bonne destination en fonction des événements (ex : après traitement).

### 6. **Diffusion du Contenu**

Pour garantir une lecture fluide, YouTube s’appuie sur un **CDN** (Content Delivery Network).

- Le **CDN** permet de mettre en cache les vidéos au plus près des utilisateurs, selon leur position géographique.
- Quand quelqu’un regarde une vidéo, elle est servie depuis le **nœud CDN le plus proche**, ce qui réduit le **temps de chargement** et la **latence**.
- Si la vidéo n’est pas encore en cache, elle est récupérée depuis le stockage objet, puis mise en cache pour les prochaines requêtes.

---

## 3 - Rechercher et Regarder des Vidéos

![](/portfolio/projects/cea-youtube-architecture/youtube_watch_video_architecture.gif)

### 1. **Accès à YouTube**

Quand un utilisateur arrive sur YouTube, il est accueilli par la **page d’accueil**.

- Cette page est composée principalement de **contenu statique** (miniatures, suggestions, etc.).
- Ce contenu statique est stocké dans du **stockage objet**, ce qui permet un chargement rapide.

### 2. **Recherche de Vidéos**

Quand un utilisateur effectue une recherche, la requête passe d’abord par le **CDN** :

- Si les **résultats de recherche** sont déjà en cache, ils sont renvoyés **instantanément**.
- Sinon, la requête passe par un **API Gateway**, qui la transfère à une **fonction serverless**.
  - Cette fonction interroge la **base de métadonnées** pour trouver les vidéos correspondantes (titre, description, tags…).
  - Les résultats sont ensuite affichés dans la page, qui contient surtout des métadonnées.

La **page d’accueil** est plutôt statique, mais après une recherche, YouTube affiche du **contenu dynamique** et personnalisé.

### 3. **Lecture d’une Vidéo**

Quand un utilisateur clique sur une vidéo :

- Si elle est déjà dans le **cache CDN**, elle est servie instantanément.
- Sinon, le CDN va la récupérer dans le **stockage objet**, tout en la **mettant en cache** pour les futurs utilisateurs de la même région.

Ce système garantit que les **vidéos populaires** sont toujours servies avec une **latence minimale** et un usage **optimisé de la bande passante**.

---

## 4 - Composants Clés de l’Architecture YouTube

### 1. **Stockage Objet**

- Sert à stocker les fichiers vidéo non structurés.
- Offre **scalabilité**, **durabilité** et **coût optimisé** pour de gros volumes de données.

### 2. **Base de Données NoSQL**

- Utilisée pour stocker les **métadonnées** de millions de vidéos.
- On choisit une base **NoSQL** car :
  - Les données sont de type **"free form"** (chaque vidéo peut avoir des champs différents).
  - Elle scale **horizontalement**, donc plus adaptée au trafic massif que les bases relationnelles classiques.

### 3. **Traitement & Analyse Vidéo**

- Convertit les vidéos en plusieurs formats.
- Effectue des **vérifications automatiques** pour détecter du contenu inapproprié.

### 4. **CDN (Content Delivery Network)**

- Met en cache les vidéos au plus proche des utilisateurs.
- Réduit les temps de chargement et **améliore l’expérience de streaming**.

### 5. **API Gateway**

- Sert de point d’entrée pour les requêtes **dynamiques** (recherche, recommandations...).
- Route les requêtes vers les bons services backend.

### 6. **Fonctions Serverless**

- Utilisées pour des tâches **événementielles** :
  - Déplacement automatique des fichiers vidéos après upload.
  - Traitement des recherches utilisateur.
  - Automatisation des workflows.

---

## 5 - Considérations

### **1. Scalabilité**

Pour gérer une base d’utilisateurs massive et un flux continu d’uploads, l’architecture de YouTube doit être capable de scaler **horizontalement** et **verticalement**, à plusieurs niveaux :

- **Upload et Stockage Vidéo** :
  
  - **Stockage Objet** : Grâce à un service de stockage objet scalable, YouTube peut stocker et gérer une quantité énorme de données non structurées. Ce type de stockage s’adapte automatiquement aux volumes croissants (vidéos, miniatures, assets médias) sans interruption.
  
  - **Auto-scaling pour le traitement vidéo** : La couche de traitement (ex : transcodage) repose sur un **groupe auto-scalé** de serveurs ou microservices, qui monte ou descend en capacité en fonction de la charge. Résultat : plusieurs vidéos peuvent être traitées en parallèle, avec un usage optimisé des ressources.

- **Stockage des métadonnées** :

  - **Base NoSQL** : Une base NoSQL scalable horizontalement permet de gérer et rechercher à travers des milliards d’entrées de métadonnées. Elle scale en ajoutant des **nœuds** supplémentaires, ce qui garantit des perfs élevées même en cas de trafic intense.

- **Diffusion du contenu** :
  
  - **CDN** : Le CDN met les vidéos en cache près des utilisateurs, ce qui allège la charge sur les serveurs principaux et permet de répondre à un grand nombre de requêtes simultanées. Les CDN scalent dynamiquement leurs **points d’accès** partout dans le monde, en fonction de la demande.



### **2. Résilience**

La résilience garantit que YouTube reste dispo et opérationnel même en cas de panne, souci réseau ou défaillance matérielle :

- **Redondance des données** :
  
  - **Stockage Objet** : Des services comme Amazon S3 offrent une redondance native, avec réplication automatique des fichiers dans plusieurs **zones de disponibilité**. Ça assure la **durabilité** des données, même si un data center tombe.
  
  - **Réplication multi-région** : Les bases NoSQL peuvent se synchroniser entre plusieurs régions. En cas de panne régionale, le trafic est redirigé vers une **réplica** sans coupure de service.

- **Tolérance aux pannes** :
  
  - **Microservices** : Le découpage en microservices permet d’isoler les problèmes. Si le service de traitement vidéo plante, ça n’impacte ni la recherche ni la lecture. Chaque service est géré et scalé indépendamment.
  
  - **Load Balancers** : Ils répartissent la charge entre plusieurs instances. Si une instance tombe, le load balancer redirige automatiquement vers une autre instance **saine**.

- **Dégradation progressive (graceful degradation)** :
  
  - **Fallbacks** : Si un service est temporairement HS (ex : le transcodage), l’app peut continuer à fonctionner en mode dégradé (on autorise les uploads, mais on différera le traitement par exemple).



### **3. Latence**

La **latence** est un facteur clé pour YouTube : les utilisateurs attendent un démarrage rapide et une lecture fluide.

- **Lecture Vidéo** :
  
  - **CDN** : Le caching côté **edge** réduit le temps de récupération de la vidéo. L’utilisateur commence à regarder sans attendre, même en haute qualité.
  
  - **Streaming adaptatif** : Les vidéos sont disponibles en plusieurs résolutions. Le lecteur s’adapte automatiquement à la bande passante de l’utilisateur → pas de buffering.

- **Recherche & Accès aux données** :
  
  - **Cache mémoire** : Les données les plus demandées (ex : vidéos populaires) peuvent être mises en cache (ex : **Redis**, **Memcached**) pour accélérer les temps de réponse.
  
  - **Requêtes distribuées** : Les bases NoSQL permettent de faire des requêtes rapides, même à grosse échelle. Les requêtes sont réparties entre plusieurs nœuds pour optimiser la latence.

- **API Gateway** :
  
  - **Routage optimisé** : Le gateway oriente les requêtes vers les bons services en back. Il peut aussi **cacher** les réponses fréquentes, ce qui réduit la charge côté backends et accélère les réponses.

---


## 6 - **Conclusion**

L’architecture de YouTube doit être capable de gérer un **trafic massif**, de **stocker et retrouver des volumes énormes de données vidéo**, tout en **livrant le contenu rapidement** à des utilisateurs répartis partout dans le monde.

En s’appuyant sur du **stockage objet** pour les vidéos, des **bases NoSQL** pour les métadonnées, et des **CDN** pour distribuer le contenu, YouTube garantit une **scalabilité** optimale, une **haute disponibilité** et de **bonnes performances**.

L’ajout de **fonctions serverless** et d’un **API Gateway** permet de gérer efficacement les requêtes dynamiques, tout en facilitant les échanges dans une architecture microservices complexe — de façon fluide, rapide et sécurisée.
