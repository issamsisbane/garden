---
creation date: 2026-08-26-21:22:06
modification date: 2026-08-26-21:22:06
imageNameKey: Kube-bench
---
# Kube-bench

Kube-bench is a tool developed by aqua to check if a kubernetes cluster is compliant with security best-practices.

It uses CIS Kubernetes benchmark.

It can be deployed as : 
- container
- pod in a cluster
- binary [[Install a binary from github]]

To to run a particular benchmark :

```bash
kube-bench run --config-dir=/root/kube-config/cfg --benchmark=cis-1.10
```

To run a particular test : 

```bash
kube-bench --check="1.3.1"
```

To run a particular target (set of components) :

```bash
kube-bench run --targets="master,etcd"
```

Targets are `[master node controlplane etcd policies]`
