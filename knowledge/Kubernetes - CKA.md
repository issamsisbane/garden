2 hours duration
La documentation Kubernetes officielle est accessible

> [!NOTE] Reduction Code
> Use code **30KK to get 30% OFF** site-wide on any Linux Foundation Certification.

Helpful references :
- [**Certified Kubernetes Administrator (CKA) official info**](https://www.cncf.io/certification/cka/)
- [**Exam Curriculum (Topics)**](https://github.com/cncf/curriculum)
- [**Candidate Handbook**](https://www.cncf.io/certification/candidate-handbook)
- [**Exam Tips**](http://training.linuxfoundation.org/go//Important-Tips-CKA-CKAD)
- https://kodekloud.com/community/
- [**Kode cloud CKA GitHub Repo**](https://github.com/kodekloudhub/certified-kubernetes-administrator-course)
- [Kode Cloud Notes](https://notes.kodekloud.com/docs/CKA-Certification-Course-Certified-Kubernetes-Administrator/Introduction/Course-Introduction)

# Global Architecture

There is different types of nodes :
- master : Manage, plan schedule, monitor nodes
- worker :Host application as containers 
![[Pasted image 20250901133324.png]]
![[frame_510.jpg]]
## Master

Control planes compoents are used.

### ETCD
We to keep the informations about containers, on which nodes its running, when did it start...

Everything is stored as a key value format

### Kube-Scheduler
Identify the right node to place the container on based on the container resources requirements, the node capacity or other policy and constraints (taints).

### Controller-Manager

There exists differents controllers that are responsible for different area.
#### Node-Controller
Onboarding nodes to clusters
handlesituations where nodes become unavailable
#### Replication-Controller
Ensure that the exact desired number of containers are running at all times in a replication group.

### Kube-apiserver
Primary management compoenent of the cluster

Responsible for orchestrating all operations within the cluster. It exposes the kubernetes API.

Helps monitoring the state of the cluster and make the necessary changes by the controllers.

### Containers Runtime Engine
It must be installed on each node to run containers.
It can be : 
- docker
- containerd
- rocket
- ...

## Worker
### Kubelet

Listens for instruction of the API server. One on each Node.
Deploy or destroy containers on the node as required.
The kubeapi periodically fetch status from the kubelet to monitor the state of the nodes and containers on them.

### Kube-proxy
Ensure that the necessary rules are in place in the worker nodes to allow the containers running on them to reach each other

---

# Containerd vs Docker

It exists different runtime that can be used as a Container Runtime Interface (CRI) for Kubernetes. 
They are all using the Open Container Initiative which give a standard for : 
- imagespec
- runtimespec

It was built by kubernetes to support other tools than docker. 

Docker was still supported via dockershim (a workaround to still get docker work because at the time it wasn't OCI compliant and so wasn't using the CRI).

Since then dockershim was decomissionned because all the others components of docker was taken care directly by kubernetes and so not needed anymore (just the container runtime containerd).

![[Pasted image 20250903072154.png]]
Docker is composed of differents composants and more particularly containerd. containerd is CRI compliant. So containerd is supported but not the whole docker engine since kubernetes v1.24

# Containerd

It works separately from docker now and is supported by the [[CNCF]].

![[Pasted image 20250903073653.png]]

We can install it only without docker. IT comes with a cli tool called `ctr`. It only supports limited features and was made only for debugging containerd. 

`nerdctl` cli tool offers a more user friendly experience and Docker-like experience.

nerdctl supports :
- Docker compose
- Encrypted container images
- Lazy pullin
- P2p image distribution
- Image signing and verifying
- Namesapces in Kubernetes

`crictl` CLI tool provides a CLI for compatible container runtimes.
It installed separately works with all CRI compliant tools.
It was made to inspect et debug container runtimes in worker nodes and not to create containers like nerctl.

`crtictl` is aware of kubernetes pods.


> [!NOTE] crictl & Kubelete 
> If we create something with crictl the kubelet will eventually delete it because its unaware of pods assiocated with the container.

By default kubernetes try to connect to the following CRI endpoints in the same order (no more dockershim) :
- unix://run/containerd/containerd.sock
- unix://run/crio/crio.sock
- unix://var/run/cri-dockerd.sock

---

# ETCD

This is a distributed reliable key-value store that is **simple**, **secure** and **fast**.
Its a project incubated in [[CNCF]].

One element is an object of itself and doesn't follow a strict strucutre like in SQL format.

By default it run on port 2379.
We run etcd by launching : 
```
./etcd
```
And we use the CLI `etcdctl` to interact with it : 
```
./etcdctl put key1 value1                  # set in API Version 2
./etcdctl get key1
```

There are 2 versions of the API of etcd `2` and `3`.
We need to check which version we are using :
```
./etcdctl --version
```
![[Pasted image 20250903075112.png]]

To change the API version we can use the env var :
```
export ETCDCTL_API=3
```
With the release `3.4` the default API Version is set to `3`.

---

# ETCD In Kubernetes

Every informations we see when using the kubectl command comes from the ETCD Cluster. It stores informations about everything in the cluster.

## ETCD Setup

### Manual

1 - Download the binaries :

```
wget -q --https-only "https://github.com/coreos/etcd/releases/download/v3.3.9/etcd-v3.3.9-linux-amd64.tar.gz"
```

2 - Run etcd as a service in the master node : 

![[Pasted image 20250903075659.png]]
`--avertise-client-urls` is the listenning adress of etcd (where INTERNAL_IP is the IP of the Cluster, master node).

#### ETCD HA

In HA mode we would have an etcd cluster with multiple nodes one on each kube master nodes. We need to set the specific servers when running the etcd services.
![[Pasted image 20250903080229.png]]
### Kubeadm

It deploys the etcd server directly for us as a pod in the kube-system namespace.

![[Pasted image 20250903080037.png]]

---

# Kube-apiserver

The kubectl cli tool reach out to kube-apiserver.

```
kubectl get pods
```

The kube-apiserver :
1 - Authenticate the requests
2 - Validates it
3 - Retrieve the data from the ETCD Cluster
4 - Response back with the requested response

We can use the API directly instead of using the kubectl CLI.
```
curl -X POST /api/v1/namespaces/default/pods ...[other]
```

![[Pasted image 20250903081325.png]]

The kube-apiserver :
1 - Authenticate the requests
2 - Validates it
3 - Retrieve the data from the ETCD Cluster
4 - Update ETCD
5 - Kube-scheduler identify the node to create the new pod as he constantly watch the apiserver for new pods to be created. Then he communicates the node back to the apiserver.
6 - The apiserver writes the information to the etcd cluster
7 - The apiserver communicates the information to the kubelet in the right worker node
8 - The kubelet creates the pod on the node
9 - The Container Runtime is instructed to deploy the container image
10 - Once done, the Kubelet send back the information to the apiserver and the apiserver updates the data in the etcd cluster.

The apiserver is at the center of all the communication of the components inside the cluster. It is the only component to interact directly with the etcd cluster.

## Installation

### Manual
It is available as a binary.

1 - Install the binary
```
wget https : //storage.googleapis.com/kubernetes-release/release/vl.13.0/bin/1inux/amd64/kube-apiserver
```

2 - Create a service
```
ExecStart=/usr/10ca1/bin/kube-apiserver \\
--advertise-address=${INTERNAL_IP} \\
--allow-privileged=true \\
--apiserver-count=3 \\
--authorization-mode=Node, RBAC \\
--bind-address=e.ø.ø.ø \\
--client-ca-file=/var/lib/kubernetes/ca. pem \\
- -enable-admission-
plugins—lnitializers , NamespaceLifecyc1e , NodeRestriction , LimitRanger, ServiceAccount , DefaultStorageC1ass , Reso
urceQuota \\
--enable-swagger-ui=true \\
- -etcd-cafile=/var/lib/kubernetes/ca. pem \\
--etcd-certfile=/var/lib/kubernetes/kubernetes. pem \\
--etcd-keyfile=/var/lib/kubernetes/kubernetes-key. pem \\
--etcd-servers=https://127.e.e.1:2379 \\
- -event-ttl=lh \\
--experimental-encryption-provider-config=/var/lib/kubernetes/encryption-config.yaml \\
--kubelet-certificate-authority=/var/lib/kubernetes/ca.pem \\
--kubelet-client-certificate=/var/lib/kubernetes/kubernetes. pem \\
kubelet-client-key=/var/lib/kubernetes/kubernetes-key. pem \\
kubelet-https=true \\
--runtime-config=api/all \\
--service-account-key-file=/var/lib/kubernetes/service-account. pem \\
service-
cluster-iD-ranee=1ø.32.ø.e/24
```
### Kubeadm

Installed automatically as a pod inside the cluster.

## View apiserver config options

### As a pod

Inside the kube-apiserver pod :
```
cat /etc/kubernetes/manifests/kube-apiserver.yaml
```
![[Pasted image 20250903081910.png]]

### As a service

```
/etc/systemd/system/kube-apiserver.service
```
![[Pasted image 20250903081959.png]]

See the process :
```
ps -aux | grep kube-apiserver
```

---

# Kubecontroller Manager

A controller is like an office within the mastership that have is own set of responsibilities.
- monitoring and takes necessary actions when ships arrived, leaves or get destroyed.
- takes cares of containers damaged or falls of ships.

A controller is constantly :
- watching the status of the cluster / particular resources 
- take the necessary actions in a particular situation

## Node controller

- Monitor the states of the nodes
- Take necessary actions to keep the application running

The node controller : 
1. Watch the status of each nodes each 5 seconds through the kube-apiserver. 
2. If a node is unreachable, the node controller wait 40 seconds and set the status as NotReady. 
3. Then it wait 5 min after that it will evict all the pods in the nodes to put them in a healthy node (if there are part of a replicasets ?).

`Node Monitor Period = 5s`
`Node Monitor Grace Period = 40s`
`POD Eviction Timeout = 5min`

## Replication-controller

responsible for monitoring the replicasets and ensure the specified number of pods are available at all times within the sets. If a pod dies it creates another one.

## Other controllers

![[Pasted image 20250903083054.png]]

All the controllers are packaged inside a single process called the Kube-controller-manager

## Installation

### Manual
1 - install the binary
```
wget https://storage.googleapis.com/kubernetes-release/release/vl.13.0/bin/1inux/amd64/kube-contr011er-manager
```

2 - Run as a service
```
ExecStart=/usr/10ca1/bin/kube-contr011er-manager \\
--address=e.e.ø.ø \\
--c1uster-cidr=1ø.20e.e.e/16 \\
--cluster-name=kubernetes \\
--cluster-signing-cert-file=/var/lib/kubernetes/ca. pem \\
--cluster-signing-key-file=/var/lib/kubernetes/ca-key.pem \\
--kubeconfig=/var/lib/kubernetes/kube-controller-manager. kubeconfig \\
-- leader-elect-true \\
-- root-ca-file=/var/lib/kubernetes/ca.pem \\
--service-account-private-key-file—/var/lib/kubernetes/service-account-key.pem
--service-cluster-ip- range—1Ø.32.e.Ø/24 \\
--use-service-account-credentials=true \\
--node-monitor-period=5s
--node-monitor-grace-period=40s
--pod-eviction-timeout=5m0s
--controllers stringS1ice
Default:
A list of controllers to enable.
enables all on-by-default controllers, 'foo' enables the controller
named 'foo', -foo' disables the controller named 'foo' .
All controllers: attachdetach, bootstrapsigner, clusterrole-aggregation, cronjob, csrapproving,
csrcleaner, csrsigning, daemonset, deployment, disruption, endpoint, garbagecollector,
horizontalpodautoscaling, job, namespace, nodeipam, nodelifecycle, persistentvolume-binder,
persistentvolume-expander, podgc, pv-protection, pvc-protection, replicaset, replicationcontroller,
```

We can select which controller to enable.

The config is located at `/etc/systemd/system/kube-controller-manager.service` :
![[Pasted image 20250903083602.png]]
Get the process : 
```
ps -aux | grep kube-controller-manager
```
### kubeadm

It deploys the kube-controller-manager as a pod in the kube-system namespace on the master nodes.

The config is located at `cat /etc/kubernetes/manifests/kube-controller-manager.yaml`
![[Pasted image 20250903083523.png]]

---

# Kube-Scheduler

Its decides which pod go to which node. It doesn't actually places the pod into the nodes that is the job of the kubelet.

It useful to make sure that a specific pod gets deployed to a nodes that has the sufficient capacity to handles it.



The scheduler choose the node by using 2 phases :

We have 4 nodes and we want to deploy a pod with a need of 10 CPU.

![[Pasted image 20250903083946.png]]

1. Filter Nodes

![[Pasted image 20250903084019.png]]

Only those two correspond.

2. Rank Nodes

A priority function is used to assign a score to the node on a scale of 0 to 10. 
For example, it will calculate the ressources that will be free after putting the pod on the node.
![[Pasted image 20250903084247.png]]
In this case the pod on the right wins as he will have the most remaining CPU ressources after running the pod.

It can be customized and we can create our own scheduler.
We have a lot of options we can use to select the node such as :
- Resource Requirements and Limits
- Taints and Tolerations
- Node Selectors/Affinity

## Installation

### Manual

1 - Install the binaries
```
wget https://storage.googleapis.com/kubernetes- release/ release/ vl .13. e/bin/1inux/amd64/kube-schedu1er
```

2 - run the service 
```
ExecStart=/usr/10ca1/bin/kube-scheduler \\
--config=/etc/kubernetes/config/kube-scheduler.yaml \\
```

view the config files :
```
cat /etc/systemd/system/kube-scheduler.service
```

view the process : 
```
ps -aux | grep kube-scheduler
```
### Kubeadm

It is created automatically within a pod inside the kube-system namespace.

We can see the config inside the pod at : 

```
/etc/kubernetes/manifests/kube-scheduler.yaml
```
![[Pasted image 20250903084749.png]]

 Kubelet
 
The captain of a ship. It's responsible for all activities inside a node.
 
It handles : 
- **Register Node :** cluster joining
- **Admin PODs :** load or unload container by unstruction of the master by requesting the CRI to run the container or delete it
- **Monitor Node & PODs :** send back reports at regular times
 
## Installation
 
The kubelet is not installed automatically by kubeadm. We always need to install it manually on the worker nodes.
 
1 - Install the binaries
```
wget https://storage.googleapis.com/kubernetes-release/release/v1.13.0/bin/linux/amd64/kubelet
```
 
2 - Create the service
```
```
 
View the process :
```
ps -aux | grep kubelet
```
 
---
 
# Kube-proxy
 
Every pods can reach any other pod thanks to a pod networking solution deployed in the cluster.

## Pod network

A pod network is an internal virtual network that spands around all the pods within the cluster to reach all the pods connected.

## Service

Instead of using the IP of the pod to reach it within the cluster, we will instead use a service as the IP may changer but the service is like a DNS entry to the pod and so can have a dynamic IP.

The service also has an IP address but it is not a pod, it is not an actual thing running. It doesn't have interfaces or listenning process. It's a virtual components that only lives within the kubernetes memory.
 
The service is accessible accros any nodes within the cluster. This is achieved through kube-proxy.

## Kube-proxy

It is a process that runs on every nodes within the kubernetes cluster. 
Its job is to look for new services. Everytime a new service is created it created the appropriate rules on each node to forward traffic to the services to the backend pods.

One way to achieve this, is using iptables rules. This is an example : 

![[Pasted image 20250905075804.png]]

All the traffic to the service is forwarded to the pods, the rules lives on all nodes of the cluster.

## Install 

### Manual

1 - Install the binary
```
wget https : // storage . googleapis . com/kubernetes-release/release/vl .13. e/bin/1inux/amd64/kube-proxy
```

2 - Launch the service
```
ExecStart=/usr/10ca1/bin/kube-proxy \\
- - config=/var/ lib/ kube- proxy/ kube- proxy-config. yaml
Restart—on-failure
RestartSec=5
```

### Kubeadm

Kube-proxy is deployed as a daemon sets so pods on each nodes in the kube-system ns :
![[Pasted image 20250905080107.png]]

---

# POD

Smallest object we can create in kubernetes. It encapsulates containers.

We scale increasing the numbers of pods and not the number of containers in the pods. This because all the traffic is handle by the pod so it's better to create others pods to have less traffic on each.

A pod has a 1:1 relationship with the containers in it. We do not have multiple instances of the same container in a same pod. But we can have different containers in the same pod. It can be helper containers that does a certain task for the main container (process users data in a file...). The talk using localhost because they share the same network space and they also can easily share the same storage space.

--- 
# ReplicaSets

The replication controller can handle one pod, creating a new one of the previous fails.

Replication controller is the older technologie being replaced by replicasets. 


> [!ATTENTION] IMPORTANT
> THIS IS DIFFERENT FROM THE KUBERNETES CONTROLLER - REPLICATION CONTROLLER [[#Controller-Manager]]


We can create replica set like this : 

![[Pasted image 20250905083716.png]]

We will never use pods or replicaSets directly but more Deployment et StatefulSets which will be using replicaSets.

To scale replicaset we can use : 

```sh
kubectl replace -f replicaset-definition.yml
kubectl scale --rep1icas=6 -f replicaset-definition.yml
kubectl scale --rep1icas=6 replicaset myapp-replicaset
```
---

# Deployment

![[Pasted image 20250905085017.png]]
- Rolling updates
- Pause / Resume Changes
- Rollback

The Deployment automatically creates a replicaset.

Create a deployment :
```
kubectl create deployment --image=nginx nginx --replicas=4 --dry-run=client -o yaml > nginx-deployment.yaml
```

--- 

# Service

## Types

### NodePort

Use the ip of **any node of the cluster**, if we can access the node we can access the service using the right port from outside.

![[Pasted image 20250905091015.png]]

If we do not set a port it will be the same as targetport.
If we do not set a NodePort it will be one random in the range 30000-32767
``` yaml
apiVersion: VI
kind: Service
metadata :
	name : myapp—service
spec :
	type : NodePort
	ports : 
		port: 80
		targetPort: 80
		nodePort: 30008
	selector:
		app: myapp
		type: frontend
```
![[Pasted image 20250905090333.png]]
![[Pasted image 20250905090423.png]]

The traffic is distributed randomly.
![[Pasted image 20250905090900.png]]

### ClusterIP

Create a virtualIP within the cluster accessible internally only.
We use this to make the pods of the cluster communicates between them
![[Pasted image 20250905091155.png]]

``` yaml
apiVersion: VI
kind: Service
metadata :
	name: back—end
spec :
	type: Cluster TP
	ports :
	— targetPort: 80
	  port: 80
	selector :
		app: myapp
		type: back—end
```

### LoadBalancer

Load balancer for apps in supported cloud providers.

If we want to expose our applications to the web, we won't create a NodePort services and give all the nodes IPs to access it.

We could create a specific VM with a reverse-proxy to redirect traffic to the node from an url.

![[Pasted image 20250905091554.png]]

If we are on a Cloud we can use LoadBalancer Service to use the native Load Balancers of the cloud Platform we are on (AWS, AZURE, GCP).

If we are not in a supported cloud provider, the service created will juste be a NodePort service.

``` yaml
apiVersion: vl
kind: Service
metadata :
	name: myapp—service
spec:
	type: LoadBa1ancer
	ports :
	— targetPort: 80
	  port: 80
	  nodePort: 30008
```

To get endpoints of a service we do : 
```
k get endpoints <svc-name> -n <ns>
```

---

# Namespaces

Analogy :
![[Pasted image 20250905095407.png]]

Set the namespaces globally for the current context :
```
kubectl config set-context $(kubectl config current-context) --namespace-dev
```

## Ressources quotas

Limit ressource inside a namespaces
```
apiVersion: vl
kind: ResourceQuota
metadata :
	name : compute—quota
	namespace : dev
spec :
	hard :
		pods : "10"
		requests . cpu: "4"
		requests . memory: 5Gi
		limits . cpu: "10"
		limits . memory: IOGi
```

---

# Imperative vs Declarative

## Imperative

We would do all the steps manually or describe specifically what to do.

With kubernetes running kubectl commmand to manage ressources is imperative. It will be useful during the exams but in the real worlds we don't want to use it. 
Indeed, if we are not alone working on the cluster if we just run commands like this, we cannot know all the commands that was launch to get to the current state.

![[Pasted image 20250906154856.png]]

## Declarative

We specify what we want and the system will know what to do.

In Kubernetes we would use manifests and then we would use the command : 

```
kubectl apply -f file.yaml
```

Then creation or update would be handle by the api server directly without us specifying exactly what we want. It will check if the object exist or no to create or update the ressource according to the manifest.

At the contrary of imperative approach, it is easy to see directly what the manifest is doing and so easy to work with other people with git for example.

---

# Certification Tips - Imperative Commands with Kubectl

While you would be working mostly the declarative way - using definition files, imperative commands can help in getting one time tasks done quickly, as well as generate a definition template easily. This would help save considerable amount of time during your exams.

Before we begin, familiarize with the two options that can come in handy while working with the below commands:

`--dry-run`: By default as soon as the command is run, the resource will be created. If you simply want to test your command , use the `--dry-run=client` option. This will not create the resource, instead, tell you whether the resource can be created and if your command is right.

`-o yaml`: This will output the resource definition in YAML format on screen.

  

Use the above two in combination to generate a resource definition file quickly, that you can then modify and create resources as required, instead of creating the files from scratch.

  

#### POD

**Create an NGINX Pod**

`kubectl run nginx --image=nginx`

  

**Generate POD Manifest YAML file (-o yaml). Don't create it(--dry-run)**

`kubectl run nginx --image=nginx --dry-run=client -o yaml`

  

#### Deployment

**Create a deployment**

`kubectl create deployment --image=nginx nginx`

  

**Generate Deployment YAML file (-o yaml). Don't create it(--dry-run)**

`kubectl create deployment --image=nginx nginx --dry-run=client -o yaml`

  

**Generate Deployment with 4 Replicas**

`kubectl create deployment nginx --image=nginx --replicas=4`

  

You can also scale a deployment using the `kubectl scale` command.

`kubectl scale deployment nginx --replicas=4`

**Another way to do this is to save the YAML definition to a file and modify**

`kubectl create deployment nginx --image=nginx --dry-run=client -o yaml > nginx-deployment.yaml`

  

You can then update the YAML file with the replicas or any other field before creating the deployment.

  

#### Service

**Create a Service named redis-service of type ClusterIP to expose pod redis on port 6379**

`kubectl expose pod redis --port=6379 --name redis-service --dry-run=client -o yaml`

(This will automatically use the pod's labels as selectors)

Or

`kubectl create service clusterip redis --tcp=6379:6379 --dry-run=client -o yaml` (This will not use the pods labels as selectors, instead it will assume selectors as **app=redis.** [You cannot pass in selectors as an option.](https://github.com/kubernetes/kubernetes/issues/46191) So it does not work very well if your pod has a different label set. So generate the file and modify the selectors before creating the service)

  

**Create a Service named nginx of type NodePort to expose pod nginx's port 80 on port 30080 on the nodes:**

`kubectl expose pod nginx --type=NodePort --port=80 --name=nginx-service --dry-run=client -o yaml`

(This will automatically use the pod's labels as selectors, [but you cannot specify the node port](https://github.com/kubernetes/kubernetes/issues/25478). You have to generate a definition file and then add the node port in manually before creating the service with the pod.)

Or

`kubectl create service nodeport nginx --tcp=80:80 --node-port=30080 --dry-run=client -o yaml`

(This will not use the pods labels as selectors)

Both the above commands have their own challenges. While one of it cannot accept a selector the other cannot accept a node port. I would recommend going with the `kubectl expose` command. If you need to specify a node port, generate a definition file using the same command and manually input the nodeport before creating the service.

#### **Reference:**

[https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands)

[https://kubernetes.io/docs/reference/kubectl/conventions/](https://kubernetes.io/docs/reference/kubectl/conventions/)

---

## Create a pod with a label

```
k run redis --image=redis:alpine --labels="tier=db"
```
## Expose a service

```
k expose pod redis --name redis-service --port=6379 --type=ClusterIP
service/redis-service exposed
```
## Create a deployment with replicas

```
k create deploy webapp --image=kodekloud/webapp-color --replicas=3
```

## Create a pod expose it through a service in 1 command

```
kubectl run httpd --image=httpd:alpine --expose=true --port=80
```

---
# Kubectl Apply

When we create a ressources within the `kubectl apply` command , it creates converts the manifest to json and store within the resources in the annotations field `kubectl.kubernetes.io/last-applied-configuration`. This allow the `kubectl` command to know what has changes when we call the command again to remove or create missing fields.

![[Pasted image 20250906161312.png]]


> [!ATTENTION] DO NOT MIX IMPERATIVE AND DECLARATIVE
> Last applied config only works with `apply`. `create` and `replace` doesn't use this so if the start using declarative mode we should stick to it and mix imperative and declarative

https://kubernetes.io/docs/tasks/manage-kubernetes-objects/declarative-config

---

# Schedulers

1. The scheduler constantly monitor all the pods.
2. It takes those pods who now becomes candidates for scheduling.
3. It then identifies the right pod for the node using a particular scheduling algorithm
4. It schedules the pod on the node by setting the nodeName properties on the ressource ==and create a binding object ?==

If there are no scheduler for the pod, the pod will be stuck in a `Pending` state.
We can easily set the nodeName property ourselves to schedule the pod to a specific node. We can only do this if the pod doesn't exist yet because kubernetes doesn't allow to change the nodeName property of a pod.

``` yaml
apiVersion: v1
kind: Pod
metadata :
	name: nginx
	labels :
		name: nginx
spec :
  containers :
	- name: nginx
	  image: nginx
	  ports :
	  - containerPort: 8080
  nodeName: node 02
```

If the pod already exists, we can do what the scheduler does behind the scene and create a binding resource connecting the node and the pod : 

``` yaml
apiVersion: vl
kind: Binding
metadata:
	name: nginx
target:
	apiVersion: vl
	kind: Node
	name: node02
```

and then send it through the api selecting the pod we want using the url path: 

``` sh
curl --header "Content-Type : application/json" --request POST --data '{" apiVersion":"vl",""kind": "Binding"...}
http://$SERVER/api/v1/namespaces/defau1t/pods/$PODNAME/binding/
```

---

# Labels & Selectors

labels allow to class ressources and select them using selectors from others resources.

We can specify labels like this : 

``` yaml
metadata:
	labels:
		app: App1
```

We can retrieve it using : 

```
kubectl get pods --selector app=App1
```

Compter les ressources en excluant les entetes et les lignes vides : 
```
kubectl get all --selector="env=prod" | grep -v '^NAME' | grep -v '^$' | wc -l
```

```
kubectl get pods --selector env=dev --no-headers | wc -l
```
# Annotations

There are use to give information about the ressource like : 
- version
- name
- build information

---

# Taints and Tolerations

**Taints** are put on a **Node** restricting pods to be scheduling.
**Tolerations** are put on a **Pod** to be allowed to be scheduling on nodes with taints.

If we taint Node1 with the taint blue then only the D pod with toleration blue can be schedule in the node.

![[Pasted image 20250906182254.png]]

> [!IMPORTANT]
> Taint and tolerations don't garantee that a pod will be schedule on a specific nodes but more the restrict and choose specific pods with certain tolerations to be schedule on nodes. 

Indeed the D pod could also be schedule in Node2 or Node3 as they don't have any Taint.

Specify a taint for a node : 
```
kubectl taint nodes node-name key=value:taint-effect
```

Example : 
```
kubectl taint nodes node1 app=blue:NoSchedule
```

It exists 3 taints effects : 
- **NoSchedule** : Pods without the correct tolerations will not be schedule in the node in the future
- **PreferNoSchedule** : If the pods can be schedule to other node it will but if not it will be schedule on the node
- **NoExecute** : Pods without the correct tolerations will not be schedule in the node in the future and current running pods will be deleted (This supposed that pods from a deployment will be reschedule in others pods but pods only will be deleted).

Specify a tolerations :
``` yaml
apiVersion :
kind: Pod
metadata :
	name: myapp—pod
spec :
	containers :
	— name: nginx—container
	  image: nginx
	tolerations :
	- key : "app"
	  operator: "Equal"
	  value: " blue"
	  effect:" NoSchedu1e
```


---

# Master Node

The Master Node is a node as much as other "workers nodes" so they could in theory have pods being scheduled. 

The master Node host the control plane and so as best practices we prefer not to schedule pods in it.

There is a taint on the master node to prevent pods form being scheduled : 

![[Pasted image 20250906183600.png]]

---

# Find in resources

Find image in resource using yq : 
``` yaml
k get pod kube-scheduler-controlplane -n kube-system -o yaml | yq ".spec.containers[0].image"
```

Find image in resource using jq :
``` yaml 
k get pod kube-scheduler-controlplane -n kube-system -o json | jq ".spec.containers[0].image"
```

Find images of all containers in a pod : 
``` yaml
kubectl get pod mon-pod -o json | jq -r '.spec.containers[].image'
```

If we don't have jq or yq in the cli we can just use jsonpath : 

``` yaml
kubectl get pod mon-pod -o jsonpath='{.spec.containers[*].image}{"\n"}'
```

Query many ressources : 
``` yaml
kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{": "}{.spec.nodeName}{"\n"}{end}
```

For taints we can do a describe instead of a -o yaml and just use grep : 
``` yaml
kubectl describe node node01 | grep Taints
```

--- 

# Node Selectors

We need to label our nodes : 
```
kubectl label nodes <node-name> <key>=<label>
```

```
kubectl label nodes node-1 size=Large
```

We can add a node selector to our pod meaning that it will be scheduled on the node or nodes with the particular label : 

``` yaml
apiVersion: v1
kind: Pod
metadata:
	name: myapp—pod
spec:
	containers:
		- name: data—processor
		  image: data—processor
	nodeSelector:
		size: Large
```

## Limitations

We cannot say :
- Schedule on node that have the label Large OR Medium
- Scdule on node that is NOT Small

---

# NodeAffinity

It allow to specify on which node a pod will be schedule using labels but allowing us to use more complex expression such as OR, AND, NOT...

The syntax is a bit more complex although : 

``` yaml
apiVersion:
kind :
metadata :
	myapp—pod
spec:
  containers :
	- name: data-processor
	  image: data—processor
  affinity :
    nodeAffinity :
	  requiredDuringSchedulingIgnoredDuringExecution :
        nodeSelectorTerms :
        - matchExpressions :
          - key: size
            operator : In
            values :
            - Large
```

``` yaml
    nodeAffinity :
	  requiredDuringSchedulingIgnoredDuringExecution :
        nodeSelectorTerms :
        - matchExpressions :
          - key: size
            operator : NotIn
            values :
            - Small
```

We can see the documentation for others operators.
https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#node-affinity

## Node Affinity Types

What happens if we change the label of a node ? 
What happens if no nodes fit the nodeAffinity ? 

The node affinity type answer those questions : 
- `requiredDuringSchedulingIgnoredDuringExecution`
- `preferredDuringSchedulingIgnoreDuringExecution`

**Scheduling** meaning the pod **is not created** yet.
**Execution** meaning the pod **is created** and changed has been made to nodeaffinity or the nodes labels.

We can see that both node affinity types available cannot allow change to pods during execution.

### In the future

In the future this is announced : `requiredDuringSchedulingIgnoredDuringExecution`

If we remove the label from the node when the pod is running it. The pod will be evicted from the node.

---

# Resource Limits

## Request

We can set requests to containers, it is the initial amount use by the container : 

``` yaml
spec:
  containers:
  - name: simple
    image: simple
    resources:
	  requests:
	    memory: "4Gi"
	    cpu: 2
```

### CPU

1 CPU is 1 vCPU in all cloud providers : 
- 1 AWS vCPU
- 1 GCP Core
- 1 Azure Core
- 1 Hyperthread

### Memory

![[Pasted image 20250906195021.png]]

## Limits

This is the maximum amount of CPU and RAM the container can use : 

``` yaml
spec:
  containers:
  - name: simple
    image: simple
    resources:
	  requests:
	    memory: "4Gi"
	    cpu: 2
	  limits:
	    memory: "6Gi"
	    cpu: 3
```

If we exceed the limit : 
- **CPU** : The system throttle the CPU so it can't go beyond the specified limit
- **Memory** : A container can use more memory than specified in the limit but it will be terminated with a status of OOM (Out Of Memory)

## Default Behavior

By default there are no Requests or Limits for the pods in the cluster.

If we put Limits but no Requests, the Requests is automatically set to the same Limits.

Setting requests assure that it will be schedule and have the requested ressources and that it will not be use by another pod.

Setting no limits but requests allow a pod to use as much resources as he need as long as all requests of others pods are fullfilled : 

![[Pasted image 20250906200028.png]]

## LimitRange

It allow to create default limits and requests to containers within the same namespace : 

``` yaml
apiVersion: vl
kind: LimitRange
metadata :
	name: cpu-resource-constraint
spec :
  limits :
  - default:
      cpu: 500m
    defaultRequest :
      cpu: 500m
    max:
     cpu: "1"
    min:
     cpu: 100m
    type : Container
```

``` yaml
apiVersion: vl
kind : LimitRange
metadata : 
	name : memory-resource-constraint
spec :
  limits:
  - default:
      memory: IGi
    defaultRequest :
      memory: IGi
    max :
      memory: IGi
    min:
      memory : 50ØMi
    type: Container
```

## Resource Quotas

This allow to set total limits and requests on cpu and memory  within the namespaces : 
``` yaml
apiVersion: v1
kind: ResourceQuota
metadata :
	name: my-resource-quota
spec:
	hard:
		requests.cpu: 4
		requests.memory: 4Gi
		limits.cpu: 10
		limits.memory : 10Gi
```

--- 

# A quick note on editing Pods

#### Edit a POD

Remember, you CANNOT edit specifications of an existing POD other than the below.
- spec.containers[*].image
- spec.initContainers[*].image
- spec.activeDeadlineSeconds
- spec.tolerations

1. We need to extract the pod definition in YAML format to a file using the command 
2. Then make the changes to the exported file using an editor (vi editor). Save the changes
3. Then delete the existing pod
4. Then create a new pod with the edited file

---

# Debugging pods

If we need to debug a pod from a deployment. We can remove all the labels of the pod which will make the deployment recreate the pod and create a sort of quarantine zone for the pod to debug it. Free from traffic

---

# Daemon Sets

It creates one copy of a pod on each node of the cluster.
It ensures that at any time a copy of the pod is always on all nodes.

It can be useful for monitoring or logging purpose. ==Prom and loki ?==

For example the kube-proxy must be deployed on each node so a Daemonset is used.

``` yaml
apiVersion: apps/vl
kind: DaemonSet
metadata:
	name: monitoring—daemon
spec :
	selector :
		matchLabe1s :
			app: monil-oring—agenL
	templa te :
		metadata :
			labels :
				app: monitoring—agent
	spec :
		containers :
		— name: monitoring—agent
		  image: monitoring—agent
```

behind the scenes the kubernetes use the default scheduler and NodeAffinity rules to make sure on pod is scheduled on each node.


> [!IMPORTANT]
> If we use NodeAffinity rules, taints and tolerations then the pods of the daemonsets will only be scheduled on the matching nodes


> [!TIPS] Tip
> We can create a deployment using the command : 
> `kubectl create deploy test --image=nginx -o yaml --dry-run=client > test.yaml` and edit the manifest to create a Daemonset.
> We cannot create a Daemonset using the `kubectl create` directly.
i

---

# Static Pods

If we were to have only one node with a kubelet and no other component of the kubernetes cluster. We could create pods (only pods) by adding the yaml manifests in the directory `/etc/Kubernetes/manifests` to create static pods.

![[Pasted image 20250907081611.png]]
![[Pasted image 20250907081649.png]]

The cluster is aware of the pods created this way. Indeed we can do : 
```
kubectl get pods
```

And we will see our static pods. But we can only view the pod and his configuration and not edit or delete it from the kube-apiserver and from the kubectl cli.


> [!IMPORTANT] 
> We can identify static pods by their name : `name-nodename`
> Or we can see in the pods definition this : 
> ![[Pasted image 20250907084306.png]]


> [!IMPORTANT]
> We can find the configfile where the directory for static pods are set in `/var/lib/kubelet`

## Use Case

### Deploy control plane component

1. Install kubelets on all nodes
2. Create and place manifests on the right directory

![[Pasted image 20250907082109.png]]

We have our control planes components running and they will be restarted if they crash.


---

# Priority Classes

In the cluster we have workloads that are more important to others and that need to run no matter what. An example is the control plane component. We can define priority classes for that. 
![[Pasted image 20250907085129.png]]
*The names at left is just for explanatory reasons it doesn't exists by default within kubernetes*

To list priority classes  :
![[Pasted image 20250907085253.png]]

To create Priority Class : 
``` yaml
apiVersion: scheduling . k8s . io/vl
kind: PriorityCIass
metadata :
	name: high—priority
value: 1000000000
description : "Priority class for mission critical pods"
globalDefault: true # Defined global default priority of all the pods
preemptionPolicy: PreemptLowerPriority 
# Defined what to do if ther is no resources free and that there exists lower priority workloads. 
# In this case, it delete the lower priority to run.
# Can also be set to never where it wont delete other pods if there are no resources left.
```

To assign it to a pod : 
``` yaml
apiVersion: vl
kind: Pod
metadata :
	name: nginx
	labels :
		name: nginx
spec :
	containers :
	— name: nginx
	  image: nginx
	  ports :
		— containerPort: 8080
	priorityC1assName: high—priority:
```

 Compare priority classes of pods : 
 ```
 kubectl get pods -o custom-columns="NAME:.metadata.name,PRIORITY:.spec.priorityClassName"
 ```

---

# Multiple Schedulers

We can create custom schedulers to meet our needs and deploy it to our clusters.
We can use specific schedulers for specific applications.
We can have multiple schedulers at the same time.

The default scheduler is `default-scheduler`.

To create a scheduler : 

``` yaml
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration
profiles :
— schedulerName : my—scheduler
```

To select a scheduler from a pod : 

``` yaml
apiVersion : v1
kind: Pod
metadata :
	name: nginx
spec :
	containers :
	-	image: nginx
		name: nginx
	schedulerName: my—custom—scheduler
```

To get the logs of the scheduler : 
![[Pasted image 20250907105342.png]]
## Deploy as Service

We would deploy the scheduler by downloading the binaries and launch another service for this particular scheduler.

![[Pasted image 20250907104317.png]]

## Deploy as Pod

This is done differently using kubeadm.

``` yaml
apiVersion: vl
kind: Pod
metadata:
name: my-custom—scheduler
namespace: kube-systetn
spec:
containers:
— command:
	- kube-scheduler
	- --address=127.0.0.1
	- --kubeconfig=/
	- --config=/etc/kubernetes/my-scheduler-config.yaml
  image: k8s.gcr.io/kube-scheduler-amd64:v1.11.3
  name: kube-scheduler
```

``` yaml
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration
profiles :
— schedulerName : my—scheduler
leaderElection: # If we have multiple instances of the same scheduler on different nodes.
	leaderElect: true
	resourceNamespace: kube-system
	resourceName: lock-object-my-scheduler
```

---

# Scheduler Profiles

#ToReview
## Scheduling

When we want to create a pod,
1. **Scheduling Queue**: it will be added first to a Scheduling queue sorted by priorityClass - ==PrioritySort Plugin==
2. **Filtering**: The nodes with the capacity sufficient for the nodes will be kept - ==NodeResourceFit,  NodeName, NodeUnschedulable Plugin==
3. **Scoring**: A note will be attributed to each node on a scale of 0 to 10 - ==NodeResourcesFit, ImageLocality Plugin== *For the scoring if the image is present on the node ?*
4. **Binding**: The pod is bound to the node with the higher score - ==Default binder Plugin==

## Extensions and plugins

The plugins are bound to extensions (some sort of hooks) : 
![[Pasted image 20250907111154.png]]

We can customize the scheduling process as much as we want to meet our needs.

## Profiles

We can create different schedulers by deploying another one using is own binary like this : 
![[Pasted image 20250907111830.png]]

But we can also use profiles to create different schedulers using the same binary : 

![[Pasted image 20250907111904.png]]

And we can custom them like we want by enabling or disabling plugins.

![[Pasted image 20250907112017.png]][https://github.com/kubernetes/community/blob/master/contributors/devel/sig-scheduling/scheduling_code_hierarchy_overview.md](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-scheduling/scheduling_code_hierarchy_overview.md)

[https://kubernetes.io/blog/2017/03/advanced-scheduling-in-kubernetes/](https://kubernetes.io/blog/2017/03/advanced-scheduling-in-kubernetes/)

[https://jvns.ca/blog/2017/07/27/how-does-the-kubernetes-scheduler-work/](https://jvns.ca/blog/2017/07/27/how-does-the-kubernetes-scheduler-work/)

[https://stackoverflow.com/questions/28857993/how-does-kubernetes-scheduler-work](https://stackoverflow.com/questions/28857993/how-does-kubernetes-scheduler-work)

---

# Admission Controllers

#ToReview 

![[Pasted image 20250907112325.png]]
When using the kube-apiserver directly or through the `kubectl` cli. An authentication process happens. The authentication is done using certificates.
It thens go to an authorization process where the user roles and permissions are checked to ensure it can launch the command. 

![[Pasted image 20250907113355.png]]

There are needs to go deeper and have more complex verification on the requests before creating it : 
- Verify the podSecurityContext
- Ensure we do not use public image registries...

All of those can be done using Admission Controllers. Like [[Kyverno]].

There are built-ins admissions controllers but also dynamic admissions controllers that are custom.

We can see enabled admission controllers by running the command : 
``` sh
kubectl exec kube-apiserver-controlplane -n kube-system -- kube-apiserver -h | grep enable-admissions-plugins
```
![[Pasted image 20250907113553.png]]

To Add an admissions controller : 
![[Pasted image 20250907113720.png]]
Since the `kube-apiserver` is running as pod you can check the process to see enabled and disabled plugins.

```
ps -ef | grep kube-apiserver | grep admission-plugins
```

![[Pasted image 20250907115318.png]]
There are two types of dynamic admission controllers extending the API via webhooks : 
- **MutatingAdmissionWebhook**: can modify a request.
- **ValidatingAdmissionWebhook**: can validate whether the request should be allowed to be created or not.

We can do both within the same controller.

First we mutate and then we validate.

![[Pasted image 20250907115854.png]]

These dynamic admission controllers are webhook that send the informations to a server which will evaluate the request and send back a response. 

We can make our custom controller  to send request to our Admission Webhook Server with our own code and logic that is inside or outside the kubernetes cluster.

![[Pasted image 20250907120341.png]]

https://kyverno.io/docs/introduction/admission-controllers/

---

# Monitoring

In a kubernetes cluster we want to monitor : 
- Nodes : 
	- CPU
	- RAM
	- DISK
- Pods :
	- CPU
	- RAM
	- DISK

We need somehting to monitor and store this data.

It exists many differents tools to do this. 
The default one is Metrics Server (only one per cluster)
The Metrics Server is **only IN-MEMORY** and **doesn't store** data on disk.

So we can't see historical data.

The Kubelet as a component call **cAdvisor**. It is responsible for collecting metrics from pods and expose them through the kubelet api to make metrics available to the metrics server.

## Deployment 
![[Pasted image 20250907121855.png]]

## Use

We can then use it : 

```
kubectl top node
```

```
kubectl top pods
```

---

# Logging

We can see the logs by using this command which will print the stdout of the container : 

```
kubectl logs -f pod containername
```

We must specify the container if there are many of them within the pod.

---

# Rolling Updates and Rollbacks

When we create a deployment it triggers a rollout and create a revision (revision 1).
If we update our deployment a new rollout and so a new revision (revision 2).

It allows to track the changes made to the deployment and allows to rollback to a previous version if there are any problems after an update.

We can get the status of the current rollout using : 

``` bash
kubectl rollout status deployment/myapp-deployment
```
![[Pasted image 20250908072136.png]]

We can get rollout history by using : 

``` bash
kubectl rollout history deployment/myapp-dep1
```

## Deployment Strategy

When we update a deployment it exists diffferent strategies to create the new pods.
Under the hood a new replica sets is created and the old replicaset is scale down to 0.
### Recreate

All the previous pods are deleted and after they are recreated.


### Rolling Updates

This is the default strategy.

The new pods are created **one by one** along side the old pod, as soon as they are started then the old pods are deleted. Only one pod can be down at times.

> Deployment ensures that only a certain number of Pods are down while they are being updated. By default, it ensures that at least 75% of the desired number of Pods are up (25% max unavailable).

> Deployment also ensures that only a certain number of Pods are created above the desired number of Pods. By default, it ensures that at most 125% of the desired number of Pods are up (25% max surge).

## Rollback

To rollback to the previous version : 
```
kubectl rollback undo deploymeny/myapp-deployment
```

We can also rollback to older version. Under the hood it will bring back the old replicaset and scale down the new one.

---
# Command containers

## Docker
![[Pasted image 20250908074815.png]]

In the first if we want to overrides to 10 we need to set back the sleep command.
With the entrypoint, no need.

WE need to set the CMD after the entrypoint the have by defaults args.
![[Pasted image 20250908074925.png]]
## Kubernetes
The command field overrides the entrypoint field.
The args field overrides the CMD field.

![[Pasted image 20250908074700.png]]

---

# ENV

#ToReview 

![[Pasted image 20250908075835.png]]![[Pasted image 20250908075853.png]]
![[Pasted image 20250908081028.png]]![[Pasted image 20250908081940.png]]

Using a secret from a volume, each attributes of the secrets will be created as a file.


> [!DANGER]
> A Secret is only encoded and not encrypted meaning anyone can read it if it has access to the cluster. It is also stored in unencrypted format in etcd at rest.
> https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/
> https://www.udemy.com/course/certified-kubernetes-administrator-with-practice-tests/learn/lecture/34549248#overview

![[Pasted image 20250908083357.png]]

Remember that secrets encode data in base64 format. Anyone with the base64 encoded secret can easily decode it. As such the secrets can be considered as not very safe.

The concept of safety of the Secrets is a bit confusing in Kubernetes. The [kubernetes documentation](https://kubernetes.io/docs/concepts/configuration/secret) page and a lot of blogs out there refer to secrets as a "safer option" to store sensitive data. They are safer than storing in plain text as they reduce the risk of accidentally exposing passwords and other sensitive data. In my opinion it's not the secret itself that is safe, it is the practices around it. 

Secrets are not encrypted, so it is not safer in that sense. However, some best practices around using secrets make it safer. As in best practices like:

- Not checking-in secret object definition files to source code repositories.
    
- [Enabling Encryption at Rest](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/) for Secrets so they are stored encrypted in ETCD. 
    

  

Also the way kubernetes handles secrets. Such as:

- A secret is only sent to a node if a pod on that node requires it.
    
- Kubelet stores the secret into a tmpfs so that the secret is not written to disk storage.
    
- Once the Pod that depends on the secret is deleted, kubelet will delete its local copy of the secret data as well.
    

Read about the [protections](https://kubernetes.io/docs/concepts/configuration/secret/#protections) and [risks](https://kubernetes.io/docs/concepts/configuration/secret/#risks) of using secrets [here](https://kubernetes.io/docs/concepts/configuration/secret/#risks)

---

# Multi container pods

![[Pasted image 20250908084956.png]]

- **Co-located Containers :** share the same lifecycle, volume, network and work together
![[Pasted image 20250908085510.png]]
- **Init-containers :** does a task before launching other container (waiting for a database to be ready). Init containers are started in order of there definitions in the array.
![[Pasted image 20250908085457.png]]
- **Sidecar containers :** starts before the other containers and stop after (istio and encrypted communication)
![[Pasted image 20250908085441.png]]

Example : 
![[Pasted image 20250908085605.png]]


> [!NOTE]
> Practice Test - Multi Container PODs in kodekloud show how to connect a pod elastic search and kibana with logs viewing.

Liveness & Probes are not in the CKA exams but in the CKAD exam.

---

#ToReview 
ATOS

---

# Vertical Pod Autoscaler

VPA doesn't come by default in kubernetes, so we have to install it manually : 

```
kubectl apply -f https://github.com/kubernetes/autoscaler/releases/latest/download/vertical-pod-autoscaler.yaml
```

![[Pasted image 20250909210434.png]]

We can only create it decalratively.

``` yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticatPodAutoscater
metadata:
	name: my-app-vpa
spec:
	targetRef:
		apiVersion: apps/vl
		kind: Deployment
		name: my-app
	updatePolicy:
		updateMode: "Auto"
resourcePolicy:
	containerPoticies :
	- containerName: "my-app"
	  minAtIowed:
	   cpu: "250m"
	  maxAttowed :
	   cpu: "2"
	controlledResources : ["cpu"]
```

There exists 4 modes : 

![[Pasted image 20250909210857.png]]

![[Pasted image 20250909211112.png]]

- Flask application is running with only 1 replica pod.
- The Vertical Pod Autoscaler (VPA) needs to evict (remove) the existing pod to create a new one with updated resource settings.
- Kubernetes has a safety feature that prevents removing the last pod of a deployment to avoid service downtime.
- When you have only 1 replica and VPA tries to evict it, Kubernetes blocks this action with the error message: "too few replicas".
- VPA wants to optimize your pod's resources but cannot because Kubernetes is protecting your service availability.
- As a result, VPA cannot apply its resource recommendations, and application cannot benefit from automatic resource optimization.

#ToReview 
# VOIR MI resources c'est quoi bytes

---

#  Operating System Upgrade

When a pod go offline because a node is taken down, it has 5 minutes to be back. Otherwise the master node consider it dead.
It is the **pod-eviction-timeout**.

If the pod was part of a replica set, it will be schedule on another pod. If not it's just gone.

If the node come back online after the eviction timeout, then it will be blank wanting for scheduling be the master node.

So if we need to do an update. We will obviously do it nodes by nodes. We can wait for the 5 minutes for the pods to be reschedule. But we are not sure if it will be no problem and we have to be sure that a 5 minutes with no services it acceptable.

A safer way to do this is to use the `drain` command. It will set the node has **unschedulable** and all the workload will be **gracefully terminated** and so **rescheduled** and placed on other nodes.

``` bash
kubectl drain node-1
```

After the update of the node we to `uncordon` it so it can be schedulable again : 

``` bash
kubectl uncordon node-1
```


> [!IMPORTANT]
> The pods present before the update will not come back to this node. There was a new scheduling so only new workloads can be schedule on this node now.

It exist also the command `cordon`, it will just set the node as unschedulable preventing new workload to be scheduled but keeping the current workload in the node : 

``` bash
kubectl cordon node-2
```

When we want to `drain` a node and a daemonset exists we need to use this command (if we uncordon the node the pod from the daemonset will be created) : 

``` bash
kubectl drain node01 --ignore-daemonsets
```

When we want to drain a node and a pod exist without a deployment or replicaset we will have an error preventing us to lose to workload for ever (we can force it though) : 

![[Pasted image 20250913171918.png]]

---

# Kubernetes Releases

A version is composed of : 
![[Pasted image 20250913172321.png]]
- minors every few months : feature and functionalities
- patch more often : correct bugs

1. **Alpha**: All the features and functionalities comes in a alpha release first. Where new features are disabled by default and need a flag to enable them.
2. **Beta**: The features are enabled by default
3. **Stable**

All the components of the control plane have the same versions : 
- kube-apiserver
- Controller-manager
- kube-scheduler
- kubelet
- kube-proxy
- kubectl

But there are components which are separated projects and so have differents versions numbers : 
- etcd cluster
- CoreDNS

The kubernetes versions releases notes gives the specification about supported version of other applications such as the above ones.

---

# Cluster Upgrade Process

The components of the control can have a difference in version but not a later version than the kube-apiserver. 

The schema below show the version gap allowed : 
![[Pasted image 20250913173021.png]]

## Best time to update

If we are in 1.10 and the current version of kubernetes is 1.12 so the version supported by kubernetes are 1.10, 1.11, 1.12 But when the 1.13 is released the versions supported are 1.11, 1.12 and 1.13.


> [!IMPORTANT] BEST TIME TO UPGRADE
 > The best time to update is before the release of the version that will make our version obsolete so juste before 1.13 in this case.

We will not update straight from 1.10 to 1.13 but one minor version by one minor version : 
- 1.10 -> 1.11
- 1.11 -> 1.12
- 1.12 -> 1.13

## Different update process

- **Using managed service** : few clicks to update the cluster (GKE, AKS, EKS)
- **Using kube adm** : 2 commands
	- `kubeadm upgrade plan`
	- `kubeadm upgrade apply`
- **Manually from scratch** : update all the components ourselves

## Update with kubeadm

### 1 - Update the master nodes

- the control plane components are going down briefly
- we cannot access the cluster using kubectl
- the workloads is still running on workernodes serving users
- we cannot create new applications or update or delete existing ones
- if a pod was to fail a new would NOT be automatically created
- after the update the master node will be at 1 version newer than the worker nodes, this is a supported configuration so everything should work correctly
### 2 - Update the workers nodes

#### Strategy 1 - Update all the nodes at the same time

**Requires downtime**
The users won't be able to access the applications anymore during the udpate.
Once the update is done, pods will be reschule and access to users restored.

#### Strategy 2 - Update one node at a time

**Requires NO downtime**
1. **node01** : We first update the first node, workload will be reschedule on other nodes
2. **node02** : When the node is updated and backup we update the second node, workload are scheduled on node 1 and 3
3. **node03** : Same thing for node 3

#### Strategy 3 - Adding new updated nodes

**Requires NO downtime**
Especially useful in a cloud environment where we can easily provision and decommission machines.
1. We create a new vm with the new version we want to upgrade, we make it joined the cluster, we drain node01, wait for the workload to be rescheduled and we decomission node01
2. same for node02
3. same for node02

### How it is done - 1.11 to 1.13

We launch this command : 
![[Pasted image 20250913175101.png]]

#### Master Node

We need to update the kubeadm tool before performing the update. It follows the same version as kubernetes.

We need to manually update the kubelet on each node.

So we would need here we would need to : 

1. Update kubeadm
``` bash
apt-get upgrade -y kubeadm=1.12.0-00
```
2. Update the cluster
```
kubeadm upgrade apply v1.12.0
```

If we do : 
![[Pasted image 20250913175447.png]]

We still see the old version, this is the because it is showing the kubelet version of the nodes registred within the apiserver and not the version of the apiserver itself.

If we have kubelet not running as pods we would have to upgrade it manually as it runs as a service on each node :

``` bash
apt-get upgrade -y kubelet=1.12.0-00
systemctl restart kubelet
```

![[Pasted image 20250913175834.png]]

#### Worker Node

We drain node 01 :
![[Pasted image 20250913175920.png]]

Launching all these commands will set the node back up and updated :
![[Pasted image 20250913175946.png]]

We still need to update kubeadm before the kubelet.
``` bash
apt-get upgrade -y kubeadm=1.12.0-00
apt-get upgrade -y kubelet=1.12.0-00
kubeadm upgrade node config --kubelet-version v1.12.0
systemctl restart kubelete
```

We need to uncordon it : 
```
kubectl uncordon node-1
```

We do the same thing for other nodes.


> [!IMPORTANT] STATIC PODS REAMAINS - DRAIN
> When we drain pods, static pods remains as they are not created by the clusters (control plane pods)

---

# Practice update 

[Upgrade Master Nodes](https://v1-33.docs.kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/)
[Upgrade Worker Nodes](https://v1-33.docs.kubernetes.io/docs/tasks/administer-cluster/kubeadm/upgrading-linux-nodes/)
[Update the Repo Version](https://v1-33.docs.kubernetes.io/docs/tasks/administer-cluster/kubeadm/change-package-repository/#verifying-if-the-kubernetes-package-repositories-are-used)

To install a new minor first thing to do is update the apt repo the next minor and then run the apt update commands : 
```
nano /etc/apt/sources.list.d/kubernetes.list
```

```
deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.32/deb/ / # to 1.33
```

if the update show an error about held packages we just have to relanch it with the flag :

```
sudo apt-get update && sudo apt-get install -y kubelet='1.33.0-*' --allow-change-held-packages
```

or run the commands said by the documentation : 
``` shell
sudo apt-mark unhold kubeadm && \
sudo apt-get update && sudo apt-get install -y kubeadm='1.33.x-*' && \
sudo apt-mark hold kubeadm
```

--- 

# Backup and Restore

There are 2 ways of backing up a cluster.
- Resource Config
- Etcd cluster

|Critère|API (kubectl + YAML)|Snapshot etcd|
|---|---|---|
|🎯 Ciblage précis|✅ Oui|❌ Non (tout ou rien)|
|💯 Couverture complète|❌ Non|✅ Oui|
|👀 Lisibilité / audit|✅ Facile|❌ Difficile|
|🔐 Sauvegarde des secrets|⚠️ Partielle|✅ Complète|
|🔁 Portabilité|✅ Haute|⚠️ Moyenne|
|🧰 Complexité technique|✅ Simple|❌ Plus complexe|
|🕑 Consistance du snapshot|❌ Moyenne|✅ Forte|
|🛠️ Dépendance etcd|❌ Aucune|✅ Oui|

Sometimes in managed cluster we won't have access to the etcd cluster so we would backup the resource config.

## Resource Config

We can backup every resource config using the following method (only for the default resource group) : 

``` bash
kubectl get all -A -o yaml > all-deploy-services.yaml
```

There are tools for this job, for example [[Velero]].

## ETCD

The data is stored in --data-dir `/var/lib/etcd`.

We can take snapshot of the etcd using the command : 
```
ETCDCTL_API=3 etcdctl snapshot save snapshot.db
```

We can view the snapshot status using : 
```
ETCDCTL_API=3 etcdctl snapshot status snapshot.db
```

### Restore from an etcd snapshot

1. Stop the kube-apiserver : 

``` bash
systemctl stop kube-apiserver
```

2. Restore : 

```
ETCDCTL_API=3 etcdctl snapshot restore snapshot.db --datadir /vat/lib/etcd-from-backup
```

3. Specify the new data dir in the etcd.service : 
``` bash
--data-dir=/var/lib/etcd-from-backup
```

This will create a new etcd-cluster adding the current members of the cluster and preventing new members to join a existing one.

4. Restart the service 

``` bash
systemctl daemon-reload
service etcd restart
```

5. Restart the kube-apiserver service

```
systemctl kube-apiserver start
```


### Snapshot based Backup

To connect to the etcd cluster we need to specify the following informations.

Backup using the etcd api (Cluster must be online).
``` bash
ETCDCTL_API=3 etcdctl snapshot save /backup/etcd-snapshot.db
--endpoints=https://127.0.0.1:2379 \
--cacert=/etc/etcd/ca.crt \
--cert=/etc/etcd/etcd-server.crt \
-key=/etc/etcd/etcd-server.key
```

To restore a snapshot to a new data directory:

```
etcdutl snapshot restore /backup/etcd-snapshot.db \
  --data-dir /var/lib/etcd-restored
```

- `etcdctl snapshot save` is used for creating `.db` snapshots from live etcd clusters.
    
- `etcdctl snapshot status` provides metadata information about the snapshot file.
    
- `etcdutl snapshot restore` is used to restore a `.db` snapshot file.
### File Based Backup

Backup only using files (Cluster can be offline) : 

```
etcdutl backup \
	--data-dir /var/lib/etcd
	--backup-dir /backup/etcd-backup
```

To use a backup made with `**etcdutl backup**`, simply copy the backup contents back into `**/var/lib/etcd**` and restart etcd.

`**etcdutl backup**` performs a raw file-level copy of etcd’s data and WAL files without needing etcd to be running.

ETCD listens to port `2379`.


### Exemple

When doing the backup of an etcd cluster running as static pods. 
We need to change the --data-dir with the dir of the new data in the config of the static pod : 
``` yaml
volumeMounts:
- mountPath: /var/lib/etcd-from-backup
  name: etcd-data
- mountPath: /etc/kubernetes/pki/etcd
  name: etcd-certs
volumes:
- hostPath:
  path: /etc/kubernetes/pki/etcd
  type: DirectoryOrCreate
name: etcd-certs
- hostPath:
  path: /var/lib/etcd-from-backup
  type: DirectoryOrCreate
name: etcd-data
```

---

# Security Primitives

## Secure Hosts

If the machines are compromised then everything is compromised.

Access to machine must be :
- SSH based authentication
- Password based authentication disabled

## Secure Kubernetes

The point of access to Kubernetes is the kube-apiserver. Then the first ligne of defense is to control access to the kube-apiserver : 
- **Authentication** : Who can access ?
	- Files - Username and Password
	- Files - Username and Tokend
	- Certificates
	- External Authentication providers - LDAP
	- Service Account
- **Authorization** : What can they do ?
	- RBAC Authorization
	- Attribute BAC Authorization
	- Node Authorization
	- Webhook Mode

All the communications between the api-server and the other control plane component is encrypted using tls : 
- ETCD Cluster
- Kube Controller Manager
- Kube Scheduler
- Kube Proxy
- Kubelet

---

# Authentication

There are differents type of users that will access the cluster : 
- Admins (User)
- ~~Developers (handle by the application deployed directly)~~
- End Users (User)
- Bots (Service Account)

## Users Auth Mecanism

There are 4 ways to authenticate to a cluster : 
- **Static Password File** : With a username passowrd listed in a static password file - NOT RECOMMENDED - DEPRECATED
- **Static Token File** : With a username token listed in a static token file - NOT RECOMMENDED
- **Certificates**
- **Identity Services** : LDAP

### Static Password File

We can used a csv and specify it to the kube-apiserver which will reload to take the new configuration.

![[Pasted image 20250914103333.png]]
If the kube-apiserver is a static pod we need to consider volume mounts from host.

To authenticate we would do it this way then : 

``` bash
curl -v -k https://master-node-ip:6443/api/v1/pods -u "user1:password123"
```

We can also specify a group in the 4th column of the csv file.

### Static Token File

Works the same way as the static password file but using tokens instead of password.

![[Pasted image 20250914103614.png]]

---

# TLS BASICS

TLS use asymmetric encryption with : 
- A public key used by the client to encrypt and send data to the server
- A private key used by the server to decrypt the data sent by the client. The private key stay on the server.

## Public Key Infrastructure

A communication is done with symmetric and asymmetric. 

Asymetric is used to encrypt the symmetric key of the client to send it to the server. They know can exchange with the data encrypted by the symmetric key.

The server sends the public key within a certificate. This allow us to verify that it is the correct source we are trying to hit by verifying the signature. We have to be sure it is signed by a certificate authority recognize and not a self-signed certificate.

To have a certificate sign we have to create a CSR and send it to CA for validation which will verify you are the owner of the site and then sign the certifcate.

The CA use their private keys to sign the certicate so it is easy to verify with the public key that it has been sign by the CA itself. The CA are built-in the browser.

For private site accross an organization we can host a private CA and add the public key to the browsers of our organization.

We have also client certificates to validate the client is who he says he is.

---

# TLS in Kubernetes

3 types of certificate : 
- Server Certificate
- CA certificate
- Client Certificate

Servers and clients are identifiy within the control plane.

The servers will have a certificate and a private key.
The clients will have a certifivate and a private key.
## Servers & Clients

Everything that exposes an https endpoint :
- Kube-apiserver
	- Admin
	- Kube Scheduler
	- Kube Controller Manager
	- Kube-Proxy
	- Kubelet
- ETCD Server
	- Kube-apiserver (can use his server cert and key and generate new ones dedicated)
- Kubelet Server
	- Kube-apiserver

![[Pasted image 20250914110607.png]]


> [!IMPORTANT] CA 
> We can have only one CA to sign all our certs or we can have a dedicated CA for ETCD server cert and Kube-apiserver client cert.

---

# TLS Certificate generation

## Genearate a CA Certicate


> [!IMPORTANT] 
> All the components must have a copie of the CA certificate to verify the Signing Authority mentioned in all the certificate.

1. Generate a private key

``` bash
openssl genrsa -out ca.key 2048
```

2. Generate a CSR

``` bash
openssl req -new -key ca.key -subj "/CN=KUBERNETES-CA" -out ca.csr
```

3. Generate and Sign the certificate

For a CA certificate we just need to sign it with the ca key previously generated :

``` bash
openssl x509 -req -in ca.csr -signkey ca.key -out ca.crt
```

## Generate a Client User Certificate signed by a CA

1. Generate a key

``` bash
openssl genrsa -out admin.key 2048
```

2. Generate the CSR

This will be the client certificate for the kube-admin user.

``` bash
openssl req -new -key admin.key -subj "/CN=kube-admin/O=system:masters" -out admin.csr
```

3. Generate and Sign the certificate

``` bash
openssl x509 -req -in admin.csr -CA ca.crt -CAkey ca.key -out admin.crt
```

We need to add the group detail in the certificate for the user. For the kube-admin user it will be : `SYSTEM:MASTERS` 

## Generate a Client Component Certificate signed by a CA

kube-controller-manager: the CN would be `system:kube-controller-manager`
kube-scheduler: the CN would be `system:kube-scheduler`
kube-proxy: the CN would be `system:kube-proxy` ????

## Use

We can use it like this : 

``` bash
curl https://kube-apiserver:6443/api/v1/pods \
  --key admin.key
  --cert admin.crt
  --cacert ca.crt
```

Or using a kubeconfig file : 

``` yaml
apiVersion: vl
clusters:
— cluster:
	certificate—authority: ca . crt
	server: https://kube—apiserver.6443
name: kubernetes
kind: Config
users :
- name: kubernetes-admin
  user :
    client-certificate: admin. crt
	client—key: admin.key
```

## Generate a Server Certificate for ETCD

We follow the same steps as above.
The name will be : `etcd-server`.

ETCD works in a cluster so we need to create additional peer certificates.
- 1 server ceritifcat for inbound client requests
- 1 peer certificate for each etcd node for internal communication

![[Pasted image 20250914113837.png]]
## Generate a Server Certificate for Kube-apiserver

The kube-apiserver has many names and all of them should be present in the certificate :
- kube-api server : the default one
- kubernetes
- kubernetes.default
- kubernetes.default.svc
- kuberntes.default.svc.cluster.local
- 10.96.0.1
- 172.17.0.87

``` bash
openssl req -new -key apiserver.key -subj "/CN=kube-apiserver" -out apiserver.csr -config openssl.cnf
```

We must create a openssl.cnf file : 
``` c
[req]
req_extensions = v3_req
distinguished name = req distinguished name
[ v3_req ]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation,
subject-AltName = @alt_names
[alt names]
DNS.1 = kubernetes
DNS.2 = kubernetes.default
DNS.3 = kuberetes.default.svc
DNS.4 = kubernetes.default.svc.cluster.local
IP.1 = 10.96.0.1
IP.2 = 172.17.0.87
```

![[Pasted image 20250914114522.png]]
## Generate Server Certificate for the kubelet

We need to generate a certificate by number of node and so kubelet. There are no common server cert here because each kubelet is independant and are not cluster.

The name on the certificate are the nodes names :
- node01
- node02
- node03

We also need to generate client cert for communication with the kube-apiserver. One for each kubelet.

The name in the cert certificate are : 
- system:node:node01

They must be added in the `SYSTEM:NODES` group.

---
# Diagnostics

How can we see logs of the components to diagnose : 
## Hard way

``` bash
journalctl -u etcd -l
```

## Kubeadm

``` bash
kubectl logs etcd-master
```

## Last resort

If the kube-apiserver is failing we can see the container directly in the nodes : 

``` bash
docker ps -a
```

or the cli tool of the cri used : 
``` bash
crictl ps -a
crictl logs container-id
```



---

# View Certificate Details

The hard way launch components as service when kubeadm launch components as static pods.

![[Pasted image 20250914115613.png]]

To view a certificate : 

``` bash

openssl x509 -in /etc/kubernetes/pki/apiserver.crt -text -noout
```

![[Pasted image 20250914115840.png]]

---

# Certificates API

## Manually

If a new member arrive in the team. The steps are : 
1. new member generate a private key and a csr
2. new member send the csr to an admin of the cluster
3. the admin create the certificate using the csr and the ca key and certificate
4. the admin send back the certificate to the user

If a certificate expires, we need to do all the steps again.

The Kube master node is also the CA server, this is the architecture use by kubeadm.

## Automated

We can use the certificates API to do this.

1. New user generates key

``` bash
openssl genrsa -out jane.key 2048
```

2. New user generates a CSR

``` bash
openssl req -new -key jane.key -subj "/CN=jane" -out jane.csr
```

3. Admin take the CSR and create a certificate sign request using the kubernetes API

``` yaml
apiVersion: certificates . k8s . io/vl
kind: CertificateSigningRequest
metadata :
	name: jane
spec :
	expirationSeconds : 600
	usages :
		- digital signature
		- key encipherment
		- server auth
request :
		base64EncodedCSR
```

To put the certificate inside the yaml : 
``` bash
:.!cat jane.csr | base64 | tr -d "\n"
```
or
```
:.!cat jane.csr | base64 -w 0
```

We can see it using : 

``` bash
kubectl get csr
```

4. Admin approve the csr

``` bash
kubectl certificate approve jane
```

Under the hood kuberntes sign the ceritifcate using the CA.

5. Send the certificate generated to the user

We can see the certificate in the status field of the csr (in base64).
![[Pasted image 20250914135352.png]]

### Controller Manager

The controller manager is reponsible for all the certificates actions using controllers : 
- CSR-APPROVING
- CSR-SIGNING

We can specify the cluster signing cert and key in the configuration of the kube-controller-manager config : 

![[Pasted image 20250914135628.png]]

To view a csr we use : 

```bash
openssl req -in test.csr -text -noout
```

We can deny a csr using (and delete it after) : 

```
kubectl certificate deny mycsr
```

To view the CSR yaml search for [CertificateSigningRequest](https://kubernetes.io/docs/tasks/tls/certificate-issue-client-csr/)


--- 
# Kubeconfig

To authenticate to a cluster we need to specify the following fields : 

```
kubectl get pods \
  --server my-kube-playground:6443
  --client-key admin.key
  --client-certificate admin.crt
  --certificate-authority ca.crt
```

To make it easier we can use a kubeconfig file which will keep all of these information for us. Then we just need to specify it : 

``` bash
kubectl get pods --kubeconfig config
```

By default, kubectl search for the kubeconfig file inside `$HOME/.kube/config`.
We can also specify another file using the env var `$KUBECONFIG`.

## File

There a 3 sections :
- **Clusters** : the various kubernetes clusters that we have access to (dev, prod...)
- **Contexts** : Defines which user account is used to access which cluster
- **Users :** The user account we have access to (admin, dev user, prod user...). The users may have different privileges on differents clusters.

![[Pasted image 20250914142205.png]]

> [!IMPORTANT]
> In the kubeconfig we juste specify existing users we are not creating anything 

The format of the file, we can use path to certificate or put the full cert in base64 directly.

``` yaml
apiVersion: v1
kind: Config

current-context: my-kube-admin@my-kube-playground

clusters :
- name: my—kube—playground
  cluster:
  # certificate—authority: /path/to/cert/ca.crt
  certificate-authority-data: base64data
  server: https://my-kube-playground:6443
  
contexts :
- name: my—kube—admin@my—kube—playground
  context:
    cluster: my-kube-playground
    user: my-kube-admin
	namespace: finance
	
users :
- name: my—kube-admin
  user:
    # client-certificate: /path/to/cert/admin.crt
	client-certificate-data: base64Data
	# client-key: /path/to/key/admin.key
    client-key-data: base64Data 
```

![[Pasted image 20250914142622.png]]

To view the config file : 

``` bash
kubecl config view
```

 To change context we do : 
 
 ``` bash
 kubectl config use-context prod-user@production
 ```

---

# API Groups

There is different apis we can interacti with using the kube-apiserver : 
- `/metrics`
- `/healthz`
- `/version`
- `/api`
- `/apis`
- `/logs`

To show this we can do : 

```bash
curl http://localhost:6443 -k
```
## Cluster Functionnality APIs

### Core Group
`/api`
![[Pasted image 20250914150259.png]]

### Named Group
`/apis`

We can find the detail and the group of a resource using the [api specification](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.13)

We can view this using : 
```
curl http://localhost:6443/apis -k | grep "name"
```

![[Pasted image 20250914151015.png]]


## Use the api

### Auth certs

We have to authenticate : 
``` bash
curl http://localhost:6443 -k
  --key admin.key
  --cert admin.crt
  --cacert ca.crt
```

### Kubectl proxy

An alternative is to start a kubectl proxy client on port 8001 that use the content of the kubeconfig file to authenticate to the cluster.

```
kubectl proxy
```

Then we use it : 

```
curl http://localhost:8081 -k
```

---

# Authorization

This is the concept of verify the user privileges to do things.

There exists 4 different authorization mechanisms : 
- **Node**
- **ABAC**
- **RBAC**
- **Webhook**

## Node Authorizer

**Only for nodes**

The kubelet use a client certificate with the name `system:node:node01` which allow it to autenticate against the kube-apiserver.

The kubelet : 
- Read 
	- Services
	- Endpoints
	- Nodes
	- Pods
- Write
	- Node Status
	- Pod Status
	- Events

The requests of the kubelet are handle by a special authorizer called the Node Authorizer (the authorizer is called when we have the `system:node` in the name of a component).

# ABAC

**Difficult to manage**

Attribute Based Access Control.


This allows external access to the api.

We specify the attribute to a user specifying what he can do : 
- view PODs
- create PODs
- delete PODs

We do this creating a policy file in a json format : 

``` json
{
	"kind": "Policy",
	"spec": {
		"user": "dev-user",
		"namespace": "*",
		"resource": "pods",
		"apiGroup": "*"
	}
}
{
	"kind": "Policy",
	"spec": {
		"user": "dev-user-2",
		"namespace": "*",
		"resource": "pods",
		"apiGroup": "*"
	}
}
```

For each user we create a Policy definition for each user defining their rights.

Every time we need to update this file we need to restart the kube-apiserver to takes the new changes.

## RBAC

Instead of assign all the attribute to the user we assign them to a role and then we have a reusable role we can set to users.

![[Pasted image 20250914152156.png]]

The modification made on role are reflecting immedatly no need to restart the kube-apiserver.

## Webhook

If we want to handle the authorization externally outsourcing and not using the built-ins mechanisms.

Example : **Open Policy Agent**

## AlwaysAllow

Always allow every requests

## Always Deny

Always Deny every requests

## How does it works ?

We set the mode in the configuration of the kube-apiserver : 

```
--authorization-mode=AlwaysAllow
```


> [!NOTE] Default
> By default it is always 

We can also specify several modes : 

```
--autorization-mode=Node,RBAC,Webhook
```

It then be called in order of the specification if the request is denied : 
1. Node
2. RBAC
3. Webhook

---

# RBAC 

`Role` and `RoleBinding` are scoped to the namespace they are created. 

1. Create a Role

``` yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
	name: developer
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs : ["list", "get", "create", "update", "delete"] 
  resourceNames: ["blue", "orange"] # restrict to only those pods
```

view detail about a role : 
``` bash
kubectl describe role name
```

2. Link the user to the role, create RoleBinding

``` yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
	name: devuser—developer—binding
subjects:
— kind: User
  name: dev—user
  apiGroup: rbac.authorization.k8s.io
roleRef :
  kind: Role
  name: developer
  apiGroup: rbac.authorization.k8s.io
```

view detail about rolebinding :
```
kubectl describe rolebinding name
```


## Check Access

To check if we can do something within the cluster we can use : 

``` bash
kubectl auth can-i create deployments
```

``` bash
kubectl auth can-i delete nodes
```

As an admin user we can see what an other user can do inside a specific namespace using : 
``` bash
kubectl auth can-i create pods --as dev-user --namespace test
```

We can also use the --as with any kubectl commands.

---

# ClusterRoles

Roles are namespaced. ClusterRoles are cluster wide.

In a Kubernetes cluster resources a separated as : 
- **Namespaced resources** : pods, secrets...
```
kubectl api-resources --namespaces=true
```
- **Cluster scoped** : nodes, certificateSigningRequests...
```
kubectl api-resources --namespace=false
```

Create a cluster role :
``` YAML
apiVersion: rbac.authorization.kt3s.io/v1
kind: ClusterRole
metadata :
	name: cluster—administrator
rules :
— apiGroups : [""]
  resources : ["nodes"]
  verbs : ["list", "get"]
```

Create a cluster role binding :
``` yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata :
	name: cluster-admin-role-binding
subjects :
— kind: User
  name: cluster—admin
  apiGroup: rbac.authorization.k8s.io
roleRef :
  kind: ClusterRole
  name: cluster—administrator
  apiGroup: rbac.authorizat-ion.k8s.io
```

To see Api Resources we can do : 

``` bash
kubect api-resources
```

---
# Service Accounts

User Account are for user.
Service Account are used by machines.

When creating a service account a token is automatically created. That is what should be use to authenticate to the kube-apiserver. The token is stored as a secret object.

## External Application

We can use the api using : 

``` bash
curl https://192.168.56.70:6443/api -insecure --header "Authorization: Bearer Token"
```

## Internal Application hosted in Kubernetes

Instead of getting the secret manually we can just mount the secret containing the token inside our pod for authentication.

## Default

A service account is automatically created inside each namespaces is automatically mounted with its token to all new pods.

The default service account is very restricted.

## Custom

We can specify a serviceAccount using : 

``` yaml
spec:
  serviceAccountName: my-sa
```

Not mounting the service Account Token :

``` yaml
spec: 
  automountServiceAccountToken: false
```

## Changes

### Before v1.22

The token used for service accounts are jwt token we can decode.
These tokens didn't have an expiration date. And it cause security issue.
Also they are not bound to any audience (anyone can read it, not for a specific receiver).

The JWT Is valid as long as the SA exists.

Any component that can see a service account secret of another component is at least as powerful as the component.

JWTs requires a Kubernetes secret by service account only.

### Since v1.22

The TokenRequestApi was introduced. By default creating a service doesn't create a token associated automatically.

The tokens generated by the TokenRequestApi are : 
- Audience Bound
- Time Bound
- Object Bound

When creating a pod, the default token of the service account is no longer used.

Instead a token with an expiration is created for the pod through the TokenRequestApi By the service account admission controller when the pod is created : 

![[Pasted image 20250915080844.png]]

What are projected volumes ? 

### Since v1.24

A secret is no longer automatically created when a service account is created.

So we need to create the token manually (for external source ) : 
```
kubectl create token my-sa
```

For a pod it will be automatically created with a default expiration date and will be renew automatically by the kubelet.

It will then print that token on screen. 1h by default.

We can still create secrets the old way with no expiring tokens. But it is not recommended. 

We can do it by creating a secret with a specific annotation :
```yaml 
apiVersion: v1
kind: Secret
type: kubernetes.io/service-account-token
metadata:
  name: mysecretname
annotations:
  kubernetes.io/service-account.name: dashboard-sa
```

---

# Image Security

If we put : 
```
image: nginx
```

By default it use dockerhub and it use the library default account where official images are stored : `image: docker.io/library/nginx`

## Pull from a private registry

![[Pasted image 20250915084458.png]]