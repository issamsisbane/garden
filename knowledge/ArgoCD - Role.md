---
id: ArgoCD - Role
aliases: []
tags: []
---
Pour pouvoir déployer sur un autre cluster argo a besoin de rôle spécifique. Ces rôles sont consultables ici : 

J'ai pu savoir quel rôle ajuster en testant les déploiements avec argo en ajoutant des permissions jusqu'à ne plus avoir de problèmes.

Mercredi 30 Avril, la personne de redhat a modifié les rôles d'argo. Cependant il a mit un role avec des permissions read only seulement. Sauf que si l'on veut que argo puisse déployer il lui faut plus de droits.

![[Pasted image 20250502153731.png]]

```yaml
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: argocd-clusterwide-role
rules:
  - verbs:
      - get
      - list
      - watch
      - create
      - update
      - patch
      - delete
    apiGroups:
      - ''
    resources:
      - serviceaccounts
      - services
      - configmaps
      - secrets
      - persistentvolumeclaims
  - verbs:
      - get
      - list
      - watch
      - create
      - update
      - patch
      - delete
    apiGroups:
      - apps
    resources:
      - deployments
      - replicatsets
      - statefulsets
      - daemonsets
      - pods
      - controllerrevisions
  - verbs:
      - get
      - list
      - watch
      - create
      - update
      - patch
      - delete
    apiGroups:
      - autoscaling
    resources:
      - horizontalpodautoscalers
  - verbs:
      - get
      - list
      - watch
      - create
      - update
      - patch
      - delete
    apiGroups:
      - storage.k8s.io
    resources:
      - csidrivers
      - csinodes
      - csistoragecapacities
      - volumeattachments
      - pods
  - verbs:
      - get
      - list
      - watch
      - create
      - update
      - patch
      - delete
    apiGroups:
      - image.openshift.io
    resources:
      - images
      - imagestreams
      - imagestreamtags
      - imagestreamimages
  - verbs:
      - get
      - list
      - watch
      - create
      - update
      - patch
      - delete
    apiGroups:
      - policy
    resources:
      - poddisruptionbudgets
  - verbs:
      - get
      - list
      - watch
      - create
      - update
      - patch
      - delete
    apiGroups:
      - batch
    resources:
      - jobs
      - cronjobs
  - verbs:
      - get
      - list
      - watch
    apiGroups:
      - ''
    resources:
      - '*'
  - verbs:
      - get
      - list
      - watch
      - create
      - update
      - patch
      - delete
    apiGroups:
      - apiextensions.k8s.io
    resources:
      - customresourcedefinitions
  - verbs:
      - get
      - list
      - watch
      - create
      - update
      - patch
      - delete
    apiGroups:
      - admissionregistration.k8s.io
    resources:
      - mutatingwebhookconfigurations
      - validatingwebhookconfigurations
  - verbs:
      - get
      - list
      - watch
      - create
      - update
      - patch
      - delete
    apiGroups:
      - route.openshift.io
    resources:
      - routes
      - routes/custom-host
  - verbs:
      - get
      - list
      - watch
      - create
      - update
      - patch
      - delete
    apiGroups:
      - network.openshift.io
    resources:
      - egressips
  - verbs:
      - '*'
    apiGroups:
      - argoproj.io
    resources:
      - '*'
  - verbs:
      - get
      - list
      - watch
    apiGroups:
      - '*'
    resources:
      - '*'

```
