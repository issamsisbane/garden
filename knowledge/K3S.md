K3S run as a single binary. Its a service ran by [[Systemd]].

When we launch pods in K3S it will spawn containers in the container runtime => [[Containerd]].
A [[Pod]] is like an interface wrapped around [[Containerd]] containers to make easier the management of the containers.