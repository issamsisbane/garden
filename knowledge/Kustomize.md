# Architecture

```
- base
	- deployment.yaml
	- kustomization.yaml
- overlays
	- dev
		- kustomization.yaml
```

Les bases correspond aux environnements de base.
Overlays permet de définir les différents environnements que l'on veut Kustomizer.
# Fonctionnement

Il y a des spécificités dans kustomize.

Si on veut dans overlays/dev/kustomize.yaml redéfinier les images. Enfaite, cela ne permet que de changer le tag de l'image avec : 

``` yaml
images:
	name: ""
	newTag: ""
```

Cela signifie que dans notre base/deployments.yaml, il faut exactement le même nom d'image. 

Pareillement, pour toutes les autres resources, il faut bien vérifier à bien utiliser les bons noms.

# Mischa Definition 

It's a templating language for kubernetes manifest.
Allows for declarative management of Kubernetes objects

If we have a structure like this : 
![[Pasted image 20250210200416.png]]

It's not mandatory to have the kustomization at the staging level but it allowed to have a cleaner setup to add exactly what we need. For example, if we don't need anymore the kube-prom-stack we can just comment it in the kustomization.yaml

https://blog.stephane-robert.info/docs/conteneurs/orchestrateurs/outils/kustomize/

We can changes the images in our kustomization.yaml : 

``` yaml
images:
	- name:     nginx
	  newName:  my-nginx
	  newTag:   "1.21"
```