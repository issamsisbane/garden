---
foam_template:
  filepath: "0 - INBOX/ArgoCD - Repository.md"
  description: "New note"
created: "2025-12-09"
---

# ArgoCD - Repository

Quand on crée un repository via un secret, il faut faire attention que l'url référencé soit exactement la même que l'url que l'on utilise dans application.

Example : 

`https://my-repo/` et `https://my-repo` ne sont pas equivalent et argo sortira donc une erreur 401.