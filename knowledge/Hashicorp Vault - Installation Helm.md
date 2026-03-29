developer.hashicorp.com/vault/docs/platform/k8s/helm

https://developer.hashicorp.com/vault/tutorials/kubernetes/kubernetes-raft-deployment-guide

Its recommended to have a dedicated cluster only for vault.
```
helm repo add hashicorp https://helm.releases.hashicorp.com
```

```
helm install vault hashicorp/vault
```

