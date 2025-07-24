# Egress

[Egress dans OpenShift 4](https://chatgpt.com/c/67b5e439-d73c-8008-a486-b8a1f4a70339)

Kubernetes-OVN permet de configurer un [[Egress]].

Seuls les EgressIPs sont disponibles avec ce CNI.

## EgressIP

Un EgressIp est une ressource rendu disponible via un CRD par l'opérateur Kubernetes-OVN.  
Cette ressource permet d'affecter à des noeuds des IPs spécifiques pour la sortie du traffic et de selectionner des namespaces et pods précis qui doivent utilisés ces IPs.

De base, les noeuds ont chacun une IP publique assigné et cette dernière est utilisé pour la sortie du traffic.

L'objet est clusterwide. Le ciblage s'effectue via l'utiliation de labels.

### Exemple

L'exemple a été trouvé dans la documentation openshift : [Configuring an egress IP address - OVN-Kubernetes network plugin | Networking | OpenShift Container Platform 4.17](https://docs.openshift.com/container-platform/4.17/networking/ovn_kubernetes_network_provider/configuring-egress-ips-ovn.html)

Il est possible de configurer un EgressIP comme cela :

``` yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all-egress
  namespace: my-namespace
spec:
  podSelector: {}  # Applique la règle à tous les Pods du namespace
  policyTypes:
    - Egress  # S’applique au trafic sortant
```

Voici les namespaces :

``` yaml
apiVersion: v1
kind: Namespace
metadata:
  name: namespace1
  labels:
    env: prod
---
apiVersion: v1
kind: Namespace
metadata:
  name: namespace2
  labels:
```

Voici l'infrastructure de notre cluster :

![[Pasted image 20250227175521.png]]

Ainsi les pods dans les namespaces avec le label `env: prod` vont utiliser l'egressIP affectés a leur Node pour sortir du cluster.

Par exemple :

- Pod1 sort avec 192.168.126.10
- Pod4 sort avec 192.168.126.102

Cela s'explique par le label `k8s.ovn.org/egress-assignable: ""` qui permet de définir les noeuds qui vont sortir avec une egressIP.

Pour le Node 2, les choses vont être différentes. En effet, le label `k8s.ovn.org/egress-assignable: ""` n'est pas présent. Ainsi le pod3 va sortir via un NAT d'un des deux autres Nodes. L'election va se faire via un algorithme de choix (round-robin) et donc le traffic sera natté par une des deux IPs des noeuds egress adressables.

Pour les pods qui n'appartiennent pas aux namespaes définis dans l'EgressIP, il sortiront par défaut par l'ip publique du noeud sur lequel ils sont situés.

## Filtrage

Il est possible de filtrer plus finement les droits de sorties des Noeuds via des Network Policies.

### Exemple

Dans cette exemple, seuls les pods backend sont autorisés à sortir vers l'ipblock définis. Les autres pods sont bloqués et ne peuvent pas sortir :

``` yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all-egress
  namespace: my-namespace
spec:
  podSelector: {}  # Applique la règle à tous les Pods du namespace
  policyTypes:
    - Egress  # S’applique au trafic sortant
```

``` yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-egress-backend
  namespace: my-namespace
spec:
  podSelector:
    matchLabels:
      role: backend  # Seuls les Pods "backend" sont autorisés à sortir
  policyTypes:
    - Egress
  egress:
    - to:
        - ipBlock:
            cidr: "203.0.113.0/24"
```

## EgressRouter

On préfère utilise les EgressIPs car ils sont plus simple a mettre en place et ne nécessite pas le déploiement et la gestion de pods. Cependant, on peut considérer les EgressRouter pour les cas suivants : 
- Besoin d'un contrôle très précis sur les destinations (redirection vers IPs et ports spécifiques)
- Transformation du traffic (comm'e le mode HTTP proxy ou DNS proxy)

---

# Tests

## Setup de l'environnement


``` yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: httpd
  name: httpd
  namespace: test-egress
spec:
  replicas: 1
  selector:
    matchLabels:
      app: httpd
  template:
    metadata:
      labels:
        app: httpd
    spec:
      containers:
      - image: docker-redhat.nexus-primaire.integration.ulmj.intranet.justice.gouv.fr/rhel9/httpd-24:9.5
        name: httpd-24
        ports:
          - name: http
            containerPort: 8080
            protocol: TCP

---

apiVersion: v1
kind: Service
metadata:
  labels:
    app: httpd
  name: httpd
  namespace: test-egress
spec:
  ports:
    - name: http
      port: 80
      protocol: TCP
      targetPort: 8080
  selector:
    app: httpd
  type: ClusterIP

---

apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: httpd
  namespace: test-egress
spec:
  host: "httpd-test-egress.apps.ocp-otc-dc1-t11.ocp01.tbot.dc.justice.gouv.fr"
  port:
    targetPort: http
  tls:
    termination: edge
    insecureEdgeTerminationPolicy: Redirect
  to:
    kind: Service
    name: httpd

```

## Setup de l'Egress IP



### Egress IP

![[egressIP.drawio.png]]

``` yaml
apiVersion: k8s.ovn.org/v1
kind: EgressIP
metadata:
  name: egr-test
spec:
  egressIPs:
    - 172.21.68.52
  namespaceSelector:
    matchLabels:
      kubernetes.io/metadata.name: test-egress
```
### Egress Firewall




## Vérification

J'ai configurer l'egressIP pour mon namespace. J'ai fait un requete à mon route qui redirige vers l'egressIP depuis mon pod et j'ai bien l'ip que j'ai configuré en sortie. Cela est vérifiable en allant dans les logs du server httpd `/etc/httpd/logs/modsec_audit.log`

Requète sans l'egressIP : 

![[Pasted image 20250227173222.png]]

On peut verifier que c'est bien l'address IP de notre node : 
Récupération du Node ou tourne notre pod httpd :

![[Pasted image 20250227173358.png]]

Vérification de l'IP du node : 
![[Pasted image 20250227173321.png]]

Requète avec l'egressIP : 

![[Pasted image 20250227173008.png]]