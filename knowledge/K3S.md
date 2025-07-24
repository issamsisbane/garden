# Definition
**K3S** (Rancher Kubernetes Engine 2) est une [[Distribution Kubernetes]] développée par Rancher Labs. Il est conçu pour être sécurisé par défaut, léger et facile à déployer. 

K3S run as a single binary. Its a service ran by [[Systemd]].

When we launch pods in K3S it will spawn containers in the container runtime => [[Containerd]].
A [[Pod]] is like an interface wrapped around [[Containerd]] containers to make easier the management of the containers.

[[K3S vs RKE2]]