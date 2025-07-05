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