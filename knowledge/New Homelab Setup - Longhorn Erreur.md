---
creation date: 2026-03-29-23:33:32
modification date: 2026-03-29-23:33:32
imageNameKey: New_Homelab_Setup_-_Longhorn_Erreur
---
Cette Issue m'a bien aidé  :


J'ai decidé de mettre 1 replicas par defaut pour la storage class par défaut de longhorn.
Et ça m'a porté préjudice ;)

J'avais des pods qui ne montait plus après avoir été pété.

![[New_Homelab_Setup_-_Longhorn_Erreur-1.png]]

![[New_Homelab_Setup_-_Longhorn_Erreur-2.png]]

![[New_Homelab_Setup_-_Longhorn_Erreur-3.png]]

# Rapport d'investigation : Volume Longhorn non montable sur Kubernetes

**Environnement :** Homelab Kubernetes 3 nœuds (`ih-node-1`, `ih-node-2`, `ih-node-3`)  
**Stockage :** Longhorn v1.11.0 avec StorageClass à 1 replica  
**Application concernée :** Alertmanager (StatefulSet, namespace `observability`)  
**Date :** 31 mars 2026

---

## 1. Contexte et symptômes initiaux

Le pod `alertmanager-kube-prometheus-stack-alertmanager-0` était bloqué en état `Pending` depuis plus de 46 heures. L'erreur suivante apparaissait en boucle dans les events du pod :

```
Warning  FailedMount  5m18s (x1385 over 46h)  kubelet
MountVolume.MountDevice failed for volume "pvc-ce0eb9f4-cb7d-4e05-bf4f-363d5eecfab9"
: rpc error: code = Internal desc = mount failed: exit status 32

Mounting command: mount
Mounting arguments: -t ext4 -o defaults
  /dev/longhorn/pvc-ce0eb9f4-cb7d-4e05-bf4f-363d5eecfab9
  /var/lib/kubelet/plugins/kubernetes.io/csi/driver.longhorn.io/
  f83eeba2f92b55d9bfdcd08de80051c1dc8fb3e4fba703e05aa070719449bbef/globalmount

Output: mount: [...]/globalmount:
  /dev/longhorn/pvc-ce0eb9f4-cb7d-4e05-bf4f-363d5eecfab9
  already mounted or mount point busy.
```

Le PVC était bien en état `Bound`, ce qui a rendu le diagnostic initial difficile.

---

## 2. Comprendre le fonctionnement du stockage Kubernetes + Longhorn

Avant d'investiguer, voici comment fonctionne le cycle de vie d'un volume dans cet environnement.

### 2.1 Le PVC : la demande de stockage

Un **PVC (PersistentVolumeClaim)** est une demande de stockage. Kubernetes y répond en créant un **PV (PersistentVolume)** provisionné par Longhorn. À ce stade, le PVC est `Bound` : le disque est alloué mais personne n'y accède encore.

### 2.2 L'Attach : le volume voyage vers le nœud

Quand un pod est schedulé sur un nœud, Kubernetes demande à Longhorn d'**attacher** le volume à ce nœud. Longhorn expose alors le volume comme un block device :

```
/dev/longhorn/pvc-ce0eb9f4-cb7d-4e05-bf4f-363d5eecfab9
```

### 2.3 Le Mount : le pod accède au volume

Une fois le device disponible, kubelet effectue deux opérations :

1. **GlobalMount** : monter le device dans un répertoire intermédiaire géré par le driver CSI
2. **BindMount** : exposer ce répertoire dans le container à son chemin de montage (`/data`, etc.)

### 2.4 Le rôle d'iSCSI

**iSCSI** est un protocole qui permet d'accéder à un disque à distance via le réseau, comme s'il était branché localement.

```
Disque classique (USB)        Disque iSCSI (Longhorn)
──────────────────────        ──────────────────────
Branché physiquement          Branché sur ih-node-1
sur ih-node-2                 Accessible via réseau TCP
Visible comme /dev/sda        Visible comme /dev/sdi
                              sur ih-node-2
```

Longhorn utilise iSCSI pour permettre à un pod sur `ih-node-2` d'accéder à des données physiquement stockées sur `ih-node-1`. Le pod ne sait pas que les données sont ailleurs.

### 2.5 Comportement avec 1 seul replica

Avec 1 replica, les données sont stockées physiquement sur **un seul nœud**. Elles ne se déplacent pas quand le pod change de nœud. C'est l'**accès** au volume qui voyage via iSCSI.

```
ih-node-1                    ih-node-2
─────────────────            ─────────────────
Données sur disque  ←──────  Pod accède au volume
(replica physique)  iSCSI    (device /dev/sdi créé localement)
```

---

## 3. Chronologie de l'investigation

### 3.1 Vérification de l'état du volume Longhorn

```bash
kubectl get volume pvc-ce0eb9f4-cb7d-4e05-bf4f-363d5eecfab9 -n longhorn-system -o yaml | grep -E "state|nodeID|robustness"
```

Résultat :

```yaml
nodeID: ih-node-2
state: ""
robustness: healthy
state: attached
```

Le volume était bien attaché sur `ih-node-2`, le même nœud que le pod. Pas de problème apparent côté Longhorn.

### 3.2 Recherche d'un mount fantôme

```bash
# Pas de mount actif trouvé
mount | grep pvc-ce0eb9f4-cb7d-4e05-bf4f-363d5eecfab9
# (aucun résultat)

# Mais le device block existe bien
ls -la /dev/longhorn/pvc-ce0eb9f4-cb7d-4e05-bf4f-363d5eecfab9
brw-rw---- 1 root disk 8, 128 mars 31 20:26 /dev/longhorn/pvc-ce0eb9f4-cb7d-4e05-bf4f-363d5eecfab9
```

### 3.3 Consultation de dmesg

```bash
sudo dmesg | grep -E "pvc-ce0eb9f4|longhorn|ext4" | tail -30
```

Résultat révélateur :

```
[2175311.385473] /dev/longhorn/pvc-ce0eb9f4-cb7d-4e05-bf4f-363d5eecfab9: Can't open blockdev
```

Le kernel signale qu'il ne peut pas ouvrir le block device, malgré sa présence dans `/dev/longhorn/`.

### 3.4 Vérification de la session iSCSI

```bash
sudo iscsiadm -m session -P 3 | grep -A 10 "pvc-ce0eb9f4"
```

Résultat :

```
Target: iqn.2019-10.io.longhorn:pvc-ce0eb9f4-cb7d-4e05-bf4f-363d5eecfab9 (non-flash)
    Current Portal: 10.233.67.222:3260,1
    Persistent Portal: 10.233.67.222:3260,1
    Iface IPaddress: 192.168.1.16
```

La session iSCSI existe et pointe vers l'instance manager Longhorn.

### 3.5 Test de lecture du device

```bash
sudo dd if=/dev/longhorn/pvc-ce0eb9f4-cb7d-4e05-bf4f-363d5eecfab9 of=/dev/null bs=512 count=10
```

Résultat :

```
10+0 records in
10+0 records out
5120 bytes (5,1 kB, 5,0 KiB) copied, 7,9929e-05 s, 64,1 MB/s
```

Le device lit parfaitement. Le problème n'est donc pas dans la connexion réseau ni dans les données.

### 3.6 Suppression et recréation du PVC

Face au blocage persistant, le PVC a été supprimé et recréé (les données Alertmanager n'étant pas critiques) :

```bash
kubectl scale statefulset alertmanager-kube-prometheus-stack-alertmanager -n observability --replicas=0
kubectl delete pvc alertmanager-kube-prometheus-stack-alertmanager-db-alertmanager-kube-prometheus-stack-alertmanager-0 -n observability
kubectl scale statefulset alertmanager-kube-prometheus-stack-alertmanager -n observability --replicas=1
```

Le même problème est réapparu immédiatement sur le nouveau volume `pvc-e68afc5c`, avec une erreur différente cette fois :

```
Warning  FailedMount  kubelet
MountVolume.MountDevice failed for volume "pvc-e68afc5c-6f3e-4361-93d4-23fcde8ded38"
: format of disk "/dev/longhorn/pvc-e68afc5c-6f3e-4361-93d4-23fcde8ded38" failed:

Output: /dev/longhorn/pvc-e68afc5c-6f3e-4361-93d4-23fcde8ded38
  is apparently in use by the system; will not make a filesystem here!
```

Le même comportement sur un volume tout neuf confirme qu'il ne s'agit pas d'un problème sur ce volume spécifique.

### 3.7 Identification du coupable : multipathd

En consultant le statut de multipathd :

```bash
systemctl status multipathd
```

Les logs ont révélé l'événement clé, horodaté exactement au moment de l'attach Longhorn :

```
mars 31 21:06:01 ih-node-2 multipathd[3654310]: mpathb: addmap [0 2097152 multipath 0 0 1 1 service-time 0 1 1 8:128 1]
mars 31 21:06:01 ih-node-2 multipathd[3654310]: sdi [8:128]: path added to devmap mpathb
```

La corrélation entre le major:minor `8:128` du device Longhorn et celui intercepté par multipath :

```bash
ls -la /dev/longhorn/pvc-e68afc5c-6f3e-4361-93d4-23fcde8ded38
brw-rw---- 1 root disk 8, 128 mars 31 21:20 /dev/longhorn/pvc-e68afc5c-6f3e-4361-93d4-23fcde8ded38

ls -la /dev/sd* | grep "8, 128"
brw-rw---- 1 root disk 8, 128 mars 31 21:20 /dev/sdi
```

**`multipathd` interceptait `/dev/sdi` (= le device iSCSI Longhorn) et le gérait dans son propre device mapper `mpathb`, rendant le device original inaccessible à kubelet.**

---

## 4. Explication du problème

### 4.1 C'est quoi multipathd ?

**Multipath** est un service Linux qui gère la redondance des chemins d'accès aux disques. Dans les environnements avec du stockage SAN professionnel, un même disque peut être accessible via plusieurs chemins réseau. Multipathd les agrège en un seul device virtuel pour la haute disponibilité.

### 4.2 Pourquoi il a causé ce problème

Longhorn crée ses volumes via iSCSI. Multipathd surveille tous les nouveaux disques iSCSI qui apparaissent sur le nœud. Dès qu'un volume Longhorn est attaché, multipathd le détecte et l'enveloppe dans son propre device mapper (`/dev/dm-1`), pensant qu'il s'agit d'un disque SAN à gérer.

```
Longhorn crée le device iSCSI → /dev/sdi (major:minor 8:128)
           ↓
multipathd l'intercepte → l'enveloppe dans mpathb (/dev/dm-1)
           ↓
kubelet essaie de monter /dev/longhorn/pvc-xxx (= /dev/sdi)
           ↓
Kernel : "device already in use by device mapper" → ERREUR
```

### 4.3 Pourquoi ça n'arrivait pas avant

Tant que le pod tournait sur le **même nœud** que son replica Longhorn, l'accès était local — pas besoin d'iSCSI réseau, et multipathd n'interceptait pas le device.

Le jour où Kubernetes a schedulé le pod sur un **nœud différent** de son replica, Longhorn a dû créer une connexion iSCSI réseau pour la première fois. C'est ce nouveau type de device que multipathd a intercepté.

---

## 5. Résolution

La solution est de blacklister les devices iSCSI Longhorn dans la configuration de multipathd, sur **tous les nœuds** du cluster.

### 5.1 Éditer `/etc/multipath.conf`

```bash
sudo nano /etc/multipath.conf
```

Ajouter ou compléter avec :

```
blacklist {
    devnode "^sd[a-z]$"
}

blacklist_exceptions {
    property "(SCSI_IDENT_|ID_WWN)"
}
```

### 5.2 Redémarrer multipathd

```bash
sudo systemctl restart multipathd
```

### 5.3 Vérifier que le volume se monte correctement

Après un detach/reattach depuis l'UI Longhorn ou un redémarrage du pod :

```bash
kubectl get pod alertmanager-kube-prometheus-stack-alertmanager-0 -n observability -w
```

Le pod passe par `ContainerCreating` puis `Running`.

---

## 6. Actions préventives recommandées

|Action|Raison|
|---|---|
|Appliquer la config multipath sur tous les nœuds|Le problème se reproduira sur `ih-node-1` et les autres au prochain changement de nœud|
|Passer à 2 replicas pour les volumes critiques|Évite les migrations iSCSI réseau, améliore la résilience|
|Activer `Replica Auto-Balance` dans Longhorn|Aide Longhorn à co-localiser les replicas avec leurs pods|

---

## 7. Résumé

Le pod Alertmanager était bloqué car le service `multipathd`, actif sur les nœuds du cluster, interceptait automatiquement les block devices iSCSI créés par Longhorn au moment de l'attach. Ce comportement est normal pour multipathd dans un contexte SAN, mais inadapté aux volumes Longhorn. Le problème n'est apparu qu'au moment où le pod a changé de nœud, forçant Longhorn à utiliser iSCSI réseau pour la première fois sur ce volume. La solution est de blacklister ces devices dans la configuration multipath.