# Setup Istio TLS peer authent (Kubernetes)

It would be difficult to let application handle the secure mTLS communication directly because it would had complexity to it.

The solution is to let them communicate as plain http and use sidecar for mTLS.

For [[Istio]] there are 2 modes :
- Enforces/Strict : mTLS must be enforce every single time
- Permissive/Opportunistic : Istio can allow plain-text communication for particular service (for example an external app which can't use mTLS).

By default Istio doesn't enforce mTLS and allow all trafic. To enable mTLS we need to : 

```yaml
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default
  namespace: mynamespace
spec:
  mtls:
    mode: STRICT
```

All namespaces must have the correct label for istio to get a sidecar and be able to communicate correctly.


`istio-injection=enabled`

We can use the `istioctl` cli to diagnose : 

```bash
istioctl analyse -n mynamespace
```

![[Kubernetes_-_CKS-19.png]]

To make a `PeerAuthentication` policy global we need to create it in the istio root ns `istio-system`.

```yaml
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: STRICT
```

Then if we create a PeerAuthentication policy in a namespace it will override the global PA policy in that namespace.

We can also restrict to specific pods :

```yaml
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default
  namespace: default
spec:
  mtls:
    mode: PERMISSIVE
  selector:
    matchLabels:
      app: helloworld
```

If we add the annotation to a namespace, the namespace get a sidecar on all the pods. And expect an mTLS connexion depending on the PeerAuthentPolicy. So controlplane components would not be affected. By default there are already talking via mTLS.

Istio inject a container in a pod. With GitOps tools generally we deploy deployment so a drift would not be detected because the container is injected as the pod level. The deployment is not mutated.