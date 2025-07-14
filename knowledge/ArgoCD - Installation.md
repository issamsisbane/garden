[[ArgoCD - Installation Information]]
# Create a namespace for argo
``` bash
k create ns argocd
```

# Install Argo
``` bash
k apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

# Get the admin password

Argo CD store the default admin password in the secret `argocd-initial-admin-secret`. We need to get it.

# Expose ArgoCD Server

We can use the different option : 
- Service : Load Balancer
- Ingress
- Port-forward

We will be using port-forwarding.

```
kubectl port-forward svc/argocd-server -n argocd-server -n argocd 8080:443
```

We connect to https://localhost:8080
And we use the password we got earlier with the `admin` user.

# Install ArgoCD CLI

We can manage everything from the CLI. It can be useful to interact with ArgoCD from CI pipelines.

```
brew install argocd
```

We need to login to ArgoCD Server.

```
argocd login localhost:8080
```

We can verify using : 
```
argocd cluster list
```