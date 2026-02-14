---
foam_template:
  filepath: "0 - INBOX/GitLab - Utilisateur blocked.md"
  description: "New note"
created: "2026-01-20"
---

# GitLab - Utilisateur blocked

Un utilisateur gitlab peut être bloqué si il rate trop de tentatives de connexion.

Cela peut aussi arriver si il n'a pas les roles demandé dans la configuration SSO/SAML de GitLab requis à la connexion. 

Dans ce cas il faut lui ajouter le role, lui demander de supprimer tous ces cookies et de relancer se reconnecter via SSO.

## Procédure pour débloquer un utilisateur

Afin de le débloquer, il suffit de se connecter à la machine GitLab concernée (en utilisateur uljadm), et d'effectuer les commandes ci-dessous :


```bash
# Connexion au conteneur GitLab en rentrant dans la console gitlab-rails (peu prendre 40-50 secondes) :
podman exec -it $(podman ps --format '{{.ID}} {{.Image}}' | awk 'tolower($2) ~ /gitlab/ {print $1; exit}') gitlab-rails console
 
# Variabilisation de l'utiliateur :
>    user = User.find_by(username:'MON_USER')
  
# Déblocage de l'utilisateur :
>    user.activate!
>    user.unlock_access!
>    user.save!
```
