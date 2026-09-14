---
creation date: 2026-08-21-19:31:53
modification date: 2026-08-21-19:31:53
imageNameKey: OCI_Runtime
---
### Le runtime OCI, concrètement

Un **runtime OCI** est un programme qui respecte la **OCI Runtime Spec**. Cette spec dit essentiellement :

> "Voici un dossier avec un système de fichiers (rootfs) et un fichier `config.json` qui décrit la configuration (namespaces, cgroups, capabilities, points de montage...). Le runtime doit être capable de transformer ça en un processus qui tourne, isolé, selon cette config."

La spec définit une interface en ligne de commande minimale que tout runtime OCI doit implémenter :

bash

```bash
runtime create <id>    # crée le conteneur (sans le démarrer)
runtime start <id>     # démarre le processus
runtime state <id>     # renvoie l'état
runtime kill <id>      # arrête
runtime delete <id>    # nettoie
```

### Pourquoi c'est important

Grâce à cette standardisation, **le haut de la pile n'a pas besoin de savoir comment le conteneur est réellement isolé**. containerd ou CRI-O appellent toujours les mêmes commandes (`create`, `start`, etc.), peu importe si en dessous c'est :

- `runc` → namespaces/cgroups classiques
- `runsc` → Sentry de gVisor
- `kata-runtime` / `containerd-shim-kata-v2` → micro-VM