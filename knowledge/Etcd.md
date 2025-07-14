# RKE2 Installation

```sh
# copy archive to machine
tsh scp etcd.tar.gz  outscale@machine:/tmp

# Copy certificate to change permissions
sudo cp /var/lib/rancher/rke2/server/tls/etcd/server-ca.crt /tmp/
sudo cp /var/lib/rancher/rke2/server/tls/etcd/server-client.crt /tmp/
sudo cp /var/lib/rancher/rke2/server/tls/etcd/server-client.key /tmp/

sudo chmod 777 /tmp/server-ca.crt
sudo chmod 777 /tmp/server-client.crt
sudo chmod 777 /tmp/server-client.key

# Env variables
export ETCDCTL_ENDPOINTS="https://10.0.10.11:2379,https://10.0.11.11:2379,https://10.0.12.11:2379"
export ETCDCTL_API=3
export ETCDCTL_CACERT="/tmp/server-ca.crt"
export ETCDCTL_CERT="/tmp/server.crt"
export ETCDCTL_KEY="/tmp/server.key"

# Commands
./etcdctl member list
./etcdctl endpoint status --write-out=table
```