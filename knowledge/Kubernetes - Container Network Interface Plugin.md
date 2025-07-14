CNI plugin provides connectivity to containers
Configures network interfaces in containers
Assignes IP addresses and sets up routes => IPTables on nodes

When we create a cluster from scratch we need to choose a CNI plugins : 
- Cilium
- Calico
- Flannel

To know which CNI our clusters is using. We can access a node of our cluster and look in `/etc/cni`.