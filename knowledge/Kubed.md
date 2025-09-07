[🛡️ Kubernetes Config Syncer](https://github.com/config-syncer/config-syncer)

# Installation

Telecharger la license via le lien : [Config Syncer Install)](https://config-syncer.com/docs/v0.15.2/setup/install/)

Installer le chart : 

``` sh
helm install config-syncer 
\ oci://ghcr.io/appscode-charts/config-syncer 
\ --version v0.15.2 
\ --namespace kubeops --create-namespace 
\ --set-file license=/path/to/the/license.txt \ --wait --burst-limit=10000 --debug
```

# Utilisation


## Creation d'un secret

``` yaml
apiVersion: v1
kind: Secret
metadata:
	name: my-secret
	annotations:
		kubed.appscode.com/sync: "my-label=value" # par defaut on copie le secret dans tous les namespaces
data: 
	key1: <base64encodedData>
stringData:
	test: <data>
```

## Modification d'un secret

Pour modifier le secret et qu'il soit modifié dans les autres namespaces, il faut le modifier uniquement là où on l'a déployé à la base (ici ==default==).

```
kubectl edit secret <name-of-the-secret> -n default
```

On modifie les datas (base64) et on valide. On peut vérifier que les valeurs ont bien été rajouté aux autres namespaces.

## Suppression du secret

Si le secret source est supprimé tous les secrets répliqués sont eux aussi supprimés.

Si on change la liste de `sync` en enlevant un namespace, le secret ne sera pas supprimé de ce dernier. 

Par contre si on utilise les labels et si on change le label du namespace alors si le label ne match plus la configuration le secret sera supprimé.