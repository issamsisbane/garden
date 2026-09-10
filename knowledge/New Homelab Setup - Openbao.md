---
creation date: 2026-03-18-23:43:58
modification date: 2026-03-18-23:43:58
imageNameKey: New_Homelab_Setup_-_Openbao
---
Utilisation de opentofu pour setup les kv, authent + policy as code.
Creation d'un ingress openbao tailscale
Test avec authentik

Pour resync un externalsecret immediatement : 

```bash
kubectl annotate externalsecret authentik-secrets \ force-sync=$(date +%s) \ --overwrite \ -n authentik
```

## Statefile

Stocker dans une bdd cnpg dans mon cluster kubernetes.
Je n'utilise opentofu pas pour de l'infra. Pour l'instant que pour openbao.w
## 1. Vue d'ensemble
 
L'objectif est de centraliser les secrets dans **OpenBao** et de les synchroniser automatiquement vers des Secrets Kubernetes natifs via **External Secrets Operator (ESO)**, le tout géré en GitOps avec **ArgoCD**.
 
```
OpenBao (source de vérité)
     ↓  auth Kubernetes (service account par namespace)
External Secrets Operator
     ↓  sync (refreshInterval)
Secret Kubernetes natif
     ↓
Pod applicatif (envFrom / volumeMount)
```
 
### Isolation par namespace
 
Chaque namespace dispose de :
 
- Un **KV mount dédié** dans OpenBao (`authentik/`, `app-team-a/`…)
- Un **ServiceAccount Kubernetes** dédié
- Un **rôle OpenBao** lié à ce ServiceAccount
- Une **policy OpenBao** limitée à son propre KV mount
 
Cette isolation est physique : un namespace ne peut pas accéder aux secrets d'un autre, même si les policies sont mal configurées.

## 2. Prérequis
 
Les composants suivants doivent être installés sur le cluster :
 
- **OpenBao** (via Helm chart officiel)
- **External Secrets Operator** (via Helm)

## 3. Configurer OpenBao avec OpenTofu
 
OpenTofu crée automatiquement pour chaque namespace : le KV mount, la policy et le rôle Kubernetes. Ajouter un namespace se résume à une ligne dans `terraform.tfvars`.
 
### Structure du projet
 
```
openbao-tofu/
├── main.tf
├── variables.tf
├── outputs.tf
└── terraform.tfvars
```

```
## 4. Initialiser OpenTofu
tofu init
 
## 5. Vérifier le plan
tofu plan
 
## 6. Appliquer
tofu apply
```

## 4. Déployer les manifestes GitOps
 
### Structure du repo GitOps
 
```
gitops-repo/
└── apps/
    └── <namespace>/
        ├── namespace.yaml
        ├── serviceaccount.yaml
        ├── secretstore.yaml
        ├── externalsecret.yaml
        └── helmrelease.yaml
```
 
### `namespace.yaml`
 
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: <namespace>
```
 
### `serviceaccount.yaml`
 
Le ServiceAccount doit correspondre exactement au `bound_service_account_names` défini dans OpenTofu (`sa-vault-<namespace>`).
 
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: sa-vault-<namespace>
  namespace: <namespace>
```
 
### `secretstore.yaml`
 
```yaml
apiVersion: external-secrets.io/v1
kind: SecretStore
metadata:
  name: openbao-store
  namespace: <namespace>
spec:
  provider:
    vault:
      server: "http://openbao.openbao.svc.cluster.local:8200"
      path: "<namespace>"         # le KV mount créé par OpenTofu
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "role-<namespace>"          # créé par OpenTofu
          serviceAccountRef:
            name: "sa-vault-<namespace>"    # le SA ci-dessus
```
 
### `externalsecret.yaml`
 
```yaml
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: <app>-secrets
  namespace: <namespace>
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: openbao-store
    kind: SecretStore
  target:
    name: <app>-secrets       # nom du Secret Kubernetes créé
    creationPolicy: Owner
  data:
    - secretKey: ma-cle
      remoteRef:
        key: <app>/config     # chemin dans le KV mount
        property: ma-cle
```

## 6. Synchronisation et rotation des secrets
 
### Comportement par défaut
 
Avec `refreshInterval: 1h`, ESO resynchronise OpenBao toutes les heures. Si le secret change dans OpenBao, il faut attendre au plus 1h pour que le Secret Kubernetes soit mis à jour.
 
### Forcer une resynchronisation immédiate
 
```bash
kubectl annotate externalsecret authentik-secrets \
  force-sync=$(date +%s) \
  --overwrite \
  -n authentik
```
 
ESO détecte le changement de valeur de l'annotation et resynchronise immédiatement. La valeur `date +%s` (timestamp Unix) garantit que la valeur change à chaque exécution. Le cycle normal `refreshInterval` reprend ensuite — il n'est pas nécessaire de supprimer l'annotation.
 
### Redémarrage automatique des pods avec Reloader
 
Kubernetes ne redémarre pas les pods quand un Secret change. Reloader surveille les Secrets et déclenche un rolling restart automatiquement.
 
Annoter le déploiement :
 
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: authentik-server
  namespace: authentik
  annotations:
    reloader.stakater.com/auto: "true"
```
 
Flux complet avec Reloader :
 
```
bao kv put (nouveau secret)
     ↓ refreshInterval (1h max, ou force-sync immédiat)
ESO met à jour le Secret Kubernetes
     ↓ Reloader détecte le changement
Rolling restart automatique du pod
```
 
### Vérifier le statut de la synchronisation
 
```bash
# Statut de l'ExternalSecret
kubectl get externalsecret -n authentik
 
# Détail et événements
kubectl describe externalsecret authentik-secrets -n authentik
 
# Vérifier le Secret créé
kubectl get secret authentik-secrets -n authentik -o yaml
```