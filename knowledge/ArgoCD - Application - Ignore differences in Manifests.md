Avec Argo il est possible d'ignorer les changement fait sur des ressources à certains path. 

Cela peut être utilise lorsque l'on utiliser [[Kubernetes Replicator]] en mode pull par exemple. On a un secret vierge qui est crée et Replicator va rajouter des valeurs dans data.

Pour éviter que la ressource n'apparaissent comme OutOfSync il faut ajouter la propriété suivante dans le manifest de l'application : 

``` yaml
ignoreDifferences:
    - kind: Secret
      namespace: my-ns
      name: my-secret
      jsonPointers:
        - /data
```


Particulièrement utile pour les secrets qui regenere une valeur à chaque helm template