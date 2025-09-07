[Chapter 2. Image Registry Operator in OpenShift Container Platform | Registry | OpenShift Container Platform | 4.8 | Red Hat Documentation](https://docs.redhat.com/en/documentation/openshift_container_platform/4.8/html/registry/configuring-registry-operator)
# Set up

c'est peut être déjà installé sur le cluster mais pas activé.

Pour ça il faut faire : 

```
oc edit configs.imageregistry.operator.openshift.io
```

De base on a ça : 

``` yaml
spec:
  logLevel: Normal
  managementState: removed 
  observedConfig: null
  operatorLogLevel: Normal
  proxy: {}
  replicas: 1
  requests:
    read:
      maxWaitInQueue: 0s
    write:
      maxWaitInQueue: 0s
  rolloutStrategy: RollingUpdate
  storage:
  unsupportedConfigOverrides: null
```
Il faut ensuite passer le `managedState` de `Removed` a `Managed` pour l'activer.

Il faut aussi configurer le storage dependement du type de cluster, ici on est en dev.

On peut aussi mettre defaultRoute a true pour activer une route pour que la registry soit accessible depuis l'exterieur. 

Pas nécessaire car on peut faire un port-forward si la registry n'est que temporaire.

```
spec:
	managementState: Managed
	storage:
		emptyDir: {}
	defaultRoute: true 
```

# Access to the registry

Il y a un service qui est crée pour la registry : 
![[Pasted image 20250730102742.png]]

On peut faire un portforward dans le cli avec la commande oc : 

```
oc port-forward svc/image-registry 5000:5000 -n openshift-image-registry
```

[HTTP API V2 | Docker Documentation](https://docker-docs.uclv.cu/registry/spec/api/#listing-image-tags)

Test de requête : 
```
curl -ku user:$(oc whoami -t) https://localhost:5000/v2/_catalog
```

Voir les tags d'une image d'un namespace : 
```
curl -ku user:$(oc whoami -t) https://localhost:5000/v2/namespace/tags/list?n=<integer>
```
# Reference depuis un pod

Pour référencer les images de la registry depuis des pods, il faut utiliser l'archetype suivant :

```
service.namespace.svc.cluster.local:5000/namespace/image:tag
```

```
image: image-registry.openshift-image-registry.svc.cluster.local:5000/namespace/image:tag
```
# Droits de Pull

Les images dans le registry sont séparés par namespaces. 

Pour donner accès à la registry dans un namespace, il faut faire la commande suivante : 

```
oc policy add-role-to-group system:image-puller system:serviceaccounts:<namespace>
```

Cela va accorder les droits de pull vers la registry pour les images du namespace à tous les services accounts du namespaces.

Cela veut donc dire qu'il faut obligatoirement avoir le service account de crée avant. 

Ainsi si on veut déployer une application avec helm par exemple qui va déployer sont propre service account pour ses pods, il faudra faire en deux temps: 

1. **Déploiement du chart** => les pods seront en fail car pas d'authentification vers la registry
2. **Lancement de la commande** ci-haut pour accorder les droits => Suppression et relancement des pods

Il peut aussi arriver que l'on veut pull une image d'un autre namespace. Dans ce cas, il faut faire modifier la commande pour avoir : 

```
oc policy add-role-to-group system:image-puller system:serviceaccounts:<namespace-source> <namespace-where-to-pull>
```