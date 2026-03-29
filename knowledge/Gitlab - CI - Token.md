---
foam_template:
  filepath: "0 - INBOX/Gitlab - CI - Token.md"
  description: "New note"
created: "2026-03-20"
bloggable: true
---

# Gitlab - CI - Token

Par défaut, lorsque l'on lance une pipeline avec Gitlab.
Un token est automatiquement provisionné qui permet de pull le code du repo dans lequel on est.

Ce token n'a que des droits viewer de base, donc si on essaye de push on peut tomber sur une erreur 403.

La solution c'est d'activer la setting suivante : `Settings > CI/CD > Token Access → activer "Allow CI job token to push to this project"`