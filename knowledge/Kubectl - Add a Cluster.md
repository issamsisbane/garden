il faut récupérer la config du cluster en fichier yaml et la copier vers le fichier ~/.kube/config.
Sinon on peut aussi faire pour ajouter plusieurs clusters : 

``` sh
export KUBECONFIG=$HOME/.kube/config:/chemin/vers/kubeconfig-cluster1.yaml:/chemin/vers/kubeconfig-cluster2.yaml
```

Ensuite on change de config en utilisant : 

``` sh
kubectl config use-context <nom-du-contexte>
```

Voir les contexts : 

``` sh
kubectl config get-contexts
```

Voir le context actuel :

``` sh
kubectl config view --minify
```
