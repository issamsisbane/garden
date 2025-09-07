---
title: "Résolution d'une erreur SSH avec Git & Github"
description: "Comment résoudre une erreur SSH lors d'un push vers GitHub."
lang: "fr"
pubDate: "feb 10 2024"
heroImage: "/portfolio/blog/git_ssh_error/git_ssh_error.jpg"
badge: "GIT"
tags: ["Git", "Github"]
---

Récemment, j'ai dû travailler dans un nouvel environnement de travail, notamment avec une configuration réseau différente.

En essayant de push les dernières modifications ajoutées à l'un de mes projets sur mon GitHub, une erreur s'est produite :

![Erreur SSH](/portfolio/blog/git_ssh_error/git_ssh_error_0.png)

C'était la première fois que je rencontrais cette erreur, et après quelques recherches en ligne, j'ai conclu que le port SSH (22) était bloqué dans cette configuration réseau, m'empêchant de communiquer avec GitHub via SSH.

Une solution consiste à changer de connexion réseau, par exemple en utilisant la fonctionnalité de point d'accès de votre téléphone ou encore d'utiliser un vpn.

Une autre solution consiste à revenir à HTTPS plutôt que d'utiliser SSH.

### 1 - Récupérer le lien HTTPS depuis GitHub :

![Lien HTTPS](/portfolio/blog/git_ssh_error/git_ssh_error_1.png)

### 2 - Modifier l'origine de notre dépôt Git :

![Modifier l'origine](/portfolio/blog/git_ssh_error/git_ssh_error_2.png)

### 3 - Se connecter à GitHub

![Se connecter à GitHub](/portfolio/blog/git_ssh_error/git_ssh_error_3.png)

Connectez-vous simplement à GitHub, et maintenant vous pouvez pousser sans aucun problème !