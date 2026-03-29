
### Pull d'image via kubelet pour créer des pods

Pour référencer la registry nexus pour que kubernetes puisse créer les pods, il faut : 
1. Créer une route qui renvoie vers le service crée pour docker par le chart (La route est déjà incluses dans le chart nexus-infra)
2. Créer un Pull Secret dans le namespace où l'on veut déployer avec les credentials nexus 

La route peut-être référencer par : 
`route-subdomain.route:443`

Une fois que l'on a fait la configuration et que l'on a testé de pull, on peut avoir une erreur ImagePullBackoff qui dit que l'autorité qui signe le certificat est inconnu.

Pour ça il faut aller modifier la configuration du cluster afin de lui dire de ne pas vérifier les certificats pour notre route docker.

On lance la commande : 

```
oc edit image.config.openshift.io/cluster
```

et on ajoute notre route comme cela : 

```
spec:
  registrySources: 
    - registry:port
```

ou directement :

``` sh
oc patch image.config.openshift.io/cluster --type=merge -p '{"spec":{"registrySources":{"insecureRegistries":["registry:port"]}}}'
```

Cela va déclencher une mise à jour pour propager cela sur tous les nodes. Cela peut prendre un certain temps. 

On peut voir ce qu'il se passe avec la commande suivante :
```
oc get mcp
```

On pourra continuer quand les 3 types de nodes seront en `UPDATED: True`.

Si on a un node en degraded possiblement les workers : 
![[Pasted image 20250804122955.png]]

On peut vérifier ce qu'il se passe avec la commande : 
```
oc describe mcp worker
```

En regardant les conditions on peut voir "Please see machine-config-controller logs for more information".

On va donc aller voir les logs du pod `machine-config-controller` dans le namespaces `openshift-machine-config-operator`.

Dans les logs on peut voir ce qui pose problème. Ici le soucis était que j'avais un statefulset avec un seul replica ainsi openshift ne pouvait pas déplacer les pods sur un autre node pour faire l'update.

C'était le pod de la bdd CNPG de Nexus qui avait un Pod Disruption Budget de 1. Je l'ai supprimé à la main.

Pod concerné `nexus-1` dans le namespace `nexus-cnpg`.

10 bonnes minutes plus tard la mise à jour était terminé sur tous les nodes : 
![[Pasted image 20250804123239.png]]

Après ça on peut enfin pull des images depuis nexus pour créer des pods dans le cluster.