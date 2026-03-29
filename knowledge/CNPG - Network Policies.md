[Accessing Kubernetes API Server When There Is An Egress NetworkPolicy | by Paul Dally | Medium](https://pauldally.medium.com/accessing-kubernetes-api-server-when-there-is-an-egress-networkpolicy-af4435e005f9)

Si on met une network policy qui coupe tout le traffic vers l'exterieur. Il faut une netpol dans le namespace applicatif pour permettre le traffic vers le namespace cnpg et une netpol pour permettre le traffic depuis le namespace cnpg

Il faut aussi permettre l'accès vers le namespaces cnpg-system et vers l'api kubernetes.
Le soucis se pose pour le flux vers l'api kubernetes.

le service utilisé pour l'api server c'est le service kubernetes dans le ns default. Sauf que ça ne redirige pas vers un pods namespace directement.

Il n'est pas possible de définir une netpol via le namesapce.
# Solution restrictive

La solution c'est de récupérer les endpoints du service kubernetes.
Et de faire une netpol qui autorise la sortie vers ces IPs.

Ça fonctionne mais le soucis c'est que ce n'est pas une configuration facilement replicable. 
Les IPs endpoints sont dynamique et peuvent changer, il faut donc modifier la netpol à chaque fois que les endpoints change.

# Solution la plus flexible

L'autre solution c'est de permettre la sortie pour toutes les requêtes en 443 et 6443.
Ça restreint moins et moins secure mais c'est plus flexible et plus durable. Tout en sachant qu'on part du principe que les namespaces sont tous cloisonnés et qu'on mettrait un proxy pour filtrer les requêtes sortantes.

Netpol côté CNPG pour l'accès au ns applicatif : 

```
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-backend-access
  namespace: test-cluster-cnpg
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress:
    - from: # Permet l'accès au namespace applicatif
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: test-cluster
    - from: # Permet l'accès au namespace de l'operateur CNPG
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: cnpg-system
          podSelector:
            matchLabels:
              app.kubernetes.io/name: cloudnative-pg
      ports:
        - port: 8000
        - port: 5432
  egress: # Permet l'accès à l'API Server
    - to:
      ports:
        - protocol: TCP
          port: 443
        - protocol: TCP
          port: 6443
```

Netpol côté applicatif pour l'accès au ns cnpg :

```
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-cnpg-access
  namespace: test-cluster
spec:
  podSelector:
    matchLabels: {}
  policyTypes:
  - Egress
  egress:
    - to:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: test-cluster-cnpg
```

Netpol Globale : 
```
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: mj-defaut
  namespace: test-cluster-cnpg
spec:
  podSelector: {}
  ingress:
    - from:
        - podSelector: {}
    - from:
        - namespaceSelector:
            matchLabels:
              network.openshift.io/policy-group: ingress
    - from:
        - namespaceSelector:
            matchLabels:
              network.openshift.io/policy-group: monitoring
  egress:
    - to:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: openshift-dns
        - podSelector:
            matchLabels:
              dns.operator.openshift.io/daemonset-dns: default
      ports:
      - protocol: UDP
        port: 53
      - protocol: TCP
        port: 53
      - protocol: UDP
        port: 5353
      - protocol: TCP
        port: 5353
  policyTypes:
    - Ingress
    - Egress
```