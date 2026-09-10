---
creation date: 2026-02-25-23:26:12
modification date: 2026-02-25-23:26:12
imageNameKey: Untitled
---
[[New Homelab Setup - Openbao]]
[[Terraform - Statefile]]
[[Direnv - Usage]]
[[New Homelab Setup - Prises connectés]]
[[New Homelab Setup - ArgoCD Reorganisation]]
[[New Homelab Setup - Observability]]
[[New Homelab Setup - Longhorn Erreur]]
[[New Homelab Setup - Scheduling Error]]
[[New Homelab Setup - Restart Everything]]
[[New Homelab Setup - SSO]] 
[[New Homelab Setup - Tailscale DNS Error]]

# Install OS

I have 3 nodes for now.
I want a consistent OS for all the machines now.

I choosed ubuntu server because that's what I know the most.

I wanted to have a consistent and reproductible installation. But I didn't wanted to do too much effort for the OS installation.

I hope I will never do this again.

I choose to change from Rufus to Ventoy. I used cloud-init scripts to init the machine like setup the wifi, my ssh key, the hostname...

```

```

## Problems
### 1. Ventoy Booting

When booting I went into this problem : verification failed 0x1a ventoy
The following article help me resolve it : https://www.technewstoday.com/ventoy-secure-boot/

### 2. Raspberry

The raspberry is different it doesn't have a uefi boot system, so I can't use ventoy.
But I used the rapsberry pi installer which allow me to do the same by configuring the hostname, my ssh key and the wifi. So it's not a big problem

### 3. Wifi

#### Package

I found some problems when installing because I was using the wifi.
Indeed, for now I didn't wanted to have a switch to connect my machine to my router. So I'm going with wifi. 

The problem is that by default, the package used for wifi is not installed when running ubuntu server. The package is called wpa_applicant.

So i added it to my autoinstall script, and to configure correctly my machine, I had to use ethernet in order to install this package and configure the wifi.

It's not a big problem for the installation as long as the wifi is ok when the machine are running after

#### Interface

The other problem I encountered was that the interface name are changing depending machine. Indeed, I'm using old laptop and there are not all the same. So sometimes the wifi interface is called wlp13s0 or another name like wlp01s0. 

This is annoying to automate the configuration. I found a workaroung by renaming all interface as wlan0. So now I can configure the wifi evenly between all my machines.

### Hostnames

I also had a problems with hostname. 
I decided to name my nodes like this : 
- ih-node-01
- ih-node-02
- ih-node-03
ih for Issam Homelab.

I'm using the router of my Internet Provider and it has some limitations. Indeed it delete the 0.
So in the machine 1 I have the hostname ih-node-01 but to contact it from another machine of the network I have to use ih-node-1.
I hate to have inconsistencies like this.
I could have just update the file /etc/hosts for each machine of the network but it add a manual action I don't want.
So I decided to just change the hostname for each machine and delete the 0.

### Fix IPs

I can't automate much with my router, so I had to fix the ip for each machines by hand.

### Keep the machine up when closing the laptop

`/etc/systemd/conf`
```conf
HandleLidSwitch=ignore
HandleLidSwitchExternalPower=ignore
HandleLidSwitchDocked=ignore
```

```bash
sudo systemctl restart systemd-logind
```
# Provisionning

I will use ansible to provisionne the machines.

## Machines ressources

I wanted firstly to know excatly what ressources I had on my machines to choose the role of each of them.

For now I have only 3. So I decided to create a simple playbook to generate a report for all my machines.

## Shutdown

I'm working on my homelab everyday, so as long as there are no workloads running on it yet, I prefer to shutdown all my machines when I'm not using them. I created a simple playbook for that too.

## Kubernetes

I choose to use kubeadm with vanilla kubernetes to learn.

So I will use kubespray to install the cluster.

I choose iptables instead of ipvs.

I choose to install argoCD and metrics-server.

The playbook ran for 20 minutes.

![[kubespray-playbookl-execution-20260301232100.png]]

I got the kubeconfig from the master node with the following command : 

```
ssh kuadm@ih-node-1 "sudo cat /etc/kubernetes/admin.conf" > ~/.kube/homelab
```

I change the context of kubectl using my custom command : 
![[kc-custom-command-20260301232314.png]]

I verify that everything works correctly : 
![[homelab-verification-init-20260301232607.png]]
#### Control plane (tourne sur ih-node-1)

- **kube-apiserver** — le cerveau du cluster, tout passe par lui
- **kube-controller-manager** — surveille l'état du cluster et corrige les écarts
- **kube-scheduler** — décide sur quel nœud placer les pods

#### Réseau — Calico

- **calico-node** — un pod par nœud, gère le réseau entre les pods
- **calico-kube-controllers** — gère les politiques réseau

#### DNS

- **coredns** — DNS interne du cluster, permet aux pods de se parler par nom
- **dns-autoscaler** — ajuste le nombre de replicas CoreDNS selon la charge
- **nodelocaldns** — cache DNS local sur chaque nœud pour les performances

#### Réseau des services

- **kube-proxy** — un par nœud, gère les règles réseau pour accéder aux services

#### Proxy

- **nginx-proxy** — sur ih-node-2 et ih-node-3, proxy local vers l'API server pour que les workers puissent le joindre sans passer par une IP externe

#### Métriques

- **metrics-server** — collecte CPU/RAM des pods et nœuds, nécessaire pour `kubectl top`


### ArgoCD

An old version of Argo was installed using the kubespray playbook. `v2.14.5+f463a94`

I decided to delete it and reinstall a new version using the helm chart.

I had to delete the namespace, delete the CRDs and delete the ClusterRoles and ClusterRolesBindings.

```bash
kubectl get crd | grep argoproj | awk '{print $1}' | xargs kubectl delete crd
kubectl get clusterrole | grep argocd | awk '{print $1}' | xargs kubectl delete clusterrole
kubectl get clusterrolebinding | grep argocd | awk '{print $1}' | xargs kubectl delete clusterrolebinding
```

![[argo-helm-installation-20260301234515.png]]

I now have the latest version `3.3.2` of ArgoCD installed in the cluster.

![[argocd-ui-latest-version-20260301234840.png]]
# Calico

VXLAN + without cross-subnet overlay

I'm limited with my grand public router, I don't have BGP for example.

So I must use VXLAN or IP on IP mode and an overlay network for the network inside my cluster.

I choose VXLAN because its the new default of Calico and apparently the most compatible than IP on IP.

We could then ask why choose calico to do the same VXLAN we are doing with flannel ?

Because calico has a lot more features :
- observability
- Network policies
- ...
iptables and no ipvs
## Network Policies

https://docs.tigera.io/calico/latest/about/kubernetes-training/about-network-policy
> Kubernetes and Calico network policies can be mixed together seamlessly. One common use case for this is to split responsibilities between security / cluster ops teams and developer / service teams. For example, giving the security / cluster ops team RBAC permissions to define Calico policies, and giving developer / service teams RBAC permissions to define Kubernetes network policies in their specific namespaces. As Calico policy rules can be ordered to be enforced either before or after Kubernetes network policies, and can include actions such as deny and log, this allows the security / cluster ops team to define basic higher-level more-general purpose rules, while empowering the developer / service teams to define their own fine-grained constraints on the apps and services they are responsible for.

We can also protect nodes with calico

## Cluster

### Infra

- Argo
- CNPG
- External-secrets
- Openbao
- Tailscale-operator
- Authentik

- Replicator
- Cert-manager


headlamp => dashboard kubernetes ui

### Longhorn for Storage

Error job needed a service account to start.
### Authentik for SSO

Config as code en utilisant terraform.
Car les blueprints authentik ils faut forcément aller modifier le chart pour rajouter la configmap. C'est pas dingue je pense.
### Tailscale operator to expose service
### SSH with devcontainers

Open a socket


## Longhorn

Longhorn consomme trop : 

![[longhorn-ih-cluster-consmption.png]]
Alors que je n'ai rien du tout comme volumes :

![[volumes-homelab-longhorn-comsumption.png]]

La solution : 
https://longhorn.io/docs/1.11.0/important-notes/#longhorn-instance-manager-image

Un hotfix pour l'image. C'est un problème connu.

## TRAEFIK CERT MANAGER ERROR

![[Pasted-image-20260311233537.png.png]]
il fallait creer le certiicat à la main avant avec la ressource certificat probleme oeuf poule.

## EXTERNAL DNS CLOUDFLARE TUNNEL

il faut mettre sur la gateway l'annotation avec le tunnel.
et sur la httproute l'annotation pour le hostname.

https://github.com/kubernetes-sigs/external-dns/blob/master/docs/sources/gateway-api.md

On tombe sur une erreur :
![[Pasted-image-20260312002304.png.png]]

L'erreur venait de la gateway j'avais fait une erreur en ecrivant itunnelid d'ou le problème.

J'ai recreer un tunnel via la commande cloudflared tunnel.
Remis le configmap et le secret avec credentials.json
mis en tlsfalse
et tout fonctionnait.

## Authentik

J'ai cette erreur quand je veux utiliser le SSO authentik pour me connecter a headlamp.

Failed to verify ID Token: oidc: malformed jwt: go-jose/go-jose: unexpected signature algorithm "HS256"; expected ["RS256"]

J'ai rajouter ce qu'il fallait dans blueprints.

J'ai rajouter une clé SSH pour le HS256

J'ai rajouter aussi le signing alg dans l'api server

En fait il fallait juste aller dans le provider authentik, deselectionner la clé et la reselectionner. Et tout marchait.

Ensuite il fallait attribuer les roles aux users sur authentik qui match le group mis dans le Cluster Role Binding et c'était tout bon non peut se connecter à headlamp via SSO Authentik.

Il reste à créer un role readonly et de créer de users et de faire ça programmaticallement.

Authentik consomme trop. Il fait tourner un worker et le server ce qui donne 1Gb de consommation de RAM.

Je suis un peu short en ressource dans mon homelab sachant que j'utilise pas tout ce que propose Authentik et que c'est une solution construite pour des besoins d'entreprises en fait.
## ETCD Crash controller scheduler

le controller et le scheduler n'arrete pas de crash

```
error":"rpc error: code = DeadlineExceeded desc = context deadline exceeded"}                                                │
│ {"level":"warn","ts":"2026-03-16T23:08:23.946036Z","logger":"etcd-client","caller":"v3@v3.6.5/retry_interceptor.go:65","msg":"retr │
│ ying of unary invoker failed","target":"etcd-endpoints://0xc00088cd20/192.168.1.15:2379","method":"/etcdserverpb.KV/Range","attemp │
│ t":0,"error":"rpc error: code = DeadlineExceeded desc = context deadline exceeded"}                                                │
│ {"level":"warn","ts":"2026-03-16T23:08:25.954079Z","logger":"etcd-client","caller":"v3@v3.6.5/retry_interceptor.go:65","msg":"retr │
│ ying of unary invoker failed","target":"etcd-endpoints://0xc0001c3a40/192.168.1.15:2379","method":"/etcdserverpb.KV/Range","attemp │
│ t":0,"error":"rpc error: code = DeadlineExceeded desc = context deadline exceeded"}                                                │
│ {"level":"warn","ts":"2026-03-16T23:08:28.150880Z","logger":"etcd-client","caller":"v3@v3.6.5/retry_interceptor.go:65","msg":"retr │
│ ying of unary invoker failed","target":"etcd-endpoints://0xc0102a5680/192.168.1.15:2379","method":"/etcdserverpb.KV/Range","attemp │
│ t":0,"error":"rpc error: code = Canceled desc = context canceled"}                                                                 │
│ E0316 23:08:28.151019       1 status.go:71] "Unhandled Error" err="apiserver received an error that is not an metav1.Status: &erro │
│ rs.errorString{s:\"context canceled\"}: context canceled" logger="UnhandledError"                                                  │
│ E0316 23:08:28.151158       1 writers.go:123] "Unhandled Error" err="apiserver was unable to write a JSON response: http: Handler  │
│ timeout" logger="UnhandledError"                                                                                                   │
│ E0316 23:08:28.152777       1 status.go:71] "Unhandled Error" err="apiserver received an error that is not an metav1.Status: &erro │
│ rs.errorString{s:\"http: Handler timeout\"}: http: Handler timeout" logger="UnhandledError"                                        │
│ E0316 23:08:28.152883       1 writers.go:136] "Unhandled Error" err="apiserver was unable to write a fallback JSON response: http: │
│  Handler timeout" logger="UnhandledError"                                                                                          │
│ E0316 23:08:28.154191       1 timeout.go:140] "Post-timeout activity" logger="UnhandledError" timeElapsed="3.273983ms" method="GET │
│ " path="/apis/postgresql.cnpg.io/v1/namespaces/authentik/clusters/authentik-cnpg" r
```
```
1 tlsconfig.go:243] "Starting DynamicServingCertificateController"                                     │
│ E0316 23:04:52.328801       1 leaderelection.go:452] "Error retrieving lease lock" err="Get \"https://192.168.1.15:6443/apis/coord │
│ ination.k8s.io/v1/namespaces/kube-system/leases/kube-controller-manager?timeout=5s\": context deadline exceeded" lock="kube-system │
│ /kube-controller-manager"                                                                                                          │
│ E0316 23:05:06.287650       1 leaderelection.go:488] "Failed to update lease" err="the server was unable to return a response in t │
│ he time allotted, but may still be processing the request (put leases.coordination.k8s.io kube-controller-manager)" lock="kube-sys │
│ tem/kube-controller-manager"                                                                                                       │
│ I0316 23:05:12.622606       1 leaderelection.go:272] "Successfully acquired lease" lock="kube-system/kube-controller-manager"      │
│ I0316 23:05:12.623260       1 event.go:389] "Event occurred" object="kube-system/kube-controller-manager" fieldPath="" kind="Lease │
│ " apiVersion="coordination.k8s.io/v1" type="Normal" reason="LeaderElection" message="ih-node-1_1be54603-8d8a-4b9e-ab2f-be41d54823c │
│ d became leader"                                                                                                                   │
│ E0316 23:05:19.718364       1 leaderelection.go:445] "Failed to update lease optimistically, falling back to slow path" err="Put \ │
│ "https://192.168.1.15:6443/apis/coordination.k8s.io/v1/namespaces/kube-system/leases/kube-controller-manager?timeout=5s\": context │
│  deadline exceeded" lock="kube-system/kube-controller-manager"                                                                     │
│ E0316 23:05:24.718246       1 leaderelection.go:452] "Error retrieving lease lock" err="Get \"https://192.168.1.15:6443/apis/coord │
│ ination.k8s.io/v1/namespaces/kube-system/leases/kube-controller-manager?timeout=5s\": context deadline exceeded" lock="kube-system │
│ /kube-controller-manager"                                                                                                          │
│ I0316 23:05:24.718342       1 leaderelection.go:299] "Failed to renew lease" lock="kube-system/kube-controller-manager" err="conte │
│ xt deadline exceeded"                                                                                                              │
│ E0316 23:05:24.718660       1 controllermanager.go:368] "leaderelection lost
```

ça à l'air d'etre un problème de communication entre les differents nodes etcd.

Deja pas besoin de 1 etcd sur chaque node car 1 seul master kube...

En plus etcd est installé comme service system et pas pod.

Lister les nodes etcd : 
```
sudo ETCDCTL_API=3 etcdctl member list -w table   --endpoints=https://192.168.1.15:2379   --cacert=/etc/ssl/etcd/ssl/ca.pem   --cert=/etc/ssl/etcd/ssl/member-ih-node-1.pem   --key=/etc/ssl/etcd/ssl/member-ih-node-1-key.pem
```

![[homelab-etcd-list-1.png]]
J'aimerais revenir à un seul node.

Pour ça 

1. Backup etcd

```
ETCDCTL_API=3 etcdctl snapshot save /root/etcd-backup-$(date +%Y%m%d).db --endpoints=https://192.168.1.15:2379 --cacert=/etc/ssl/etcd/ssl/ca.pem   --cert=/etc/ssl/etcd/ssl/member-ih-node-1.pem   --key=/etc/ssl/etcd/ssl/member-ih-node-1-key.pem
```

2. Verification du backup

```
sudo etcdutl snapshot status etcd-backup-20260317.db -w table
```

3. Supprimer etcd worker 2 et 3
```
# Supprimer etcd2 
ETCDCTL_API=3 etcdctl member remove 5306eee70c5d385c --endpoints=https://192.168.1.15:2379 --cacert=/etc/ssl/etcd/ssl/ca.pem   --cert=/etc/ssl/etcd/ssl/member-ih-node-1.pem   --key=/etc/ssl/etcd/ssl/member-ih-node-1-key.pem

# Supprimer etcd3 
ETCDCTL_API=3 etcdctl member remove 7a2118b371513eef --endpoints=https://192.168.1.15:2379 --cacert=/etc/ssl/etcd/ssl/ca.pem   --cert=/etc/ssl/etcd/ssl/member-ih-node-1.pem   --key=/etc/ssl/etcd/ssl/member-ih-node-1-key.pem
```

Il reste bien 1 seul node :
![[homelab-etcd-list-2.png]]

4. Suppression des nodes dans l'api server

5. Verification
![[homelab-list-pods-kube-system-etcd.png]]

On verifiera si le scheduler et le controller manager redemarre maintenant avec 1 seul node etcd.
![[homelab-etcd-pods-verif.png]]

#### Passage vers pods etcd

Il faut déjà copier les certificats dans /etc/kubernetes/ssl

```

```

Voici les manifests : 
```
apiVersion: v1
kind: Pod
metadata:
  name: etcd
  namespace: kube-system
  labels:
    component: etcd
    tier: control-plane
spec:
  hostNetwork: true
  priorityClassName: system-node-critical
  containers:
  - name: etcd
    image: registry.k8s.io/etcd:v3.6.8
    command:
    - etcd
    - --advertise-client-urls=https://192.168.1.15:2379
    - --cert-file=/etc/kubernetes/pki/etcd/server.crt
    - --client-cert-auth=true
    - --data-dir=/var/lib/etcd
    - --initial-advertise-peer-urls=https://192.168.1.15:2380
    - --initial-cluster=ih-node-1=https://192.168.1.15:2380
    - --initial-cluster-state=existing
    - --key-file=/etc/kubernetes/pki/etcd/server.key
    - --listen-client-urls=https://127.0.0.1:2379,https://192.168.1.15:2379
    - --listen-metrics-urls=http://127.0.0.1:2381
    - --listen-peer-urls=https://192.168.1.15:2380
    - --name=ih-node-1
    - --peer-cert-file=/etc/kubernetes/pki/etcd/peer.crt
    - --peer-client-cert-auth=true
    - --peer-key-file=/etc/kubernetes/pki/etcd/peer.key
    - --peer-trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
    - --snapshot-count=10000
    - --trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
    livenessProbe:
      httpGet:
        host: 127.0.0.1
        path: /livez
        port: 2381
        scheme: HTTP
      initialDelaySeconds: 10
      periodSeconds: 10
      failureThreshold: 8
    readinessProbe:
      httpGet:
        host: 127.0.0.1
        path: /readyz
        port: 2381
        scheme: HTTP
      initialDelaySeconds: 10
      periodSeconds: 10
    ports:
    - containerPort: 2379
      name: client
      protocol: TCP
    - containerPort: 2380
      name: peer
      protocol: TCP
    - containerPort: 2381
      name: metrics
      protocol: TCP
    volumeMounts:
    - mountPath: /var/lib/etcd
      name: etcd-data
    - mountPath: /etc/kubernetes/pki/etcd
      name: etcd-certs
  volumes:
  - hostPath:
      path: /var/lib/etcd
      type: DirectoryOrCreate
    name: etcd-data
  - hostPath:
      path: /etc/kubernetes/pki/etcd
      type: DirectoryOrCreate
    name: etcd-certs
```



Quand je suis passé à un seul noeud en redemarrant j'ai eu plein d'erreur.

J'ai du redemarrer etcd avec les flags suivants : 
```
- --initial-cluster-state=existing
- --force-init-cluster
```

et aussi supprimer le dossier data etcd et restore le backup qu'on a fait au préalable.

etcdutl restore

etcdutl ne nécessite pas etcd qui tourne.


Au final je suis passé en static pods et j'ai arreté le service etcd.

J'avais des problème de readiness, probeness parceque je n'avais pas mis le host.
Je le sais car mon pod s'arretait au bout de 1min.

J'ai aussi disable le service systemd etcd

kubespray installe par defaut en mode systemd

https://github.com/kubernetes-sigs/kubespray/blob/master/docs/operations/etcd.md

## Récap de la session

### Problème initial

- kube-controller-manager et kube-scheduler en crashloop
- Cause : etcd trop lent → API server timeout → perte de lease

### Diagnostic

- Cluster etcd réparti sur 3 nodes (master + 2 workers) avec 1 seul master
- Architecture incohérente : la HA etcd ne sert à rien sans plusieurs masters
- L'apiserver pointait sur les 3 membres etcd

### Ce qu'on a fait

**✅ Backup etcd** sur `/root/etcd-backup-YYYYMMDD.db`

**✅ Suppression des membres workers** du cluster etcd

- Supprimé `5306eee70c5d385c` (ih-node-2 / 192.168.1.16)
- Supprimé `7a2118b371513eef` (ih-node-3 / 192.168.1.17)

**✅ Restauration depuis backup** via `etcdutl snapshot restore` pour recréer un WAL propre en single-node

**❌ Tentative migration service systemd → static pod** — abandonnée, trop complexe avec Kubespray et pas nécessaire

### État actuel

- Etcd démarre et élit bien un leader ✅
- Mais redémarre en boucle ⏳
- Cause probable : config systemd Kubespray contient encore les 3 membres

## Homepage

Je voulais un dashboard pour mes services. J'ai décidé d'utiliser homepage, il y avait aussi glance qui me faisait de l'oeil

[[Homelab - Homepage Authent]]
[[Homelab - Homepage Setup]]
## TO SEE

BGP
https://medium.com/@Phoenixforge/diving-deeper-with-ubuntu-autoinstall-b15e5bdffbb5
https://blog.stephane-robert.info/docs/cloud/cloud-init/
https://www.ventoy.net/en/doc_start.html
https://docs.cloud-init.io/en/latest/tutorial/lxd.html#tutorial-lxd
https://blog.zwindler.fr/2017/12/05/installer-kubernetes-kubespray-ansible/
https://blog.nebrass.fr/playing-with-kyverno/
https://blog.nebrass.fr/
https://headlamp.dev/docs/latest/installation/in-cluster/oidc/
https://headlamp.dev/docs/latest/installation/in-cluster/keycloak/
https://medium.com/@mattiaforc/zero-trust-kubernetes-ingress-with-tailscale-operator-cert-manager-and-external-dns-8f42272f8647
https://une-tasse-de.cafe/blog/apiserver-multi-idp/