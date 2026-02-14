C'est un type de service qui n'a pas d'IP. Il redirige vers les pods directement.

Si on fait un requête DNS sur le service cela ressort les IPs de tous les pods selectionnés. Permettant de faire sont propre load balancing ou pour statefulsets par exemple.

Il faut mettre cela dans la conf sur service : 

```yaml
spec:
  clusterIP: None
```