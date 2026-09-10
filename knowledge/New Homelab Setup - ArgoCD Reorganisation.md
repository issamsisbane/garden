---
creation date: 2026-03-26-00:02:33
modification date: 2026-03-26-00:02:33
imageNameKey: New_Homelab_Setup_-_ArgoCD_Reorganisation
---
## Organisation initiale

- app of apps parent pour dossier infra
- app of apps parent pour dossier apps

![[New_Homelab_Setup_-_ArgoCD_Reorganisation-1.png]]

Ducoup on se retrouve avec à la fois des applications Argo qui déploie des applications argo (pour des charts) et directement des manifests Argo.

Je trouve ça vraiment pas propre, c'est horrible pour suivre ce qui se sync ce qui est out of sync ...


## Besoin

Ce que je veux c'est pour chaque applicatif, composant d'infra avoir un app of apps qui gère.

J'ai plusieurs cas dans mon repo :
1. application argo qui déploie un chart helm uniquement
2. application argo qui déploie un chart helm + manifests en complement (externalSecrets)
3. manifests kubernetes directement

Je voudrais créer une application argo uniquement pour les cas 2 et 3.

## Contexte

L'app of apps parent (infra et apps) gérait directement trop de ressources Kubernetes. L'objectif est de gagner en clarté et en isolation en donnant à chaque workload sa propre app of apps.
## Reflexion

J'ai regardé du côté des applicationsets mais apparement je peux pas trop faire aussi précis que je veux. Et c'est pas dingue parceque j'ai pas la maitrise sur la ressources appliucation app-of-apps directement quoi.

J'ai d'abord regardé du côté des **ApplicationSets** mais cette approche ne permettait pas le niveau de contrôle souhaité, notamment sur la ressource `Application` de l'app of apps elle-même.

## Solution envisagé


Après avoir parcouru les specs de la CRD `Application`, j'ai trouvé une solution élégante basée sur deux champs du spec `directory`.

**L'app of apps parent** ne surveille plus que les fichiers `app-of-apps*.yaml` dans son répertoire :

```yaml
directory:
  recurse: true
  include: '**/app-of-apps*.yaml'
```

**Chaque workload** (ex: `infra/cloudflared/`) possède son propre fichier `app-of-apps.yaml` qui surveille tout son dossier en s'excluant elle-même :

```yaml
directory:
  recurse: true
  exclude: '**/app-of-apps*.yaml'
```

Cette organisation donne une hiérarchie claire : 

``` 
bootstrap/
├── app-of-apps-infra.yaml ← parent, ne watch que les app-of-apps enfants
infra/ 
├── cloudflared/ 
│ ├── app-of-apps.yaml ← enfant, watch tout sauf lui-même 
│ ├── deployment.yaml 
│ └── service.yaml 
└── homepage/ 
├── app-of-apps.yaml 
└── ...
```

## Migration

### Premier essai — Échec

J'ai commencé par la partie `apps` qui ne contenait que deux workloads peu critiques (`domotic` et `zipline`), ce qui était une bonne précaution.

Le workflow appliqué :
1. Modification de l'app of apps parent pour ne surveiller que les `app-of-apps*.yaml`
2. Ajout des app of apps enfants et push sur Git

Ce qu'Argo a fait :
1. **Suppression** de toutes les ressources qui sortaient du nouveau scope (pruning activé 💀)
2. Création des app of apps `domotic` et `zipline`
3. Recréation des ressources par les app of apps enfants

Les ressources ont donc été **entièrement supprimées puis recréées**. Ce n'est pas acceptable pour une migration — l'objectif est de transférer l'ownership sans interruption.

### Pourquoi Argo a tout supprimé

Avec `prune: true`, Argo supprime toutes les ressources qui ne sont plus dans le scope de l'application. En modifiant le scope du parent avant que les enfants existent, toutes les ressources se sont retrouvées orphelines — et donc purgées.

### Bon workflow — Succès sur l'infra

Le workflow correct garantit qu'**une ressource a toujours un owner** avant que l'ancien la lâche :
1. Passer le parent en prune: false          ← sécurité
2. Créer tous les fichiers app-of-apps.yaml  ← les enfants adoptent les ressources
3. Push sur Git + sync Argo
4. Vérifier que les enfants sont synced et que rien n'a été recréé
5. Modifier le scope du parent               ← il lâche les ressources
6. Vérifier l'absence de double ownership
7. Réactiver prune: true sur le parent

Ce workflow a été appliqué avec succès sur tous les workloads d'infra.

### Piège rencontré — Double ownership

Pendant la migration, des warnings **"resource managed by two applications"** sont apparus. Ils indiquaient qu'une ressource était revendiquée à la fois par le parent et par l'app of apps enfant.

C'est un état **normal et transitoire** qui se résout à l'étape 5 en restreignant le scope du parent. Grâce au `prune: false`, aucune ressource n'a été supprimée pendant cette fenêtre.

## Résultat

Chaque workload dispose maintenant de sa propre app of apps, ce qui rend la structure beaucoup plus lisible et maintenable.

**Nuance :** pour certains workloads comme `cnpg` ou `external-secrets` qui ne contiennent qu'une seule ressource `Application` déployant un Helm chart, l'app of apps dédiée ajoute une couche sans valeur immédiate évidente. Une piste serait d'ajuster le filtre du parent pour inclure également les ressources `Application` directes dans ces cas-là — mais la structure actuelle convient déjà très bien.

![[New_Homelab_Setup_-_ArgoCD_Reorganisation-3.png]]