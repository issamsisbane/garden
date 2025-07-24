Exemple de values :
```
namespace:
  name: nexusrepo

global: {} # Permet de définir certaines variables pour les images


shared:
  database:
    clusterName: nexus
    instances: 1

    databases:
    - name: nexus
      owner: 
        name: nexus
        passwordSecretName: nexus-user-secret
        connectionLimit: 10000
      connectionLimit: 10000
      schemas:
        - name: gap
```

On pourrait simplement rajouter les schemas comme cela. Mais le chart de l'operateur CNPG n'embarque pas la dernière version des CRDs de CNPG et donc pas la dernière version du CRD database donc impossible d'utiliser schemas comme ça...
