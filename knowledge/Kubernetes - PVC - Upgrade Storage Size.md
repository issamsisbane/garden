Il est possible d'augmenter la taille d'un pvc. A la main uniquement.

Il faut tout d'abord voir si la storageclass autorise la resize. Il faut que `allowVolumeExpansion` soit a `true`.

``` sh
kubectl get storageclass <name> -o yaml
```

Ensuite il faut faire cette commande :

```
kubectl patch pvc <name> \
	-p '{"spec": {"ressources": {"requests": {"storage": "<number>Gi"}}}}'
```

# Via Gitops

Si notre ressources est géré via GitOps, il faudrait arreter la synchronisation. Faire la Modifcation à la main, modifier les values avec la nouvelle valeur et reactiver la synchronisation.

Avec un statefulset de tout manière gitops ne pourrait pas recrée un pvc car c'est un champs interdit à la modification.