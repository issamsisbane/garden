---
title: "Mise en place d'une Solution d'analytics pour mon Portfolio"
description: "Guide ultra‑concis pour installer Umami (analytics auto‑hébergé, RGPD‑compatible) sur un VPS Hetzner avec Terraform, Ansible, Docker‑Compose et Certbot."
lang: "fr"
pubDate: "Sept 14 2025"
heroImage: "/portfolio/blog/analytics-umami-portfolio/analytics-umami-portfolio.png"
badge: "Portfolio"
tags: ["Docker", "Self-Host", "Analytics", "Umami"]
---

- [Introduction](#introduction)
	- [1 - Choix](#1---choix)
	- [2 - Creation du VPS](#2---creation-du-vps)
	- [3 - Provisionnement](#3---provisionnement)
	- [4 - Generation du certificat](#4---generation-du-certificat)
	- [5 - Test de l'application](#5---test-de-l'application)
- [Conclusion](#conclusion)
# Introduction

Cela fait plus d’un an que j’ai développé et déployé mon portfolio sur Internet. 

Le design minimaliste me plaît, mais il me manque **une visibilité** sur les visiteurs de mon site. En effet, Aujourd'hui je ne sais pas :
- Qui consulte mon site ?
- D'où on consulte mon site ?
- Qu'est ce amene à mon site ?

Lorsque je postule à un emploi, je partage le lien à beaucoup de personnes et sur différents canaux, mais je ne peux pas mesurer l’impact. 

Ma première idée : créer un *short‑link* avec une fonction serverless et une petite base de données pour compter les clics. Le problème ? Aucun aperçu du trafic provenant de Google ou d’autres sources où le short‑link n’est pas utilisé.  

Ma deuxième tentative : installer Google Analytics (décrit dans mon [précédent article](https://issamsisbane.github.io/portfolio/fr/blog/a-la-recherche-dun-outil-danalyse-du-traffic-web/)). Le service est puissant, mais il est **trop lourd** et je ne veux pas dépendre d’une plateforme tierce.  

J’ai donc cherché une solution **auto‑hébergée**, simple à déployer et adaptée à mes besoins.

# 1 - Choix

## Besoin

- Comptabiliser le nombre d’utilisateurs quotidiens.
- Être **RGPD‑compliant** (je réside en Europe).
- Installation et administration simples, sans dépendance à un homelab (service 24 h/24).

## Architecture

![[analytics-umami-portfolio.png]]

*Schéma simplifié de l’infrastructure : VPS Hetzner → Nginx ↔ Umami + PostgreSQL, Certbot pour TLS.*

## Choix des outils

- *Cloud Provider* : **Hetzner** – le meilleur compromis prix/performance du marché européen.
- *Application d'Analytics* : **Umami** – léger, open‑source et RGPD‑friendly.  
	J’ai brièvement testé **Plausible**; il offre les mêmes garanties mais reste trop gourmand pour mon usage minimaliste. C'est RGPD compliant en plus.
- *Reverse Proxy* : **NGINX** – le classique, fiable et largement documenté.
- *Certificats* : **Certbot** – automatisation ACME via le container officiel.
- *Déploiement* : 
	- **Docker** : chaque composant tourne dans son propre conteneur, ce qui garantit isolation et facilité de suppression.
	- **Terraform** : provisionne le VPS, les firewalls et l’adresse IP. Même si le projet est petit, cela rend l’infrastructure **reproductible**.
	- **Ansible** : configuration du serveur (Docker, firewall, …) – je l’utilise déjà quotidiennement au travail, d’où le choix naturel.

# 2 - Creation du VPS

## Terraform

Globalement le [code](https://github.com/issamsisbane/analytics) permet de crée une instance Hetzner, ouvre les ports 80 et 443, et génère automatiquement l’IP publique.

## Gestion des limites Hetzner

Problème, avec Hetzner il peut y avoir un nombre de ressources limitées. Ainsi on peut ne peut pas pouvoir créer de machine et tomber sur une erreur : 

```
# error during placement (resource_unavailable)
```

La solution est de changer de zone (`location`) et réessayer après quelques minutes.. Il faut être patient et attendre qu'un slot se libère car Hetzner à un quota de VM déployés dans un zone.

## Astuce Pool d'adresses IP

Dans mes ressources terraform j'avais ajouté une IP primaire mais peu importe la zone j'avais cette erreur : 

```
IP pool exhausted (unavailable, d7c020884fcdc481)
```

Pour résoudre le problème, il faut juste laisser Hetzner créer l'IP automatiquement en spécifiant : 

```
public_net {
    ipv4_enabled = true  # Création automatique d'une IPv4
    ipv6_enabled = false # Non-Création automatique d'une IPv6 
  }
```

# 3 - Provisionnement

## DNS

Pour que tout soit sécurisé via https et accessible de l'exterieur il faut créer un enregistrement de type **A** pour notre VM. On ajoute simplement l'IP publique de notre machine Hetzner et on crée un hostname qui va avec. 
Pour moi ce sera `analytics.issamhomelab.org`.

## Installation Docker

Mon role ansible permet d'installer tout ce qu'il faut pour lancer des conteneur via docker.

## Docker compose

J'utilise docker compose pour lancer tous les éléments nécessaire.

``` yaml
version: '3.8'

services:
  umami-db:
    image: postgres:15
    restart: always
    environment:
      POSTGRES_DB: $DB
      POSTGRES_USER: $USER
      POSTGRES_PASSWORD: $PASSWORD
    volumes:
      - umami-db-data:/var/lib/postgresql/data

  umami:
    image: ghcr.io/umami-software/umami:postgresql-latest
    depends_on:
      - umami-db
    environment:
      DATABASE_URL: postgres://$USER:$PASSWORD@umami-db:5432/$DB
      APP_SECRET: "an_interesting_secret"
    restart: always
    expose:
      - 3000

  nginx:
    image: nginx:alpine
    restart: always
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
      - certbot-etc:/etc/letsencrypt
      - certbot-var:/var/lib/letsencrypt
      - certbot-www:/var/www/certbot
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - umami

  certbot:
    image: certbot/certbot
    volumes:
      - certbot-etc:/etc/letsencrypt
      - certbot-var:/var/lib/letsencrypt
      - certbot-www:/var/www/certbot

volumes:
  umami-db-data:
  certbot-etc:
  certbot-var:
  certbot-www:
```

## Configuration Nginx initiale

Voici la configuration Nginx initial. Cela va permettre à certbot de pouvoir accèder à notre application et de valider que je suis bien le proprietaire du site. Après cela, un certificat va pouvoir être généré.

``` nginx
server {
    listen 80;
    server_name analytics.issamhomelab.org;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}
```

## Problème Rencontré : Package Ansible manquant 

J'ai eu cette erreur ansible : 
```
No module named 'ansible.module_utils.six.moves'
```

Cela venait de la version d'ansible que j'utilisais qui était trop ancienne. 

J'avais un environnement ou j'ai installé **Hashicorp Vault** sur des machines **RHEL** que j'ai crée avec **vagrant** et elles avaient d'anciennes version de python. 

Ducoup j'utilisais ce Dockerfile pour ansible : 
``` Dockerfile
FROM python:3.6-slim

# Mettre à jour les paquets et installer les dépendances nécessaires
RUN apt-get update && apt-get install -y \
    sshpass \
    openssh-client \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Installer une version spécifique d'Ansible
RUN pip install ansible==210

# Ajouter un utilisateur non-root pour la sécurité
RUN useradd -m dockeruser
COPY . /home/dockeruser
RUN chown -R dockeruser:dockeruser /home/dockeruser
USER dockeruser

# Définir le répertoire de travail
WORKDIR /home/dockeruser

# Entrée par défaut dans le conteneur
CMD ["/bin/bash"]
```

Or sur ma machine hetzner j'ai python 3.12, j'ai donc modifié : 

``` Dockerfile
FROM python:3.12-slim
RUN pip install ansible==210
```

# 4 - Génération du certificat
### Etapes manuelles

Il y a des étapes manuelles a faire pour générer un certificat via certbot.

Une fois que l'on a déployé et que notre application est accessible sur le port 80.
Il faut lancer cette commande qui va générer le certificat : 
```
docker compose run --rm  certbot certonly --webroot --webroot-path /var/www/certbot/  -d analytics.issamhomelab.org
```

### Configuration Nginx Finale

Ensuite on peut mettre toute la conf nginx : 

``` nginx
server {
    listen 80;
    server_name analytics.issamhomelab.org;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name analytics.issamhomelab.org;

    ssl_certificate /etc/letsencrypt/live/analytics.issamhomelab.org/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/analytics.issamhomelab.org/privkey.pem;

    location / {
        proxy_pass http://umami:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### Renouvellement

A termes (tous les 3 mois), il faudra faire un renouvellement du certificat.

Cela doit aussi être fait à la main.

``` bash
docker compose run --rm certbot renew
```

On pourrait ajouter un cron pour l'automatiser de cette manière :

```
0 3 * * */30 docker compose -f ~/docker-compose.yml run --rm certbot renew && docker compose restart nginx
```
_(Renouvelle toutes les 30 jours à 03 h du matin, puis redémarre Nginx.)_

# 5 - Test de l'application

On peut finalement accéder à l'application umami via l'[url](https://analytics.issamhomelab.org).

## Insertion du script Umami

Il suffit juste d'ajouter cette balise dans le code de mon portfolio : 
```
<!-- Umami Analytics -->
<script defer src="https://analytics.issamhomelab.org/script.js" data-website-id="my-id"></script>
```

Il faut ensuite repousser le code, redéployer, accèder au portfolio.

## Vérifications

Et on peut voir qu'umami a détecté l'accès au site : 

![[zen_284.png]]

# Conclusion

Après avoir un peu jouer avec. Umami fonctionne très bien mais il ne détecte pas précisément ce qu'est un **utilisateur unique**. 

Par exemple si je me connecte sur le meme pc depuis le navigateur Opera puis que je me connecte ensuite depuis Firefox, Umami va détecter **2 utilisateurs**.

C'est un logiciel privacy focus donc il n'utilise pas l'IP par exemple pour définir un utilisateur qui aurait pu servir à identifier que je ne suis qu'un seul utilisateur. 

Finalement, pour mes besoins personnels c'est **amplement suffisant**. Je n'ai pas besoin de savoir précisément combien de personnes visitent mon site, c'est juste pour avoir un aperçu global. Je suis donc **satisfait** d'avoir pu mettre en place cette solution assez facilement.

**Ameliorations envisagées** : 
1. Déploiement sur mon homelab Kubernetes.  
2. Restreindre l’accès public via un VPN ou un réseau privé Hetzner.  
3. Automatiser entièrement la génération/renouvellement du certificat avec un job Cron ou un service systemd‑timer.

**Resources utilisées** :
- https://mindsers.blog/fr/post/remplacer-google-analytics-alternative-ethique/
- https://mindsers.blog/en/post/https-using-nginx-certbot-docker/
