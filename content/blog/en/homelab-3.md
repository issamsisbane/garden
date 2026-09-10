---
title: "Homelab - 3 - Deploying Kubernetes with Kubespray"
description: "How I used Kubespray to deploy a production-grade Kubernetes cluster on three bare-metal nodes, and the etcd crash that taught me about quorum."
lang: "en"
pubDate: "Sept 21 2025"
heroImage: "/portfolio/blog/homelab-3/homelab-3.png"
badge: "Homelab"
tags: ["Kubernetes", "Self-Host", "DevOps"]
---

*With the three nodes provisioned (see part 2), it was time to install Kubernetes. Having gone through a simpler K3s installation in my previous homelab, I wanted something closer to how real clusters are built — something that would teach me about the actual moving parts rather than hiding them behind a single binary.*

*K3s is fantastic for getting a cluster running in minutes. But it bundles so much — embedded etcd, a built-in load balancer, Traefik pre-installed — that you can run it for months without understanding what's actually happening underneath. This time I wanted to feel every component: etcd, the API server, the scheduler, the controller manager, the CNI. All of it explicit, all of it mine to break.*

*This part covers the full Kubespray installation: the Ansible setup, the configuration choices I made, the Calico CNI wiring, and — honestly the most instructive part — the etcd crash that brought down the controller manager and scheduler a few weeks in, and what it took to fix it.*

---

1 - [Why Kubespray](#1---why-kubespray)
2 - **Setting up the Ansible environment** <br/>
3 - **Cluster topology and Kubespray configuration** <br/>
4 - **Calico CNI: VXLAN over BGP** <br/>
5 - **Running the playbook** <br/>
6 - **Replacing ArgoCD with a fresh Helm install** <br/>
7 - **The etcd crash** <br/>
8 - **Fixing the quorum problem** <br/>
9 - **Operational playbooks** <br/>
10 - **Installing Tailscale** <br/>

---

## 1 - Why Kubespray

The three main paths to a self-managed Kubernetes cluster are kubeadm directly, K3s, or Kubespray. I ruled out K3s for the reasons above. Between raw kubeadm and Kubespray, the choice was straightforward.

Kubespray is essentially a curated Ansible wrapper around kubeadm. It handles all the steps you would otherwise run by hand: installing container runtime dependencies, generating certificates, bootstrapping the control plane, joining worker nodes, installing a CNI, and configuring add-ons. Every step is codified and repeatable.

The key advantage for a homelab is that the full cluster lifecycle — install, upgrade, add a node, tear it down — stays inside a single Ansible project. If I need to rebuild from scratch because a node dies or I want to try a new Kubernetes version, I run one command. No post-it notes, no "I think I did this manually last time."

I pinned Kubespray at **v2.30.0**. Pinning is important: Kubespray upgrades can carry breaking changes in variable names and defaults, and I want cluster upgrades to be a deliberate decision, not something that happens silently on the next `git pull`.

## 2 - Setting up the Ansible environment

Ansible has a reputation for being annoying to set up consistently across machines — Python version conflicts, collection version drift, the usual. I solved this once by putting the entire Ansible environment in a devcontainer.

The `.devcontainer/` in the ansible folder gives me an Ubuntu 24.04 container with Ansible, ansible-lint, and the required collections pre-installed. I open the `ansible/` folder in VS Code, select "Reopen in Container", and I have a clean, reproducible environment regardless of what is or isn't installed on the host machine.

Before running anything, install the Kubespray collection dependencies:

```bash
ansible-galaxy install -r requirements.yml
```

This pulls in the Kubespray roles and any community collections they depend on. With that done, the environment is ready.

## 3 - Cluster topology and Kubespray configuration

### Topology

My cluster is 1 control plane + 2 workers:

| Node | Control plane | etcd | Worker |
|------|:---:|:---:|:---:|
| ih-node-1 | ✓ | ✓ | ✓ |
| ih-node-2 | | | ✓ |
| ih-node-3 | | | ✓ |

**No HA control plane.** In a three-node homelab, making two nodes control plane would mean one worker node, which is not a good trade. If `ih-node-1` is lost entirely, I rebuild from scratch — the etcd backup strategy (covered below) handles disaster recovery, not a second control plane.

This is the same reasoning I applied to etcd. A 3-node etcd cluster requires quorum of 2. With a single control plane, that quorum adds latency without adding real availability. I initially left the default on, which turned out to be a mistake I paid for later.

### SSH user

Kubespray connects to the nodes as `kuadm`. This is the provisioning user set up in part 2. The inventory uses `ansible_user: kuadm` with passwordless sudo.

### Network CIDRs

```
Service CIDR: 10.233.0.0/18
Pod CIDR:     10.233.64.0/18  (/24 per node)
```

These are the Kubespray defaults and they are well-chosen: they do not overlap with typical home network ranges (192.168.x.x), and the `/18` gives plenty of headroom. The `/24` per-node allocation means each node gets 254 usable pod addresses, which is more than enough for a homelab.

### Other configuration choices

**iptables over IPVS.** I chose iptables for `kube-proxy`. IPVS has better performance at scale but requires extra kernel modules and makes debugging harder. For a homelab, iptables is fine and better understood.

**Add-ons.** I enabled `metrics-server` and `argocd` in the Kubespray add-ons configuration. The ArgoCD version that Kubespray installs turned out to be outdated — I replaced it after the initial run, covered in section 6.

## 4 - Calico CNI: VXLAN over BGP

Kubespray supports multiple CNI plugins. I chose Calico.

The honest answer for why Calico over Flannel is features. Flannel does VXLAN overlay networking, full stop. Calico does VXLAN, BGP routing, network policies with proper ordering semantics, observability hooks, and node protection. Even if I only use a subset of that today, I want the option.

### Why not BGP

Calico's preferred mode at home would be pure BGP — no overlay, packets routed directly between nodes as if the cluster were a proper datacenter. BGP eliminates the VXLAN encapsulation overhead and makes packet captures much easier to read.

The problem is that BGP requires the router to participate in the routing protocol, which means it needs to understand and redistribute BGP routes. My ISP-provided home router does not support BGP. Full stop.

So I run Calico in **VXLAN mode** with an overlay network. Packets between pods on different nodes are encapsulated in VXLAN frames and sent across the home network. It's slightly less efficient, but it works with any router and requires no special network configuration.

VXLAN is now the default mode in recent Calico versions specifically because it is the most compatible choice. This is the right call for home and many cloud environments alike.

### Network policies

One of the main reasons to pick Calico over a simpler CNI is the network policy model. Calico extends the standard Kubernetes NetworkPolicy with its own `NetworkPolicy` and `GlobalNetworkPolicy` CRDs, which add:

- Explicit `Deny` rules (Kubernetes policies are allow-only)
- Ordered rule evaluation
- Node-level policies
- RBAC separation between cluster-ops and developer teams

I'm not using all of this from day one, but having it available means I can properly isolate namespaces and enforce least-privilege networking as I add more services to the cluster.

## 5 - Running the playbook

With the inventory configured and the devcontainer open, deploying the cluster is a single command:

```bash
ansible-playbook playbooks/kubespray.yml
```

The playbook ran for about 20 minutes on my three nodes. Kubespray is thorough — it checks prerequisites, installs container runtime, handles certificates, bootstraps etcd, brings up the API server, joins workers, installs Calico, and deploys the enabled add-ons.

![[kubespray-playbookl-execution-20260301232100.png]]

After the playbook completed, I pulled the kubeconfig from the master node:

```bash
ssh kuadm@ih-node-1 "sudo cat /etc/kubernetes/admin.conf" > ~/.kube/homelab
```

Then verified the cluster:

![[homelab-verification-init-20260301232607.png]]

All three nodes ready. The `kube-system` namespace had everything expected:

**Control plane (running on ih-node-1)**
- `kube-apiserver` — everything goes through it
- `kube-controller-manager` — watches cluster state and reconciles differences
- `kube-scheduler` — decides which node gets each pod

**Networking — Calico**
- `calico-node` — one pod per node, handles inter-pod networking
- `calico-kube-controllers` — manages network policies

**DNS**
- `coredns` — internal cluster DNS
- `dns-autoscaler` — adjusts CoreDNS replica count under load
- `nodelocaldns` — per-node DNS cache for performance

**Service networking**
- `kube-proxy` — one per node, manages iptables rules for Service routing

**Proxy**
- `nginx-proxy` — running on ih-node-2 and ih-node-3, local proxy to the API server so workers can reach it without going through an external IP

**Metrics**
- `metrics-server` — collects CPU and RAM usage per pod and node, powers `kubectl top`

## 6 - Replacing ArgoCD with a fresh Helm install

Kubespray installed ArgoCD as part of the add-ons run, but the version it shipped was `v2.14.5+f463a94` — significantly behind the current release.

I wanted ArgoCD v3.x. Rather than trying to upgrade in place, I wiped the installation and started clean with Helm:

```bash
kubectl get crd | grep argoproj | awk '{print $1}' | xargs kubectl delete crd
kubectl get clusterrole | grep argocd | awk '{print $1}' | xargs kubectl delete clusterrole
kubectl get clusterrolebinding | grep argocd | awk '{print $1}' | xargs kubectl delete clusterrolebinding
```

Then deleted the namespace and reinstalled via Helm, which pulled the latest chart targeting **v3.3.2**.

![[argo-helm-installation-20260301234515.png]]

![[argocd-ui-latest-version-20260301234840.png]]

The reason for the full CRD cleanup before reinstalling is that ArgoCD's CRDs evolve between major versions. Leaving stale v2 CRDs in place causes the v3 controller to either fail or produce confusing behavior as it interprets old schema fields.

## 7 - The etcd crash

A few weeks after the cluster was running, the `kube-controller-manager` and `kube-scheduler` started crash-looping. Everything that depended on the API server became unreliable.

The logs from the controller manager were immediate:

```
E0316 23:04:52.328801       1 leaderelection.go:452] "Error retrieving lease lock" err="Get \"https://192.168.1.15:6443/apis/coordination.k8s.io/v1/namespaces/kube-system/leases/kube-controller-manager?timeout=5s\": context deadline exceeded" lock="kube-system/kube-controller-manager"
E0316 23:05:06.287650       1 leaderelection.go:488] "Failed to update lease" err="the server was unable to return a response in the time allotted, but may still be processing the request (put leases.coordination.k8s.io kube-controller-manager)" lock="kube-system/kube-controller-manager"
I0316 23:05:12.622606       1 leaderelection.go:272] "Successfully acquired lease" lock="kube-system/kube-controller-manager"
E0316 23:05:19.718364       1 leaderelection.go:445] "Failed to update lease optimistically, falling back to slow path" err="Put \"https://192.168.1.15:6443/apis/coordination.k8s.io/v1/namespaces/kube-system/leases/kube-controller-manager?timeout=5s\": context deadline exceeded" lock="kube-system/kube-controller-manager"
E0316 23:05:24.718246       1 leaderelection.go:452] "Error retrieving lease lock" err="Get \"https://192.168.1.15:6443/apis/coordination.k8s.io/v1/namespaces/kube-system/leases/kube-controller-manager?timeout=5s\": context deadline exceeded" lock="kube-system/kube-controller-manager"
I0316 23:05:24.718342       1 leaderelection.go:299] "Failed to renew lease" lock="kube-system/kube-controller-manager" err="context deadline exceeded"
E0316 23:05:24.718660       1 controllermanager.go:368] "leaderelection lost"
```

The controller manager was acquiring the lease, immediately losing it because it couldn't renew fast enough, then crashing. The API server itself was saturated:

```
{"level":"warn","ts":"2026-03-16T23:08:23.946036Z","logger":"etcd-client","caller":"v3@v3.6.5/retry_interceptor.go:65","msg":"retrying of unary invoker failed","target":"etcd-endpoints://0xc00088cd20/192.168.1.15:2379","method":"/etcdserverpb.KV/Range","attempt":0,"error":"rpc error: code = DeadlineExceeded desc = context deadline exceeded"}
{"level":"warn","ts":"2026-03-16T23:08:25.954079Z","logger":"etcd-client","caller":"v3@v3.6.5/retry_interceptor.go:65","msg":"retrying of unary invoker failed","target":"etcd-endpoints://0xc0001c3a40/192.168.1.15:2379","method":"/etcdserverpb.KV/Range","attempt":0,"error":"rpc error: code = DeadlineExceeded desc = context deadline exceeded"}
E0316 23:08:28.151019       1 status.go:71] "Unhandled Error" err="apiserver received an error that is not an metav1.Status: &errors.errorString{s:\"context canceled\"}: context canceled" logger="UnhandledError"
E0316 23:08:28.151158       1 writers.go:123] "Unhandled Error" err="apiserver was unable to write a JSON response: http: Handler timeout" logger="UnhandledError"
E0316 23:08:28.152777       1 status.go:71] "Unhandled Error" err="apiserver received an error that is not an metav1.Status: &errors.errorString{s:\"http: Handler timeout\"}: http: Handler timeout" logger="UnhandledError"
```

Every KV range call to etcd was timing out. The API server was dropping requests, handlers were timing out, and anything relying on leader election — controller manager, scheduler — was falling apart.

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