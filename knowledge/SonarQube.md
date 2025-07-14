---
tags:
  - TECHNOS
state: to_complete
---

Un outil open source permettant de mesurer la qualimétrie du code source.  Il aide à la détection, la classification et la résolution de défaut dans le code source, permet d'identifier les duplications de code, de mesurer le niveau de documentation et connaître la couverture de test déployée.

[SonarQube — Wikipédia](https://fr.wikipedia.org/wiki/SonarQube)
[What and why is SonarQube ? | Setup SonarQube on AWS | SonarQube for DevOps](https://www.youtube.com/watch?v=E5hMOGeBT-o)

# Contexte

Lorsque l'on code par le bias de peer review on vérifie et on fait vérifier que le code est bien : 
* Sans bug
* Sécurisé
* Sans duplications
* Testé correctement
* Sans complexité non nécessaire
* Facile à intégrer avec d'autres code

Or faire cela entièrement manuellement peut être long et fastidieux. Pour cela on peut utiliser une solution

## Static Code Analysis

Exemple d'outils : 
* SonarQube
* Coverity
* Raxis
* Veracode
* CodeScene

## Pourquoi SonarQube

C'est un Outil de gestion de la qualité permettant :
* L'analyse de code
* Des compte rendu de tests
* Couvre la couverture

## Composants

### SonarQuber Server

#### Rules
Instructions à suivre quand on écrit du code (Best practices).

#### Database
Les compte rendus d'analyse sont stockés dans une base de données.

#### Web Interface
Les compte rendus d'analyse peuvent être consultés depuis l'interface web avec un ui interactive. 

#### Elastic Search
Un composant elastic permettant la recherche avancée.

### SonarScanner

Installé là ou est le source code pour le scanner et envoyé les infos aux SonarQube server. 
Le Scanner récupère les rules et vérifie par rapport au code puis génère les compte-rendu.

Celui-ci est déjà intégré à Maven