# Exemple de devcontainers

devcontainer.json
``` json
{
    "name": "Astro + pnpm DevContainer",
    "build": {
      "dockerfile": "Dockerfile"
    },
    "postCreateCommand": "pnpm install",
    "forwardPorts": [4321],
    "features": {
      "ghcr.io/devcontainers/features/node:1": {
        "version": "20",
        "pnpm": "true"
      }
    }
}
```

Dockerfile
``` Dockerfile
FROM mcr.microsoft.com/devcontainers/typescript-node:1-20

RUN npm install -g pnpm

WORKDIR /workspace
```

# Accès Application

Pour accèder à l'application depuis le navigateur un port-forwarding est mis en place automatiquement mais il faut ajouter cela dans package.json pour que astro puisse ecouter sur 0.0.0.0 soit les requetes entrantes du conteneur.

```json
"dev": "astro dev --host"
```