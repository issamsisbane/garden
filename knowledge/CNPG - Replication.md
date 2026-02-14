Avec CNPG il est possible de mettre en place de la replication entre 2 clusters.


[Replica clusters - CloudNativePG v1.25](https://cloudnative-pg.io/documentation/1.25/replica_cluster/)
# Fonctionnement

![[Pasted image 20250827141229.png]]

# Replication Options

**1. Réplication en continu (Streaming Replication)**
- Principe : Synchronisation en temps réel entre le cluster source et le réplica.
- Configuration : 
	- Nécessite une connexion réseau stable entre les clusters.
	- Mise en place de mesures administratives et de sécurité pour garantir un transfert fluide des données.

**2. Archivage des WAL (Write-Ahead Logging)**
- Principe : Utilisation des fichiers WAL stockés dans un objet store (ex : S3, GCS).
- Fonctionnement : 
	- Les fichiers WAL sont transférés régulièrement depuis le cluster source vers l'objet store.
	- Le réplica les récupère via l'outil barman-cloud-wal-restore.

**3. Approche hybride**
- Principe : Combinaison des deux méthodes précédentes.
- Avantages : 
- PostgreSQL bascule automatiquement entre la réplication en continu et l'archivage des WAL selon les besoins.
- Garantit une disponibilité et cohérence optimales des données.
# Exemple

[CloudNativePG Replica Cluster using Kind | by Nabil Abdi | Medium](https://medium.com/@nabil.abdi/cloudnativepg-replica-cluster-using-kind-9353f9569f67)

Cluster Primaire composé de :
- 3 pods replicas pour le HA
- 1 base de données app

Cluster Replica similaire au cluster primaire composé de :
- 3 pods replicas pour le HA
- 1 base de données app

Dans cet exemple la replication est faite via streaming replication. Un flux doit donc être ouvert entre les deux cluster.

Toutes les modifications faites depuis le cluster primaire sont répliqués vers le cluster replica.

> [!NOTE] Source
> La replication peut se faire depuis un leader mais aussi depuis un standby.

![[Pasted image 20250827140730.png]]

## Manifests

`primary-cluster.yaml`
```
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: primary
  namespace: cnpg-replication-primary
spec:
  imageName: ghcr.io/cloudnative-pg/postgresql:17.4
  instances: 3
  storage:
    size: 1Gi
```

`replica-cluster.yaml`
```
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: replica
  namespace: cnpg-replication-replica
spec:
  instances: 3
  imageName: ghcr.io/cloudnative-pg/postgresql:17.4

  bootstrap:
    pg_basebackup:
      source: primary
  replica:
      source: primary
      enabled: true

  storage:
    size: 1Gi

  externalClusters:
  - name: primary
    connectionParameters:
      host: primary-rw.cnpg-replication-primary.svc.cluster.local
      user: streaming_replica
      sslmode: verify-full
    sslKey:
      name: primary-replication
      key: tls.key
    sslCert:
      name: primary-replication
      key: tls.crt
    sslRootCert:
      name: primary-ca
      key: ca.crt
```

`export-tls.sh`
```
#!/bin/bash

namespace=cnpg-replication-primary

oc get secret primary-replication -n $namespace -o jsonpath='{.data.tls\.crt}' | base64 -d > tls.crt

oc get secret primary-replication -n $namespace -o jsonpath='{.data.tls\.key}' | base64 -d > tls.key

oc get secret primary-ca -n $namespace -o jsonpath='{.data.ca\.crt}' | base64 -d > ca.crt
```

`setup-replica.sh`
```
#!/bin/bash

namespace=cnpg-replication-replica

kubectl create namespace $namespace
kubectl create secret -n $namespace tls primary-replication --cert=tls.crt --key=tls.key
kubectl create secret -n $namespace generic primary-ca --from-file=ca.crt=ca.crt
```