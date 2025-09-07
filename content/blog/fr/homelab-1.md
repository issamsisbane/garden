---
title: "Homelab - 1 - Setup"
description: "Guide étape par étape pour construire un home-lab K3s personnel, couvrant le matériel, HA etcd, Flux GitOps et plus encore."
lang: "fr"
pubDate: "Sept 07 2025"
heroImage: "/portfolio/blog/homelab-1/homelab-1.png"
badge: "Homelab"
tags: ["Kubernetes", "Self-Host", "GitOps"]
---

[Introduction](#introduction)
	[1 - Architecture](#1---architecture)
	[2 - Principes](#2---principes)
	[3 - Choix technologiques](#3---choix-technologiques)
	[4 - Configuration des machines](#4---configuration-des-machines)
	[5 - Configuration étape par étape](#5---configuration-étape-par-étape)
	[6 - Installer Flux](#6---installer-flux)
[Conclusion](#conclusion)

## Introduction

J'ai passé les **trois dernières années** à travailler avec des clusters Kubernetes en production au travail. Bien que cette expérience m'ait exposé à des problèmes réels, elle laissait peu de place à l'expérimentation. Pour combler ela, j'ai décidé de lancer un homelab personnel où je peux tester des choses sans conséquence et explorer de nouvelles technologies à ma guise.

Depuis janvier, j'ai pris l'habitude de déployer des clusters localement avec Minikube ou Rancher pour configurer rapidement des environnements, tester des idées et apprendre de nouveaux concepts.

Cela m'aide beaucoup d'avoir un environnement jetable où je peux tout casser sans conséquences. Mais au fur et à mesure que j'acquiers de l'expérience, je travaille avec des configurations plus complexes avec de nombreux outils différents sur plusieurs nœuds, ce qui entraîne des défis spécifiques qu'un cluster jetable à un seul nœud ne peut pas relever.

J'ai donc construit mon propre laboratoire à la maison, j'ai décidé de l'appeler mon HomeLab :) (Attendez, ça existe déjà ? Je ne l'ai pas inventé ?)

Ceci est le premier article d'une longue série, je l'espère !

## 1 - Architecture

Mon homelab sera un cluster kubernetes (évidemment). J'ai choisi K3S comme distribution car je l'ai déjà utilisé dans le passé, l'installation est assez simple et il est pris en charge par le CNCF.

J'ai préféré le **bare metal** aux VM ou aux instances cloud pour avoir une expérience pratique dans la gestion de la stack complète.

De plus, je veux héberger des applications que j'utiliserai dans ma vie quotidienne, ce qui me forcera à gérer cette configuration comme un véritable environnement de production avec des utilisateurs (oui, juste moi pour l'instant...)

![[homelab-1.png]]

Le cluster sera composé de :
- **RaspberryPi** : Un raspberry PI 5 exécutant PI OS - 16 Go de RAM, processeur 4 cœurs
- **Archy** : Ancien ordinateur portable 1 exécutant arch linux - 8 Go de RAM, processeur 4 cœurs
- **Ubuntuserv** : Ancien ordinateur portable 2 exécutant ubuntu serveur - 4 Go de RAM, processeur 4 cœurs

*Ne faites pas attention aux noms des nœuds, j'ai du mal avec les noms...*

Un total de **trois nœuds** et tous seront à la fois un nœud maître et un nœud worker.

La meilleure pratique en production est de séparer le controlplane des workloads, mais j'ai décidé de garder les noeuds polyvalents pour maintenir le quorum et pouvoir beneficier de noeuds workers sans ajouter de matériel supplémentaire.

## 2 - Principes

Je veux suivre les meilleures pratiques et intégrer les dernières innovations et façons de faire dans mon homelab.

Ceci est sujet à changement, mais pour l'instant, j'ai décidé de :
- Tout gérer via GitOps et automatiser tous les déploiements
- Suivre les principes du moindre privilège et sécuriser mes conteneurs
- Ne pas exposer les services directement à Internet
- Créer des alertes et un tableau de bord de surveillance pour tout surveiller

## 3 - Choix technologiques

La plupart de mes choix sont les technologies les plus utilisées ou celles que nous utilisons au travail.

### Gitops - Flux

Au travail, je n'utilise actuellement qu'Argo, j'ai donc voulu explorer ce que Flux a à offrir.

### Gestion des secrets - Vault

Au travail, nous utilisons Vault pour la gestion des secrets, mais je voulais essayer de l'utiliser de manières que je n'ai pas utilisées au bureau.

### Surveillance

La pile classique : Grafana, Loki et Prometheus. Je ne l'ai pas vraiment utilisé avant il y a quelques mois.

## 4 - Configuration des machines

Les machines de mon homelab sont toutes des appareils réutilisés - je partagerai plus de détails sur chacun ci-dessous.

### RaspberryPi

J'ai celui-ci de l'école. Je l'ai initialement utilisé pour suivre les cours GitOps Kubernetes de [Mischa VAN DEN BURG](https://mischavandenburg.com/), mais il dormait depuis. Je lui donne une seconde vie dans mon homelab.

Fun Fact: Lorsque j'ai essayé de redémarrer le Pi des mois plus tard, j'ai rencontré d'étranges erreurs de stockage. Il s'avère que les cartes SD ne sont pas idéales pour Kubernetes car le controlplane est très gourmand en écriture.

J'ai acheté une nouvelle carte SD (oui, la même erreur) et reconstruit le système d'exploitation à partir de zéro en utilisant **Rufus** pour flasher la carte. À l'avenir, j'investirai dans un SSD.

### Archy

C'était un vieil ordinateur portable qui prenait la poussière chez mes parents. Il était livré avec Windows 10 et était à peine utilisable. J'ai d'abord essayé Mint Linux, ce qui était mieux, mais toujours lent.

Finalement, j'ai installé Arch Linux car je voulais approfondir le fonctionnement de Linux et voir si je pouvais rendre la machine à nouveau utilisable. J'écrirai un article complet sur cette expérience un jour.

### UbuntuServ

C'est un autre vieil ordinateur portable que j'ai réutilisé. J'ai simplement installé Ubuntu Server dessus. Rien de fou, juste un autre nœud pour mon cluster.

## 5 - Configuration étape par étape

### Amorcer le premier nœud

J'avais déjà un cluster K3S en cours d'exécution sur mon raspberry PI en utilisant la base de données intégrée par défaut.

https://docs.k3s.io/datastore/ha-embedded

Pour changer ce comportement et utiliser etcd pour notre cluster HA à 3 nœuds, j'ai dû mettre à jour le service à `/etc/systemd/system/k3s.service` pour ajouter `cluster-init` :

```
ExecStart=/usr/local/bin/k3s server --cluster-init --disable=helm-controller
```

Redémarrer k3s :

``` bash
sudo systemctl daemon-reload
sudo systemctl restart k3s
```

Nous pouvons vérifier le changement de base de données en tapant :

``` bash
kubectl get nodes
```

![[Pasted image 20250724000936.png]]

### Rejoindre des nœuds supplémentaires

Nous devons maintenant installer k3s sur les deux ordinateurs portables et rejoindre le cluster.

Nous devons lancer cette commande :

``` bash
curl -sfL https://get.k3s.io | K3S_TOKEN=SECRET sh -s - server \    --server https://raspberry.home:6443 \
```

Nous pouvons trouver le jeton dans le raspberryPi à `/var/lib/rancher/k3s/server/token` et le remplacer dans la commande.

Après avoir lancé la commande :

![[Pasted image 20250724001141.png]]

### Alignement des versions

On remarque une incompatibilité de version entre les nœuds.

C'est une bonne pratique d'avoir la même version entre nos nœuds.

https://docs.k3s.io/upgrades/manual#upgrade-k3s-using-the-installation-script

Pour mettre à niveau notre version raspberryPi, il suffit de relancer le script d'installation :

``` bash
curl -sfL https://get.k3s.io | K3S_TOKEN=SECRET sh -s - server  --cluster-init
```

### Finalement

On fait la même chose pour les deux nœuds.

![[Pasted image 20250724235043.png]]

## 6 - Installer Flux

Nous allons installer [FluxCd](https://fluxcd.io/flux/get-started/) dans notre cluster K3S.

### Créer un PAT GitHub

Nous devons créer un jeton d'accès personnel GitHub avec les `permissions du référentiel`.

Nous pouvons utiliser des jetons classiques, mais pour être plus conforme et sécurisé, il est préférable d'utiliser un PAT précis uniquement pour notre référentiel.

Nous avons besoin des autorisations suivantes :
- `Administration` : Lecture et écriture
- `Contenu` : Lecture et écriture
- `Métadonnées` : Lecture seule

Nous devons exporter ces variables :

``` bash
export GITHUB_TOKEN=<your-token>
export GITHUB_USER=<your-username>
```

J'ai créé un script pour charger les variables d'environnement pour un projet spécifique. Vous pouvez le trouver [ici](https://github.com/issamsisbane/tools/blob/main/bash/func/load_env.sh).

C'est utile car si on l'exporte simplement. On perdrait les variables en fermant le shell. Je ne sais pas si j'en aurai besoin plus tard. Bien sûr, je ne le commit pas dans git.

Nous installons l'outil cli flux :
``` bash
brew install fluxcd/tap/flux
```

### Installer flux sur le cluster

``` bash
flux bootstrap github \
  --owner=$GITHUB_USER \
  --repository=pi-cluster \
  --branch=main \
  --path=./clusters/staging \
  --personal
```

Cette commande permet de configurer dans quel dépôt et branche nous voulons que flux surveille. Ensuite, Flux créera le fichier manifeste dans le dépôt pour se gérer lui-même.

Nous pouvons gérer plusieurs clusters avec le même dépôt GitOps (production, staging..)

### Résultats

- Flux crée les manifestes nécessaires dans le dépôt GitHub
- Un nouvel espace de noms 'flux-system' est créé sur le cluster avec les composants Flux
- Le contrôleur GitOps est maintenant actif sur le cluster

À partir de maintenant, le contrôleur GitOps est installé dans notre cluster. Et nous pouvons commencer à déployer des choses.

## Conclusion

Je peux enfin me sentir comme un véritable ingénieur car j'ai un homelab où je peux expérimenter librement !

Il y a des années, je regardais de nombreux YouTubers construire des homelabs. Je les enviais et je me suis promis que je ferais de même un jour.

J'ai un objectif maintenant qui est d'avoir une pièce entière dédiée à mon homelab, un véritable datacenter !