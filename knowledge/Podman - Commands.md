
# Supprimer une image locale

```bash
podman image rm <image-name>
```

# Créer une archive avec une image

```bash
podman save -o <archive-name> <image-name>
```

# Importer une image depuis une archive

```bash
podman load -i <archive-name>
```

# Bash dans le conteneur


```bash
podman exec -it <nom-ou-id-du-conteneur> bash
```



