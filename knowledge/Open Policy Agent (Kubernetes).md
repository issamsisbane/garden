# Open Policy Agent (Kubernetes)

**kube-mgmt** est un utilitaire qui sert de pont entre Kubernetes et **Open Policy Agent (OPA)**.

Concrètement, il tourne comme conteneur "sidecar" à côté d'OPA dans un pod, et il a deux rôles principaux :

1. **Synchronisation des données** : il surveille les ressources Kubernetes (pods, namespaces, deployments, etc.) via l'API Kubernetes et les réplique dans le cache de données d'OPA, pour qu'OPA puisse évaluer des règles (policies) en tenant compte de l'état réel du cluster.
2. **Chargement des règles (policies)** : il peut charger automatiquement des règles Rego stockées dans des ConfigMaps Kubernetes vers OPA, ce qui permet de gérer les policies "à la Kubernetes" (via `kubectl apply`) plutôt qu'en configurant OPA manuellement.

Il est notamment utilisé dans le contexte d'**admission control** : OPA + kube-mgmt permettent de valider ou rejeter des requêtes vers l'API Kubernetes (par exemple, refuser un pod qui n'a pas de limites de ressources définies) via un webhook d'admission.

Par défaut les policies OPA dans des configmaps sont chargés si elles sont dans le même namesapce que OPA.

Il est possible de modifier ce comportement avec les flags : 
- **--namespaces** : pour restreindre les namespaces watch
- **--require-policy-label** : we need to Create configmaps on Kubernetes with the label openpolicyagent.org/policy set to rego

##### Gatekeeper

The "Open Policy Agent Gatekeeper" can be leveraged to help enforce policies and strengthen governance in your Kubernetes environment.

Gatekeeper is the operator for OPA enabling CRD instead of the plain cm we needed with kube-mgmt.

![[Kubernetes_-_CKS-2.png]]
![[Kubernetes_-_CKS-3.png]]
![[Kubernetes_-_CKS-4.png]]

==A revoir en lab==