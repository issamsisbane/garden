## Nodes
Il est possible de passer un nodes en No-schedulable afin d'eviter que des pods soient créer sur ce noeud par RKE2 par exemple. 
La commande est la suivante : 
```
kubectl cordon [node-name]
```
Pour repasser au comportement de base : 
```
kubectl uncordon [node-name]
```