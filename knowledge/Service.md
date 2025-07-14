A service offers a consistent address to access a set of pods. 

# Why do we need it ?

Pod are ephermeral they do not have a long lifetime. 
They are consistently changing and so the ip change also a lot. 
So we can rely on that directly to set up communication within our cluster.


We can create service by using the command below : 
```
kubectl expose 
```

The service use the selector app to know which pods it need to serve.

[[Kubernetes - Port Forwarding]]

# Services Types

## ClusterIP

Default. Creates cluster-wide IP for the service. The IP lives as long as the service live.

## NodePort

Exposes a port on each node allowing direct access to the service through any node's IP address.

We don't use it in production.

## LoadBalancer

Used for cloud providers . Will create an Azure LoadBalancer to route traffic into the cluster.

(can also be used in K3s / Rancher Desktop)