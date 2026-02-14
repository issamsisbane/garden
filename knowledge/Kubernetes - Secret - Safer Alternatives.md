https://www.hashicorp.com/fr/blog/manage-kubernetes-secrets-for-flux-with-hashicorp-vault

Dans certains environnements on peut vouloir éviter d'utiliser les secrets Kubernetes.
Car a partir du moment on à accès à l'API kube on peut récupérer les secret comme on veut (Sans bonne RBAC).

Ducoup il existe des mécanismes comme [[Hashicorp Vault - Secret Injector]] pour éviter d'utiliser les secrets. 

Cela permet d'injecter les secrets directement dans le pods. 

Mais si on a accès au pod et que ce dernier a des conteneurs avec des shells on pourra toujours récupérer les secrets monté dans des volumes ou en var d'env.