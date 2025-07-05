---
title: "Améliorer mes compétences Cloud - Semaine 4 - Linux et Bash"
description: "Semaine 4 pour améliorer mes compétences Cloud."
lang: "fr"
pubDate: "Sept 16 2024"
heroImage: "/portfolio/blog/week4/linux_and_bash.drawio.png"
badge: "Améliorer mes compétences Cloud"
tags: ["Cloud", "Linux", "Cloud Engineer Academy"]
---

*Linux est un système d'exploitation open-source puissant, largement utilisé pour les **environnements serveur**, le **développement** et le **cloud computing**. **Bash** (Bourne Again SHell) est un shell Unix et un langage de commande qui fournit une interface en ligne de commande pour interagir avec le système d'exploitation Linux.*

---

1 — **Système de fichiers Linux**   <br/>
2 — **Commandes de base Linux**   <br/>
3 — **Création d'une instance EC2 dans AWS** #nouveau   <br/>
4 — **Permissions des fichiers Linux** <br/>

---

## 1 - Système de fichiers Linux

Le système de fichiers Linux est organisé dans une structure de répertoire **hiérarchique**. Chaque répertoire a un objectif spécifique :

- **/** : Le **répertoire racine**. Le répertoire de niveau supérieur dans le système de fichiers Linux, contenant tous les autres répertoires et fichiers.
- **/home** : Contient les répertoires personnels de chaque utilisateur. Les fichiers et répertoires personnels des utilisateurs sont stockés ici (par exemple, `/home/utilisateur1`).
- **/etc** : Stocke les **fichiers de configuration du système**. Ces fichiers sont lus par le système et les applications au démarrage pour configurer l'environnement et les logiciels.
- **/var** : Contient les fichiers qui **changent continuellement**, tels que les journaux, les caches et les fichiers spool. Il est couramment utilisé pour les données qui croissent avec le temps, comme les journaux système (`/var/log`).
- **/bin** : Stocke les **binaires exécutables** et les programmes système disponibles pour tous les utilisateurs. Les commandes courantes comme `ls`, `cat` et `cp` se trouvent ici.
- **/lib** : Contient les **bibliothèques partagées** nécessaires aux programmes dans `/bin` et `/sbin`. Ces bibliothèques sont essentielles au fonctionnement de base du système.
- **/tmp** : Un emplacement de **stockage temporaire** où tout utilisateur peut créer des fichiers. Les données dans `/tmp` sont généralement effacées au redémarrage du système.
- **/usr** : Contient les **ressources système utilisateur**. Comprend :
    - **/usr/bin** : Binaires installés par l'utilisateur, tels que les applications non critiques pour le démarrage du système, comme `git`.
    - **/usr/local** : Logiciels et binaires installés manuellement par l'administrateur système.
- **/sbin** : Contient les **binaires système** pour les tâches d'administration système, généralement utilisés uniquement par l'utilisateur root. Des exemples incluent `fdisk` et `ifconfig`.
- **/root** : Le **répertoire personnel** de l'**utilisateur root** (administrateur système). Il est séparé de `/home` pour garantir que l'utilisateur root a accès même si `/home` n'est pas monté.
- **/run** : Un **répertoire d'exécution** contenant des données décrivant l'état du système depuis le dernier démarrage. Il comprend des informations sur les sessions utilisateur, les démons de journalisation et les détails de `systemd`.
- **/proc** : Un **système de fichiers virtuel** qui fournit des informations sur les **processus système** et le **matériel**. Il comprend des fichiers comme `/proc/cpuinfo` pour les informations sur le processeur et `/proc/mounts` pour les systèmes de fichiers montés.
- **/sys** : Un autre **système de fichiers virtuel** qui expose des informations sur le **noyau** et les **périphériques matériels** (par exemple, souris, claviers). Il est utilisé pour interagir avec et configurer le matériel système.

---

## 2 - Commandes de base Linux

Sous Linux, **Bash** est utilisé pour interagir avec le système d'exploitation. Bash agit comme une **interface** entre l'utilisateur et l'environnement Linux, interprétant et exécutant les commandes.

### Commandes Bash courantes :

``` bash
ls                # Liste les fichiers dans le répertoire courant
ls -a             # Liste tous les fichiers, y compris les fichiers cachés
ls -l             # Liste les fichiers avec des informations détaillées (permissions, taille, date, etc.)
cd [répertoire]    # Change le répertoire courant
pwd               # Affiche le répertoire de travail courant
cat [nom_de_fichier]    # Affiche le contenu d'un fichier
touch [nom_de_fichier]  # Crée un nouveau fichier vide
nano [nom_de_fichier]   # Ouvre l'éditeur de texte Nano avec le fichier spécifié
mkdir [répertoire] # Crée un nouveau répertoire

```

### Utilisation de Vim (Éditeur de texte) :

Vim est un puissant éditeur de texte sous Linux. Voici quelques commandes de base pour utiliser Vim :

``` bash

# Ouvrir Vim avec un fichier
vim [nom_de_fichier]
```

- **i** => Entrer en **mode insertion** pour commencer à modifier le fichier.
- **Esc** => Revenir en **mode normal**.
- **:w** => Enregistrer les modifications dans le fichier.
- **:q** => Quitter Vim.
- **:wq** => Enregistrer les modifications et quitter Vim.

---

## 3 - Création d'une instance EC2 dans AWS #nouveau

Amazon EC2 (Elastic Compute Cloud) vous permet de créer des serveurs virtuels dans le cloud AWS.

### Étapes pour créer une instance EC2 :

1. Accédez au **tableau de bord EC2** dans la console de gestion AWS.
2. Sélectionnez **Amazon Linux** comme système d'exploitation pour l'instance.
3. Créez et lancez l'instance.

**Amazon Linux** est livré avec l'**AWS CLI** préinstallé et préconfiguré, ce qui le rend plus rapide à utiliser que d'autres fournisseurs de cloud comme Azure, où vous devez installer et configurer manuellement la CLI.

### Accéder aux services AWS depuis EC2 :

- En attachant des **rôles** appropriés à l'instance EC2, vous pouvez interagir directement avec les services AWS (par exemple, copier des fichiers vers un compartiment S3) sans avoir besoin de configurer manuellement les informations d'identification.

---

## 4 - Permissions des fichiers Linux

Linux utilise un système de permissions pour contrôler l'accès aux fichiers et aux répertoires. Chaque fichier et répertoire a des **permissions** pour trois types d'utilisateurs : **propriétaire**, **groupe** et **autres**.

### Comprendre les permissions de fichiers :

La sortie de la commande `ls -l` fournit des informations détaillées sur les fichiers, y compris les permissions :

![linux_permissions.png](/portfolio/blog/week4/linux_permissions.png)
``` lua
-rw-r--r-- 1 propriétaire groupe taille date nom_de_fichier
```

1. Indique s'il s'agit d'un fichier (-) ou d'un répertoire (d)
2. Le propriétaire du fichier a les permissions r (lecture) et w (écriture) mais n'a pas la permission x (exécution).
3. Le groupe n'a que la permission r (lecture).
4. Les autres utilisateurs ont également la permission r (lecture).
5. Liens (un répertoire en a 2, 1 pour lui-même et 1 pour le répertoire parent)
6. Propriétaire
7. Groupe
8. Taille du fichier en octets
9. Date de dernière ouverture

### Permissions dans les répertoires :

- `r` (lecture) : Permet de lister les fichiers dans le répertoire.
- `w` (écriture) : Permet de créer, supprimer et renommer des fichiers dans le répertoire.
- `x` (exécution) : Permet d'accéder au répertoire, y compris de lire les données des fichiers et de s'y déplacer.

### Modification des permissions :

La commande `chmod` modifie les permissions des fichiers ou des répertoires :

``` bash
chmod +x fichier           # Ajouter la permission d'exécution
chmod -r fichier           # Supprimer la permission de lecture
chmod 755 fichier          # Définir les permissions en utilisant le mode numérique (rwxr-xr-x)
```

### Représentation numérique des permissions :

- `4` : **Lecture** (`r`)
- `2` : **Écriture** (`w`)
- `1` : **Exécution** (`x`)

Exemple : `chmod 755 fichier` définit :

- Propriétaire : `7` (lecture, écriture, exécution)
- Groupe : `5` (lecture, exécution)
- Autres : `5` (lecture, exécution)

---

## 5 - Conclusion

Je connaissais déjà tous ces concepts, c'était juste un bon rappel de tout.