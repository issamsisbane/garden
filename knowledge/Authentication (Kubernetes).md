---
creation date: 2026-08-26-22:24:55
modification date: 2026-08-26-22:24:55
imageNameKey: Authentication_(Kubernetes)
---

# Authentication (Kubernetes)

Differents types of users : 
- Admins ([[Users (Kubernetes)]])
- Developers ([[Users (Kubernetes)]])
- End Users (Manged by the application itself not directly by Kube)
- Bots ([[Service Account]])

The authentication can be done using tokens or [[TLS Certificate (Kubernetes)]].


## Accessing the Kubernetes API

1. Start a kubectl proxy which will manage credentials using kubeconfig file to access kubernetes api

``` bash
kubectl proxy --port 8090
`http://localhost:8090/api/`
```

2. Access the cluster from api with credentials
- View the cluster configuration to find the cluster name and server address.
- Set the `CLUSTER_NAME` environment variable with your cluster name.
- Retrieve the API server address using `kubectl config`.
- Use Secret of namespace `kube-system` where name is similar to `bootstrap-token-*` to get the default token secret.
- Get the authentication token by decoding the default token secret.
- Use `curl` to access the Kubernetes API directly using the token for authentication.
    - example: `curl -X GET $APISERVER/api --header "Authorization: Bearer $TOKEN" --insecure`

You have to use secret decoding to get the token. The token is in the format `<token-id>.<token-secret>`

==A REVOIR : BOOTSTRAP TOKEN FOR AUTHENTICATION==

We can create a bootstrap secret manually : https://kubernetes.io/docs/reference/access-authn-authz/bootstrap-tokens/

Or with kubadm : 
```
kubeadm token create [random-token-id].[random-secret] --dry-run --print-join-command --ttl 2h
```

We can use these token to make a node join the cluster.

## Accessing the Kubelet

The ports exposed by the kubelet api :

![[Kubernetes_-_CKS_8.png]]

![[Kubernetes_-_CKS_9.png]]

We can disabled it via config file : 

```yaml
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
authentication:
  anonymous:
    enabled: false
```

or via kubelet flags :
```
--anonymous-auth=false
```

The authentication method are : 
- certificates (The api server need to authenticate)
![[Kubernetes_-_CKS_10.png]]
- bearer tokens

If those 2 fail, the user will be system:anonymous with a role system:unauthenticated => fail if disable.