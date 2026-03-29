We want to create an Ingress which will allow us to access resources from an url. 

We want to expose our grafana application.

To do that we need : 
	- An Ingress Controller which will enable the Ingress resource within the cluster => Ingressclasses Traefik automatically set by K3S
	- Create an Ingress Resource

Automatically was created a traefik Load Balancer service : 
![[Pasted image 20250207182731.png]]
![[Pasted image 20250207182912.png]]
The Load Balancer Ingress is the ip we use to connect to the raspberrypi.

The ingress controller is going to check for a request he get, if there is a ingress resource to match that request.

We will create an ingress : 

``` yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: linkding
  namespace: linkding
spec:
  ingressClassName: traefik
  rules:
    - host: linkding-test.net
      http:
        paths:
          - backend:
              service:
                name: linkding
                port:
                  number: 9090
            path: /
            pathType: Prefix
```

In order to test if its work, we just have to add this entry to our host file : 
```
192.168.1.14  linkding-test.net # Raspberry pi IP
```

# Exercise

The goal is to expose our grafana application using an ingress by overloading the kube-prometheus-stack `values.yaml`.
We also want to expose it using https and so tls.
See commands in [[Helm]].

## Ingress

We need to add this : 
``` yaml
  values:
    grafana:
      adminPassword: issam
      ingress:
        enabled: true
        ingressClassName: traefik

        hosts:
          - grafana.homelab.net

        tls:
          - secretName: grafana-tls-secret
            hosts:
              - grafana.homelab.net
```
## TLS

Generate a self-signed certificate : 

```
# Generate the private key and certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ./tls.key \
  -out ./tls.crt \
  -subj "/C=US/ST=France/L=Basement/O=Home Lab Heroes Inc./OU=Department of Monitoring/CN=grafana.homelab.net" \
  -addext "subjectAltName=DNS:grafana.homelab.net"
```

Create a secret : 
```
kubectl create secret tls grafana-tls-secret \
  --cert=tls.crt \
  --key=tls.key \
  --namespace=monitoring \
  --dry-run=client \
  -o yaml > grafana-tls-secret.yaml
```

We need to SOPS it : [[Managing Secrets]]