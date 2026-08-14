---
foam_template:
  filepath: "0 - INBOX/CNPG - Backup.md"
  description: "New note"
created: "2025-12-04"
bloggable: true
---

# CNPG - Backup

## Table des matières

1. [Architecture générale](#architecture-générale)
2. [Les deux composantes du backup](#les-deux-composantes-du-backup)
3. [Configuration avec le plugin Barman](#configuration-avec-le-plugin-barman)
4. [ScheduledBackup et ressources Backup](#scheduledbackup-et-ressources-backup)
5. [Full Recovery vs PITR](#full-recovery-vs-pitr)
6. [La procédure de recovery](#la-procédure-de-recovery)
7. [Le piège du serverName](#le-piège-du-serverName)
8. [Intégration Helm + ArgoCD](#intégration-helm--argocd)

---

## Architecture générale

CNPG supporte les backups **online/hot** via de l'archivage continu vers un object store. La base de données reste disponible en permanence (aucun downtime), et le PITR (Point In Time Recovery) est disponible.

L'opérateur orchestre l'infrastructure de backup en s'appuyant sur les outils Barman Cloud :

- `barman-cloud-wal-archive` — archivage des WALs
- `barman-cloud-backup` — prise de base backup
- `barman-cloud-backup-list` — liste des backups disponibles
- `barman-cloud-backup-delete` — nettoyage selon la retention policy
- `barman-cloud-restore` — restoration d'un base backup
- `barman-cloud-wal-restore` — restoration des WALs

```
Cluster PostgreSQL
       │
       ├── WAL archiving continu ──────────────────────────────► Object Store
       │   (toutes les 5 min max)                                  │
       │                                                           ├── /mon-cluster/wals/
       └── Base backups (ScheduledBackup) ─────────────────────►  └── /mon-cluster/base/
```

---

## Les deux composantes du backup

### 1. WAL Archiving (continu)

Les **WAL** (Write-Ahead Logs) sont les journaux de transactions de PostgreSQL. Ils sont archivés en continu dans l'object store, par défaut toutes les 5 minutes maximum (`archive_timeout = 5min`).

C'est ce mécanisme qui permet le **PITR** : en rejouant les WALs depuis un base backup, on peut reconstruire l'état exact de la base à n'importe quel instant couvert par les archives.

### 2. Base Backups (snapshots)

Un base backup est une **copie complète du PGDATA** à un instant T (format tarball). Il n'est pas incrémental. Il sert de point de départ pour la recovery — les WALs sont ensuite rejoués depuis ce point.

```
Lundi 02h00    Mardi 02h00    Mercredi 02h00
     │               │               │
  [BASE]──WALs──[BASE]──WALs──[BASE]──WALs──► maintenant
```

Lors d'un Full Recovery, CNPG prend automatiquement le **base backup le plus récent**, puis rejoue les WALs depuis ce point.

> **Fréquence recommandée** : un base backup par semaine est généralement suffisant. Entre deux base backups, la recovery repose sur le WAL archive, ce qui est plus lent mais fonctionnel. Des backups trop fréquents génèrent de la charge et des coûts inutiles.

---

## Configuration avec le plugin Barman

Depuis CNPG 1.26, le support natif de Barman Cloud est déprécié en faveur du **plugin Barman Cloud** (`barman-cloud.cloudnative-pg.io`). C'est cette approche qui est décrite ici.

### Étape 1 — Créer le Secret avec les credentials

```bash
kubectl create secret generic aws-creds \
  --from-literal=ACCESS_KEY_ID=<ta_clé> \
  --from-literal=ACCESS_SECRET_KEY=<ta_clé_secrète>
```

### Étape 2 — Créer l'ObjectStore

L'`ObjectStore` est une CRD propre au plugin (`barmancloud.cnpg.io/v1`). Elle contient toute la configuration de connexion à l'object store, ainsi que la retention policy.

```yaml
apiVersion: barmancloud.cnpg.io/v1
kind: ObjectStore
metadata:
  name: mon-object-store
spec:
  configuration:
    destinationPath: "s3://mon-bucket/postgres/"
    # endpointURL: "http://minio:9000"  # si MinIO ou S3-compatible
    s3Credentials:
      accessKeyId:
        name: aws-creds
        key: ACCESS_KEY_ID
      secretAccessKey:
        name: aws-creds
        key: ACCESS_SECRET_KEY
    wal:
      compression: gzip
  retentionPolicy: "30d"  # avec le plugin, la retention est dans l'ObjectStore
```

> **Important** : le bucket doit exister avant de créer la ressource `Cluster`. Depuis Barman Cloud 3.16, les commandes ne créent plus automatiquement le bucket cible.

### Étape 3 — Référencer dans le Cluster

```yaml
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: mon-cluster
spec:
  instances: 3
  plugins:
    - name: barman-cloud.cloudnative-pg.io
      isWALArchiver: true       # active le WAL archiving continu
      parameters:
        barmanObjectName: mon-object-store
  storage:
    size: 10Gi
```

> **Note** : un seul plugin peut être responsable du WAL archiving à la fois.

---

## ScheduledBackup et ressources Backup

### Backup à la demande

```yaml
apiVersion: postgresql.cnpg.io/v1
kind: Backup
metadata:
  name: backup-now
spec:
  cluster:
    name: mon-cluster
  method: plugin
  pluginConfiguration:
    name: barman-cloud.cloudnative-pg.io
```

### Backup schedulé

```yaml
apiVersion: postgresql.cnpg.io/v1
kind: ScheduledBackup
metadata:
  name: backup-daily
spec:
  schedule: "0 2 * * *"    # tous les jours à 2h
  backupOwnerReference: self
  cluster:
    name: mon-cluster
  method: plugin
  pluginConfiguration: # IMPORTANT
    name: barman-cloud.cloudnative-pg.io
```

### Les ressources Backup dans Kubernetes

Chaque exécution du `ScheduledBackup` crée une ressource `Backup` dans le namespace :

```bash
kubectl get backup -n mon-namespace

NAME                          CLUSTER        STATUS      STARTED
mon-cluster-20260414020000    mon-cluster    completed   2026-04-14T02:00:00Z
mon-cluster-20260413020000    mon-cluster    completed   2026-04-13T02:00:00Z
mon-cluster-20260412020000    mon-cluster    completed   2026-04-12T02:00:00Z
```

Ces ressources sont des **pointeurs** vers les données dans l'object store. Supprimer la ressource `Backup` ne supprime pas les données dans S3/MinIO — c'est la `retentionPolicy` dans l'`ObjectStore` qui gère le nettoyage réel des fichiers.

---

## Full Recovery vs PITR

### Full Recovery — "Dernier état connu"

CNPG prend le dernier base backup disponible, puis rejoue **tous les WALs jusqu'au dernier disponible** dans l'object store.

```
Base backup         WALs archivés
    │                    │
[08h00] ──────────────► [14h32]  ← état final
```

C'est le comportement par défaut, aucun `recoveryTarget` n'est nécessaire.

**Cas d'usage** : perte totale du cluster (disque mort, namespace supprimé), ou corruption infrastructure détectée récemment.

> **Attention** : le Full Recovery ne protège pas contre une erreur humaine. Si un `DROP TABLE` a été commis et archivé dans les WALs, il sera rejoué également.

### PITR — "Revenir à un instant précis"

PostgreSQL rejoue les WALs jusqu'à un instant précis et s'arrête là. Tout ce qui s'est passé après est ignoré.

```
Base backup         WALs archivés
    │                    │
[08h00] ──────► [11h45] ✋ stop     [14h32]
                    ↑
              targetTime
              (juste avant l'incident)
```

**Cas d'usage** : erreur humaine (`DROP TABLE`, `UPDATE` sans `WHERE`), corruption logique des données.

### Comparaison

| | Full Recovery | PITR |
|---|---|---|
| Point d'arrivée | Dernier WAL disponible | Instant choisi |
| Données perdues | Rien (en théorie) | Tout après le `targetTime` |
| Cas d'usage | Crash / perte infra | Erreur humaine / corruption logique |
| Config | Aucun `recoveryTarget` | `recoveryTarget.targetTime` |

---

## La procédure de recovery

### Principe fondamental

**CNPG ne permet pas de restaurer en place sur un cluster existant.** La recovery est uniquement un mécanisme de bootstrap pour créer un nouveau cluster. Le champ `bootstrap` est ignoré par le reconciler sur un cluster déjà initialisé.

La stratégie est donc :
1. Créer un nouveau cluster avec `bootstrap.recovery`
2. Valider que le cluster est sain
3. Supprimer l'ancien cluster
4. Basculer le trafic

### Manifest de recovery (Full Recovery)

```yaml
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: mon-cluster-recovered     # nom différent de l'original
spec:
  instances: 3

  bootstrap:
    recovery:
      source: source-cluster      # référence à externalClusters

  # Continuer à backuper après recovery (vers un dossier différent)
  plugins:
    - name: barman-cloud.cloudnative-pg.io
      isWALArchiver: true
      parameters:
        barmanObjectName: mon-object-store
        # pas de serverName → utilise "mon-cluster-recovered" comme dossier d'écriture

  externalClusters:
    - name: source-cluster
      plugin:
        name: barman-cloud.cloudnative-pg.io
        parameters:
          barmanObjectName: mon-object-store
          serverName: mon-cluster  # ← dossier de LECTURE (l'ancien cluster)

  storage:
    size: 10Gi
```

### Manifest de recovery avec PITR

```yaml
  bootstrap:
    recovery:
      source: source-cluster
      recoveryTarget:
        targetTime: "2026-04-14T11:45:00Z"  # juste avant l'incident
```

### Cibler un backup précis

Au lieu du dernier backup automatique, on peut pointer une ressource `Backup` spécifique :

```yaml
  bootstrap:
    recovery:
      source: source-cluster
      backup:
        name: mon-cluster-20260413020000  # backup du jour précédent
```

Utile si le dernier backup est lui-même corrompu.

---

## Le piège du serverName

Par défaut, CNPG utilise le **nom du cluster comme nom de dossier** dans l'object store :

```
s3://mon-bucket/mon-cluster/wals/
s3://mon-bucket/mon-cluster/base/
```

Si tu crées un nouveau cluster `mon-cluster-recovered` sans préciser `serverName`, Barman cherche dans :

```
s3://mon-bucket/mon-cluster-recovered/  ← n'existe pas !
```

La solution est le paramètre `serverName` dans `externalClusters` :

```yaml
externalClusters:
  - name: source-cluster
    plugin:
      name: barman-cloud.cloudnative-pg.io
      parameters:
        barmanObjectName: mon-object-store
        serverName: mon-cluster   # ← où LIRE (dossier de l'ancien cluster)
```

### Lecture vs Écriture

| | Configuration | Dossier dans l'object store |
|---|---|---|
| **Lecture** (recovery) | `serverName` dans `externalClusters` | `mon-cluster/` |
| **Écriture** (nouveaux backups) | nom du nouveau cluster (par défaut) | `mon-cluster-recovered/` |

Les deux dossiers sont distincts — pas de risque d'écrasement des données d'origine.

> **Attention** : si tu réutilises le même `ObjectStore` pour lecture et écriture dans le même cluster sans `serverName` distinct, CNPG lève une erreur et le cluster reste bloqué en état `Setting up primary` avec `ERROR: WAL archive check failed for server: Expected empty archive`.

---

## Tests

### Rajout de la conf de backup

Si on a un cluster CNPG sans conf de backup et qu'on rajoute la conf de Backup, CNPG va recréer le pod en rajoutant le sidecar Barman et en conservant les données déjà dans la BDD.

### Création d'un cluster avec le même nom

On ne peut pas restorer un cluster avec le même nom que la source.
Les WALs ne pourront plus être archiver. Il faut donc un nouveau nom dédié pour le cluster restoré.

## Intégration Helm + ArgoCD

### Le problème

ArgoCD reconcilie en permanence l'état désiré (Git) vers l'état réel (cluster). En cas de recovery, il faut éviter qu'ArgoCD recrée le cluster original pendant l'opération.

### Stratégie recommandée : toggle dans values.yaml

```yaml
# values.yaml
postgres:
  instances: 3
  storage:
    size: 10Gi
  objectStoreName: mon-object-store

  recovery:
    enabled: false              # passer à true en cas d'incident
    sourceClusterName: mon-cluster
    targetTime: ""              # laisser vide pour Full Recovery
                                # ex: "2026-04-14T11:45:00Z" pour PITR
    specificBackup: ""          # nom d'un Backup précis si nécessaire
```

```yaml
# templates/cluster.yaml
{{- if .Values.postgres.recovery.enabled }}
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: {{ include "app.fullname" . }}-recovered
spec:
  instances: {{ .Values.postgres.instances }}
  bootstrap:
    recovery:
      source: origin
      {{- if .Values.postgres.recovery.specificBackup }}
      backup:
        name: {{ .Values.postgres.recovery.specificBackup }}
      {{- end }}
      {{- if .Values.postgres.recovery.targetTime }}
      recoveryTarget:
        targetTime: {{ .Values.postgres.recovery.targetTime | quote }}
      {{- end }}
  plugins:
    - name: barman-cloud.cloudnative-pg.io
      isWALArchiver: true
      parameters:
        barmanObjectName: {{ .Values.postgres.objectStoreName }}
  externalClusters:
    - name: origin
      plugin:
        name: barman-cloud.cloudnative-pg.io
        parameters:
          barmanObjectName: {{ .Values.postgres.objectStoreName }}
          serverName: {{ .Values.postgres.recovery.sourceClusterName }}
  storage:
    size: {{ .Values.postgres.storage.size }}
{{- else }}
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: {{ include "app.fullname" . }}
spec:
  instances: {{ .Values.postgres.instances }}
  plugins:
    - name: barman-cloud.cloudnative-pg.io
      isWALArchiver: true
      parameters:
        barmanObjectName: {{ .Values.postgres.objectStoreName }}
  storage:
    size: {{ .Values.postgres.storage.size }}
{{- end }}
```

### Workflow complet en cas d'incident

```
1. Identifier l'incident et son heure exacte
         ↓
2. Désactiver l'auto-sync ArgoCD
   → argocd app set mon-app --sync-policy none
         ↓
3. Activer le toggle recovery dans values.yaml
   → postgres.recovery.enabled: true
   → postgres.recovery.targetTime: "2026-04-14T11:45:00Z"  # si PITR
         ↓
4. Sync manuel ArgoCD → déploie le cluster recovered
   → argocd app sync mon-app
         ↓
5. Vérifier que le cluster recovered est sain
   → kubectl get cluster mon-cluster-recovered
   → kubectl get pods -l cnpg.io/cluster=mon-cluster-recovered
         ↓
6. Supprimer l'ancien cluster corrompu
   → kubectl delete cluster mon-cluster
         ↓
7. Remettre le toggle à false, renommer si nécessaire
   → postgres.recovery.enabled: false
         ↓
8. Réactiver l'auto-sync ArgoCD
   → argocd app set mon-app --sync-policy automated
```

> **Note** : modifier le champ `bootstrap` d'un cluster existant et en bonne santé n'a aucun effet. CNPG utilise ce champ uniquement lors de la création initiale du cluster (quand le PGDATA est vide). Il est donc safe de pré-préparer ton chart avec les sections `externalClusters` — elles n'impacteront pas le cluster en cours d'exécution.
