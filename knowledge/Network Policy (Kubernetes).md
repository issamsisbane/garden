# Network Policy (Kubernetes)

*Netpol to deny traffic from a certain source and allow everything else*

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-metadata
  namespace: default
spec:
  podSelector:
    matchLabels:
      app: app
  policyTypes:
  - Egress
  egress:
  - to:
    - ipBlock:
        cidr: 0.0.0.0/0
        except:
        - <controlplane-ip>/32 # Replace with the actual IP address of the controlplane node
```