---
title: "Concevoir une Architecture VPC Basique"
description: "Ce projet a pour objectif de créer une architecture de base pour un VPC."
lang: "fr"
pubDate: "Sept 17 2024"
heroImage: "/portfolio/projects/cea-design-vpc/vpc.webp"
badge: "PERSONNEL"
tags: ["Cloud", "AWS", "Network", "VPC", "Cloud Engineer Academy"]
---

C’était ma **première** vraie experience avec des **VPC**, et le fait d’en concevoir un m’a énormément appris. J’avais des bases en réseau, mais je ne savais pas encore comment cela s’appliquait dans le cloud. Le défi était à la fois **stimulant** et super **intéressant**.

---

1 — **Besoins** </br>
2 — **Conception de l’Architecture** </br>
3 — **Conclusion** </br>

---

## 1 - Besoins

1. **Conception VPC** : Créer un VPC avec un bloc CIDR défini.
2. **Conception des Subnets** :
   - Deux subnets publics (un dans chaque zone de dispo).
   - Quatre subnets privés (deux par AZ) pour l'app et les bases de données.
3. **Connectivité Internet** :
   - Un Internet Gateway pour les subnets publics.
   - Un NAT Gateway dans les subnets publics pour permettre aux subnets privés d'accéder à Internet.
4. **Tables de Routage** :
   - Configurer les routes pour gérer les flux entre subnets publics et privés.
5. **Sécurité** :
   - Limiter l’accès aux bases de données : uniquement accessible depuis les serveurs d’app.
6. **Documentation** :
   - Fournir un schéma d’architecture et expliquer les choix faits.

## 2 - Architecture

![](/portfolio/projects/cea-design-vpc/AWS_VPC_Architecture.png)

### Composants

- **Région** : L’archi est déployée dans une seule région AWS : `eu-west-3` (Paris).
- **VPC** : Un seul VPC contenant toutes les ressources réparties sur deux AZs.
- **AZs (Zones de Disponibilité)** : Les ressources sont réparties sur deux zones pour garantir de la haute dispo et de la tolérance aux pannes.
- **Subnets Publics** : 2 subnets (1 par AZ), avec un accès Internet via les NAT Gateways.
- **Subnets Privés** : 4 subnets (2 par AZ), sans accès direct à Internet, pour les serveurs d’app et les bases de données.
- **Internet Gateway (IGW)** : Un seul IGW attaché au VPC pour donner accès Internet aux subnets publics.

### Réseau

J’ai choisi un bloc CIDR large : `10.0.0.0/16`. Ça donne une bonne marge avec 65 534 adresses IP utilisables, ce qui permet d’être à l’aise maintenant comme plus tard. AWS réserve quelques adresses comme expliqué [ici](https://docs.aws.amazon.com/vpc/latest/userguide/subnet-sizing.html) :

- **10.0.0.0** : Adresse réseau
- **10.0.0.1** : Pour le routeur du VPC
- **10.0.0.2** : Pour le DNS
- **10.0.0.3** : Réservée pour usage futur
- **10.0.0.255** : Adresse de broadcast

Pour répondre aux besoins, j’ai découpé le réseau comme ça :

| Nom du Subnet           | Adresse        | Masque | Nb d'IP utilisables |
|-------------------------|----------------|--------|---------------------|
| az1-public-subnet       | 10.0.1.0       | /24    | 251                 |
| az1-application-subnet  | 10.0.2.0       | /24    | 251                 |
| az1-database-subnet     | 10.0.3.0       | /24    | 251                 |
| az2-public-subnet       | 10.0.4.0       | /24    | 251                 |
| az2-application-subnet  | 10.0.5.0       | /24    | 251                 |
| az2-database-subnet     | 10.0.6.0       | /24    | 251                 |

Chaque subnet en `/24` offre 251 IPs utilisables. C’est large et ça permet de scaler tranquille, même si dans beaucoup de cas des plages plus petites suffiraient.

### Tables de Routage

La config réseau est assez simple :

**Subnets Publics** : Ils ont besoin d’un accès Internet via l’IGW pour permettre les connexions entrantes/sortantes.

| Destination | Cible |
|-------------|--------|
| 0.0.0.0/0   | IGW    |
| 10.0.0.0/16 | Local  |

**Subnets App** : Pour que les instances privées aient accès à Internet (ex: pour les updates), on passe par un NAT Gateway. Le reste est routé en interne.

| Destination | Cible |
|-------------|--------|
| 0.0.0.0/0   | NAT    |
| 10.0.0.0/16 | Local  |

**Subnets DB** : Les bases de données n’ont pas besoin d’Internet. Seuls les serveurs d’app peuvent y accéder.

| Destination | Cible |
|-------------|--------|
| 10.0.0.0/16 | Local  |

### Haute Disponibilité

L'archi est pensée pour être résiliente : les ressources sont réparties sur deux AZs. Si une zone tombe, l’autre continue à gérer le trafic sans souci. On pourrait aussi étendre cette archi sur plusieurs régions, mais pour un projet basique c’est déjà bien complet.

### Sécurité

La sécurité est gérée via :

- **Subnets Privés** : Les apps et bases sont isolées de l’Internet. Le NAT Gateway gère les connexions sortantes (si besoin).
- **Groupes de Sécurité** :
    - **App SG** : Gère les flux entrants/sortants des serveurs d’app.
    - **DB SG** : Accepte uniquement les connexions venant du SG des apps. Ça donne un contrôle plus précis que les NACLs.
- **NAT Gateway** : Permet aux instances privées d’aller vers l’extérieur sans être exposées.

En combinant tout ça (private subnets + NAT + SG bien configurés), on limite énormément la surface d’attaque et on garde un bon contrôle du trafic réseau.

## 3 - Conclusion

Cette archi suit les **best practices AWS** pour garantir un environnement **scalable**, **disponible** et **sécurisé** pour une application web. Elle répond aux besoins actuels, tout en laissant de la **flexibilité** pour des évolutions futures.