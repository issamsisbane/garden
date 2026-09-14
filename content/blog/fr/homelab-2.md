---
title: Homelab - 2 - De la machine nue à un nœud de cluster bootable
description: Comment j'ai automatisé le provisionnement de trois nœuds Ubuntu bare-metal en utilisant cloud-init, Ventoy et un seul fichier user-data.
lang: fr

pubDate: Feb 26 2026
heroImage: /portfolio/blog/homelab-2/homelab-2.png
badge: Homelab
tags:
  - Kubernetes
  - Self-Host
  - Linux
  - Homelab
---
- [Introduction](#introduction)
- [1 - Pourquoi reconstruire à partir de K3s](#1---pourquoi-reconstruire-à-partir-de-k3s)
- [2 - Le matériel](#2---le-matériel)
- [3 - Pourquoi un provisionnement automatisé](#3---pourquoi-un-provisionnement-automatisé)
- [4 - Ventoy : Une seule clé USB pour les gouverner toutes](#4---ventoy--une-seule-clé-usb-pour-les-gouverner-toutes)
- [5 - Ubuntu Autoinstall et cloud-init](#5---ubuntu-autoinstall-et-cloud-init)
- [6 - Le fichier user-data](#6---le-fichier-user-data)
- [7 - Le WiFi : La partie énervante](#7---le-wifi--la-partie-énervante)
- [8 - Problèmes de nom d'hôte avec le routeur FAI](#8---problèmes-de-nom-dhôte-avec-le-routeur-fai)
- [9 - L'utilisateur kuadm](#9---lutilisateur-kuadm)
- [10 - Garder l'ordinateur portable allumé lorsqu'il est fermé](#10---garder-lordinateur-portable-allumé-lorsquil-est-fermé)
- [11 - Leçons apprises](#11---leçons-apprises)
- [Conclusion](#conclusion)

## Introduction

*Après avoir écrit le premier article sur mon homelab initial avec K3s et Flux, je l'ai continué à l'utiliser pendant un certain temps. Ça fonctionnait. Mais plus je l'utilisais, plus j'avais l'impression de manquer de contrôle. K3s est génial — opinionné, complet, facile à installer — mais il cache beaucoup de ce qui fait réellement fonctionner Kubernetes. Je voulais tout reconstruire à partir de zéro en utilisant kubeadm et Kubespray pour une configuration plus proche de la production. Cette série documente ce parcours de reconstruction.*

*Avant d'en arriver à la partie Kubernetes, cependant, il y a une étape que la plupart des tutoriels sautent : l'installation du système d'exploitation sur chaque machine. Cela semble trivial jusqu'à ce que vous ayez trois ordinateurs portables différents avec du matériel différent, aucun moniteur à brancher, et un fort désir de ne jamais toucher un clavier pendant l'installation.*

*Cet article couvre exactement cela — la couche système d'exploitation. Comment je suis passé de trois machines vierges à trois nœuds Ubuntu identiques et joignables sur le réseau, provisionnés automatiquement à partir d'une seule clé USB et d'un seul fichier de configuration.*

*C'est moins glamour que de déployer des charges de travail, mais bien faire cette étape est ce qui rend tout le reste reproductible. Si vous devez un jour reconstruire un nœud à 23h parce que quelque chose s'est mal passé, vous serez content d'avoir automatisé cette partie.*

## 1 - Pourquoi reconstruire à partir de K3s

Le premier homelab a été construit avec K3s. Ça fonctionnait, Flux tournait, les applications étaient déployées. J'étais content.

Mais en creusant plus profondément dans Kubernetes au travail et en continuant à lire sur le fonctionnement réel des choses en coulisses, j'ai commencé à remarquer à quel point K3s abstrait. Tout est dans un seul binaire. La base de données intégrée, l'équilibreur de charge de service intégré, la façon dont il regroupe containerd et le plugin CNI — tout cela est vraiment pratique, mais cela signifie que vous n'apprenez pas vraiment les primitives brutes de Kubernetes.

J'ai passé mon CKA en septembre 2025, j'ai donc appris à travailler avec kubeadm, etcd... Et j'ai adoré travailler directement avec ces outils et apprendre tous les composants d'un cluster Kubernetes.

J'ai donc voulu migrer de K3S pour tout contrôler dans mon cluster.

J'ai tout effacé et j'ai recommencé. kubeadm pour l'initialisation du cluster, Kubespray pour automatiser le déploiement sur les trois nœuds avec Ansible.

La première chose à résoudre avant tout le reste : un système d'exploitation propre, cohérent et reproductible sur chaque machine.

## 2 - Le matériel

Le cluster est toujours constitué des trois mêmes machines que lors de la première configuration.

- **RaspberryPi** : Un Raspberry Pi 5, 16 Go de RAM, 4 cœurs. Le cheval de bataille du cluster et le nœud du plan de contrôle.
- **Archy** : Un vieil ordinateur portable récupéré chez mes parents, 8 Go de RAM, 4 cœurs. Il tournait sous Arch Linux avant. Il tourne maintenant sous Ubuntu Server comme les autres.
- **Ubuntuserv** : Un autre vieil ordinateur portable, 4 Go de RAM, 4 cœurs. Il tournait déjà sous Ubuntu Server.

*Ne faites pas attention aux noms. Je suis conscient qu'ils ne sont pas cohérents entre eux. Je les ai nommés avant de me soucier des conventions de nommage.*

Ce qui est important ici, c'est que les trois machines sont du matériel différent. Différentes puces WiFi, différentes versions de BIOS, différentes conventions de nommage d'interface. Cette hétérogénéité est ce qui rend l'automatisation à la fois plus utile et plus douloureuse à configurer correctement.

## 3 - Pourquoi un provisionnement automatisé

La réponse évidente est : parce que faire les choses manuellement trois fois est trois fois plus sujet aux erreurs que de les faire automatiquement une fois.

Mais il y a une raison plus profonde. Lorsque vous provisionnez des nœuds manuellement — en cliquant à travers un installateur, en définissant un nom d'hôte, en créant un utilisateur — vous vous retrouvez avec des machines qui sont *probablement* similaires mais pas *certainement* identiques. Avez-vous créé le même utilisateur sur les trois ? Les avez-vous toutes activées pour SSH ? Avez-vous défini la même locale ? Vous le pensez, mais vous n'êtes pas sûr.

Avec un provisionnement automatisé, la configuration est un fichier. Le fichier est la vérité. Si les trois nœuds ont été installés à partir du même fichier, ils sont identiques par construction.

Cela signifie également que lorsque quelque chose tombe en panne — et quelque chose tombe toujours en panne — vous pouvez reconstruire un nœud dans le temps nécessaire à l'exécution de l'installateur. Pas d'étapes manuelles à retenir, pas de documentation à consulter. Boot, attendez, terminé.

Pour un homelab, c'est une amélioration de la qualité de vie. Dans un environnement réel, c'est une exigence. Je préfère prendre de bonnes habitudes maintenant.

## 4 - Ventoy : Une seule clé USB pour les gouverner toutes

Lors de la première configuration de l'homelab, j'ai utilisé Rufus pour flasher la carte SD du Raspberry Pi. Rufus écrit une seule ISO sur un lecteur et c'est tout. Si vous voulez essayer une autre ISO, vous reformatez et re-flashez.

Cette fois, je suis passé à [Ventoy](https://www.ventoy.net/). Ventoy formate la clé USB une fois, puis vous copiez simplement des fichiers ISO dessus comme un système de fichiers ordinaire. Lorsque vous démarrez à partir du lecteur, Ventoy affiche un menu et vous permet de choisir quelle ISO démarrer. Pas de reflash, pas de reformatage.

Pour provisionner trois machines avec la même ISO, la différence n'est pas énorme. Mais lorsque vous transportez également une ISO de secours, un outil de diagnostic et votre installateur, les avoir tous sur une seule clé est vraiment utile.

La configuration est simple : téléchargez Ventoy, exécutez l'installateur en ciblant votre clé USB, puis copiez l'ISO d'Ubuntu Server 24.04 sur la partition de données du lecteur. C'est tout.

### Problème de démarrage sécurisé (Secure Boot)

La première fois que j'ai démarré à partir de la clé Ventoy sur l'un des ordinateurs portables, j'ai obtenu cette erreur :

```
Verification failed: (0x1A) Security Violation
```

C'est un problème de démarrage sécurisé. Le chargeur de démarrage de Ventoy n'est pas signé par la clé de Microsoft par défaut, donc UEFI refuse de l'exécuter. La solution consiste à enregistrer le propre certificat de Ventoy dans la base de données de démarrage sécurisé UEFI, ce que Ventoy peut faire pour vous via son utilitaire `VentoyEnroll`. Il existe un guide clair sur le [site Web de Ventoy](https://www.technewstoday.com/ventoy-secure-boot/) pour cela.

Alternativement, vous pouvez simplement désactiver le démarrage sécurisé dans le BIOS. Moins élégant mais plus rapide pour un homelab que vous contrôlez entièrement.

### L'exception Raspberry Pi

Le Raspberry Pi n'a pas de système de démarrage UEFI standard, donc Ventoy ne fonctionne pas dessus. Ce n'est pas un problème en pratique : le Raspberry Pi Imager fait le même travail. Il vous permet de configurer le nom d'hôte, d'injecter une clé SSH et de configurer le WiFi avant d'écrire l'image sur la carte SD.

La seule différence est que j'utilise un SSD directement au lieu d'une carte SD, ce qui est plus adapté à un cluster Kubernetes. Le résultat est équivalent — un nœud sans tête et joignable sur le réseau sans configuration manuelle.

## 5 - Ubuntu Autoinstall et cloud-init

Ubuntu Server 24.04 est livré avec un installateur intégré appelé **autoinstall**. Il lit un fichier de configuration appelé `user-data` et exécute l'installation entièrement sans intervention. Pas de clics, pas d'invites, pas d'interaction au clavier.

Le fichier `user-data` utilise le format cloud-init. Il couvre tout : disposition du disque, locale, clavier, comptes utilisateurs, clés SSH, paquets à installer et fichiers arbitraires à écrire sur le disque avant le premier démarrage.

La façon dont cela fonctionne avec Ventoy est simple : vous placez le fichier `user-data` à la racine de la clé USB à côté de l'ISO. Lorsque l'installateur Ubuntu démarre, il recherche ce fichier et l'utilise automatiquement. L'installateur s'exécute, le nœud redémarre, et vous avez une machine configurée.

Il existe une approche alternative où vous servez `user-data` via HTTP et passez un paramètre de noyau au démarrage :

```
autoinstall ds=nocloud-net;s=http://<votre-serveur>/
```

C'est plus propre pour les déploiements à grande échelle mais nécessite un serveur HTTP en cours d'exécution. Pour trois nœuds, placer le fichier sur la clé USB est plus simple.

L'objectif de la conception était d'avoir un seul fichier `user-data` qui fonctionne sur les trois machines, avec seulement le nom d'hôte modifié entre les installations. Tout le reste — l'utilisateur, la clé SSH, la configuration WiFi, les paquets — reste le même.

## 6 - Le fichier user-data

Voici la structure du fichier `user-data` que j'ai fini par utiliser. Je vais passer en revue chaque section.

```yaml
#cloud-config
autoinstall:
  version: 1

  locale: fr_FR.UTF-8
  keyboard:
    layout: us
    variant: intl

  identity:
    hostname: ih-node-1
    username: kuadm
    password: "<mot-de-passe-haché>"

  ssh:
    install-server: true
    authorized-keys:
      - "ssh-ed25519 AAAA... votre-clé-ici"
    allow-pw: false

  storage:
    layout:
      name: direct

  packages:
    - wpasupplicant

  write_files:
    - path: /etc/netplan/99-wifi.yaml
      content: |
        network:
          version: 2
          wifis:
            wlan0:
              dhcp4: true
              access-points:
                "VotreSSID":
                  password: "VotreMotDePasseWiFi"

  kernel:
    cmdline: "net.ifnames=0 biosdevname=0"

  late-commands:
    - "echo 'kuadm ALL=(ALL) NOPASSWD:ALL' > /target/etc/sudoers.d/kuadm"
```

Permettez-moi de passer en revue les décisions clés ici.

### Disposition du stockage

J'ai utilisé la disposition `direct`, qui écrit directement sur tout le disque sans LVM. LVM ajoute de la flexibilité pour redimensionner les volumes plus tard, mais pour un nœud homelab avec un seul disque et uniquement Kubernetes dessus, je n'ai pas besoin de cette complexité. Plus simple, c'est mieux.

### Locale et clavier

```yaml
locale: fr_FR.UTF-8
keyboard:
  layout: us
  variant: intl
```

Je suis français, donc `fr_FR.UTF-8` est ma locale. Mais mon clavier est un agencement international US, ce que j'utilise depuis des années. C'est une distinction subtile qui compte : la locale contrôle les formats de date, les séparateurs de nombres et les valeurs par défaut de la langue, tandis que la disposition du clavier contrôle les caractères que les touches produisent. Les avoir correctement alignés évite les surprises désagréables.

### Paquets

```yaml
packages:
  - wpasupplicant
```

Un seul paquet supplémentaire est nécessaire au moment de l'installation. Plus d'informations à ce sujet dans la section suivante.

### Ligne de commande du noyau

```yaml
kernel:
  cmdline: "net.ifnames=0 biosdevname=0"
```

C'est important. Plus d'informations à ce sujet dans la section WiFi également.

### Sudo sans mot de passe

```yaml
late-commands:
  - "echo 'kuadm ALL=(ALL) NOPASSWD:ALL' > /target/etc/sudoers.d/kuadm"
```

Le bloc `late-commands` s'exécute après la fin de l'installation mais avant le premier redémarrage. Je l'utilise pour déposer un fichier sudoers accordant à `kuadm` le droit de sudo sans mot de passe. C'est ce à quoi s'attendent les playbooks Ansible de Kubespray — ils se connectent via SSH et exécutent des commandes privilégiées sans invite de mot de passe.

## 7 - Le WiFi : La partie énervante

Les nœuds n'ont pas de connexion filaire au routeur. Il n'y a pas de switch réseau dans ma configuration. Tout fonctionne via WiFi. C'est bien pour un homelab, mais cela a créé deux problèmes distincts pendant le provisionnement.

### Problème 1 : wpasupplicant n'est pas installé par défaut

L'installation minimale d'Ubuntu Server n'inclut pas `wpasupplicant`, le paquet responsable de l'authentification WiFi WPA2. Sans lui, le système ne peut pas du tout se connecter à un réseau WiFi.

Cela crée un problème d'œuf et de poule : l'installateur a besoin d'une connexion réseau pour télécharger des paquets, mais le WiFi ne fonctionne pas tant que `wpasupplicant` n'est pas installé.

La solution : pendant l'installation, branchez la machine via Ethernet pour que l'installateur ait une connexion réseau. Cela lui permet de télécharger et d'installer `wpasupplicant`. Une fois l'installation terminée et la machine redémarrée, le WiFi fonctionne — car le paquet est maintenant installé et la configuration Netplan est en place.

Ce n'est pas élégant. Mais cela ne doit se produire qu'une seule fois par nœud, et un seul câble Ethernet déplacé entre les machines est acceptable.

### Problème 2 : Les noms d'interface changent entre les machines

Ubuntu utilise par défaut des noms d'interface réseau "prévisibles" comme `enp3s0` pour Ethernet ou `wlp13s0` pour le WiFi. La partie "prévisible" signifie que le nom encode la topologie du bus PCI du périphérique.

Le problème avec trois ordinateurs portables différents est que chacun a une topologie de bus différente, donc chacun obtient un nom d'interface WiFi différent. `wlp13s0` sur une machine, `wlp0s20f3` sur une autre. Il est donc impossible d'écrire une seule configuration Netplan qui fonctionne sur toutes.

La solution consiste à désactiver complètement la dénomination prévisible en passant des paramètres de noyau au démarrage :

```
net.ifnames=0 biosdevname=0
```

Avec ces indicateurs, le noyau revient aux anciens noms : `eth0` pour la première interface Ethernet, `wlan0` pour la première interface WiFi. Ceux-ci sont cohérents sur les trois machines, quelles que soient les différences matérielles.

Dans le fichier `user-data`, cela est défini via le champ `kernel.cmdline` :

```yaml
kernel:
  cmdline: "net.ifnames=0 biosdevname=0"
```

Et la configuration Netplan dans `write_files` utilise directement `wlan0` :

```yaml
write_files:
  - path: /etc/netplan/99-wifi.yaml
    content: |
      network:
        version: 2
        wifis:
          wlan0:
            dhcp4: true
            access-points:
              "MonRéseau":
                password: "MonMotDePasse"
```

Une configuration, trois machines. C'est pourquoi le README liste cela comme une décision de conception délibérée : des noms d'interface cohérents sont ce qui rend l'approche à fichier unique viable.

## 8 - Problèmes de nom d'hôte avec le routeur FAI

### Noms d'hôte

J'ai décidé de nommer les nœuds comme suit :

- `ih-node-01`
- `ih-node-02`
- `ih-node-03`

`ih` pour Issam Homelab. Simple, cohérent, clair.

Le problème est le routeur fourni par mon FAI. Il a une particularité : il supprime les zéros de tête des noms d'hôte. Ainsi, `ih-node-01` est enregistré dans le DNS du routeur sous le nom `ih-node-1`. Le nom d'hôte *sur la machine* est `ih-node-01`, mais pour l'atteindre depuis une autre machine sur le réseau, vous devez utiliser `ih-node-1`.

*Je ne peux pas contrôler cela sur mon routeur directement car c'est un routeur grand public... Big Up à mon fournisseur FAI*

Cette incohérence m'a agacé plus que ce qu'elle aurait probablement dû. Utiliser `ih-node-01` dans l'inventaire Ansible, les configurations SSH et kubeconfig mais devoir utiliser `ih-node-1` pour la résolution DNS réelle est le genre de chose qui provoque des échecs mystérieux à 1h du matin.

J'aurais pu contourner le problème en modifiant `/etc/hosts` sur chaque machine pour ajouter les mappages corrects. Mais c'est une étape manuelle qui doit être répétée chaque fois qu'une nouvelle machine rejoint le réseau, et cela va à l'encontre d'une partie de l'objectif de l'automatisation.

La solution la plus simple : renommer simplement les nœuds en `ih-node-1`, `ih-node-2`, `ih-node-3`. Pas de zéros de tête. Maintenant, le nom d'hôte sur la machine correspond à ce que le routeur résout. Cohérence restaurée.

### Adresses IP fixes

Le routeur FAI n'offre pas non plus beaucoup d'options d'automatisation. Pour attribuer des adresses IP statiques aux nœuds, j'ai dû le faire via l'interface Web du routeur, en réservant un bail DHCP pour l'adresse MAC de chaque nœud. C'est une étape manuelle que je n'ai pas pu automatiser du côté `user-data`.

C'est une opération unique par nœud, et le résultat est stable : chaque nœud obtient toujours la même adresse IP, ce qui est ce que Kubernetes exige pour un cluster fiable.

```markdown
---
title: "9 - L'utilisateur kuadm"
description: "Découvrez comment l'utilisateur kuadm est créé et configuré pour permettre une connexion SSH sans mot de passe et des privilèges sudo."
lang: fr
---
## 9 - L'utilisateur kuadm

Chaque nœud reçoit un utilisateur unique : `kuadm`.

Ce nom est un quasi-homophone délibéré de `kubeadm`, l'outil d'amorçage de Kubernetes. C'est également l'utilisateur que les playbooks Ansible de Kubespray s'attendent à trouver lorsqu'ils se connectent aux nœuds via SSH.

L'utilisateur est créé par le bloc `identity` d'autoinstall :

```yaml
identity:
  hostname: ih-node-1
  username: kuadm
  password: "<hashed-password>"
```

Le hachage du mot de passe est généré avec :

```bash
openssl passwd -6
```

Ceci produit un hachage salé SHA-512 que cloud-init accepte. Le mot de passe réel n'a pas beaucoup d'importance car la connexion par mot de passe via SSH est désactivée de toute façon :

```yaml
ssh:
  install-server: true
  authorized-keys:
    - "ssh-ed25519 AAAA..."
  allow-pw: false
```

Seule l'authentification par clé est autorisée. La clé autorisée est la clé publique SSH de mon poste de travail, intégrée dans le fichier `user-data`. Après l'installation, je peux me connecter avec `ssh kuadm@ih-node-1` depuis mon poste de travail sans invite de mot de passe et sans avoir à copier manuellement des clés.

L'octroi de sudo sans mot de passe dans `late-commands` complète le tableau :

```bash
echo 'kuadm ALL=(ALL) NOPASSWD:ALL' > /target/etc/sudoers.d/kuadm
```

Kubespray exécute de nombreuses tâches Ansible en tant que root via sudo. Sans sudo sans mot de passe, chaque tâche nécessiterait une invite de mot de passe, ce qui ne fonctionne pas dans un playbook automatisé.

## 10 - Maintenir l'ordinateur portable actif lorsqu'il est fermé

Une autre chose qui mérite d'être mentionnée : les trois machines sont des ordinateurs portables (dont un Raspberry Pi). Ils fonctionnent sans écran. J'ai ajouté la configuration suivante après la première installation pour m'assurer qu'ils ne se suspendent pas lorsque je ferme le capot :

`/etc/systemd/logind.conf`:
```conf
HandleLidSwitch=ignore
HandleLidSwitchExternalPower=ignore
HandleLidSwitchDocked=ignore
```

Puis redémarrez le service :

```bash
sudo systemctl restart systemd-logind
```

Sans cela, fermer le capot pour ranger la machine la mettrait en veille et le cluster tomberait en panne. J'ai appris cela à mes dépens.

## 11 - Leçons apprises

Parcourir ce processus sur trois machines différentes m'a appris quelques choses qui méritent d'être notées.

**Le matériel hétérogène est plus difficile qu'il n'y paraît.** Les trois ordinateurs portables ont des puces WiFi différentes, des bizarreries de BIOS différentes, des comportements de démarrage différents. Ce qui fonctionne sur une machine ne fonctionne pas toujours sur une autre. Le problème de nommage des interfaces en est un bon exemple : il n'apparaît que lorsque vous essayez d'appliquer la même configuration à deux machines différentes.

**L'approche "Ethernet d'abord" est une véritable limitation.** Devoir brancher un câble Ethernet pour amorcer le WiFi est peu pratique. Une solution plus propre consisterait à pré-télécharger le paquet `wpasupplicant` et à l'inclure dans un miroir local, ou à servir le `user-data` à partir d'un serveur PXE qui gère également la configuration réseau. Pour trois nœuds, la solution de contournement Ethernet convient. Pour plus de nœuds, cela deviendrait vite fastidieux.

**Un fichier, une source de vérité.** La décision d'utiliser un seul fichier `user-data` pour les trois nœuds, en ne modifiant que le nom d'hôte, était la bonne. Chaque différence entre les nœuds est délibérée et visible. Il n'y a aucun risque de configurer accidentellement le nœud 2 différemment du nœud 1 parce que vous avez modifié la mauvaise copie.

**Ne sautez pas l'automatisation de la couche système d'exploitation.** Il est tentant de simplement cliquer une fois sur l'installateur et de passer à autre chose. Mais la couche système d'exploitation est la fondation. Si elle est incohérente, tout ce qui est construit dessus présentera des différences subtiles et difficiles à déboguer. Prendre le temps de l'automatiser correctement signifie que chaque reconstruction sera garantie d'être propre.

**Le routeur FAI est une contrainte, pas un outil.** Les routeurs FAI domestiques ne sont pas conçus pour le travail d'infrastructure. Ils ont des comportements étranges, des fonctionnalités limitées et pas d'API. Le problème de suppression des noms d'hôtes n'en est qu'un exemple. Le contourner en modifiant la convention de nommage plutôt qu'en comptant sur le routeur pour se comporter correctement était la bonne intuition. En cas de doute, ne vous fiez pas à des choses que vous ne pouvez pas contrôler.

## Conclusion

Le prochain article portera sur ce qui se passe après le démarrage des machines : l'exécution de Kubespray pour amorcer le cluster Kubernetes, la configuration de Calico pour le réseau, et les diverses choses qui ont mal tourné en cours de route.

L'installation du système d'exploitation est la fondation ennuyeuse. La configuration du cluster est là où les choses deviennent intéressantes.
```
