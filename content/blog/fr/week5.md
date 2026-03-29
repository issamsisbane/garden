---
title: "Améliorer mes compétences Cloud - Semaine 5 - Principes fondamentaux d'AWS"
description: "Semaine 5 pour améliorer mes compétences Cloud."
lang: "fr"
pubDate: "Sept 17 2024"
heroImage: "/portfolio/blog/week5/week5.webp"
badge: "Améliorer mes compétences Cloud"
tags: ["Cloud", "AWS", "Cloud Engineer Academy", "Architecture"]
---

_Venant d'un environnement Azure, je n'avais jamais pleinement exploré AWS et ses composants jusqu'à présent. Ce fut ma première plongée en profondeur dans l'architecture réseau de base d'AWS. Compte tenu des similitudes avec ce que je connaissais déjà d'Azure, la courbe d'apprentissage n'a pas été trop raide, ce qui m'a permis de saisir les concepts plus facilement._

> Comme je l'ai mentionné dans mes articles précédents, je viens d'un background en **cloud computing** et en **ingénierie logicielle**, donc tout au long de mon parcours d'apprentissage, je marquerai les nouveaux concepts avec le hashtag **#nouveau**. Cela aidera à mettre en évidence ce qui est nouveau pour moi et à offrir aux lecteurs une idée plus claire de l'endroit où ils pourraient trouver une valeur ajoutée, qu'ils revisitent des concepts familiers ou qu'ils rencontrent de nouveaux éléments.

> Restez à l'écoute, car je continue de documenter mon processus d'apprentissage et de partager des points à retenir pratiques de chaque module !

---

1 - **Architecture globale AWS** <br/>
2 - **VPC** <br/>
3 - **NOTES/CLOUD ACADEMY/Content/IAM** <br/>
4 - **Projet - 4 - Concevoir un VPC** <br/>
5 - **Configurer un hôte Bastion** <br/>

---

# 1 - Architecture globale AWS

Les **Régions AWS** sont un réseau mondial de clusters de centres de données situés dans des zones géographiques spécifiques. Chaque région est conçue pour être **complètement indépendante** des autres, offrant résilience et isolation des pannes. Cela signifie que si une région rencontre un problème, cela n'affecte pas les autres. Les régions sont identifiées à l'aide de conventions de dénomination spécifiques, telles que `eu-west-2` pour la région de Londres. Cette indépendance garantit que les applications et les services peuvent rester disponibles même en cas de défaillance régionale.
![AWS_Regions.png](/portfolio/blog/week5/AWS_Regions.png)

Les **Zones de disponibilité (AZ) AWS** sont des emplacements isolés au sein d'une région AWS, chacun comprenant un ou plusieurs centres de données discrets avec leur propre alimentation redondante, réseau et connectivité. En étant **physiquement séparées** (généralement jusqu'à 100 km de distance), les AZ offrent une tolérance aux pannes et une stabilité améliorées. Elles vous permettent d'exécuter des services sur plusieurs zones, garantissant que si un centre de données rencontre un problème, les autres zones peuvent continuer à fonctionner sans interruption, maintenant ainsi une haute disponibilité pour vos applications.

Les **Zones locales** sont des extensions plus petites et plus localisées des régions AWS qui rapprochent les services de calcul, de stockage et autres services AWS des utilisateurs finaux. Elles sont conçues pour les **applications sensibles à la latence** qui nécessitent une latence ultra-faible en réduisant la distance physique entre l'utilisateur et les services cloud. Ceci est particulièrement utile pour les cas d'utilisation comme les jeux, le streaming multimédia et les simulations en temps réel, où chaque milliseconde compte.
![AWS_Local_zones.png](/portfolio/blog/week5/AWS_Local_zones.png)

Les **Emplacements périphériques** font partie du réseau de diffusion de contenu (CDN) mondial d'AWS, Amazon CloudFront. Ils **mettent en cache les données** plus près des utilisateurs finaux, assurant une latence encore plus faible et une livraison plus rapide du contenu. En positionnant les données au "dernier kilomètre" entre AWS et le client, les emplacements périphériques améliorent considérablement l'expérience utilisateur en réduisant le temps nécessaire pour charger le contenu, quelle que soit la situation géographique de l'utilisateur.

### Disponibilité des services dans les régions

Tous les services AWS ne sont pas disponibles dans toutes les régions. Les services sont lancés dans les régions en fonction de facteurs tels que la demande, les exigences réglementaires et les capacités d'infrastructure. Cependant, certains services, tels que **IAM (Identity and Access Management)** et **S3 (Simple Storage Service)**, sont considérés comme des **services globaux** et sont accessibles depuis n'importe quelle région.

### Fiabilité et performance

La vaste et très fiable infrastructure mondiale d'AWS garantit que vos applications peuvent être **hautement disponibles et performantes** de n'importe où dans le monde. En tirant parti des régions, des zones de disponibilité, des zones locales et des emplacements périphériques, AWS vous permet de créer des applications robustes à faible latence qui peuvent résister aux pannes et offrir des performances constantes aux utilisateurs du monde entier.

# 2 - VPC

Un VPC est un **réseau privé logiquement isolé** au sein du cloud AWS, offrant la flexibilité de concevoir et de gérer votre environnement cloud de manière sécurisée et contrôlée.

### Blocs CIDR

Les blocs CIDR (Classless Inter-Domain Routing) définissent la plage d'adresses IP attribuée à votre VPC. Cette plage détermine le nombre de ressources que vous pouvez déployer, car elle fixe la limite supérieure du nombre d'adresses IP disponibles au sein du réseau. Planifier soigneusement le bloc CIDR est crucial pour garantir des adresses IP suffisantes pour les besoins actuels et futurs.

### Sous-réseaux

Un VPC est un réseau virtuel, et les sous-réseaux sont des subdivisions au sein de ce réseau. Les sous-réseaux vous permettent d'organiser et de séparer vos ressources cloud en fonction des **exigences d'accès et de sécurité**. Les sous-réseaux peuvent être classés en publics ou privés, chacun servant des objectifs différents.

### Sous-réseaux publics

Les sous-réseaux publics sont conçus pour les ressources qui doivent être accessibles directement depuis Internet. Ceci est réalisé en associant le sous-réseau à une **Passerelle Internet (IGW)**, un composant VPC qui fournit un itinéraire pour le trafic entrant et sortant entre Internet et les ressources au sein du sous-réseau. Pour être accessible depuis Internet, une ressource dans un sous-réseau public doit avoir une **adresse IP publique** ou une **adresse IP Elastic**. Les sous-réseaux publics sont idéaux pour les serveurs web frontaux, les API publiques ou les services qui nécessitent une interaction directe avec les utilisateurs ou les systèmes externes.

-   **Adresse IP Elastic** : Une adresse IP Elastic est une adresse IPv4 publique statique qui peut être facilement réaffectée à différentes instances. Contrairement à une adresse IP publique standard, qui peut changer si une instance est arrêtée ou redémarrée, une adresse IP Elastic reste cohérente, assurant un point d'accès stable.

### Sous-réseaux privés

Les sous-réseaux privés sont conçus pour les ressources qui ne doivent **pas être directement accessibles** depuis Internet. Les ressources au sein des sous-réseaux privés peuvent communiquer entre elles et avec les ressources des sous-réseaux publics, mais elles n'ont pas d'itinéraire direct vers Internet dans leurs tables de routage. Au lieu de cela, elles accèdent à Internet via une **Passerelle NAT** dans un sous-réseau public, ce qui permet le trafic sortant pour des tâches telles que les mises à jour logicielles tout en bloquant le trafic entrant depuis Internet.

Les sous-réseaux privés sont généralement utilisés pour les serveurs back-end, les bases de données et autres couches d'application à haute sécurité. L'utilisation de sous-réseaux privés améliore la sécurité en isolant les charges de travail sensibles et critiques des services accessibles au public, en optimisant les performances du réseau en localisant le trafic et en simplifiant la gestion grâce à des politiques de contrôle d'accès claires.

### Composants clés

#### Passerelle Internet (IGW)

Une passerelle Internet est un composant VPC qui permet la communication entre les instances d'un sous-réseau public et Internet. Elle fournit un itinéraire pour que le trafic entrant et sortant circule entre votre VPC et le monde extérieur.

#### Routeur

Les routeurs du VPC gèrent le trafic à l'intérieur et à l'extérieur du VPC en fonction des règles de routage définies dans les tables de routage. Ils garantissent que le trafic est correctement dirigé entre les sous-réseaux, Internet et d'autres réseaux.

#### Table de routage

Les tables de routage contiennent des règles (routes) qui déterminent où le trafic réseau est dirigé. Dans un VPC, vous pouvez avoir plusieurs tables de routage :

-   **Sous-réseaux publics** : Tables de routage qui incluent une route vers la passerelle Internet (`0.0.0.0/0`) pour faciliter l'accès direct à Internet.
-   **Sous-réseaux privés** : Tables de routage qui utilisent une passerelle NAT pour le trafic lié à Internet, permettant les connexions sortantes sans exposer les ressources directement à Internet.

#### Passerelle NAT

Une passerelle NAT (Network Address Translation) permet aux instances des sous-réseaux privés d'initier le trafic sortant vers Internet (par exemple, pour les mises à jour) tout en empêchant le trafic entrant depuis Internet. Cela garantit que les instances privées peuvent communiquer en externe sans être directement exposées.

### Sécurité

#### Groupes de sécurité

Les groupes de sécurité agissent comme des pare-feu virtuels pour les instances, contrôlant le trafic entrant et sortant au niveau de l'instance. Ils définissent des règles spécifiant les protocoles, les adresses IP et les numéros de port qui sont autorisés ou restreints. Les groupes de sécurité sont **avec état**, ce qui signifie que si le trafic est autorisé à entrer, la réponse est automatiquement autorisée à sortir. Il est important de noter que les groupes de sécurité ne peuvent avoir que des règles "autoriser" ; il n'y a pas de règles "refuser" explicites. Ils fournissent un mécanisme de contrôle granulaire et avec état pour gérer l'accès aux instances individuelles.

#### Listes de contrôle d'accès réseau (NACL)

Les NACL servent de couche de sécurité supplémentaire au niveau du sous-réseau, fournissant un point de contrôle sans état pour réglementer le trafic entrant et sortant. Contrairement aux groupes de sécurité, les NACL sont **sans état**, ce qui signifie que le trafic entrant et sortant doit être explicitement autorisé via des règles distinctes. Les NACL vous permettent de définir des règles "autoriser" et "refuser", qui peuvent bloquer des adresses IP ou des plages IP spécifiques sur l'ensemble du sous-réseau, offrant une large protection contre les accès non autorisés.

### Avantages de l'utilisation de VPC et de sous-réseaux

-   **Sécurité renforcée** : En séparant les services accessibles au public des charges de travail sensibles, vous renforcez la sécurité de votre environnement cloud.
-   **Performances optimisées** : La localisation du trafic au sein de sous-réseaux privés minimise la latence et maximise le débit.
-   **Gestion simplifiée** : Des rôles et des politiques clairs simplifient le contrôle d'accès, la surveillance du trafic et la conformité aux exigences de gouvernance des données.

# 3 - IAM

IAM vous permet de contrôler en toute sécurité l'accès aux ressources AWS dans des conditions spécifiques. Avec IAM, vous pouvez créer et gérer des utilisateurs, des groupes et des politiques pour définir qui peut accéder à des ressources spécifiques et dans quelles conditions.

### Principales caractéristiques

-   **Gestion des utilisateurs** : Créez des comptes d'utilisateurs individuels avec des autorisations personnalisées.
-   **Gestion des groupes** : Organisez les utilisateurs en groupes pour appliquer les autorisations à grande échelle.
-   **Accès basé sur les conditions** : Définissez des conditions d'accès, en spécifiant quand et comment les utilisateurs peuvent accéder aux ressources.
-   **Contrôle d'accès** : Gérez qui peut accéder à des ressources spécifiques et dans quelles conditions, garantissant un environnement sécurisé.

### Principe du moindre privilège

IAM prend en charge la bonne pratique de sécurité connue sous le nom de **Principe du moindre privilège**. Ce principe garantit que chaque utilisateur, groupe ou application ne dispose que des autorisations nécessaires pour effectuer ses tâches, rien de plus. En adhérant à ce principe, vous minimisez les risques de sécurité en réduisant le potentiel d'accès non autorisé.

### Authentification multifacteur (MFA)

IAM prend également en charge l'**authentification multifacteur (MFA)**, fournissant une couche de sécurité supplémentaire pour l'accès aux ressources AWS. En exigeant que les utilisateurs fournissent une deuxième forme d'authentification (par exemple, un code unique envoyé sur un appareil mobile), la MFA réduit considérablement le risque d'accès non autorisé, même si les informations d'identification sont compromises.

### Rôles IAM et accès aux applications

IAM permet aux applications d'accéder en toute sécurité à d'autres ressources AWS à l'aide de **rôles IAM**. Ces rôles accordent les autorisations nécessaires sans avoir besoin de stocker les informations d'identification AWS au sein de l'application. Cette pratique améliore non seulement la sécurité en évitant les informations d'identification codées en dur, mais garantit également que les applications ne disposent que des autorisations dont elles ont besoin pour interagir avec les services AWS.

### Intégration et fédération

IAM peut s'intégrer aux systèmes d'identité existants, tels que Microsoft Active Directory (AD), permettant aux organisations d'utiliser leur infrastructure existante pour le contrôle d'accès. Il prend également en charge la **Fédération d'identités**, permettant aux utilisateurs de s'authentifier à l'aide d'identités existantes provenant de systèmes externes (par exemple, des annuaires d'entreprise ou des solutions d'authentification unique (SSO)) sans créer de comptes IAM distincts.

### Termes clés

-   **Utilisateurs** : Individus ou services auxquels l'accès aux ressources AWS peut être accordé.
-   **Groupes** : Collections d'utilisateurs auxquels vous pouvez appliquer des autorisations collectivement.
-   **Rôles** : Ensembles d'autorisations qui permettent aux utilisateurs ou aux services d'effectuer des actions dans AWS sans utiliser d'informations d'identification directes.
-   **Autorisations** : Définissent les actions que les utilisateurs ou les services peuvent effectuer sur les ressources AWS.
-   **Politiques** : Documents JSON qui définissent les autorisations et spécifient quelles ressources les utilisateurs ou les rôles peuvent accéder et comment ils peuvent interagir avec elles.
-   **Fédération d'identités** : Permet aux utilisateurs d'accéder aux ressources AWS à l'aide d'identités externes (par exemple, les services d'annuaire d'entreprise), évitant ainsi la nécessité d'un compte utilisateur IAM distinct pour chaque utilisateur.

# 4 - Concevoir un VPC

![AWS_VPC_Architecture.png](/portfolio/blog/week5/AWS_VPC_Architecture.png)

## Exigences

1.  **Conception VPC** : Créez un VPC avec un bloc CIDR spécifié.
2.  **Conception de sous-réseau** :
    -   Deux sous-réseaux publics (un dans chaque AZ).
    -   Quatre sous-réseaux privés (deux dans chaque AZ) pour l'application et les bases de données.
3.  **Connectivité Internet** :
    -   Passerelle Internet pour les sous-réseaux publics.
    -   Passerelle NAT dans les sous-réseaux publics pour l'accès à Internet des sous-réseaux privés.
4.  **Tables de routage** :
    -   Configurez les tables de routage pour un routage approprié entre les sous-réseaux publics et privés.
5.  **Sécurité** :
    -   Restreignez l'accès à la base de données dans le sous-réseau privé aux seuls serveurs d'applications.
6.  **Documentation** :
    -   Fournissez un schéma d'architecture et expliquez les choix de conception.

## Conception de l'architecture

### Réseau

J'ai sélectionné un grand bloc CIDR pour le VPC : `10.0.0.0/16`. Cela fournit un nombre important d'adresses IP (65 534 adresses utilisables) pour répondre aux besoins actuels et futurs potentiels. Bien que le maximum théorique soit de 65 536 adresses, AWS réserve les quatre premières et les dernières adresses IP de chaque sous-réseau, comme documenté [ici](https://docs.aws.amazon.com/vpc/latest/userguide/subnet-sizing.html) :

-   **10.0.0.0** : Adresse réseau.
-   **10.0.0.1** : Réservé par AWS pour le routeur VPC.
-   **10.0.0.2** : Réservé par AWS pour le serveur DNS.
-   **10.0.0.3** : Réservé par AWS pour une utilisation future.
-   **10.0.0.255** : Adresse de diffusion.

Compte tenu des exigences de l'architecture, nous avons besoin de six sous-réseaux, que j'ai alloués comme suit :

| Nom | Sous-réseau | Masque | Nombre d'adresses |
| --- | --- | --- | --- |
| az1-public-subnet | 10.0.1.0 | /24 | 251 |
| az1-application-subnet | 10.0.2.0 | /24 | 251 |
| az1-database-subnet | 10.0.3.0 | /24 | 251 |
| az2-public-subnet | 10.0.4.0 | /24 | 251 |
| az2-application-subnet | 10.0.5.0 | /24 | 251 |
| az2-database-subnet | 10.0.6.0 | /24 | 251 |

Chaque sous-réseau `/24` fournit 251 adresses IP utilisables (256 au total moins les 5 réservées par AWS). Cette conception utilise une large plage pour faciliter l'évolutivité et la simplicité opérationnelle, bien qu'en pratique, des sous-réseaux plus petits suffiraient pour de nombreux cas d'utilisation.

### Composants

-   **Région** : L'architecture est déployée dans une seule région AWS : `eu-west-3` (Paris).
-   **VPC** : Un seul VPC contenant toutes les ressources sur deux zones de disponibilité (AZ).
-   **Zones de disponibilité** : Les ressources sont réparties sur 2 AZ pour assurer une haute disponibilité et une tolérance aux pannes.
-   **Sous-réseaux publics** : 2 sous-réseaux, un dans chaque AZ, avec accès Internet pour les passerelles NAT.
-   **Sous-réseaux privés** : 4 sous-réseaux (2 par AZ) isolés de l'accès direct à Internet pour les serveurs d'applications et les bases de données.
-   **Passerelle Internet (IGW)** : Une seule passerelle Internet attachée au VPC pour fournir une connectivité Internet aux sous-réseaux publics.

### Tables de routage

La configuration du routage est simple :

**Sous-réseaux publics** : Les sous-réseaux publics nécessitent une route vers la passerelle Internet pour autoriser le trafic Internet entrant et sortant.

| Destination | Cible |
| ----------- | ------ |
| 0.0.0.0/0   | IGW    |
| 10.0.0.0/16 | Local  |

**Sous-réseaux d'applications :** Pour permettre aux instances des sous-réseaux privés d'accéder à Internet pour les mises à jour, nous utilisons une passerelle NAT. L'autre entrée permet de communiquer avec toutes les ressources présentes au sein du réseau.

| Destination | Cible |
| ----------- | ------ |
| 0.0.0.0/0   | NAT    |
| 10.0.0.0/16 | Local  |

**Sous-réseaux de bases de données :** Les bases de données n'ont pas besoin d'un accès direct à Internet. Seule notre application peut accéder à notre base de données.
La route `0.0.0.0/0` est une route globale, dirigeant le trafic vers la cible spécifiée lorsqu'aucune route plus spécifique n'est trouvée.

| Destination | Cible |
| ----------- | ------ |
| 10.0.0.0/16 | Local  |

### Haute disponibilité

Notre architecture est conçue pour la résilience et la haute disponibilité en distribuant les ressources sur deux zones de disponibilité (AZ). Si une AZ subit une panne, l'autre AZ peut continuer à gérer le trafic de manière transparente, assurant un service ininterrompu. Bien que l'architecture puisse être étendue pour couvrir plusieurs régions pour une tolérance aux pannes encore plus grande, cela pourrait être excessif pour une application de base de cette envergure.

### Sécurité

La sécurité est appliquée par les mesures suivantes :

-   **Sous-réseaux privés** : Les serveurs d'applications et les bases de données résident dans des sous-réseaux privés, empêchant l'accès direct à Internet. Tout le trafic lié à Internet doit passer par la passerelle NAT, offrant un contrôle et une surveillance des communications sortantes.
-   **Groupes de sécurité** :
    -   **Groupe de sécurité des applications** : Contrôle le trafic entrant et sortant pour les instances d'applications.
    -   **Groupe de sécurité de la base de données** : Configuré pour n'autoriser que le trafic entrant provenant du groupe de sécurité des applications, garantissant que la base de données n'est accessible que par les serveurs d'applications. Cela offre un niveau de sécurité plus granulaire par rapport aux listes de contrôle d'accès réseau (NACL).
-   **Passerelle NAT** : Utilisée pour faciliter l'accès Internet sortant pour les instances des sous-réseaux privés sans les exposer directement à Internet.

En combinant des sous-réseaux privés, des passerelles NAT et des groupes de sécurité étroitement contrôlés, nous maintenons un contrôle strict sur le trafic réseau, améliorant ainsi la posture de sécurité de l'application et de la base de données.

## Conclusion

Cette architecture tire parti des meilleures pratiques AWS pour garantir un environnement évolutif, hautement disponible et sécurisé pour l'application web. La conception répond non seulement aux exigences actuelles, mais offre également une flexibilité pour la croissance future.

# 5 - Configuration de l'hôte Bastion

### Qu'est-ce qu'un Hôte Bastion ?

Un **hôte bastion**, également connu sous le nom de serveur de rebond, est un **serveur sécurisé** qui agit comme une passerelle entre un réseau externe (par exemple, Internet) et un réseau privé. Il fournit un accès sécurisé aux instances au sein d'un sous-réseau privé. Les administrateurs se connectent généralement à l'hôte bastion via SSH (pour les instances Linux) ou RDP (pour les instances Windows). Une fois connectés, ils peuvent ensuite accéder aux ressources des sous-réseaux privés via l'hôte bastion.

**Sécurité** : L'hôte bastion est placé dans un sous-réseau public et sécurisé avec des règles de groupe de sécurité strictes. Seules des adresses IP spécifiques (par exemple, celles des administrateurs réseau) sont autorisées à s'y connecter, garantissant ainsi le blocage des accès non autorisés.

**Objectif** : L'objectif principal d'un hôte bastion est de gérer et d'administrer en toute sécurité les instances dans les sous-réseaux privés sans exposer directement ces instances à Internet.

### Différences clés entre l'hôte bastion et la passerelle NAT

-   **Hôte Bastion** : Fournit un point d'entrée sécurisé pour les administrateurs afin d'accéder aux instances privées pour les tâches de gestion et d'administration.
-   **Passerelle NAT** : Permet aux instances des sous-réseaux privés d'initier le trafic sortant vers Internet (par exemple, pour télécharger des mises à jour) tout en bloquant le trafic entrant depuis Internet.

Dans cette configuration, nous avons remplacé la passerelle NAT par un hôte bastion afin de réduire les coûts, car la passerelle NAT peut être assez chère. L'hôte bastion sera une instance EC2, et nous nous y connecterons via SSH depuis nos machines locales.

### Expérience pratique

En guise d'expérience pratique, j'ai utilisé mon architecture VPC de la partie précédente et l'ai remplacée par un hôte bastion afin de tester les choses et d'avoir une meilleure vue de son fonctionnement. Les passerelles NAT sont assez chères, j'ai donc voulu éviter cela. Vous pouvez voir en jaune le flux de travail de l'expérience.

![AWS_VPC_ARCHITECTURE_Bastion.png](/portfolio/blog/week5/AWS_VPC_ARCHITECTURE_Bastion.png)

Les étapes pratiques comprennent :

1.  **Se connecter à l'hôte bastion** : Tout d'abord, nous nous connectons à l'hôte bastion en utilisant SSH depuis notre machine locale.
2.  **Accéder aux instances EC2 dans le sous-réseau privé** : Depuis l'hôte bastion, nous nous connectons ensuite à une instance EC2 située dans le sous-réseau de l'application.
3.  **Ping d'une instance dans une autre zone de disponibilité (AZ)** : Depuis cette instance, nous pingons une autre instance située dans une AZ différente pour assurer la connectivité au sein des sous-réseaux privés.

### Mesures de sécurité mises en œuvre

-   Nous avons défini une règle entrante dans le groupe de sécurité de l'hôte bastion pour n'autoriser l'accès SSH qu'à partir de notre adresse IP spécifique.
-   Pour tester les configurations de sécurité :
    -   Nous avons supprimé la route vers la passerelle Internet (IGW) de la table de routage du sous-réseau public. Par conséquent, nous ne pouvions plus nous connecter à nos instances via SSH, prouvant l'efficacité de l'hôte bastion en tant que seul point d'accès.
    -   Nous avons également supprimé une règle de groupe de sécurité dans le sous-réseau de l'application de la deuxième AZ qui autorisait l'accès depuis le premier sous-réseau de l'application. Cela a empêché l'accès entre les sous-réseaux, confirmant que le trafic inter-sous-réseau est strictement contrôlé par les règles du groupe de sécurité.

### Résultats de l'apprentissage

Grâce à cette expérience pratique, j'ai acquis une compréhension pratique plus approfondie de la sécurité et du contrôle d'accès VPC. Il est crucial de maintenir les groupes de sécurité à jour, car les configurations par défaut autorisent souvent le trafic de n'importe quelle adresse IP, ce qui constitue un risque de sécurité important. La configuration correcte des groupes de sécurité est essentielle pour protéger le réseau et ses ressources.