---
title: "Homelab - 3 - Déploiement de Kubernetes avec Kubespray"
description: "Comment j'ai utilisé Kubespray pour déployer un cluster Kubernetes de qualité production sur trois nœuds bare-metal, et le crash d'etcd qui m'a appris le quorum."
lang: "fr"
pubDate: "Sept 21 2025"
heroImage: "/portfolio/blog/homelab-3/homelab-3.png"
badge: "Homelab"
tags: ["Kubernetes", "Auto-hébergement", "DevOps"]
---

*Avec les trois nœuds provisionnés (voir partie 2), il était temps d'installer Kubernetes. Ayant déjà installé K3s plus simplement dans mon homelab précédent, je voulais quelque chose de plus proche de la façon dont les vrais clusters sont construits — quelque chose qui m'apprendrait les rouages internes plutôt que de les cacher derrière un seul binaire.*

*K3s est fantastique pour mettre un cluster en service en quelques minutes. Mais il regroupe tellement de choses — etcd embarqué, un load balancer intégré, Traefik pré-installé — que l'on peut l'utiliser pendant des mois sans comprendre ce qui se passe réellement en dessous. Cette fois, je voulais ressentir chaque composant : etcd, le serveur API, le scheduler, le contrôleur manager, le CNI. Tout cela explicitement, tout cela à moi de casser.*

*Cette partie couvre l'installation complète de Kubespray : la configuration Ansible, les choix de configuration que j'ai faits, la configuration du CNI Calico, et — honnêtement la partie la plus instructive — le crash d'etcd qui a fait tomber le contrôleur manager et le scheduler quelques semaines plus tard, et ce qu'il a fallu pour le réparer.*

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

Kubespray est essentiellement un wrapper Ansible curaté autour de kubeadm. Il gère toutes les étapes que vous exécuteriez autrement manuellement : installation des dépendances du runtime de conteneur, génération des certificats, bootstrap du plan de contrôle, jonction des nœuds workers, installation d'un CNI, et configuration des add-ons. Chaque étape est codifiée et répétable.

L'avantage clé pour un homelab est que le cycle de vie complet du cluster — installation, mise à niveau, ajout d'un nœud, destruction — reste dans un seul projet Ansible. Si je dois reconstruire à partir de zéro parce qu'un nœud meurt ou que je veux essayer une nouvelle version de Kubernetes, j'exécute une seule commande. Pas de post-it, pas de "je crois que j'ai fait ça manuellement la dernière fois".

J'ai épinglé Kubespray à la version **v2.30.0**. L'épinglage est important : les mises à niveau de Kubespray peuvent entraîner des changements cassants dans les noms de variables et les valeurs par défaut, et je veux que les mises à niveau du cluster soient une décision délibérée, pas quelque chose qui se produit silencieusement lors du prochain `git pull`.

## 2 - Configuration de l'environnement Ansible

Ansible a la réputation d'être agaçant à configurer de manière cohérente sur différentes machines — conflits de versions Python, dérive des versions de collections, le lot habituel. J'ai résolu ce problème une fois pour toutes en plaçant l'intégralité de l'environnement Ansible dans un devcontainer.

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

**Pas de plan de contrôle HA.** Dans un homelab à trois nœuds, faire de deux nœuds un plan de contrôle signifierait un seul nœud worker, ce qui n'est pas un bon compromis. Si `ih-node-1` est complètement perdu, je reconstruis à partir de zéro — la stratégie de sauvegarde etcd (abordée ci-dessous) gère la reprise après sinistre, pas un deuxième plan de contrôle.

C'est la même logique que j'ai appliquée à etcd. Un cluster etcd à 3 nœuds nécessite un quorum de 2. Avec un seul plan de contrôle, ce quorum ajoute de la latence sans ajouter de disponibilité réelle. J'ai initialement laissé la valeur par défaut, ce qui s'est avéré être une erreur que j'ai payée plus tard.

### Utilisateur SSH

Kubespray se connecte aux nœuds en tant que `kuadm`. C'est l'utilisateur de provisionnement configuré dans la partie 2. L'inventaire utilise `ansible_user: kuadm` avec sudo sans mot de passe.

### CIDRs réseau

```
Service CIDR: 10.233.0.0/18
Pod CIDR:     10.233.64.0/18  (/24 par nœud)
```

Ce sont les valeurs par défaut de Kubespray et elles sont bien choisies : elles ne chevauchent pas les plages typiques des réseaux domestiques (192.168.x.x), et le `/18` offre une marge de manœuvre suffisante. L'allocation `/24` par nœud signifie que chaque nœud dispose de 254 adresses de pods utilisables, ce qui est plus que suffisant pour un homelab.

### Autres choix de configuration

**iptables plutôt que IPVS.** J'ai choisi iptables pour `kube-proxy`. IPVS offre de meilleures performances à grande échelle mais nécessite des modules noyau supplémentaires et rend le débogage plus difficile. Pour un homelab, iptables convient et est mieux compris.

**Add-ons.** J'ai activé `metrics-server` et `argocd` dans la configuration des add-ons de Kubespray. La version d'ArgoCD installée par Kubespray s'est avérée obsolète — je l'ai remplacée après l'exécution initiale, abordée dans la section 6.

## 4 - Calico CNI : VXLAN sur BGP

Kubespray prend en charge plusieurs plugins CNI. J'ai choisi Calico.

La réponse honnête pour expliquer pourquoi Calico plutôt que Flannel est les fonctionnalités. Flannel fait du réseau overlay VXLAN, point final. Calico fait VXLAN, routage BGP, politiques réseau avec des sémantiques d'ordre correctes, points d'observation, et protection des nœuds. Même si je n'utilise qu'une partie de cela aujourd'hui, je veux l'option.

### Pourquoi pas BGP

Le mode préféré de Calico à la maison serait le BGP pur — pas d'overlay, les paquets routés directement entre les nœuds comme si le cluster était un véritable centre de données. BGP élimine la surcharge d'encapsulation VXLAN et rend les captures de paquets beaucoup plus faciles à lire.

Le problème est que BGP nécessite que le routeur participe au protocole de routage, ce qui signifie qu'il doit comprendre et redistribuer les routes BGP. Mon routeur domestique fourni par mon FAI ne prend pas en charge BGP. Point final.

Je fais donc fonctionner Calico en **mode VXLAN** avec un réseau overlay. Les paquets entre les pods sur différents nœuds sont encapsulés dans des trames VXLAN et envoyés sur le réseau domestique. C'est légèrement moins efficace, mais cela fonctionne avec n'importe quel routeur et ne nécessite aucune configuration réseau spéciale.

VXLAN est maintenant le mode par défaut dans les versions récentes de Calico spécifiquement parce que c'est le choix le plus compatible. C'est la bonne décision pour la maison et de nombreux environnements cloud.

### Politiques réseau

L'une des principales raisons de choisir Calico plutôt qu'un CNI plus simple est le modèle de politique réseau. Calico étend le NetworkPolicy standard de Kubernetes avec ses propres CRDs `NetworkPolicy` et `GlobalNetworkPolicy`, qui ajoutent :

- Règles `Deny` explicites (les politiques Kubernetes sont uniquement en mode allow)
- Évaluation ordonnée des règles
- Politiques au niveau du nœud
- Séparation RBAC entre les équipes d'administration du cluster et les équipes de développement

Je n'utilise pas tout cela dès le premier jour, mais le fait d'avoir ces options disponibles me permet d'isoler correctement les namespaces et d'appliquer le principe du moindre privilège réseau à mesure que j'ajoute d'autres services au cluster.

## 5 - Exécution du playbook

Avec l'inventaire configuré et le devcontainer ouvert, le déploiement du cluster se fait en une seule commande :

```bash
ansible-playbook playbooks/kubespray.yml
```

Le playbook s'est exécuté pendant environ 20 minutes sur mes trois nœuds. Kubespray est complet — il vérifie les prérequis, installe le runtime de conteneur, gère les certificats, initialise etcd, démarre le serveur API, joint les workers, installe Calico et déploie les add-ons activés.

![[kubespray-playbookl-execution-20260301232100.png]]

Une fois le playbook terminé, j'ai récupéré le kubeconfig depuis le nœud maître :

```bash
ssh kuadm@ih-node-1 "sudo cat /etc/kubernetes/admin.conf" > ~/.kube/homelab
```

Puis j'ai vérifié le cluster :

![[homelab-verification-init-20260301232607.png]]

Les trois nœuds sont prêts. Le namespace `kube-system` contenait tout ce qui était attendu :

**Plan de contrôle (exécuté sur ih-node-1)**
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
- `kube-proxy` — un par nœud, gère les règles iptables pour le routage des Services

**Proxy**
- `nginx-proxy` — exécuté sur ih-node-2 et ih-node-3, proxy local vers le serveur API pour que les workers puissent l'atteindre sans passer par une IP externe

**Métriques**
- `metrics-server` — collecte l'utilisation CPU et RAM par pod et nœud, alimente `kubectl top`

## 6 - Remplacement d'ArgoCD par une nouvelle installation Helm

Kubespray a installé ArgoCD dans le cadre de l'exécution des add-ons, mais la version fournie était `v2.14.5+f463a94` — significativement en retard par rapport à la version actuelle.

Je voulais ArgoCD v3.x. Plutôt que d'essayer une mise à niveau sur place, j'ai effacé l'installation et recommencé proprement avec Helm :

```bash
kubectl get crd | grep argoproj | awk '{print $1}' | xargs kubectl delete crd
kubectl get clusterrole | grep argocd | awk '{print $1}' | xargs kubectl delete clusterrole
kubectl get clusterrolebinding | grep argocd | awk '{print $1}' | xargs kubectl delete clusterrolebinding
```

Ensuite, j'ai supprimé le namespace et réinstallé via Helm, ce qui a récupéré le dernier chart ciblant la version **v3.3.2**.

![[argo-helm-installation-20260301234515.png]]

![[argocd-ui-latest-version-20260301234840.png]]

La raison du nettoyage complet des CRDs avant la réinstallation est que les CRDs d'ArgoCD évoluent entre les versions majeures. Laisser des CRDs v2 obsolètes en place fait que le contrôleur v3 échoue ou produit un comportement confus car il interprète d'anciens champs de schéma.

## 7 - Le crash d'etcd

Quelques semaines après que le cluster ait été opérationnel, le `kube-controller-manager` et le `kube-scheduler` ont commencé à crash-loop. Tout ce qui dépendait du serveur API est devenu instable.

Les logs du contrôleur manager étaient immédiats :

```
E0316 23:04:52.328801       1 leaderelection.go:452] "Error retrieving lease lock" err="Get \"https://192.168.1.15:6443/apis/coordination.k8s.io/v1/namespaces/kube-system/leases/kube-controller-manager?timeout=5s\": context deadline exceeded" lock="kube-system/kube-controller-manager"
E0316 23:05:06.287650       1 leaderelection.go:488] "Failed to update lease" err="the server was unable to return a response in the time allotted, but may still be processing the request (put leases.coordination.k8s.io kube-controller-manager)" lock="kube-system/kube-controller-manager"
I0316 23:05:12.622606       1 leaderelection.go:272] "Successfully acquired lease" lock="kube-system/kube-controller-manager"
E0316 23:05:19.718364       1 leaderelection.go:445] "Failed to update lease optimistically, falling back to slow path" err="Put \"https://192.168.1.15:6443/apis/coordination.k8s.io/v1/namespaces/kube-system/leases/kube-controller-manager?timeout=5s\": context deadline exceeded" lock="kube-system/kube-controller-manager"
E0316 23:05:24.718246       1 leaderelection.go:452] "Error retrieving lease lock" err="Get \"https://192.168.1.15:6443/apis/coordination.k8s.io/v1/namespaces/kube-system/leases/kube-controller-manager?timeout=5s\": context deadline exceeded" lock="kube-system/kube-controller-manager"
I0316 23:05:24.718342       1 leaderelection.go:299] "Failed to renew lease" lock="kube-system/kube-controller-manager" err="context deadline exceeded"
E0316 23:05:24.718660       1 controllermanager.go:368] "leaderelection lost"
```

Le contrôleur manager acquérait le bail, le perdait immédiatement car il ne pouvait pas le renouveler assez rapidement, puis plantait. Le serveur API lui-même était saturé :

```
{"level":"warn","ts":"2026-03-16T23:08:23.946036Z","logger":"etcd-client","caller":"v3@v3.6.5/retry_interceptor.go:65","msg":"retrying of unary invoker failed","target":"etcd-endpoints://0xc00088cd20/192.168.1.15:2379","method":"/etcdserverpb.KV/Range","attempt":0,"error":"rpc error: code = DeadlineExceeded desc = context deadline exceeded"}
{"level":"warn","ts":"2026-03-16T23:08:25.954079Z","logger":"etcd-client","caller":"v3@v3.6.5/retry_interceptor.go:65","msg":"retrying of unary invoker failed","target":"etcd-endpoints://0xc0001c3a40/192.168.1.15:2379","method":"/etcdserverpb.KV/Range","attempt":0,"error":"rpc error: code = DeadlineExceeded desc = context deadline exceeded"}
E0316 23:08:28.151019       1 status.go:71] "Unhandled Error" err="apiserver received an error that is not an metav1.Status: &errors.errorString{s:\"context canceled\"}: context canceled" logger="UnhandledError"
E0316 23:08:28.151158       1 writers.go:123] "Unhandled Error" err="apiserver was unable to write a JSON response: http: Handler timeout" logger="UnhandledError"
E0316 23:08:28.152777       1 status.go:71] "Unhandled Error" err="apiserver received an error that is not an metav1.Status: &errors.errorString{s:\"http: Handler timeout\"}: http: Handler timeout" logger="UnhandledError"
```

Chaque appel KV range à etcd expirait. Le serveur API laissait tomber les requêtes, les gestionnaires expiraient, et tout ce qui dépendait de l'élection de leader — le contrôleur manager, le scheduler — s'effondrait.

```markdown
---
title: "Diagnostic de la cause racine"
description: "Apprenez à diagnostiquer et résoudre les problèmes de quorum et de stabilité dans un cluster Kubernetes, en particulier avec etcd."
lang: fr
---

### Diagnostic de la cause racine

J'ai listé les membres etcd pour comprendre la topologie du cluster :

```bash
sudo ETCDCTL_API=3 etcdctl member list -w table \
  --endpoints=https://192.168.1.15:2379 \
  --cacert=/etc/ssl/etcd/ssl/ca.pem \
  --cert=/etc/ssl/etcd/ssl/member-ih-node-1.pem \
  --key=/etc/ssl/etcd/ssl/member-ih-node-1-key.pem
```

![[homelab-etcd-list-1.png]]

Trois membres etcd : ih-node-1, ih-node-2, ih-node-3. Un membre etcd par nœud — le défaut de Kubespray lorsque vous avez trois nœuds dans l'inventaire.

Le problème s'est immédiatement cristallisé. J'ai **un nœud de contrôle** et **trois membres etcd**. Etcd est un système de consensus distribué : un cluster à 3 membres nécessite que 2 membres soient disponibles pour atteindre le quorum. Mais le serveur API ne tourne que sur ih-node-1. Les deux nœuds workers exécutent des processus etcd qui ne servent pas le plan de contrôle de manière significative — ils participent simplement aux élections et à la réplication, ajoutant une latence d'aller-retour à chaque écriture effectuée par le serveur API.

Kubespray a installé etcd comme un **service systemd** (pas un pod statique), un par nœud, les trois répliquant. C'est tout à fait correct pour une véritable configuration HA avec plusieurs serveurs API. Mais avec un seul plan de contrôle, cela signifie que chaque écriture etcd de `kube-apiserver` doit faire un aller-retour sur le WiFi domestique pour atteindre le quorum sur deux des trois membres. Parfois, ce problème de WiFi est suffisamment long pour dépasser les délais du serveur API, le gestionnaire de contrôleur perd son bail, et la boucle de crash commence.

La solution était claire : réduire le cluster etcd à un seul nœud sur ih-node-1. Pas d'allers-retours de quorum, pas de sensibilité au WiFi, et cela correspond à l'architecture réelle — un plan de contrôle, un etcd.

## 8 - Correction du problème de quorum

La procédure devait être prudente. Supprimer des membres d'un cluster etcd en direct pendant que le serveur API se comportait mal nécessitait de le faire dans le bon ordre.

### Étape 1 : Sauvegarde d'etcd

Avant de toucher à quoi que ce soit :

```bash
ETCDCTL_API=3 etcdctl snapshot save /root/etcd-backup-$(date +%Y%m%d).db \
  --endpoints=https://192.168.1.15:2379 \
  --cacert=/etc/ssl/etcd/ssl/ca.pem \
  --cert=/etc/ssl/etcd/ssl/member-ih-node-1.pem \
  --key=/etc/ssl/etcd/ssl/member-ih-node-1-key.pem
```

J'ai vérifié que la sauvegarde était cohérente :

```bash
sudo etcdutl snapshot status etcd-backup-20260317.db -w table
```

### Étape 2 : Suppression des deux membres etcd workers

```bash

# Suppression du membre etcd ih-node-2
ETCDCTL_API=3 etcdctl member remove 5306eee70c5d385c \
  --endpoints=https://192.168.1.15:2379 \
  --cacert=/etc/ssl/etcd/ssl/ca.pem \
  --cert=/etc/ssl/etcd/ssl/member-ih-node-1.pem \
  --key=/etc/ssl/etcd/ssl/member-ih-node-1-key.pem

# Suppression du membre etcd ih-node-3
ETCDCTL_API=3 etcdctl member remove 7a2118b371513eef \
  --endpoints=https://192.168.1.15:2379 \
  --cacert=/etc/ssl/etcd/ssl/ca.pem \
  --cert=/etc/ssl/etcd/ssl/member-ih-node-1.pem \
  --key=/etc/ssl/etcd/ssl/member-ih-node-1-key.pem
```

![[homelab-etcd-list-2.png]]

Un seul membre restant : ih-node-1.

### Étape 3 : Restauration à partir de la sauvegarde

Avec la liste des membres réduite à un seul nœud, j'avais besoin qu'etcd redémarre proprement en mode mono-nœud. L'unité systemd de Kubespray avait toujours l'ancienne configuration `--initial-cluster` à 3 membres, ce qui faisait redémarrer etcd et chercher immédiatement les deux pairs supprimés.

J'ai restauré à partir de la sauvegarde en utilisant `etcdutl` (note : `etcdutl` est l'outil de restauration autonome — il ne nécessite pas qu'etcd soit en cours d'exécution) :

```bash
etcdutl snapshot restore etcd-backup-20260317.db \
  --data-dir /var/lib/etcd-restored \
  --name ih-node-1 \
  --initial-cluster ih-node-1=https://192.168.1.15:2380 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-advertise-peer-urls https://192.168.1.15:2380
```

La restauration crée un WAL propre avec un nouvel ID de cluster et un seul membre, donc etcd démarre sans avoir besoin de se connecter à qui que ce soit.

### Étape 4 : Mise à jour de l'unité systemd

Les drapeaux critiques à ajouter lors du redémarrage avec le répertoire de données restauré :

```
--initial-cluster-state=existing
--force-init-cluster
```

Ceux-ci indiquent à etcd qu'il s'agit d'un cluster existant en cours de récupération, et non d'un nouveau démarrage, et forcent l'initialisation mono-nœud à partir de l'état restauré.

### Étape 5 : Vérification

Le planificateur et le gestionnaire de contrôleur sont revenus en ligne proprement. Plus de timeouts de bail, plus de boucles de crash. Le serveur API était à nouveau réactif.

![[homelab-list-pods-kube-system-etcd.png]]

### Ce que cela m'a appris

La vraie leçon ici concerne l'écart entre les défauts de Kubespray et ce qui a réellement du sens pour une topologie donnée. Kubespray est conçu pour gérer des déploiements HA complets, et ses défauts en témoignent. Lorsque vous lui donnez trois nœuds, il place etcd sur les trois. C'est correct pour un cluster à 3 plans de contrôle — c'est activement nuisible pour un cluster à 1 plan de contrôle car cela introduit une latence de quorum sans aucun avantage de redondance.

La note de conception que j'ai ajoutée au README après cet incident :

> **Nœud de contrôle unique** — un homelab à 3 nœuds n'a pas besoin de HA pour le plan de contrôle. Ajouter un deuxième plan de contrôle consommerait un nœud plus utile en tant que worker, et le cluster peut être redéployé à partir de zéro si `ih-node-1` est perdu. Idem pour etcd. L'homelab n'a pas besoin de HA, donc je me contente de sauvegarder la base de données etcd et de la restaurer en cas de catastrophe.

Pour un homelab : sauvegardez etcd régulièrement, conservez la sauvegarde hors site, et sachez comment la restaurer. C'est une stratégie de résilience plus pratique qu'un cluster etcd à 3 nœuds fonctionnant sur WiFi.

## 9 - Playbooks opérationnels

Au-delà du déploiement principal de Kubespray, j'ai trois playbooks opérationnels pour la gestion quotidienne du cluster.

### up.yml — vérification de la joignabilité des nœuds

```bash
ansible-playbook playbooks/up.yml
```

Une vérification rapide de la connectivité avant de faire quoi que ce soit d'autre. Elle ping tous les nœuds et vérifie l'accès SSH. Je l'exécute chaque fois que je n'ai pas touché à l'homelab depuis quelques jours et que je veux confirmer que tout est toujours en marche avant d'exécuter un playbook plus long.

### inventory_cluster.yml — rapport de ressources

```bash
ansible-playbook playbooks/inventory_cluster.yml
```

Rapporte le CPU, la mémoire et la capacité disque par nœud. Je l'utilise pour obtenir une image actuelle des ressources dont je dispose avant de déployer quelque chose de nouveau, et pour détecter les dérives si l'un des ordinateurs portables consomme silencieusement plus de disque que prévu.

### shutdown.yml — arrêt gracieux

```bash
ansible-playbook playbooks/shutdown.yml
```

Je travaille activement sur l'homelab la plupart des soirs, mais il n'y a aucune raison de laisser trois ordinateurs portables allumés au ralenti pendant la nuit quand personne n'utilise le cluster. Ce playbook arrête gracieusement tous les nœuds. Le lendemain matin, je les rallume et j'exécute `up.yml` pour confirmer qu'ils sont revenus proprement.

C'est plus important qu'il n'y paraît : un arrêt gracieux garantit qu'etcd vide correctement son WAL sur le disque. Les coupures de courant soudaines peuvent corrompre le répertoire de données etcd, ce qui est un scénario de récupération beaucoup moins amusant que la sauvegarde et restauration intentionnelle que j'ai décrite ci-dessus.

## 10 - Installation de Tailscale

La dernière étape a été de rendre le cluster accessible depuis l'extérieur du réseau domestique sans ouvrir de ports sur le routeur.

Tailscale est un VPN maillé basé sur WireGuard. Chaque appareil qui rejoint le Tailnet obtient une adresse IP stable `100.x.x.x` qui fonctionne quel que soit le réseau sur lequel se trouve l'appareil. Avec Tailscale installé sur les trois nœuds, je peux me connecter en SSH à n'importe lequel d'entre eux depuis n'importe où, et `kubectl` fonctionne depuis mon ordinateur portable, où que je sois.

L'installation de Tailscale est gérée comme un playbook Ansible distinct, intentionnellement non mélangé au déploiement Kubespray :

```bash
ansible-playbook playbooks/tailscale.yml --ask-vault-pass
```

La clé d'authentification est stockée dans `vars/tailscale.yml` sous forme de fichier chiffré par Ansible Vault. Le playbook demande le mot de passe du coffre-fort à l'exécution, déchiffre la clé et l'utilise pour authentifier chaque nœud dans le Tailnet. Conserver le secret chiffré dans le dépôt signifie que le playbook est entièrement autonome — aucun magasin de secrets externe n'est nécessaire pour quelque chose d'aussi simple.

Le playbook Tailscale peut être réexécuté indépendamment pour faire pivoter la clé d'authentification sans modifier la configuration du cluster. Cette séparation des préoccupations — provisionnement du cluster dans un playbook, VPN dans un autre — rend la maintenance beaucoup plus propre.

## Conclusion

Kubespray a livré exactement ce que je voulais : un cluster Kubernetes de qualité production où je peux voir et comprendre chaque composant, sans avoir à assembler chaque commande kubeadm à la main. L'exécution du playbook en 20 minutes a été un peu anticlimatique après tout le travail de configuration, mais c'est le but — la complexité réside dans Ansible, pas dans la saisie de commandes sur les nœuds.

Le crash d'etcd a été le meilleur moment d'apprentissage de toute la configuration. Il m'a forcé à comprendre réellement ce que fait etcd, comment fonctionne le quorum, comment utiliser `etcdctl` et `etcdutl` en pratique, et comment récupérer d'un état cassé. J'aurais continué beaucoup plus longtemps sans cette compréhension si tout avait fonctionné parfaitement dès le début.

Prochaine étape : faire fonctionner des charges de travail sur le cluster — en commençant par la couche de stockage, GitOps avec ArgoCD, et les premières applications réelles.
```