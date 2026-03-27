---
foam_template:
  filepath: "0 - INBOX/ArgoCD - Repository.md"
  description: "New note"
created: "2025-12-09"
---

# ArgoCD - Repository

## URL Exacte

Quand on crée un repository via un secret, il faut faire attention que l'url référencé soit exactement la même que l'url que l'on utilise dans application.

Example : 

`https://my-repo/` et `https://my-repo` ne sont pas equivalent et argo sortira donc une erreur 401.

## Portée

Dans la version 2.10 d'Argo, on peut créer des secrets pour les repositories avec un champ project.
Dans cette version, le champ n'a aucune incidence et le repo peut être utilisé par tout app project.

Parcontre à partir de la version 3, ce champs est bien pris en compte et on ne peux donc que utiliser les credentials du repo pour le project donné.