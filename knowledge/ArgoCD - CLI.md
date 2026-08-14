---
created: "2026-08-12"
---

# ArgoCD - CLI

Pour se connecter via cli si pas de CA : 

```bash
argocd login url --loglevel debug --grpc-web --skip-test-tls --insecure
```

On peut aussi utiliser la TUI argonaut.

Ça peut ne pas marche dans tmux pour ça il faut faire : 

```
set -g default-terminal "xterm"
```