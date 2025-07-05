---
title: "Améliorer mes compétences Cloud - Semaine 1 - Principes fondamentaux du Cloud"
description: "Semaine 1 pour améliorer mes compétences Cloud."
lang: "fr"
pubDate: "Sept 12 2024"
heroImage: "/portfolio/blog/week1/Medium_article_title.drawio.png"
badge: "Améliorer mes compétences Cloud"
tags: ["Cloud", "Network", "Cloud Engineer Academy"]
---

*J'ai passé ces cinq dernières années à étudier l'informatique à l'école, dont les trois dernières en **école d'ingénieurs**, où j'ai obtenu un **diplôme généraliste en informatique**. Pendant ce temps, j'ai eu l'occasion de travailler en tant qu'**apprenti ingénieur cloud**, ce qui m'a permis d'acquérir une expérience pratique, notamment avec **Azure** et diverses **technologies cloud**. Cette expérience pratique a approfondi ma compréhension du cloud computing et de l'informatique dans son ensemble.*

*Aujourd'hui, alors que je me prépare à entrer sur le marché du travail et à commencer un nouveau rôle d'**Ingénieur Cloud/DevOps**, je me sens confiant, mais aussi conscient qu'il y a toujours place à la croissance. Bien que mon apprentissage m'ait fourni une base solide, j'ai acquis de nombreuses compétences liées au cloud **sur le tas**, et j'ai réalisé que je voulais **améliorer mon expertise** et acquérir une expérience plus **structurée et pratique**.*

*Pour continuer à faire progresser mes compétences, j'ai pris la décision de rejoindre une **Cloud Academy** dirigée par un YouTuber que je suis depuis plus d'un an maintenant, **Suleymann**. Son approche pratique des technologies cloud a résonné en moi, et j'y ai vu une occasion parfaite de **consolider mes connaissances** et de combler les lacunes que je pourrais avoir.*

*Dans le cadre de ce nouveau parcours, j'ai décidé de **documenter tout ce que j'apprends** à travers des **articles de blog**. Cela m'aidera non seulement à conserver les connaissances, mais aussi à partager mes expériences et mes réflexions avec les autres. J'encourage tous ceux qui lisent à **commenter, à partager leurs réflexions** ou à poser des questions. L'apprentissage est un processus collaboratif, et j'aimerais beaucoup interagir avec d'autres personnes passionnées par le cloud computing.*

*Comme j'ai déjà une expérience en ingénierie cloud et logicielle, je marquerai les nouveaux concepts que je rencontrerai avec le hashtag **#nouveau**. Cela permettra aux lecteurs de voir ce qui est vraiment nouveau pour moi, ce qui rendra le blog plus accessible à ceux qui peuvent se trouver à différents stades de leur parcours d'apprentissage.*

*En général, chaque module de l'académie est conçu pour être terminé en une semaine. Cependant, compte tenu de mes connaissances antérieures et du fait que les modules initiaux sont pour la plupart des **révisions** pour moi, je prévois de **progresser à un rythme plus rapide**. Cela me permettra de passer rapidement à de nouveaux domaines et d'acquérir des connaissances plus approfondies sur les sujets avancés du cloud et de DevOps.*

---

1 - **Modèles Cloud** <br/>
2 - **Pourquoi choisir le Cloud Computing ?** <br/>
3 - **Modèles de déploiement Cloud** <br/>
4 - **Meilleures pratiques pour les comptes AWS** <br/>
5 - **SDLC (Cycle de vie du développement logiciel)** <br/>
6 - **Virtualisation** <br/>
7 - **Réseautique** <br/>
8 - **OS** <br/>
9 - **Bases de données** <br/>

---

# 1 - Modèles Cloud

**Il** existe trois principaux **modèles cloud** parmi lesquels les organisations peuvent choisir en fonction de leurs besoins :

## **IAAS** (Infrastructure en tant que service)

**L'Infrastructure en tant que service (IAAS)** est un modèle de cloud computing dans lequel le fournisseur de cloud gère l'infrastructure **matérielle** sous-jacente, notamment les **serveurs**, le **stockage** et les composants de **réseau**. Cela permet aux entreprises de louer des ressources informatiques à la demande sans avoir besoin d'acheter et de maintenir du matériel physique.

- **Serveurs** : Machines virtuelles ou physiques qui traitent les données.
- **Espace de stockage** : Solutions de stockage de données évolutives.
- **Réseaux** : Réseau virtuel qui connecte les ressources et assure la sécurité.

**Exemple** : Amazon EC2, où vous pouvez louer des serveurs virtuels pour exécuter des applications.

## **PAAS** (Plateforme en tant que service)

**La Plateforme en tant que service (PAAS)** fournit une plateforme qui abstrait l'infrastructure sous-jacente, permettant aux développeurs de se concentrer uniquement sur l'écriture de code et le déploiement d'applications. Le fournisseur de cloud prend en charge la maintenance de la plateforme, ce qui permet de rationaliser les processus de développement.

**Permet aux développeurs de** :

- **Construire** : Créer des applications à l'aide d'une variété d'outils et de langages de développement.
- **Tester** : Exécuter des tests pour garantir les performances et la fiabilité des applications.
- **Déployer** : Lancer des applications sans se soucier de l'infrastructure sous-jacente.

Le fournisseur gère :

- **Mise à l'échelle** : Ajustement automatique des ressources en fonction de la demande.
- **Patching** : Maintenir la plateforme à jour avec les dernières mises à jour de sécurité et de logiciels.
- **Maintenance** : Gérer les tâches de gestion de plateforme de routine, ce qui permet aux développeurs de se concentrer sur l'innovation.

**Exemple** : AWS Elastic Beanstalk, qui permet aux développeurs de déployer et de gérer des applications sans avoir besoin de gérer l'infrastructure sous-jacente.

## **SAAS** (Logiciel en tant que service)

**Le Logiciel en tant que service (SAAS)** fournit des applications logicielles sur Internet sur la base d'un **abonnement**. Dans ce modèle, les utilisateurs peuvent accéder aux applications logicielles à partir de n'importe quel appareil disposant d'une connexion Internet, sans se soucier de l'installation, de la maintenance ou de la gestion de l'infrastructure. Le fournisseur de cloud s'occupe de tout, y compris des mises à jour logicielles, de la sécurité et de l'infrastructure.

**Exemple** : Netflix, où les utilisateurs s'abonnent pour accéder à une vaste bibliothèque de films et de séries sans posséder ni gérer directement le contenu.

---

# 2 - Cloud Computing

Le cloud computing **transforme fondamentalement** la façon dont les entreprises **opèrent** et **gèrent** leurs données. Il fournit un large éventail de services, notamment des **serveurs**, du **stockage**, des **bases de données** et de la **réseau**, fournis via Internet. Ce modèle permet aux utilisateurs d'accéder aux ressources informatiques sur une base de **paiement à l'utilisation**, **éliminant** le besoin de centres de données et de serveurs physiques.

## Avantages du cloud

- **Self-service à la demande** : Les utilisateurs peuvent **provisionner automatiquement** des ressources informatiques presque instantanément, telles que le **temps serveur** et le **stockage réseau**, sans intervention humaine du fournisseur de services.
- **Évolutivité et élasticité** : La possibilité **d'augmenter ou de diminuer** la quantité de ressources utilisées en fonction de vos besoins actuels. Cela garantit que vous ne payez que pour ce que vous utilisez et que vous pouvez gérer efficacement les **charges de travail variables**.
- **Service mesuré** : Les services cloud sont **mesurés**, ce qui permet un **contrôle précis** des ressources. Vous pouvez **surveiller l'utilisation**, optimiser les performances et assurer une **facturation transparente**, en ne payant que ce que vous consommez.

## Migration vers le cloud

Pour les entreprises, la décision de migrer vers le cloud est souvent motivée par le besoin d'une **efficacité**, d'une **compétitivité** et d'une **innovation** accrues.

- **Rentabilité** : Élimine le besoin de maintenir des centres de données physiques, ce qui réduit les **dépenses d'investissement**. Vous ne payez que pour les ressources que vous utilisez, ce qui permet une meilleure **gestion financière**.
- **Flexibilité des ressources** : Le cloud peut facilement **s'adapter à la hausse ou à la baisse** pour répondre à vos besoins, que vous ayez besoin de plus ou de moins de ressources à un moment donné.
- **Sécurité des données** : Les fournisseurs de cloud utilisent des **mécanismes de redondance** pour assurer la **sécurité** des données, en veillant à ce que vos informations soient protégées et sauvegardées à plusieurs endroits.
- **Fiabilité** : Grâce à la **redondance** intégrée, le cloud garantit que vos applications restent **opérationnelles**, offrant une **disponibilité** élevée même en cas de défaillance matérielle.
- **Collaboration améliorée** : Le cloud permet aux personnes de **travailler de n'importe où**, ce qui facilite une meilleure **collaboration** et communication entre des équipes géographiquement dispersées.

## Avantages pour les entreprises

- **Innovation et agilité** : Le cloud permet aux entreprises **d'expérimenter** et de **mettre en œuvre** de nouvelles idées rapidement et avec un **risque moindre**. Cela accélère **l'innovation** et permet une **adaptation** rapide aux changements du marché.
- **Réactivité à la demande** : Les entreprises peuvent **répondre rapidement aux opportunités et aux défis** en provisionnant rapidement des ressources, en s'assurant qu'elles sont toujours prêtes à répondre aux besoins des clients.
- **Concentration sur les objectifs principaux** : En réduisant le temps passé à configurer les **centres de données sur site** et à effectuer des **tâches de maintenance**, les entreprises peuvent se concentrer davantage sur leurs **objectifs principaux** et leurs objectifs stratégiques.
- **Portée mondiale** : Le cloud permet aux entreprises **d'opérer à l'échelle mondiale**, améliorant **l'expérience client** en fournissant des services cohérents et fiables partout dans le monde.

Le cloud computing est une **décision stratégique** qui a un impact sur divers aspects d'une organisation. Pour rester **compétitives**, **agiles** et **efficaces**, les entreprises adoptent de plus en plus de solutions cloud.

---

# 3 - Modèles de déploiement Cloud

Les modèles de déploiement cloud déterminent plusieurs aspects clés de la façon dont les ressources de cloud computing sont utilisées et gérées, notamment :

- **Gestion des données** : Comment les données sont stockées, protégées et accessibles.
- **Contrôle des ressources** : La mesure dans laquelle vous pouvez gérer et configurer l'environnement cloud.
- **Implications en matière de coûts** : L'impact financier en fonction du modèle de déploiement choisi.
- **Évolutivité** : La capacité à faire évoluer facilement les ressources en fonction de l'évolution des demandes.

## Cloud public

Le cloud public est un environnement où les ressources informatiques (serveurs, stockage, applications, etc.) sont fournies par un fournisseur tiers via Internet. Dans ce modèle :

- Les ressources sont **partagées** entre plusieurs utilisateurs ou organisations.
- La gestion de l'infrastructure est **entièrement gérée** par le fournisseur de services cloud.
- Ce modèle offre une **évolutivité** et une **flexibilité** élevées, souvent à un coût **inférieur**, car vous ne payez que pour **ce que vous utilisez**.
- Cependant, comme les ressources sont **partagées**, il peut y avoir moins de **contrôle** sur la **sécurité** et la conformité.

## Cloud privé

Dans un cloud privé, l'infrastructure est dédiée **uniquement** à une **seule** organisation. Les principales caractéristiques sont les suivantes :

- Les ressources ne sont **pas partagées** avec d'autres, ce qui offre un **contrôle** et une **sécurité** **accrus**.
- L'organisation est **responsable** de la **gestion** et de la **maintenance** de l'infrastructure, soit sur site, soit par l'intermédiaire d'un service d'hébergement tiers.
- Ce modèle est idéal pour les organisations ayant des **exigences** **réglementaires** **strictes** ou celles ayant besoin de mesures de **sécurité** **renforcées**.
- Il implique généralement des coûts **plus élevés** en raison de la nécessité d'un matériel **dédié** et d'une gestion spécialisée.

## Cloud hybride

Le cloud hybride combine des éléments des clouds publics et privés, créant un environnement intégré où une organisation peut :

- Utiliser le cloud public pour les opérations **non sensibles** ou les charges de travail **évolutives**, en bénéficiant de sa **rentabilité** et de sa **flexibilité**.
- Conserver le cloud privé pour les opérations **sensibles** et **critiques** qui nécessitent un **contrôle** et une **sécurité** **accrus**.
- **Transférer** de manière transparente les données et les applications **entre** les clouds publics et privés, ce qui permet une utilisation optimale des ressources.
- Ce modèle offre un équilibre entre **évolutivité**, **rentabilité** et **sécurité**, ce qui le rend adapté aux entreprises ayant des besoins informatiques diversifiés.

---

# 4 - Meilleures pratiques pour les comptes AWS  #nouveau

- **1 - Activer l'authentification multifacteur (MFA) pour le compte racine** :
    La première étape consiste à activer **l'authentification multifacteur (MFA)** sur le compte racine. Cela ajoute une couche de sécurité supplémentaire, en garantissant que seuls les utilisateurs autorisés peuvent accéder au compte en exigeant une deuxième forme d'authentification en plus du mot de passe.

- **2 - Limiter l'utilisation du compte racine** :
    Pour les meilleures pratiques de sécurité, le **compte racine ne doit pas être utilisé pour les opérations quotidiennes**. Au lieu de cela, le compte racine ne doit être accessible que pour les tâches critiques qui nécessitent des autorisations de niveau racine.

- **3 - Créer un utilisateur administrateur pour les opérations régulières** :
    Après avoir sécurisé le compte racine, créez un **utilisateur IAM dédié avec des privilèges d'administrateur**. Cet utilisateur sera utilisé pour toutes les tâches régulières, y compris la gestion des ressources et la création d'applications, tout en maintenant la sécurité du compte racine. Nous devons également activer la MFA pour cet utilisateur.

- **4 - Définir des limites budgétaires** :
    Pour éviter des frais imprévus sur AWS, il est important de **définir un budget** pour vos ressources. AWS vous permet de configurer des budgets qui envoient des alertes lorsque vos dépenses approchent d'une limite prédéfinie, ce qui vous aide à maîtriser les coûts.

---

# 5 - SDLC (Cycle de vie du développement logiciel)

### Aperçu de la méthodologie de développement logiciel

La **méthodologie de construction et de livraison de projets logiciels** est axée sur la production de **logiciels de haute qualité** dans les **plus brefs délais possibles**, avec la **plus haute qualité** et le **coût le plus bas**. Cela nécessite une approche structurée et une attention aux détails à chaque étape du développement.

### Objectifs clés :

- **Fournir des logiciels de haute qualité** qui répondent aux besoins des utilisateurs.
- **Minimiser le temps de développement** sans sacrifier la qualité.
- **Réduire les coûts** en optimisant les ressources et les processus.

---

### Processus de développement pour les fonctionnalités, les projets et les idées

Pour chaque fonctionnalité, projet ou idée, nous suivons un **processus méticuleux** qui garantit une livraison en douceur et des résultats optimaux. Les étapes comprennent :

1. **Conceptualisation** :
    La phase initiale où les idées sont remuées et l'objectif général du projet est défini.

2. **Conception** :
    Dans cette phase, **l'architecture**, **l'interface utilisateur** et les **structures de base de données** sont conçues. Ceci est essentiel pour aligner la fonctionnalité sur les besoins des utilisateurs.

3. **Développement** :
    La phase de codage proprement dite, où la conception est traduite en logiciel fonctionnel.

4. **Test** :
    Le logiciel est soumis à des tests rigoureux pour identifier et corriger les **bogues, les problèmes** et pour s'assurer que toutes les **exigences sont satisfaites**.

5. **Lancement** :
    Une fois testé et approuvé, le logiciel est **déployé** en production pour que les utilisateurs puissent y accéder.

### Modèles de cycle de vie du développement logiciel (SDLC)

Il existe plusieurs modèles utilisés dans le cycle de vie du développement logiciel (SDLC), chacun ayant ses avantages en fonction des besoins du projet :

- **Modèle en cascade** :
    Un modèle linéaire et séquentiel où chaque phase doit être terminée avant de passer à la suivante.

- **Modèle Agile** :
    Un modèle flexible et itératif qui met l'accent sur la **livraison continue** et le retour d'information, ce qui le rend idéal pour les projets dont les exigences évoluent.

---

### Étapes du SDLC :

1. **Phase de planification** :

    - **Objectif principal** : Comprendre les **exigences du projet**, son objectif et identifier les ressources nécessaires.
    - **Importance** : Cette étape jette les bases de l'ensemble du projet et garantit que toutes les parties prenantes sont alignées.
2. **Analyse des exigences** :

    - **Objectif principal** : Déterminer exactement **ce que l'application doit faire**.
    - **Importance** : Des exigences claires empêchent le débordement du périmètre et garantissent que le projet fournit les fonctionnalités attendues.
3. **Conception** :

    - **Objectif principal** : Définir **comment** le projet sera construit, y compris l'architecture du système, l'interface utilisateur et la conception de la base de données.
    - **Importance** : Une conception bien structurée conduit à un développement efficace et à une phase de codage plus fluide.
4. **Phase de développement** :

    - **Objectif principal** : La **phase de codage** où les développeurs construisent l'application en fonction des spécifications de conception.
    - **Importance** : Il s'agit de la phase la plus longue et doit suivre les meilleures pratiques de codage pour assurer la maintenabilité et l'évolutivité.
5. **Phase de test** :

    - **Objectif principal** : Identifier les **bogues** et s'assurer que le logiciel fonctionne comme prévu.
    - **Importance** : Des tests approfondis garantissent que le logiciel est fiable et répond à toutes les exigences définies avant son déploiement.
6. **Déploiement** :

    - **Objectif principal** : **Publier le logiciel** sur Internet ou le rendre accessible aux utilisateurs.
    - **Importance** : Garantit que le logiciel est accessible et prêt à être utilisé dans un environnement réel.
7. **Maintenance** :

    - **Objectif principal** : **Mises à jour** régulières, correction des problèmes et maintien de la fonctionnalité continue.
    - **Importance** : Le logiciel doit être maintenu au fil du temps pour s'adapter aux nouvelles technologies et corriger les problèmes potentiels qui surviennent après le déploiement.

---

### Meilleures pratiques en développement logiciel :

- **Adopter le bon modèle SDLC** : Choisir entre Waterfall ou Agile en fonction de la portée, du calendrier et de la flexibilité du projet.
- **Tests approfondis** : Garantit la qualité du logiciel et minimise les problèmes après le lancement.
- **Planification et analyse des exigences efficaces** : Cela garantit que toutes les parties prenantes sont au clair sur les buts et objectifs du projet dès le départ.

---

# 6 - Virtualisation

## Qu'est-ce que la virtualisation

La **virtualisation** est le processus de création de versions virtuelles de composants physiques, tels que :

- **Serveurs**
- **Périphériques de stockage**
- **Réseaux**
- **Systèmes d'exploitation**

---

## Virtualisation des serveurs

La **virtualisation des serveurs** permet d'**isoler** plusieurs serveurs les uns des autres sur un seul matériel. Ceci est réalisé à l'aide d'un logiciel de virtualisation tel que **Hyper-V** ou **VMware**. Chaque serveur virtuel fonctionne indépendamment, offrant une plus grande **flexibilité** et **efficacité** dans la gestion des ressources.

### Avantages :

- **Optimisation** des ressources matérielles.
- **Isolation complète** des environnements.
- Possibilité d'exécuter plusieurs **systèmes d'exploitation** sur la même machine physique.

---

## Virtualisation du stockage

La **virtualisation du stockage** combine la capacité de stockage de plusieurs périphériques de stockage physiques en une seule unité virtuelle. Cette approche simplifie la gestion des données et **masque la complexité** du matériel physique sous-jacent.

### Avantages :

- **Utilisation optimisée** de l'espace de stockage.
- **Gestion plus facile** des volumes de données.
- **Disponibilité et récupération améliorées** des données en cas de défaillance.

---

## Virtualisation du réseau

La **virtualisation du réseau** permet la création de plusieurs réseaux virtuels sur une seule infrastructure physique. Il est **facile à ajuster** et à **mettre à l'échelle**, ce qui réduit le besoin de matériel physique supplémentaire. Cette approche rend les réseaux plus **agiles** et **flexibles**.

### Avantages :

- **Évolutivité rapide** des ressources réseau.
- **Réduction des coûts** liés à l'infrastructure physique.
- **Gestion et dépannage améliorés** des environnements réseau.

---

## Virtualisation de bureau

La **virtualisation de bureau** fournit des environnements de bureau virtuels aux utilisateurs, souvent hébergés dans un centre de données ou dans le cloud. Cela permet aux utilisateurs d'accéder à leur bureau depuis n'importe quel appareil.

### Avantages :

- **Accès à distance** aux environnements de travail.
- **Sécurité renforcée** car les données sont centralisées.
- **Gestion simplifiée** des mises à jour et des configurations.

---

## Avantages de la virtualisation

La virtualisation offre plusieurs avantages clés :

- **Flexibilité** et **agilité** dans la gestion des ressources informatiques.
- **Rentabilité**, car moins de machines physiques sont nécessaires.
- **Utilisation optimisée des ressources**, ce qui conduit à une meilleure utilisation du matériel physique.
- **Évolutivité** et **élasticité**, permettant un ajustement facile des ressources en fonction des besoins.
- **Récupération après sinistre améliorée**, avec la possibilité de déplacer ou de restaurer rapidement les machines virtuelles.
- **Isolation** des environnements, améliorant la sécurité.

---

## Défis de la virtualisation

Cependant, la virtualisation présente également certains défis :

-   **Sécurité** : La virtualisation introduit de nouvelles couches d’abstraction, ce qui peut créer des surfaces d’attaque potentielles.
-   **Gestion** : À mesure que le nombre de machines virtuelles augmente, la gestion peut devenir complexe sans les outils appropriés.
-   **Surcharge de performance** : Bien que la virtualisation optimise les ressources, une charge excessive peut entraîner une dégradation des performances, en particulier avec une mauvaise gestion des ressources.

---

## Technologies de virtualisation

### Hyperviseur

Un **hyperviseur**, ou **moniteur de machine virtuelle (VMM)**, est un logiciel qui crée et exécute des machines virtuelles. Il existe deux types d’hyperviseurs :

-   **Type 1 (bare-metal)** : S’exécute directement sur le matériel sans système d’exploitation hôte. Exemples : **VMware ESXi**, **Microsoft Hyper-V**.
-   **Type 2 (hébergé)** : S’exécute sur un système d’exploitation hôte. Exemples : **Oracle VirtualBox**, **VMware Workstation**.

### Plateformes de virtualisation

Ces plateformes offrent des outils pour créer et gérer des machines virtuelles, des réseaux virtuels et du stockage. Les principaux acteurs du marché sont :

-   **VMware vSphere**
-   **Microsoft Hyper-V**
-   **Citrix XenServer**
-   **KVM (Kernel-Based Virtual Machine)**

Ces plateformes permettent une gestion centralisée et une **automatisation** des ressources.

---

## Services de virtualisation basés sur le cloud

Les services de virtualisation basés sur le cloud fournissent des solutions évolutives et flexibles pour la gestion de l’infrastructure IT. Les principaux fournisseurs sont :

-   **AWS (Amazon Web Services)**
-   **Microsoft Azure**
-   **Google Cloud Platform (GCP)**

### Services proposés :

-   **Informatique sans serveur** : Permet d’exécuter du code sans gérer l’infrastructure sous-jacente.
-   **Réseaux virtuels** : Création et gestion de réseaux complexes dans le cloud.
-   **Stockage évolutif** : Ajustement dynamique de la capacité de stockage en fonction de la demande.

---

# 7 - Réseau

Le **réseau** fait référence à la pratique consistant à connecter des serveurs, des ordinateurs et d’autres appareils électroniques pour **partager efficacement des données et des ressources**. Il permet la communication entre les appareils et permet aux utilisateurs de collaborer de manière transparente au sein d’une organisation ou sur Internet.

## Éléments clés du réseau

Plusieurs éléments clés sont fondamentaux pour le réseau, notamment :

-   **Transmission de données** : Le transfert de données d’un appareil à un autre sur un réseau.
-   **Partage de ressources** : La possibilité de partager du matériel (par exemple, imprimantes, stockage) et des ressources logicielles.
-   **Canaux de communication** : Le support (filaire ou sans fil) par lequel les données sont transmises.
-   **Protocoles de connectivité** : Règles et normes qui régissent l’échange de données entre les appareils.

## Types de communication en réseau

Le réseau prend en charge divers types de méthodes de communication, notamment :

-   **E-mails** : Messagerie formelle et asynchrone pour la communication interne et externe.
-   **Messagerie instantanée** : Communication en temps réel entre les utilisateurs (par exemple, Slack, Microsoft Teams).
-   **Vidéoconférence** : Permet la communication vidéo et audio en temps réel pour les réunions à distance (par exemple, Zoom, Google Meet).

Chaque type de communication repose sur des **protocoles** spécifiques pour fonctionner correctement.

## Protocoles réseau courants

Le réseau repose sur plusieurs protocoles critiques pour faciliter différentes formes de communication :

-   **HTTP/HTTPS (HyperText Transfer Protocol)** : Utilisé pour la transmission du trafic Web, où **HTTPS** assure des connexions sécurisées et chiffrées.
-   **SMTP (Simple Mail Transfer Protocol)** : Gère l’envoi et la réception des **e-mails** sur le réseau.
-   **FTP (File Transfer Protocol)** : Facilite les **transferts de fichiers** entre les appareils ou les serveurs sur un réseau.
-   **TCP/IP (Transmission Control Protocol/Internet Protocol)** : L’ensemble fondamental de protocoles qui définit la manière dont les données sont transmises sur Internet ou sur n’importe quel réseau.

Ces protocoles garantissent que les données sont envoyées et reçues **avec précision** et **en toute sécurité**.

## Importance de la sécurité en réseau

La sécurité est un aspect essentiel de tout réseau, en particulier dans les environnements où des **informations sensibles** sont transmises. Plusieurs mesures de sécurité clés doivent être mises en œuvre :

-   **Protocoles de chiffrement** : Les méthodes telles que **SSL/TLS** (utilisées dans HTTPS) garantissent que les données sont chiffrées pendant la transmission, empêchant tout accès non autorisé.
-   **Pare-feu** : Matériel ou logiciel conçu pour surveiller et contrôler le trafic réseau entrant et sortant en fonction de règles de sécurité.
-   **VPN (Virtual Private Networks)** : Fournissent des connexions sécurisées et chiffrées sur des réseaux publics potentiellement non sécurisés.
-   **Gestion de la configuration réseau** : Configuration appropriée des réseaux pour limiter les vulnérabilités et assurer la **conformité** aux politiques de sécurité.

Garantir des **configurations réseau sécurisées** et un chiffrement fort est **essentiel** pour protéger les données dans les organisations où des informations sensibles, telles que des dossiers financiers ou des données personnelles, sont traitées.

## Composants de l’infrastructure réseau

Plusieurs composants physiques et logiques sont impliqués dans le réseau :

-   **Routeurs** : Appareils qui acheminent les données entre différents réseaux, garantissant que les paquets de données atteignent la bonne destination.
-   **Commutateurs** : Appareils réseau qui connectent plusieurs appareils sur le même réseau local (LAN) et dirigent les données vers l’appareil approprié.
-   **Points d’accès** : Appareils qui permettent aux appareils sans fil de se connecter à un réseau filaire via Wi-Fi.
-   **Serveurs** : Ordinateurs centralisés qui fournissent des services et des ressources (par exemple, stockage de fichiers, hébergement Web) à d’autres appareils du réseau.

Ces composants fonctionnent ensemble pour former l’infrastructure qui prend en charge la **communication** et le **partage des ressources**.

## Topologies réseau

Une topologie réseau fait référence à **l’agencement** des appareils réseau et à la manière dont ils se connectent les uns aux autres. Les topologies courantes incluent :

-   **Topologie en étoile** : Tous les appareils sont connectés à un concentrateur ou à un commutateur central. Ceci est courant dans les réseaux domestiques et les petits bureaux.
-   **Topologie en maillage** : Chaque appareil se connecte à tous les autres appareils. Cela offre une grande redondance, mais peut être complexe à gérer.
-   **Topologie en bus** : Tous les appareils partagent une seule ligne de communication (bus), bien que cela soit moins courant dans les réseaux modernes.
-   **Topologie en anneau** : Les appareils sont connectés de manière circulaire, chaque appareil étant connecté à deux autres.

Le choix de la bonne topologie est essentiel pour **l’évolutivité**, **l’efficacité** et la **tolérance aux pannes**.

## Le but du réseau

Le but principal du réseau est de créer un **écosystème** où les personnes et les appareils peuvent :

-   **Interagir** : Permettre une communication transparente entre les utilisateurs et les systèmes.
-   **Partager des ressources** : Permettre l’utilisation d’appareils partagés comme des imprimantes, des serveurs et le stockage de données.
-   **Collaborer efficacement** : Faciliter la collaboration en temps réel grâce à des documents partagés, des plateformes de messagerie et des vidéoconférences.

En construisant des réseaux robustes et sécurisés, les organisations peuvent **améliorer la productivité**, **réduire les coûts opérationnels** et **améliorer la collaboration** entre les équipes et les sites.

## Tendances émergentes en matière de réseau

Plusieurs nouvelles tendances façonnent l’avenir du réseau :

-   **Réseau défini par logiciel (SDN)** : Une approche qui permet aux administrateurs réseau de gérer les services réseau grâce à l’abstraction des fonctionnalités de bas niveau.
-   **Technologie 5G** : Offre des vitesses plus rapides, une latence plus faible et la possibilité de connecter davantage d’appareils, ce qui est particulièrement important pour les appareils IoT (Internet des objets).
-   **Réseau cloud** : Déplace la gestion du réseau vers le cloud, ce qui permet aux organisations de mettre à l’échelle rapidement les ressources et de réduire les coûts d’infrastructure sur site.
-   **Virtualisation des fonctions réseau (NFV)** : Remplace le matériel réseau traditionnel (par exemple, routeurs, pare-feu) par des solutions logicielles pour accroître la flexibilité et l’évolutivité.

Ces innovations changent la façon dont les réseaux sont conçus, gérés et mis à l’échelle, offrant une plus grande flexibilité et efficacité.

---

# 8 - OS

Les **systèmes d’exploitation (SE)** dans le cloud agissent comme la **couche logicielle fondamentale** qui gère à la fois les **ressources matérielles physiques** et **virtualisées**. Ces ressources comprennent :

-   **CPU** (Unité centrale de traitement)
-   **Mémoire** (RAM)
-   **Stockage**
-   **Réseau**

Le SE garantit que les **applications cloud** fonctionnent **efficacement** et **efficacement** en gérant ces ressources, ce qui est essentiel pour la gestion des environnements cloud à grande échelle.

## Caractéristiques des systèmes d’exploitation cloud

Les systèmes d’exploitation cloud modernes ont des caractéristiques spécifiques qui les différencient des environnements SE traditionnels. Ces caractéristiques permettent au SE de répondre aux exigences d’une infrastructure cloud dynamique, évolutive et sécurisée.

### Prise en charge de la virtualisation

Les systèmes d’exploitation cloud sont intrinsèquement conçus avec des **capacités de virtualisation**. La virtualisation permet à un seul serveur physique d’exécuter plusieurs **machines virtuelles (VM)**, chacune fonctionnant indépendamment avec son propre SE. Il s’agit d’un aspect clé du **cloud computing**, permettant :

-   **Partage des ressources** : Plusieurs VM peuvent utiliser le même matériel physique, maximisant ainsi l’utilisation des ressources.
-   **Mise à l’échelle efficace** : Les machines virtuelles peuvent être facilement créées, détruites ou migrées vers d’autres serveurs en fonction des besoins des applications.

Le SE cloud doit prendre en charge les **hyperviseurs** (par exemple, **KVM**, **VMware**, **Hyper-V**) pour gérer la couche de virtualisation, garantissant une allocation fluide des ressources et une isolation entre les VM.

### Évolutivité et élasticité

L’une des principales caractéristiques du SE cloud est sa capacité à **allouer dynamiquement des ressources** en fonction de la demande actuelle. Le SE cloud permet **l’évolutivité** et **l’élasticité** dans la gestion des ressources :

-   **Évolutivité** : Le SE peut augmenter les ressources (comme l’ajout de plus de CPU, de RAM ou de stockage) à mesure que la demande de l’application augmente, garantissant ainsi des **performances optimales**.
-   **Élasticité** : Il peut également réduire les ressources lorsque la demande diminue, ce qui conduit à une **meilleure utilisation des ressources** et à une **rentabilité**.

Ces fonctionnalités garantissent que les environnements cloud restent **réactifs** et **rentables**, car les ressources ne sont utilisées qu’en cas de besoin.

### Sécurité et isolation

Les systèmes d’exploitation cloud doivent garantir que chaque **machine virtuelle (VM)** est **isolée** des autres pour maintenir la **sécurité** et des **performances constantes**. Cette isolation empêche :

-   **Interférence** entre les VM : Garantir que les performances d’une VM n’affectent pas négativement une autre.
-   **Atteintes à la sécurité** : L’isolation garantit qu’une VM compromise n’a pas accès aux autres VM sur le même serveur physique.

Le SE cloud utilise diverses techniques telles que la **conteneurisation** (par exemple, **Docker**, **Kubernetes**) et la **segmentation du réseau** pour maintenir ces limites.

### Interface utilisateur

L’interaction avec les systèmes d’exploitation cloud est souvent **plus abstraite** par rapport aux systèmes d’exploitation traditionnels comme Windows ou macOS. Au lieu d’une interaction directe avec une interface graphique de bureau, les utilisateurs interagissent généralement avec le SE cloud via :

-   **Interfaces Web** : De nombreux fournisseurs de cloud proposent des consoles de gestion basées sur le Web, telles que la **console de gestion AWS** ou **Azure Portal**, qui permettent aux utilisateurs de gérer visuellement les ressources.
-   **API** : Les systèmes d’exploitation cloud fournissent également une prise en charge **API** étendue, permettant aux développeurs et aux administrateurs système d’interagir par programme avec l’infrastructure. Cela permet l’automatisation de tâches telles que le provisionnement de nouvelles VM, la mise à l’échelle des ressources ou le déploiement d’applications.

Ce passage aux **interfaces Web** et aux **API** reflète l’accent mis par le cloud sur l’évolutivité, l’automatisation et la gestion à distance.

## Le rôle du SE dans le cloud computing

Dans le cloud, le système d’exploitation joue un **rôle vital** en fournissant un environnement robuste, évolutif et sécurisé pour exécuter des applications. Des fonctionnalités clés telles que la **prise en charge de la virtualisation**, **l’évolutivité**, la **sécurité** et **l’abstraction des interfaces** rendent le SE cloud essentiel pour la gestion des charges de travail complexes et dynamiques. Qu’il s’agisse d’exécuter des **applications d’entreprise**, **d’analyses de données volumineuses** ou **d’architectures de microservices**, le SE cloud garantit que l’infrastructure reste efficace, flexible et sécurisée.

---

# 9 - Bases de données

Une **base de données** est une **collection structurée de données** qui est stockée électroniquement sur un système informatique. Le but principal d’une base de données est de faciliter :

-   **L’accès**
-   **La manipulation**
-   **La mise à jour**
-   **La récupération** des données

Les bases de données jouent un rôle crucial pour garantir **l’intégrité des données** et la **cohérence des données**, ce qui est essentiel pour maintenir **l’exactitude** et la **fiabilité** des informations dans diverses applications.

---

## Types de bases de données

Il existe différents types de bases de données, chacun étant conçu pour des cas d’utilisation et des besoins de gestion des données spécifiques.

### Bases de données relationnelles

Les **bases de données relationnelles** utilisent une approche structurée qui permet d’identifier et d’accéder aux données en fonction de leur relation avec d’autres données au sein de la base de données. Les données des bases de données relationnelles sont stockées dans des **tables** (souvent appelées **relations**), qui se composent de lignes et de colonnes.

-   **Tables** : Chaque table contient un type spécifique de données, et des relations peuvent être établies entre différentes tables.
-   **Structured Query Language (SQL)** : SQL est le langage standard utilisé pour interagir avec les bases de données relationnelles.

Les exemples courants de bases de données relationnelles incluent :

-   **MySQL**
-   **PostgreSQL**
-   **Microsoft SQL Server**
-   **Oracle Database**

Les bases de données relationnelles sont idéales pour les scénarios qui nécessitent des **requêtes complexes** et **l’intégrité des données** sur plusieurs types de données.

### Bases de données non relationnelles (NoSQL)

Les **bases de données non relationnelles**, souvent appelées **bases de données NoSQL**, offrent une approche plus **flexible** du stockage des données. Au lieu de s’appuyer sur des tables structurées, les bases de données NoSQL stockent les données dans divers formats, tels que :

-   **Bases de données de documents** : Stockent les données dans des documents **JSON** ou **XML** (par exemple, **MongoDB**).
-   **Bases de données graphiques** : Stockent les données sous forme de **nœuds** et **d’arêtes** pour représenter les relations (par exemple, **Neo4j**).
-   **Magasins clé-valeur** : Utilisent des **paires clé-valeur** pour une récupération rapide des données (par exemple, **Redis**, **DynamoDB**).
-   **Magasins de colonnes larges** : Stockent les données dans des lignes et des colonnes, mais sont plus flexibles que les bases de données relationnelles (par exemple, **Cassandra**, **HBase**).

Les bases de données NoSQL sont souvent utilisées pour gérer de **grands volumes de données non structurées** et offrent **évolutivité** et **performances** pour des charges de travail spécifiques comme le **traitement des données en temps réel**.

## Base de données en tant que partie intégrante des applications

Les bases de données sont une **partie intégrante** du **back-end** d’une application, interagissant avec la **logique métier** pour **traiter**, **récupérer** et **stocker les données** en fonction des interactions de l’utilisateur. Les applications communiquent avec les bases de données à l’aide de :

-   **API (Application Programming Interfaces)** : Les API agissent comme des intermédiaires qui permettent aux applications d’envoyer des requêtes et de recevoir des réponses de la base de données.
-   **Pilotes de base de données** : Composants logiciels qui permettent aux applications de communiquer directement avec la base de données en traduisant les requêtes de l’application en commandes de base de données.

Ces connexions sont souvent définies à l’aide de **chaînes de connexion**, qui spécifient les paramètres pour établir la connexion avec la base de données, notamment :

-   **Type de base de données** (par exemple, MySQL, MongoDB)
-   **Nom du serveur** (par exemple, adresse IP ou domaine)
-   **Informations d’identification** (par exemple, nom d’utilisateur et mot de passe)
-   **Base de données spécifique** à laquelle accéder (si plusieurs bases de données sont hébergées sur le même serveur)

Les chaînes de connexion garantissent une communication sécurisée et efficace entre l’application et la base de données.

## Opérations CRUD

La plupart des bases de données effectuent les quatre opérations **CRUD** de base, qui sont essentielles pour la gestion des données :

-   **Créer** : Insérer de nouvelles données dans la base de données.
-   **Lire** : Récupérer les données existantes de la base de données.
-   **Mettre à jour** : Modifier les données existantes dans la base de données.
-   **Supprimer** : Supprimer des données de la base de données.

Ces opérations sont fondamentales pour toute application qui nécessite la gestion des données, qu’il s’agisse d’une petite application personnelle ou d’un système d’entreprise à grande échelle.

## Importance des bases de données dans le développement d’applications

Les bases de données sont essentielles pour assurer le **bon fonctionnement** des applications en fournissant :

-   **Intégrité des données** : Garantir que les données restent exactes et cohérentes dans tout le système.
-   **Efficacité** : Optimiser le stockage et la récupération des données pour les applications **hautes performances**.
-   **Évolutivité** : Permettre aux applications de s’adapter et de gérer des charges de travail accrues en distribuant efficacement les données (particulièrement important dans les systèmes basés sur le cloud et NoSQL).

De plus, les bases de données aident à gérer les **transactions**, en garantissant que des ensembles complexes d’opérations sont exécutés **de manière atomique** et **sécurisée**, empêchant ainsi la corruption ou l’incohérence des données.