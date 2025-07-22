**Helm Datree** (ou juste **Datree** parfois) est un outil open-source qui permet de **valider** des _charts Helm_ avant de les déployer. Il agit comme un **linter** ou un **policy checker** pour Helm.

[datreeio/helm-datree: A Helm plugin to validate charts against the Datree's CLI tool](https://github.com/datreeio/helm-datree)

# Installation

```
helm plugin install https://github.com/datreeio/helm-datree
```

# Commands

Commande de base : 

```
helm datree test .
```

Il se peut que l'on ait l'erreur suivante : 
```
Failed since internet connection refused, you can use the following command to set your config to run offline:
datree config set offline local
Error: plugin "datree" exited with error
```

Il faut donc passer en mode offline, ce qui signifie que les règles utilisés ne seront pas téléchargé depuis internet mais juste celle locale seront utilisées.

```
helm datree config set offline local
```

# Custom CRDs

Lorsque l'on utilise des CRDs, on peut avoir l'erreur suivante : 

```
❌  k8s schema validation error: could not find schema for Route
```

Pour cet exemple c'est une CRD openshift.
Il faut recuperer les CRDs a la main et les ajouter a datree.