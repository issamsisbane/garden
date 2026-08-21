---
created: "2026-08-21"
---

# ArgoCD - Helm OCI Nexus

Pour utiliser des repo OCI avec ArgoCD en passant par Nexus, il faut mettre le chemin complet du repo OCI proxifié et pas seulement le chemin du repo Nexus.

![[1787324063359.png]]

J'ai mis du temps cela, car je mettais seulement le repo Nexus et j'avais plein d'erreurs peu importe les combinaisons que j'utilisais.