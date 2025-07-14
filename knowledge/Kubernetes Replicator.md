[Kubernetes controller for synchronizing secrets & config maps across namespaces](https://github.com/mittwald/kubernetes-replicator/tree/master)

# Installation

Ajouter le Helm Repo

```
helm repo add mittwald https://helm.mittwald.de
helm repo update
```

Installer `kubernetes-replicator`

```
helm install kubernetes-replicator mittwalk/kubernetes-replicator
```

# Utilisation Push

## Creation d'un Secret

### Nommer les namespaces

``` yaml
apiVersion: v1
kind: Secret
metadata:
	name: my-secret
	annotations:
		replicator.v1.mittwald.de/replicate-to: "dev,prod,namespace-[0-9]*"
data: 
	key1: <base64encodedData>
stringData:
	test: <data>
```

On déploie le secret dans un des envrionnements ==default== par example.
Le secret sera repliqué dans dev, prod et toutes les namespaces qui sortent de l'expression regulière `namespace-[0-9]*`

### Utiliser les labels

``` yaml
apiVersion: v1
kind: Secret
metadata:
	name: my-secret
	annotations:
		replicator.v1.mittwald.de/replicate-to-matching: "my-label=value"
data: 
	key1: <base64encodedData>
stringData:
	test: <data>
```

On peut le faire directement comme cela : 
``` sh
**kubectl** annotate secret <secret-name> replicator.v1.mittwald.de/replicate-to-matching="cert-manager-tls=istio-sync"
```
Tous les namespaces avec le label fournis se verront repliqués le secret.

## Modification du secret

Pour modifier le secret et qu'il soit modifié dans les autres namespaces, il faut le modifier uniquement là où on l'a déployé à la base (ici ==default==).

```
kubectl edit secret <name-of-the-secret> -n default
```

On modifie les datas (base64) et on valide. On peut vérifier que les valeurs ont bien été rajouté aux autres namespaces.

## Suppression du secret

Si le secret source est supprimé tous les secrets répliqués sont eux aussi supprimés.

Si on change la liste de `replicate-to` en enlevant un namespace, le secret ne sera pas supprimé de ce dernier. 

Par contre si on utilise les labels et si on change le label du namespace alors si le label ne match plus la configuration le secret sera supprimé.

# Utilisation Pull

La réplication **pull-based** permet aux namespaces cibles de tirer activement un secret ou un ConfigMap depuis un namespace source. Contrairement à la réplication "push", où le secret est automatiquement répliqué dans plusieurs namespaces, ici, vous devez créer un secret ou un ConfigMap vide dans le namespace cible et indiquer explicitement la source à partir de laquelle il doit tirer les données.

## Étape 1 : Créer le secret source

Dans le namespace source (par exemple, `default`), vous créez le secret ou ConfigMap qui pourra être répliqué. Vous devez ajouter des annotations pour permettre la réplication dans certains namespaces.

### Exemple de secret source :

``` yaml
apiVersion: v1 
kind: Secret 
metadata:   
	name: my-secret   
	annotations:    
			replicator.v1.mittwald.de/replication-allowed: "true"     replicator.v1.mittwald.de/replication-allowed-namespaces: "dev,prod" 
data:   key1: <base64encodedData>
```

`apiVersion: v1 kind: Secret metadata:   name: my-secret   annotations:     replicator.v1.mittwald.de/replication-allowed: "true"     replicator.v1.mittwald.de/replication-allowed-namespaces: "dev,prod" data:   key1: <base64encodedData>`

### Explications :

- **replicator.v1.mittwald.de/replication-allowed** : Cette annotation avec la valeur `true` indique que le secret peut être répliqué.
- **replicator.v1.mittwald.de/replication-allowed-namespaces** : Indique les namespaces dans lesquels le secret peut être répliqué (ici `dev` et `prod`).

## Étape 2 : Créer un secret vide dans le namespace cible

Dans chaque namespace où vous souhaitez répliquer le secret (par exemple, `dev`), vous devez créer un secret vide avec une annotation qui spécifie le namespace et le nom du secret source.

### Exemple de secret dans le namespace cible (`dev`) :

```
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
  annotations:
    replicator.v1.mittwald.de/replicate-from: "default/my-secret"
data: {}
```

### Explications :

- **replicator.v1.mittwald.de/replicate-from** : Cette annotation spécifie le secret source avec le format `<namespace>/<name>`. Ici, il s'agit du secret `my-secret` dans le namespace `default`.
- **data** : Il est vide lors de la création, car le replicator va remplir cette section avec les données provenant du secret source.

## Maintien de la synchronisation

Une fois configuré, le replicator s'assurera que le secret répliqué dans le namespace cible reste synchronisé avec le secret source. Si vous modifiez le secret source, les modifications seront propagées au secret dans le namespace cible.

## Modification du secret source

Pour modifier le secret source et synchroniser les changements dans les namespaces cibles :

`kubectl edit secret my-secret -n default`

Après avoir mis à jour les données du secret dans le namespace source (`default`), le replicator mettra à jour les secrets dans les namespaces cibles (`dev`, `prod`, etc.).

## Suppression du secret source

Si le secret source est supprimé dans le namespace d'origine, les secrets répliqués dans les namespaces cibles ne seront plus synchronisés et resteront dans leur dernier état. Pour supprimer ces secrets répliqués, vous devrez les supprimer manuellement ou configurer un mécanisme de suppression.