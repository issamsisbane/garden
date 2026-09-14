---
title: "Homelab - 3 - Déploiement de Kubernetes avec Kubespray"
description: "Comment j'ai utilisé Kubespray pour déployer un cluster Kubernetes de niveau production sur trois nœuds bare-metal, et le crash d'etcd qui m'a appris le quorum."
lang: "fr"
pubDate: "Sept 21 2025"
heroImage: "/portfolio/blog/homelab-3/homelab-3.png"
badge: "Homelab"
tags: ["Kubernetes", "Auto-hébergement", "DevOps"]
---

*Avec les trois nœuds provisionnés (voir partie 2), il était temps d'installer Kubernetes. Ayant déjà réalisé une installation plus simple de K3s dans mon précédent homelab, je voulais quelque chose de plus proche de la façon dont les vrais clusters sont construits — quelque chose qui m'apprendrait les rouages réels plutôt que de les cacher derrière un binaire unique.*

*K3s est fantastique pour mettre un cluster en marche en quelques minutes. Mais il regroupe tellement de choses — etcd embarqué, un load balancer intégré, Traefik pré-installé — que l'on peut l'utiliser pendant des mois sans comprendre ce qui se passe réellement en dessous. Cette fois, je voulais ressentir chaque composant : etcd, le serveur API, le scheduler, le controller manager, le CNI. Tout explicitement, tout à moi pour le casser.*

*Cette partie couvre l'installation complète de Kubespray : la configuration Ansible, les choix de configuration que j'ai faits, le câblage du CNI Calico, et — honnêtement la partie la plus instructive — le crash d'etcd qui a fait tomber le controller manager et le scheduler quelques semaines plus tard, et ce qu'il a fallu pour le réparer.*

---

1 - [Pourquoi Kubespray](#1---pourquoi-kubespray)
2 - **Configuration de l'environnement Ansible** <br/>
3 - **Topologie du cluster et configuration de Kubespray** <br/>
4 - **Calico CNI : VXLAN sur BGP** <br/>
5 - **Exécution du playbook** <br/>
6 - **Remplacement d'ArgoCD par une nouvelle installation Helm** <br/>
7 - **Le crash d'etcd** <br/>
8 - **Correction du problème de quorum** <br/>
9 - **Playbooks opérationnels** <br/>
10 - **Installation de Tailscale** <br/>

---

## 1 - Pourquoi Kubespray

Les trois principales voies pour un cluster Kubernetes auto-géré sont kubeadm directement, K3s, ou Kubespray. J'ai écarté K3s pour les raisons évoquées ci-dessus. Entre kubeadm brut et Kubespray, le choix était simple.

Kubespray est essentiellement un wrapper Ansible curaté autour de kubeadm. Il gère toutes les étapes que vous exécuteriez autrement manuellement : installation des dépendances du runtime de conteneur, génération des certificats, bootstrap du plan de contrôle, ajout des nœuds workers, installation d'un CNI, et configuration des add-ons. Chaque étape est codifiée et répétable.

L'avantage clé pour un homelab est que le cycle de vie complet du cluster — installation, mise à niveau, ajout d'un nœud, suppression — reste au sein d'un seul projet Ansible. Si je dois reconstruire à partir de zéro parce qu'un nœud meurt ou que je veux essayer une nouvelle version de Kubernetes, j'exécute une seule commande. Pas de post-it, pas de "je crois que j'ai fait ça manuellement la dernière fois".

J'ai épinglé Kubespray à la version **v2.30.0**. L'épinglage est important : les mises à niveau de Kubespray peuvent entraîner des changements majeurs dans les noms de variables et les valeurs par défaut, et je veux que les mises à niveau du cluster soient une décision délibérée, pas quelque chose qui se produit silencieusement lors du prochain `git pull`.

## 2 - Configuration de l'environnement Ansible

Ansible a la réputation d'être agaçant à configurer de manière cohérente sur différentes machines — conflits de version Python, dérive des versions de collections, le lot habituel. J'ai résolu ce problème une fois pour toutes en plaçant l'environnement Ansible complet dans un devcontainer.

Le dossier `.devcontainer/` dans le dossier ansible me fournit un conteneur Ubuntu 24.04 avec Ansible, ansible-lint et les collections requises pré-installées. J'ouvre le dossier `ansible/` dans VS Code, je sélectionne "Reopen in Container", et j'ai un environnement propre et reproductible, indépendamment de ce qui est installé ou non sur la machine hôte.

Avant d'exécuter quoi que ce soit, installez les dépendances de la collection Kubespray :

```bash
ansible-galaxy install -r requirements.yml
```

Cela télécharge les rôles Kubespray et toutes les collections communautaires dont ils dépendent. Une fois cela fait, l'environnement est prêt.

## 3 - Topologie du cluster et configuration de Kubespray

### Topologie

Mon cluster est composé de 1 plan de contrôle + 2 workers :

| Nœud     | Plan de contrôle | etcd | Worker |
|----------|:----------------:|:----:|:------:|
| ih-node-1 |        ✓         |  ✓   |   ✓    |
| ih-node-2 |                  |      |   ✓    |
| ih-node-3 |                  |      |   ✓    |

**Pas de plan de contrôle HA.** Dans un homelab à trois nœuds, faire de deux nœuds des plans de contrôle signifierait un seul nœud worker, ce qui n'est pas un bon compromis. Si `ih-node-1` est complètement perdu, je reconstruis à partir de zéro — la stratégie de sauvegarde etcd (abordée ci-dessous) gère la reprise après sinistre, pas un deuxième plan de contrôle.

C'est le même raisonnement que j'ai appliqué à etcd. Un cluster etcd à 3 nœuds nécessite un quorum de 2. Avec un seul plan de contrôle, ce quorum ajoute de la latence sans ajouter de disponibilité réelle. J'ai initialement laissé la valeur par défaut, ce qui s'est avéré être une erreur que j'ai payée plus tard.

### Utilisateur SSH

Kubespray se connecte aux nœuds en tant que `kuadm`. C'est l'utilisateur de provisionnement configuré dans la partie 2. L'inventaire utilise `ansible_user: kuadm` avec sudo sans mot de passe.

### CIDRs réseau

```
Service CIDR: 10.233.0.0/18
Pod CIDR:     10.233.64.0/18  (/24 par nœud)
```

Ce sont les valeurs par défaut de Kubespray et elles sont bien choisies : elles ne chevauchent pas les plages typiques des réseaux domestiques (192.168.x.x), et le `/18` offre une marge de manœuvre considérable. L'allocation `/24` par nœud signifie que chaque nœud dispose de 254 adresses de pod utilisables, ce qui est plus que suffisant pour un homelab.

### Autres choix de configuration

**iptables plutôt que IPVS.** J'ai choisi iptables pour `kube-proxy`. IPVS offre de meilleures performances à grande échelle mais nécessite des modules noyau supplémentaires et rend le débogage plus difficile. Pour un homelab, iptables convient et est mieux compris.

**Add-ons.** J'ai activé `metrics-server` et `argocd` dans la configuration des add-ons de Kubespray. La version d'ArgoCD installée par Kubespray s'est avérée obsolète — je l'ai remplacée après l'exécution initiale, abordée dans la section 6.

## 4 - Calico CNI : VXLAN sur BGP

Kubespray prend en charge plusieurs plugins CNI. J'ai choisi Calico.

La réponse honnête pour expliquer pourquoi Calico plutôt que Flannel est les fonctionnalités. Flannel fait du réseau overlay VXLAN, point final. Calico fait du VXLAN, du routage BGP, des politiques réseau avec des sémantiques d'ordre correctes, des hooks d'observabilité, et la protection des nœuds. Même si je n'utilise qu'une partie de cela aujourd'hui, je veux l'option.

### Pourquoi pas BGP

Le mode préféré de Calico à la maison serait le BGP pur — pas d'overlay, les paquets routés directement entre les nœuds comme si le cluster était un véritable centre de données. BGP élimine la surcharge d'encapsulation VXLAN et rend les captures de paquets beaucoup plus faciles à lire.

Le problème est que BGP nécessite que le routeur participe au protocole de routage, ce qui signifie qu'il doit comprendre et redistribuer les routes BGP. Mon routeur domestique fourni par mon FAI ne prend pas en charge BGP. Point final.

Je fais donc fonctionner Calico en **mode VXLAN** avec un réseau overlay. Les paquets entre les pods sur différents nœuds sont encapsulés dans des trames VXLAN et envoyés sur le réseau domestique. C'est légèrement moins efficace, mais cela fonctionne avec n'importe quel routeur et ne nécessite aucune configuration réseau spéciale.

VXLAN est maintenant le mode par défaut dans les versions récentes de Calico spécifiquement parce que c'est le choix le plus compatible. C'est la bonne décision pour la maison et de nombreux environnements cloud.

### Politiques réseau

L'une des principales raisons de choisir Calico plutôt qu'un CNI plus simple est le modèle de politique réseau. Calico étend le NetworkPolicy standard de Kubernetes avec ses propres CRD `NetworkPolicy` et `GlobalNetworkPolicy`, qui ajoutent :

- Règles `Deny` explicites (les politiques Kubernetes sont uniquement en mode allow)
- Évaluation ordonnée des règles
- Politiques au niveau du nœud
- Séparation RBAC entre les équipes d'administration de cluster et les équipes de développement

Je n'utilise pas tout cela dès le premier jour, mais le fait d'avoir ces options disponibles me permet d'isoler correctement les namespaces et d'appliquer le principe du moindre privilège réseau à mesure que j'ajoute plus de services au cluster.

## 5 - Exécution du playbook

Avec l'inventaire configuré et le devcontainer ouvert, le déploiement du cluster se fait en une seule commande :

```bash
ansible-playbook playbooks/kubespray.yml
```

Le playbook s'est exécuté pendant environ 20 minutes sur mes trois nœuds. Kubespray est complet — il vérifie les prérequis, installe le runtime de conteneur, gère les certificats, initialise etcd, démarre le serveur API, ajoute les workers, installe Calico et déploie les add-ons activés.

![[kubespray-playbookl-execution-20260301232100.png]]

Une fois le playbook terminé, j'ai récupéré le kubeconfig depuis le nœud maître :

```bash
ssh kuadm@ih-node-1 "sudo cat /etc/kubernetes/admin.conf" > ~/.kube/homelab
```

Puis j'ai vérifié le cluster :

![[homelab-verification-init-20260301232607.png]]

Les trois nœuds sont prêts. Le namespace `kube-system` contenait tout ce qui était attendu :

**Plan de contrôle (en cours d'exécution sur ih-node-1)**
- `kube-apiserver` — tout passe par lui
- `kube-controller-manager` — surveille l'état du cluster et réconcilie les différences
- `kube-scheduler` — décide sur quel nœud chaque pod sera exécuté

**Réseau — Calico**
- `calico-node` — un pod par nœud, gère le réseau inter-pods
- `calico-kube-controllers` — gère les politiques réseau

**DNS**
- `coredns` — DNS interne du cluster
- `dns-autoscaler` — ajuste le nombre de réplicas de CoreDNS sous charge
- `nodelocaldns` — cache DNS par nœud pour la performance

**Réseau de services**
- `kube-proxy` — un par nœud, gère les règles iptables pour le routage des services

**Proxy**
- `nginx-proxy` — en cours d'exécution sur ih-node-2 et ih-node-3, proxy local vers le serveur API pour que les workers puissent l'atteindre sans passer par une IP externe

**Métriques**
- `metrics-server` — collecte l'utilisation CPU et RAM par pod et par nœud, alimente `kubectl top`

## 6 - Remplacement d'ArgoCD par une nouvelle installation Helm

Kubespray a installé ArgoCD dans le cadre de l'exécution des add-ons, mais la version fournie était `v2.14.5+f463a94` — considérablement en retard par rapport à la version actuelle.

Je voulais ArgoCD v3.x. Plutôt que d'essayer une mise à niveau sur place, j'ai effacé l'installation et j'ai recommencé proprement avec Helm :

```bash
kubectl get crd | grep argoproj | awk '{print $1}' | xargs kubectl delete crd
kubectl get clusterrole | grep argocd | awk '{print $1}' | xargs kubectl delete clusterrole
kubectl get clusterrolebinding | grep argocd | awk '{print $1}' | xargs kubectl delete clusterrolebinding
```

Ensuite, j'ai supprimé le namespace et j'ai réinstallé via Helm, ce qui a récupéré le dernier chart ciblant la version **v3.3.2**.

![[argo-helm-installation-20260301234515.png]]

![[argocd-ui-latest-version-20260301234840.png]]

La raison du nettoyage complet des CRD avant la réinstallation est que les CRD d'ArgoCD évoluent entre les versions majeures. Laisser des CRD v2 obsolètes en place fait que le contrôleur v3 échoue ou produit un comportement confus car il interprète d'anciens champs de schéma.

## 7 - Le crash d'etcd

Quelques semaines après que le cluster ait été opérationnel, le `kube-controller-manager` et le `kube-scheduler` ont commencé à boucler sur les crashs. Tout ce qui dépendait du serveur API est devenu peu fiable.

Les logs du controller manager étaient immédiats :

```
E0316 23:04:52.328801       1 leaderelection.go:452] "Error retrieving lease lock" err="Get \"https://192.168.1.15:6443/apis/coordination.k8s.io/v1/namespaces/kube-system/leases/kube-controller-manager?timeout=5s\": context deadline exceeded" lock="kube-system/kube-controller-manager"
E0316 23:05:06.287650       1 leaderelection.go:488] "Failed to update lease" err="the server was unable to return a response in the time allotted, but may still be processing the request (put leases.coordination.k8s.io kube-controller-manager)" lock="kube-system/kube-controller-manager"
I0316 23:05:12.622606       1 leaderelection.go:272] "Successfully acquired lease" lock="kube-system/kube-controller-manager"
E0316 23:05:19.718364       1 leaderelection.go:445] "Failed to update lease optimistically, falling back to slow path" err="Put \"https://192.168.1.15:6443/apis/coordination.k8s.io/v1/namespaces/kube-system/leases/kube-controller-manager?timeout=5s\": context deadline exceeded" lock="kube-system/kube-controller-manager"
E0316 23:05:24.718246       1 leaderelection.go:452] "Error retrieving lease lock" err="Get \"https://192.168.1.15:6443/apis/coordination.k8s.io/v1/namespaces/kube-system/leases/kube-controller-manager?timeout=5s\": context deadline exceeded" lock="kube-system/kube-controller-manager"
I0316 23:05:24.718342       1 leaderelection.go:299] "Failed to renew lease" lock="kube-system/kube-controller-manager" err="context deadline exceeded"
E0316 23:05:24.718660       1 controllermanager.go:368] "leaderelection lost"
```

Le controller manager acquérait le bail, le perdait immédiatement car il ne pouvait pas le renouveler assez rapidement, puis plantait. Le serveur API lui-même était saturé :

```
{"level":"warn","ts":"2026-03-16T23:08:23.946036Z","logger":"etcd-client","caller":"v3@v3.6.5/retry_interceptor.go:65","msg":"retrying of unary invoker failed","target":"etcd-endpoints://0xc00088cd20/192.168.1.15:2379","method":"/etcdserverpb.KV/Range","attempt":0,"error":"rpc error: code = DeadlineExceeded desc = context deadline exceeded"}
{"level":"warn","ts":"2026-03-16T23:08:25.954079Z","logger":"etcd-client","caller":"v3@v3.6.5/retry_interceptor.go:65","msg":"retrying of unary invoker failed","target":"etcd-endpoints://0xc0001c3a40/192.168.1.15:2379","method":"/etcdserverpb.KV/Range","attempt":0,"error":"rpc error: code = DeadlineExceeded desc = context deadline exceeded"}
E0316 23:08:28.151019       1 status.go:71] "Unhandled Error" err="apiserver received an error that is not an metav1.Status: &errors.errorString{s:\"context canceled\"}: context canceled" logger="UnhandledError"
E0316 23:08:28.151158       1 writers.go:123] "Unhandled Error" err="apiserver was unable to write a JSON response: http: Handler timeout" logger="UnhandledError"
E0316 23:08:28.152777       1 status.go:71] "Unhandled Error" err="apiserver received an error that is not an metav1.Status: &errors.errorString{s:\"http: Handler timeout\"}: http: Handler timeout" logger="UnhandledError"
```

Chaque appel KV range à etcd expirait. Le serveur API laissait tomber les requêtes, les gestionnaires expiraient, et tout ce qui dépendait de l'élection de leader — controller manager, scheduler — s'effondrait.

<!-- Error: 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}} -->

### Diagnosing the root cause

I listed the etcd members to understand the cluster topology:

```bash
sudo ETCDCTL_API=3 etcdctl member list -w table \
  --endpoints=https://192.168.1.15:2379 \
  --cacert=/etc/ssl/etcd/ssl/ca.pem \
  --cert=/etc/ssl/etcd/ssl/member-ih-node-1.pem \
  --key=/etc/ssl/etcd/ssl/member-ih-node-1-key.pem
```

![[homelab-etcd-list-1.png]]

Three etcd members: ih-node-1, ih-node-2, ih-node-3. One etcd member per node — Kubespray's default when you have three nodes in the inventory.

The problem crystallised immediately. I have **one control plane node** and **three etcd members**. Etcd is a distributed consensus system: a 3-member cluster requires 2 members to be available to reach quorum. But the API server only runs on ih-node-1. The two worker nodes are running etcd processes that don't serve the control plane in any meaningful way — they just participate in elections and replication, adding round-trip latency to every write the API server makes.

Kubespray installed etcd as a **systemd service** (not a static pod), one per node, all three replicating. That's perfectly fine for a genuine HA setup with multiple API servers. But with one control plane, it means every etcd write from `kube-apiserver` has to round-trip across the home WiFi to reach quorum on two out of three members. Occasionally that WiFi hiccup is long enough to exceed the API server's deadlines, the controller manager loses its lease, and the crash-loop begins.

The fix was clear: reduce the etcd cluster to a single node on ih-node-1. No quorum round-trips, no WiFi sensitivity, and it matches the actual architecture — one control plane, one etcd.

## 8 - Fixing the quorum problem

The procedure had to be careful. Removing members from a live etcd cluster while the API server is misbehaving required doing it in the right order.

### Step 1: Backup etcd

Before touching anything:

```bash
ETCDCTL_API=3 etcdctl snapshot save /root/etcd-backup-$(date +%Y%m%d).db \
  --endpoints=https://192.168.1.15:2379 \
  --cacert=/etc/ssl/etcd/ssl/ca.pem \
  --cert=/etc/ssl/etcd/ssl/member-ih-node-1.pem \
  --key=/etc/ssl/etcd/ssl/member-ih-node-1-key.pem
```

Verified the backup was consistent:

```bash
sudo etcdutl snapshot status etcd-backup-20260317.db -w table
```

### Step 2: Remove the two worker etcd members

```bash

# Remove ih-node-2 etcd member
ETCDCTL_API=3 etcdctl member remove 5306eee70c5d385c \
  --endpoints=https://192.168.1.15:2379 \
  --cacert=/etc/ssl/etcd/ssl/ca.pem \
  --cert=/etc/ssl/etcd/ssl/member-ih-node-1.pem \
  --key=/etc/ssl/etcd/ssl/member-ih-node-1-key.pem

# Remove ih-node-3 etcd member
ETCDCTL_API=3 etcdctl member remove 7a2118b371513eef \
  --endpoints=https://192.168.1.15:2379 \
  --cacert=/etc/ssl/etcd/ssl/ca.pem \
  --cert=/etc/ssl/etcd/ssl/member-ih-node-1.pem \
  --key=/etc/ssl/etcd/ssl/member-ih-node-1-key.pem
```

![[homelab-etcd-list-2.png]]

One member remaining: ih-node-1.

### Step 3: Restore from backup

With the member list reduced to a single node, I needed etcd to restart cleanly in single-node mode. Kubespray's systemd unit still had the old 3-member `--initial-cluster` configuration in it, which caused etcd to restart and immediately look for the two removed peers.

I restored from the snapshot using `etcdutl` (note: `etcdutl` is the standalone restore tool — it does not require etcd to be running):

```bash
etcdutl snapshot restore etcd-backup-20260317.db \
  --data-dir /var/lib/etcd-restored \
  --name ih-node-1 \
  --initial-cluster ih-node-1=https://192.168.1.15:2380 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-advertise-peer-urls https://192.168.1.15:2380
```

The restore creates a clean WAL with a fresh cluster ID and a single member, so etcd starts without needing to peer with anyone.

### Step 4: Update the systemd unit

The critical flags to add when restarting with the restored data directory:

```
--initial-cluster-state=existing
--force-init-cluster
```

These tell etcd that this is an existing cluster being recovered, not a new bootstrap, and to force single-node initialization from the restored state.

### Step 5: Verify

The scheduler and controller manager came back up cleanly. No more lease timeouts, no more crash-loops. The API server was responsive again.

![[homelab-list-pods-kube-system-etcd.png]]

### What this taught me

The real lesson here is about the gap between Kubespray's defaults and what actually makes sense for a given topology. Kubespray is designed to handle full HA deployments, and its defaults reflect that. When you give it three nodes, it puts etcd on all three. That's correct for a 3-control-plane cluster — it's actively harmful for a 1-control-plane cluster because it introduces quorum latency without any redundancy benefit.

The design note I added to the README after this incident:

> **Single control plane node** — a 3-node homelab does not need HA control plane. Adding a second control plane would consume a node that is more useful as a worker, and the cluster can be redeployed from scratch if `ih-node-1` is lost. Same for etcd. The homelab doesn't need HA so I stick to backup the etcd database and restore if any disaster.

For a homelab: back up etcd regularly, keep the backup off-node, and know how to restore it. That is a more practical resilience strategy than a 3-node etcd cluster running on WiFi.

## 9 - Operational playbooks

Beyond the main Kubespray deployment, I have three operational playbooks for day-to-day cluster management.

### up.yml — verify nodes are reachable

```bash
ansible-playbook playbooks/up.yml
```

A quick connectivity check before doing anything else. It pings all nodes and verifies SSH access. I run this whenever I haven't touched the homelab in a few days and want to confirm everything is still up before running a longer playbook.

### inventory_cluster.yml — resource report

```bash
ansible-playbook playbooks/inventory_cluster.yml
```

Reports CPU, memory, and disk capacity per node. I use this to get a current picture of what resources I have before deploying something new, and to catch drift if one of the laptops has been quietly consuming more disk than expected.

### shutdown.yml — graceful shutdown

```bash
ansible-playbook playbooks/shutdown.yml
```

I'm actively working on the homelab most evenings, but there's no reason to leave three laptops running at idle overnight when nothing is using the cluster. This playbook gracefully shuts down all nodes. The next morning, I power them back on and run `up.yml` to confirm they came back cleanly.

This matters more than it might seem: graceful shutdown ensures etcd flushes its WAL to disk properly. Sudden power cuts can corrupt the etcd data directory, which is a much less fun recovery scenario than the intentional backup-and-restore I walked through above.

## 10 - Installing Tailscale

The last piece was making the cluster accessible from outside the home network without opening ports on the router.

Tailscale is a WireGuard-based mesh VPN. Each device that joins the Tailnet gets a stable `100.x.x.x` IP address that works regardless of which network the device is on. With Tailscale installed on all three nodes, I can SSH into any of them from anywhere, and `kubectl` works from my laptop regardless of where I am.

Tailscale installation is handled as a separate Ansible playbook, intentionally not mixed into the Kubespray deployment:

```bash
ansible-playbook playbooks/tailscale.yml --ask-vault-pass
```

The auth key is stored in `vars/tailscale.yml` as an Ansible Vault-encrypted file. The playbook prompts for the vault password at runtime, decrypts the key, and uses it to authenticate each node into the Tailnet. Keeping the encrypted secret committed to the repo means the playbook is fully self-contained — no external secret store needed for something this simple.

The Tailscale playbook can be re-run independently to rotate the auth key without touching the cluster configuration. That separation of concerns — cluster provisioning in one playbook, VPN in another — makes maintenance much cleaner.

## Conclusion

Kubespray delivered exactly what I wanted: a production-grade Kubernetes cluster where I can see and understand every component, without having to wire together every kubeadm command by hand. The 20-minute playbook run was a little anticlimactic after all the configuration work, but that is the point — the complexity is in the Ansible, not in typing commands on nodes.

The etcd crash was the best learning moment of the whole setup. It forced me to actually understand what etcd is doing, how quorum works, how to use `etcdctl` and `etcdutl` hands-on, and how to recover from a broken state. I would have gone much longer without that understanding if everything had worked perfectly from the start.

Next up: getting workloads running on the cluster — starting with the storage layer, GitOps with ArgoCD, and the first actual applications.