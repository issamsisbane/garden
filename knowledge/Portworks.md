---
foam_template:
  filepath: "0 - INBOX/Portworks.md"
  description: "New note"
created: "2026-04-07"
---

# Portworks

Container Data Managment Platform and CSI Driver for Kubernetes.

https://portworx.com/

Portworx est une solution de stockage défini par logiciel (Software-Defined Storage) conçue spécifiquement pour les charges de travail conteneurisées. Son rôle principal : fournir des volumes persistants, hautement disponibles et résilients aux applications tournant dans Kubernetes — là où le stockage natif fait défaut.

Il faut apparement désactiver le secure-boot pour que l'installation fonctionne.

## Why Portworks ?

Kubernetes gère très bien les charges stateless, mais les applications stateful (bases de données, queues, etc.) ont besoin de persistance. 

Par défaut, si un pod migre vers un autre nœud, ses données ne suivent pas. Portworx résout ça en créant une couche de stockage distribuée qui s'étend sur tous les nœuds du cluster.


## Architecture

![[1775553830948.png]]

Portworks fonctionne en cluster avec un quorum.

Concrètement, chaque nœud du cluster Kubernetes fait tourner un PX Agent (un DaemonSet). Cet agent prend le contrôle des disques locaux du nœud (SSD, HDD, NVMe) et les agrège dans un pool de stockage unifié. 

Tous les agents communiquent entre eux via un protocole gossip pour se maintenir à jour sur l'état du cluster, et les métadonnées sont stockées dans etcd.

## The need for portworks

Là où un PVC avec EBS ou un disque persistant GCP est lié à une zone de disponibilité et à un nœud spécifique, Portworx offre plusieurs garanties supplémentaires :

- **Hyperconvergence et hyperlocal** : le PX Agent essaie toujours de scheduler les I/O sur les données locales du nœud (le replica local), ce qui évite les latences réseau. C'est ce qu'ils appellent le hyper-convergence — le compute et le stockage sont co-localisés.
- **Failover automatique** : si un nœud tombe, Kubernetes reschedule le pod sur un autre nœud. Portworx y a déjà une réplique du volume, donc le pod redémarre avec toutes ses données, sans intervention humaine.
- **StorageClass avec sémantique riche** : on peut définir des profils différents selon les besoins
- **Snapshots et DR** : Portworx expose aussi des CRDs pour créer des snapshots 3DSnap (cohérents pour les groupes de volumes liés), répliquer entre clusters ou faire du disaster recovery cross-datacenter.
- **Autopilot** : un composant qui surveille les métriques de consommation et étend automatiquement les volumes ou migre des données quand les disques approchent de leur capacité — sans intervention manuelle.

En résumé, là où le CSI de base gère le cycle de vie d'un volume (créer, supprimer, monter), Portworx y ajoute une couche de intelligence distribuée : réplication, failover, snapshots, chiffrement, tiering de performance — tout piloté via des objets Kubernetes natifs.

## CSI Driver

Just like [[Longhorn]] it creates storage classes with replication if needed.

Le CSI (Container Storage Interface) est la façon standard dont Kubernetes parle aux systèmes de stockage tiers depuis 2019. Portworx implémente ce standard via son driver CSI.
Voici comment ça s'enchaîne, de la demande de stockage jusqu'au pod :

![[1775553957241.png]]

Le flux concret se déroule ainsi :

1. Le développeur déclare un PVC avec une StorageClass qui pointe vers le provisioner Portworx (pxd.portworx.com). Il peut y spécifier des paramètres comme le facteur de réplication, le profil I/O ou le chiffrement.
2. Le CSI External Provisioner détecte ce nouveau PVC via le watch de l'API Server, et appelle CreateVolume() sur le CSI Controller de Portworx.
3. Le PX Cluster crée effectivement le volume distribué : il alloue de l'espace sur un ou plusieurs nœuds selon le facteur de réplication demandé, et expose le device /dev/pxd sur le nœud concerné.
4. Quand le pod est schedulé, le CSI Node Driver appelle NodeStageVolume() puis NodePublishVolume() pour monter le device dans le filesystem du pod, de façon totalement transparente.

### Storage Class

Dans la storage class on peut gérer l'encryption, le nombre de replicas.
Le nombre de replicas correspond au replicas fait sur les nodes portworks.

Avec un cluster de 3 nodes le nombre maximum de replicas est 3 (1 par node).
Parcontre plus on a de replicas, moins on a de stockage.

```yaml
kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
  name: px-db-rf2
provisioner: pxd.portworx.com
parameters:
  repl: "2"          # facteur de réplication
  io_profile: "db"   # optimisé base de données
  priority_io: "high"
  secure: "true"     # chiffrement at-rest
```

## Limitations

1024 volumes RWO par node

256 volumes RWX par node (Fada shared v4)

Cette limitation est par node worker portworks.

Donc on a 3*1024 et 3*256.

Ces limites permettent de garantir le bon fonctionnement des pods portworks du DaemonSets qui doivent gérer beaucoup de communications.

## Encryption

Le chiffrement de volume est possible via portworks en utilisant des clés stocké dans un vault.

Pour activer le chiffrement il faut modifier l'opérateur storage cluster.

https://docs.portworx.com/portworx-enterprise/platform/secure/key-management

Il existe 2 méthodes de chiffrement de volumes :

- cluster wide : même clef pour tous les volumes > moins secure mais plus simple à gérer
- per volume: une clef par volume > très securisée 

Pour le stockage des clés, il existe plusieurs solutions :
- Vault
- k8s natif, mais cela reste la méthode la moins sécurisée.
- aws kms, gcp kms etc. (nécessitant un accès internet).

Une fois tout configurer, on peut mettre directement dans la storage class si on veut activer l'encryption ou non.

```yaml
secure: true
```