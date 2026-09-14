---
creation date: 2026-08-04-18:28:53
modification date: 2026-08-04-18:28:53
imageNameKey: Kubernetes_-_CKS
---

# Kodekloud course

- [The 4 C's of Cloud Native Security](#the-4-cs-of-cloud-native-security)
- [Cluster Setup and Hardening](#cluster-setup-and-hardening)
- [Security Primitives](#security-primitives)
  - [Secure Hosts](#secure-hosts)
  - [Secure Kubernetes](#secure-kubernetes)
  - [Securing the kubelet](#securing-the-kubelet)
  - [Kubectl Proxy \& Portforward](#kubectl-proxy--portforward)
  - [Verify Binary before deploying](#verify-binary-before-deploying)
  - [Docker](#docker)
  - [Securing Node Metadata](#securing-node-metadata)
  - [TLS Encryption Cypher](#tls-encryption-cypher)
- [System Hardening](#system-hardening)
  - [Reducting the Attack Surface](#reducting-the-attack-surface)
  - [SSH Hardening](#ssh-hardening)
  - [Sudo](#sudo)
  - [Installing Only the required packages](#installing-only-the-required-packages)
  - [Restrict Kernel Modules](#restrict-kernel-modules)
  - [Identify and disable Open Ports](#identify-and-disable-open-ports)
  - [Restricting Network Access](#restricting-network-access)
  - [Linux Sys Calls](#linux-sys-calls)
  - [App Armor](#app-armor)
  - [Linux Capabilities](#linux-capabilities)
- [Minimizing Microservices Vulnerabilities](#minimizing-microservices-vulnerabilities)
  - [Security Context](#security-context)
  - [Admission Controller](#admission-controller)
  - [Pod Security Admission](#pod-security-admission)
  - [OPA - Open Policy Agent](#opa---open-policy-agent)
  - [Secrets](#secrets)
  - [Container Sandboxing](#container-sandboxing)
  - [Multi-tenancy](#multi-tenancy)
  - [Quality Of Service](#quality-of-service)
  - [DNS isolation Multi-tenants](#dns-isolation-multi-tenants)
  - [Pod to Pod Encryption](#pod-to-pod-encryption)
- [Supply Chain Security](#supply-chain-security)
  - [Kubelinter](#kubelinter)
  - [Secure Images](#secure-images)
  - [Kubesec](#kubesec)
  - [Trivy](#trivy)
- [Monitoring, Logging \& Runtime Security](#monitoring-logging--runtime-security)
  - [Falco](#falco)
  - [Ensure immutability of containers at runtime](#ensure-immutability-of-containers-at-runtime)
  - [Kubernetes Audit](#kubernetes-audit)
- [Points Chauds](#points-chauds)
  - [User Namespaces (hostUsers)](#user-namespaces-hostusers)
  - [Netpols](#netpols-1)
  - [Sécuriser un cluster existant](#sécuriser-un-cluster-existant)
  - [DEBUG API SERVER](#debug-api-server)
  - [Secrets](#secrets-1)
  - [Service Account](#service-account)
  - [Security Context](#security-context-1)
  - [CSR](#csr)
  - [Packets](#packets)
  - [PSA](#psa)
  - [YAML](#yaml)
  - [Admission Controller Kubernetes](#admission-controller-kubernetes)
  - [User Kubernetes](#user-kubernetes)
  - [Service Account](#service-account-1)
  - [Static-analysis](#static-analysis)
  - [Secrets](#secrets-2)
  - [ReplicaSets](#replicasets)
  - [Seccomp](#seccomp)
  - [Etcd](#etcd)
  - [Audit](#audit)
  - [Network Policies Cillium](#network-policies-cillium)
  - [Istio](#istio-1)
  - [Docker](#docker-1)
  - [Nginx Ingress](#nginx-ingress)
  - [Checksum verification](#checksum-verification)
  - [Apparmor](#apparmor)
  - [Kubelet](#kubelet)
  - [CIS Benchmark](#cis-benchmark)
  - [Trivy](#trivy-1)
  - [JSONPATH](#jsonpath)
  - [GatwewayAPI](#gatwewayapi)
  - [Telecharger binaire depuis Github](#telecharger-binaire-depuis-github)
  - [API SERVER](#api-server)
  - [Seccomp vs AppArmor](#seccomp-vs-apparmor)
  - [Linux Capabilities](#linux-capabilities-1)
  - [Cilium netpols](#cilium-netpols)
  - [Env vars Secrets](#env-vars-secrets)
  - [Falco Exemple k8s audit log](#falco-exemple-k8s-audit-log)
  - [Audit logs](#audit-logs)
  - [Admission controller](#admission-controller-1)
  - [Image](#image)
  - [Scaling](#scaling)
- [Questions Examens](#questions-examens)
- [Resources](#resources)
- [Docs](#docs)
  - [Doc Officielle](#doc-officielle)
  - [Doc Utile](#doc-utile)
  - [NGINX](#nginx)
  - [AppArmor](#apparmor-1)
  - [Seccomp](#seccomp-1)
  - [Security Features](#security-features)
  - [ServiceAccount](#serviceaccount)
  - [AdmissionControllers](#admissioncontrollers)
  - [BOM](#bom)
  - [PSA](#psa-1)
  - [Cilium Policies](#cilium-policies)


## The 4 C's of Cloud Native Security 

[[The 4 C's of Cloud Native Security]]

## Cluster Setup and Hardening

[[CIS Benchmark]]
[[Kube-bench]]

## Security Primitives

### Secure Hosts

The machines hosting the cluster nodes must use : 
- ssh key based authent
- Password based authent must be disabled
- measures to secure the physical and virtual infrastructure

### Secure Kubernetes

The Api server is the component receiving all the cluster requests. The first line of defense is to secure it.

[[Authentication (Kubernetes)]] : Who can access the cluster ?
- Static Token File
- Certificates
- LDAP
- Service Accounts


[[Authorization (Kubernetes)]] : What can they do ?
- RBAC
- ABAC
- Node Authorization
- Webhook Mode

**TLS**
All the communication between the cluster component use tls certificate to communicate.

**Network Policies**
By default, each pod can communicate with all the other pod from other namespaces. We can restrict access between pods using netpols.



### Securing the kubelet

With kubeadm the kubelet is not automatically installed.

The kubelet is configured using a `KubeletConfiguration` resource. The cli flags override what is in the config file.

![[Kubernetes_-_CKS_7.png]]

#### Authentication

[[Authentication (Kubernetes)#Accessing the Kubelet]]

#### Authorization

[[Authorization (Kubernetes)#Kubelet Authorization]]

### Kubectl Proxy & Portforward

We can use kubectl proxy. It will use the credentials in the kubeconfig file to forward all api request from localhost:8081 to our cluster.

We can even requests clusterIP service from the api : 

![[Kubernetes_-_CKS_11.png]]

We can also use port-forward to do this : 

```
kubectl port-forward service/nginx <localPort>:<svcPort>
```

### Verify Binary before deploying

![[Kubernetes_-_CKS_12.png]]

We compare the hash we calcule from the one in the page.

### Docker

[[Docker Hardening]]

### Securing Node Metadata

#### Why securing ?

> [!Warning] If we expose too many metadata an attacker can for exemple get the kubelet version from a node, and if it's outdated he can launch a version-specific attack. Or can get IP address and lauch DDOS attack. 

1. Avoid attacks
2. Protect against misconfiguration
3. Maintain privacy
4. Ensure compliance (GDPR or HUPAA)

#### How to secure ?

1. **Node Isolation** : Only certain workload can be deployed on certain node + RBAC on nodes metadata
2. **Network Policies** : Restrict communication to only what's needed
3. **Audit Logs** : Track who accessed or modified node metadata and when
4. **Updates and Patches**: Fix latests vulnerabilites

#### Netpols

[[Network Policy (Kubernetes)]]

#### RBAC

This clusterRole allow to curl the nodes informations using its service account inside the pod :

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: node-viewer
rules:
- apiGroups:
  - ""
  resources:
  - nodes
  verbs:
  - get
  - list
  - watch
```

```bash
kubectl exec -it api-test-pod -n default -- /bin/bash -c 'curl -k https://kubernetes.default.svc/api/v1/nodes -H "Authorization: Bearer $(cat /var/run/secrets/kubernetes.io/serviceaccount/token)"'
```

[[Kubernetes - Pods]]

#### Auditing

[[Auditing (Kubernetes)]]

### TLS Encryption Cypher

[[TLS Encryption (Kubernetes)]]

## System Hardening

We follow the [[Least Privilege Principle]] :

1. Limit Access to nodes
2. RBAC Access
3. Remove obsolete packages and services
4. Restrict network access
5. Restrict obsolete Kernel modules
6. Identify and fix open ports

### Reducting the Attack Surface

#### Limit Node Access

We need to limit access to the cluster Nodes particularly limiting the access to the nodes from internet.

We can create Private network in a cloud Provider or in our house and use a VPN to be able to access our nodes.

We can use firewall to restrict globally the traffic coming to the nodes and we can also do this on each nodes separately.

Only administrators of the cluster should have access to the nodes and not developer or end-users.

#### RBAC Access

[[Linux - Users]]

### SSH Hardening

[[SSH Hardening]]

### Sudo

[[Linux - Sudo]]

### Installing Only the required packages

List all packages in ubuntu :

```bash
apt list --installed
```

In a cluster we just need : 
- kubelet
- kubeadm
- container runtime
- kubectl

Find out the name of the unit file:  

```bash 
systemctl list-units --all | grep nginx
```
  
Stop Nginx service:  

```bash 
systemctl stop nginx
```
  
Find out the location of the service unit:  

```bash 
systemctl status nginx
```

Update a package 

```bash
apt install wget -y
```
  
Remove the unit file:  
  
`rm /lib/systemd/system/nginx.service`

We can list services running in our host : 

==service==
```bash
systemctl list-units --type service
```

See CIS Benchmark Reference :

![[Kubernetes_-_CKS_19.png]]

### Restrict Kernel Modules

The kernel can extend its capabilities using modules.

To load a module : 

```bash
modprobe pcspkr
```

list all modules loaded into the kernel : 

```
lsmod
```

![[Kubernetes_-_CKS_20.png]]

If we have kubernetes workloads running on a host, even an unprivileged process running on a Pod can cause certain network-related modules to be loaded into the kernel by creating a network socket. This can allow an attacker to exploit a potential vulnerability.

To mitigate this, we can blacklist module on all the nodes of the cluster.

The module `sctp` must not be enabled for a kubernetes cluster.

We can blacklist a module in a host by adding it to `/etc/modprobe.d/blacklist.conf` (can be any name as long as it is on the right directory) : 

```bash
blacklist sctp
```

Then we need to reboot the host and we can verifiy if it is still here : 

```bash
shutdown -r now
lsmod | grep sctp
```

An another module to disable is the `dccp` module.

See CIS Benchmark Reference : 

![[Kubernetes_-_CKS_21.png]]

### Identify and disable Open Ports

Check if a port is used : 

netstat

```bash
netstat -antp | grep -w LISTEN
```

To get information about which service is using that port we can (classic services) : 

```bash
cat /etc/services | grep -w 53
```

We can see which ports are needed for kubernetes by consulting the documentation : 

https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#check-required-ports

![[Kubernetes_-_CKS_21-1.png]]

Then we can disable all other ports.


### Restricting Network Access

![[Kubernetes_-_CKS_22.png]]

These ports `0.0.0.0:*` are open to any client host.

This is a bad practice, we should restrict access to known host.


For this we can use : Internal packet filtering system called `netfilter`

The cli to interface the net+filter is `iptables` but it has a learning curve.

Instead we can use `ufw` Uncomplicated Firewall which is a simple frontend interface for `iptables`.

Install ufw : 

```bash
apt-get update
apt-get install ufw
systemctl enable ufw
systemctl start ufw
```

Using commands : 
```bash
# View status of te firewall and appliehd rules
ufw status

ufw default allow outgoing
ufw default deny incoming

ufw allow from <ip> to any port 22 proto tcp
ufw allow from <range> to any port 80 proto tcp

ufw deny 8080

ufw enable
```

![[Kubernetes_-_CKS_23.png]]

### Linux Sys Calls

The kernel is the interface between a computer hardware and its processes. It communicates between the 2 managing resources as efficiently as possible.

It can be devided into 2 memory Areas : 
- **Kernel Space** : Kernel Code, Kernel Extensions, Device Drivers
- **User Space** : Applications run by user (C, Java, Python, Ruby, Containers...)

Applications can make System calls to the kernel to : 
- Open a file
- Write to a file
- List processes
- Define a variable

The system calls are : 
- open()
- close()
- readdir()
- execve()
- closedir()

To trace systemcalls we can use strace.

Use Exemple : 
```bash
strace touch /tmp/error.log
```

![[Kubernetes_-_CKS_24-1.png]]

Systemcalls(argv1=absolutepath_to_program, argv2=[argstopathcommands], vars herited by the systemcalls 23 here these are the env in the current user shell. )

To trace a system call made by a running process we need to find its pid : 

```bash
pidof etcd
```

Then we can : 

```bash
strace -p <pid>
```

It will display all the calls being made by etcd.

To display all the systemcall made by a program we use : 

```bash
strace -c touch /tmp/error.log
```

![[Kubernetes_-_CKS_25.png]]

#### Aquasec Tracee

[[Tracee]] allow to trace syscalls.

#### Restrict Syscalls with seccomp

[[Seccomp]]

#### SECCOMP in Kubernetes

[[Seccomp (Kubernetes)]]

### App Armor

[[AppArmor]]

#### App Armor in Kubernetes

[[App Armor (Kubernetes)]]

### Linux Capabilities

[[Linux Capabilities (Kubernetes)]]

## Minimizing Microservices Vulnerabilities

### Security Context

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-pod
spec:
  securityContext:
    runAsUser: 1001
  containers:
  - name: ubuntu
    image: ubuntu
    command: ["sleep", "3600"]
    securityContext:
      runAsUser: 1000        # Override podSecurity Context
	  capabilities:          # Can only be defined at containerLevel
	    add: ["MAC_ADMIN"]
```

### Admission Controller

[[Kubernetes - Admission Controller]]

### Pod Security Admission

[[Kubernetes - Pod Security Admission]]

### OPA - Open Policy Agent

> [!Note] PAS AU PROGRAMME CKS

[[Open Policy Agent]]
[[Open Policy Agent (Kubernetes)]]

### Secrets

By default secrets in etcd are not encrypted at rest. Meaning if we have access to the etcd we can get all the secrets of the cluster.

https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/

We just have to create this file and add the flag and volumes to the apiServer : 

```yaml
---
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
      - secrets
      - configmaps
      - pandas.awesome.bears.example
    providers:
      - aescbc:
          keys:
            - name: key1
              # See the following text for more details about the secret value
              secret: <BASE 64 ENCODED SECRET>
      - identity: {} # this fallback allows reading unencrypted secrets;
                     # for example, during initial migration
```

The providers are taken in order. If we put indentity at the top, there will be no encryption.

If a secret were created before encryption was enabled.

### Container Sandboxing

All containers on the same host share the same kernel.

From the host we can see all processes ran on all containers but with different pid from within the container. This is called process **id namespace**. If we kill the process on the host it will wipeout the container.

VMs on a host have to make syscall to access the underlying infrastructure through the hypervisor.

So we need to sandbox our containers to lower the risks.

We can use those techniques : 
- Seccomp
- AppArmor

It is very tedious to write dedicated profiles for each different applications.

There are no perfect solution in term of security. Every way has advantages and drawbacks. We need to choose what fit our needs.

#### GVisor

We want to improve the isolation between container and container and between the container and the operating system or the kernel.

GVisor is an additional brick between the containers and the kernel.

![[Kubernetes_-_CKS-5.png|336]]

GVisor contains 2 components.

![[Kubernetes_-_CKS-6.png|238]]

**Sentry** : 
- Independent application level kernel dedicated for containers
- Each container has its own gVisor
- Intercept and respond to container's system calls
- Sentry make the syscall to the API, it does not allow container direct access to the linux kernel
- It supports far fewer system call than the linux kernel only what is needed by containerized workload.
**Gofer** :
- File System proxy for containers

The problem is that not all applications will work with gVisor. So we need to test it by ourself if our apps work with it.

More weight to the CPU so it might make applications slower.

The [[OCI Runtime]] is runsc.

#### Kata Containers

These are Lightweight Virtual Machine for each container. There is a little performance tradeoff. This means that each container has its own VM Kernel. 

The best way is to run it on a dedicated machine like baremetal servers.

We can also use nested virtualisation using a VM in the cloud. Google Cloud support it but performances are very poor. 

The [[OCI Runtime]] is kata.

But the compatibility is full compared to gVisor.

#### Container Runtime

When we use the command `docker run -d nginx`.

Docker pull the image and run it.

We can run container directly using runc but we will not have the handling of Images, Volumes and Network.

![[Kubernetes_-_CKS-7.png|482]]

runC is the default container runtime used by cri.o and podman.

There are alternatives :
- kata-runtime
- runsc

As it respect OCI, we can use docker to run containers using other container runtime.

```bash
docker run --runtime kata -d nginx
```

#### Runtime class in Kubernetes

Once we have gvisor installed on all our node, we need to create an Object called RuntimeClass : 

![[Kubernetes_-_CKS-8.png|502]]

The runtime name can be anything but we need to install the handler before to make it work. The Ressource will still be created even if the handler is not on the nodes but the pod creation will fail.

We can verify that now we can't see the process anymore in the host because its handled and isolated by gVisor : 

![[Kubernetes_-_CKS-9.png]]

### Multi-tenancy

Multi-tenancy means having several teams on the same cluster and each one will get a tenancy. A tenancy assure isolation with other teams as they are using the same hardware but cannot see other teams resources.


|                               |                                       Multi-Team                                        |                            Multi-Customer                            |
| :---------------------------: | :-------------------------------------------------------------------------------------: | :------------------------------------------------------------------: |
|           **Focus**           |                      Internal organizational team within a company                      |                    External customers or clients                     |
|  **Isolation Requirements**   |                                    Strict Isolation                                     |       Stricter isolation an security measures than multi-team        |
|    **Resource Management**    |                         Use Kubernetes Namespaces for isolation                         |               Use Kubernetes namespaces for isolation                |
| **Governance and Compliance** |          Governed by internal policies and guidelines set by the organization           |      Ensure compliance with regulatory standards (GDPR, HIPAA)       |
|    **Access Restriction**     | Team Members have direct access to Kubernetes via Kubectl or through GitOps Controllers | Customers do not have access to the cluster- Kubernetes is invisible |

We have different levels of isolation : 


| Control Plain Isolation | Data Plane Isolation |
| :---------------------: | :------------------: |
|       Namespaces        |  Network isolation   |
|     Access controls     |  Storage Isolation   |
|         Quotas          |   Nodes Isolation    |

**Hard Isolation** => a client has a dedicated Node
**Soft Isolation** => clients share infrastructure and have dedicated namespaces 

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: team-a-resource-quota
  namespace: team-a
spec:
  hard:
    pods: "5"
    requests.cpu: "0.5"
    requests.memory: 500Mi
    limits.cpu: "1"
    limits.memory: 1Gi
```

Network Isolation can be done via Network Policies. Network Policies are applied at level 2 of the OSI Model.

By default network policies restrict everything that is not defined in the netpols. For example to restrict traffic from outside we just do :

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-external-egress
  namespace: namespace-worker
spec:
  podSelector: {}  # Selects all pods in namespace-worker
  policyTypes:
  - Egress
  egress:
  # Allow egress to all pods in all namespaces
  - to:
    - namespaceSelector: {}  # All namespaces
      podSelector: {}        # All pods
```

Storage Isolation can be done via dedicated Storage Classes. 1 for high-performance workloads and the other for standard workloads for example.


Node Isolation 
This is just putting workloads on dedicated node for specific client.

Taints

```bash
kubectl taint nodes node01 team=team-a:NoSchedule
```

Ce taint indique : _"aucun pod ne peut être planifié (scheduled) sur `node01`, sauf s'il possède une **toleration** correspondante"_.

```yaml
tolerations:
- key: "team"
  operator: "Equal"
  value: "team-a"
  effect: "NoSchedule"
```

To untaint a node : 

```bash
kubectl taint nodes node01 team=team-a:NoSchedule-
kubectl taint nodes node02 team=team-b:NoSchedule-
kubectl taint nodes node03 team=team-c:NoSchedule-
```


Priority Level :

We can define different priority level. This means that the api-server will take requests from certain critical namespace before others.

We can define priority level for any Kubernetes resources.

![[Kubernetes_-_CKS-10.png]]

![[Kubernetes_-_CKS-11.png]]

![[Kubernetes_-_CKS-13.png]]

![[Kubernetes_-_CKS-12.png]]

### Quality Of Service

[[Quality Of Service (Kubernetes)]]

### DNS isolation Multi-tenants

We can restrict DNS resolution to only resolve pods and service from the same namespace by modifying the core dns configmap :

![[Kubernetes_-_CKS-17.png]]

### Pod to Pod Encryption

![[Kubernetes_-_CKS-18.png]]

There are different approach to implement Pod-to-Pod encryption :
- Mutual TLS (mTLS) : service mesh Istio or Linkerd
- Cillium : IpSec or wireguard
- Calico : IpSec

#### Istio

[[Setup Istio TLS peer authent (Kubernetes)]]

#### Cilium

[[Cilium]]

## Supply Chain Security

1. Source : The source code is written by developers and tested locally
2. Build : Compiles and build the code, OWASP, dependency check or snyk to analyse the code and ensure it's free from vulnerability.
3. Test : Testing containers for vulnerabilities using tools like claire or trivy
4. Deploy : PodSecurity Admission, Network Policies, rbac.

Benefits are : 
- Early detection of vulnerabilitis
- Better resource management
- Improved compliance
- Efficient incident response
- Enhanced security posture

The risks are :
- Cyber attacks
- Operational disruptions
- Financial losses
- Regulatory and legal consequences
- Competitive disadvantage

SBOM (Software Bills of Materials) contains : 
- Software components
- Supplier Details
- Software Composition
- Security Vulnerabilities
- Licenses
- Version
- Patch Status

Benefits of SBOM are : 
- Transparency
- Incident response
- Dependency management
- Security
- Compliance

![[Kubernetes_-_CKS-28.png]]

There are 2 format for SBOM : 
- SPDX : Focus on licensing and legal compliance
- CycloneDX : Focus on security aspects such as identifying vulnerabilities and managing supply chain risks.

![[Kubernetes_-_CKS-32.png]]

![[Kubernetes_-_CKS-33.png]]

![[Kubernetes_-_CKS-34.png]]

![[Kubernetes_-_CKS-35.png]]

![[Kubernetes_-_CKS-36.png]]

![[Kubernetes_-_CKS-37.png]]

![[Kubernetes_-_CKS-38.png]]

We pick SPDX in an open-source projects and enterprise that need to ensure licensing compliance and trace sofware origins for security audits. 

Identifying vulnerabilities accross as software lifecycle and to ensure sofware integrity we will pick CycloneDX

![[Kubernetes_-_CKS-39.png]]
 

SBOM workflow : 
1. **Generate SBOM**![[Kubernetes_-_CKS-39.png]]
2. **Store SBOM**![[Kubernetes_-_CKS-40.png]]

3. **Scan SBOM** ![[Kubernetes_-_CKS-41.png]]
4. **Analyze Results**![[Kubernetes_-_CKS-42.png]]
5. **Remediate Issues** : We update the nginx package or choose another solution
6. **Monitor** : Integrate scanning in CI/CD pipelines and we update tools regularly and we setup alerts for vulnerability or compliance issues detected

![[Kubernetes_-_CKS-29.png]]

1 image server a unique problem : 
- 1 for frontend
- 1 for backend
- 1 for database

No data or state in containers because they are by definition stateless and ephemeral.

TO choose a base image we will check the last update which must be recent and the flag official image on docker hub.

We must make sure that our image is the slimmer as possible to enhance pull time and spin more instance more easily.

We can use minimal images for that. We need to install only necessary packages to run : 
- remove shells
- package managers
- tools (curl or wget)

We can separate dev image and prod image to suit our debug needs.

We also can use multi-stage builds to create lean, production-ready images.


For exemple : 
![[Kubernetes_-_CKS-30.png]]

![[Kubernetes_-_CKS-31.png]]

Launch a scan with syft : 

```bash
syft scan docker.io/kodekloud/webapp-color:latest -o spdx=/root/webapp-spdx.sbom
syft scan docker.io/kodekloud/webapp-color:latest -o cyclonedx-json=/root/webapp-sbom.sbom
```

To analyse an sbom with syft : 

```bash
grype sbom:/root/webapp-sbom.json -o json > /root/grype-report.json
```

![[Kubernetes_-_CKS-43.png]]

Find a particular severity :

```bash
jq -r '[.matches[] | select(.vulnerability.severity == "Critical")] | length' /root/grype-report.json
```

```bash
cat grype-report.json | jq -e '.matches[] | select(.vulnerability.id == "CVE-2022-48174")'
```

Automated using github actions : https://github.com/issamsisbane/supply_chain_security

### Kubelinter

Static analysis

![[Kubernetes_-_CKS-44.png]]

![[Kubernetes_-_CKS-45.png]]

Kubelinter : 
- Prevents misconfigurations
- Improves security
- Enhances reliability
- Enables automated reviews
- Ensure cost efficiency
- Helps achieve compliance

To use it :

```bash
kube-linter lint .
```

![[Kubernetes_-_CKS-46.png]]

![[Kubernetes_-_CKS-47.png]]

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      affinity:                                               #added
        podAntiAffinity:                                      #added
          requiredDuringSchedulingIgnoredDuringExecution:     #added
          - labelSelector:                                    #added
              matchExpressions:                               #added
              - key: app                                      #added
                operator: In                                  #added
                values:                                       #added
                - nginx                                       #added
            topologyKey: "kubernetes.io/hostname"             #added
	    containers:
	      - name: nginx
	        image: nginx:1.14.2
	        ports:
	        - containerPort: 80
	        securityContext:
	          runAsNonRoot: true
	          readOnlyRootFilesystem: true
	        resources:
	          requests:
	            cpu: 250m
	            memory: 64Mi
	          limits:
	            cpu: 500m
	            memory: 128Mi
```


### Secure Images

![[Kubernetes_-_CKS-48.png]]

We can restrict registry used in the cluster with different methods : 
- A custom admission controllers we build
- OPA with rego rules
- The built-in ImagePolicyWebhook

![[Kubernetes_-_CKS-49.png]]

![[Kubernetes_-_CKS-50.png]]


![[Kubernetes_-_CKS-52.png]]

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: image-bouncer-webhook
spec:
  selector:
    matchLabels:
      app: image-bouncer-webhook
  template:
    metadata:
      labels:
        app: image-bouncer-webhook
    spec:
      containers:
        - name: image-bouncer-webhook
          imagePullPolicy: Always
          image: "kainlite/kube-image-bouncer:latest"
          args:
            - "--cert=/etc/admission-controller/tls/tls.crt"
            - "--key=/etc/admission-controller/tls/tls.key"
            - "--debug"
            - "--registry-whitelist=docker.io,registry.k8s.io"
          volumeMounts:
            - name: tls
              mountPath: /etc/admission-controller/tls
      volumes:
        - name: tls
          secret:
            secretName: tls-image-bouncer-webhook
```

```yaml
apiVersion: v1
kind: Config
clusters:
- cluster:
    certificate-authority: /etc/kubernetes/pki/server.crt
    server: https://image-bouncer-webhook:30080/image_policy
  name: bouncer_webhook
contexts:
- context:
    cluster: bouncer_webhook
    user: api-server
  name: bouncer_validator
current-context: bouncer_validator
preferences: {}
users:
- name: api-server
  user:
    client-certificate: /etc/kubernetes/pki/apiserver.crt
    client-key:  /etc/kubernetes/pki/apiserver.key
```

### Kubesec

This is a static analysis tool to analyse kubernetes manifests in CI/CD tools.

To use it with the cli : 

```bash
kubesec scan pod.yaml
```

We can also use the hosted version of kubesec via api : 

```bash
curl -sSX POST --data-binary @"pod.yaml" https://v2.kubesec.io/scan
```

Or we can deploy it as a local server : 
```
kubesec http 8080 &
```


Exemple of analysis : 
```json
controlplane ~ ➜  cat kubesec_report.json | jq
[
  {
    "object": "Pod/node.default",
    "valid": true,
    "fileName": "node.yaml",
    "message": "Failed with a score of -27 points",
    "score": -27,
    "scoring": {
      "critical": [
        {
          "id": "Privileged",
          "selector": "containers[] .securityContext .privileged == true",
          "reason": "Privileged containers can allow almost completely unrestricted host access",
          "points": -30
        }
      ],
      "passed": [
        {
          "id": "ServiceAccountName",
          "selector": ".spec .serviceAccountName",
          "reason": "Service accounts restrict Kubernetes API access and should be configured with least privilege",
          "points": 3
        }
      ],
      "advise": [
        {
          "id": "ApparmorAny",
          "selector": ".metadata .annotations .\"container.apparmor.security.beta.kubernetes.io/nginx\"",
          "reason": "Well defined AppArmor policies may provide greater protection from unknown threats. WARNING: NOT PRODUCTION READY",
          "points": 3
        },
        {
          "id": "SeccompAny",
          "selector": ".metadata .annotations .\"container.seccomp.security.alpha.kubernetes.io/pod\"",
          "reason": "Seccomp profiles set minimum privilege and secure against unknown threats",
          "points": 1
        },
        {
          "id": "AutomountServiceAccountToken",
          "selector": ".spec .automountServiceAccountToken == false",
          "reason": "Disabling the automounting of Service Account Token reduces the attack surface of the API server",
          "points": 1
        },
        {
          "id": "RunAsGroup",
          "selector": ".spec, .spec.containers[] | .securityContext .runAsGroup -gt 10000",
          "reason": "Run as a high-UID group to avoid conflicts with the host's groups",
          "points": 1
        },
        {
          "id": "RunAsNonRoot",
          "selector": ".spec, .spec.containers[] | .securityContext .runAsNonRoot == true",
          "reason": "Force the running image to run as a non-root user to ensure least privilege",
          "points": 1
        },
        {
          "id": "RunAsUser",
          "selector": ".spec, .spec.containers[] | .securityContext .runAsUser -gt 10000",
          "reason": "Run as a high-UID user to avoid conflicts with the host's users",
          "points": 1
        },
        {
          "id": "LimitsCPU",
          "selector": "containers[] .resources .limits .cpu",
          "reason": "Enforcing CPU limits prevents DOS via resource exhaustion",
          "points": 1
        },
        {
          "id": "LimitsMemory",
          "selector": "containers[] .resources .limits .memory",
          "reason": "Enforcing memory limits prevents DOS via resource exhaustion",
          "points": 1
        },
        {
          "id": "RequestsCPU",
          "selector": "containers[] .resources .requests .cpu",
          "reason": "Enforcing CPU requests aids a fair balancing of resources across the cluster",
          "points": 1
        },
        {
          "id": "RequestsMemory",
          "selector": "containers[] .resources .requests .memory",
          "reason": "Enforcing memory requests aids a fair balancing of resources across the cluster",
          "points": 1
        },
        {
          "id": "CapDropAny",
          "selector": "containers[] .securityContext .capabilities .drop",
          "reason": "Reducing kernel capabilities available to a container limits its attack surface",
          "points": 1
        },
        {
          "id": "CapDropAll",
          "selector": "containers[] .securityContext .capabilities .drop | index(\"ALL\")",
          "reason": "Drop all capabilities and add only those required to reduce syscall attack surface",
          "points": 1
        },
        {
          "id": "ReadOnlyRootFilesystem",
          "selector": "containers[] .securityContext .readOnlyRootFilesystem == true",
          "reason": "An immutable root filesystem can prevent malicious binaries being added to PATH and increase attack cost",
          "points": 1
        }
      ]
    }
  }
]
```

### Trivy

What is a CVE ? Common Vulnerabilities and Exposures

A CVE can be : 
- everything that bypass security checks and do things that we should be able to do
- eveything that allow an attacker to mess up the system, performance, interupt system..

A CVE has a score between 0 and 10 : 

![[Kubernetes_-_CKS-53.png]]

We can use a CVE scanner like trivy to find CVE on our environnement.
A good way to lower the CVEs is to restrict to the minimum, the package and application in our environnemnent.

To launch a trivy scan : 

![[Kubernetes_-_CKS-54.png]]

```bash
trivy image --severity CRITICAL,HIGH nginx:1.18.0
```

Only show what will not be fixed by updating the package : 

```bash
trivy image --ignore-unfixed nginx:1.18.0
```

We can use trivy this way : 
```bash
docker save nginx:1.18.0 > nginx.tar
```

```bash
trivy image --input archive.tar
```

![[Kubernetes_-_CKS-55.png]]

Best practices : 
- Continuously rescan images
- Kubernetes Admission Controllers to scan images (we can scan images before there deployed as pods, it can provide latency so the better is to use local registry with prescan images).
- Integrate scanning into CI/CD pipelines

## Monitoring, Logging & Runtime Security

Even using these techniques : 
- Securing Cluster
- Minimizing Microservices Vulnerability
- Sandboxing Techniques
- MTLS Encryption
- Restricting Network Access

We always need to prepare in case something goes wrong and containers become compromized.

If a breach does occur its important we find it as soon as possible to take measures.

### Falco

How can we identity breaches that are already occured in the cluster ?

We can use Falco for this.

We saw earlier that we can monitor syscalls strace and tracee.

Its hard to just monitor the syscalls when we have thousands of application.

So a tool like falco will help identify suspicious activies on the cluster, such as deleting audit log file for example which will in practice never occur normally.

So Falco we help to identify and analyze threats.

Falco need to be placed between application and kernel to monitor syscalls.

It can be through :
- Falco Kernel Module => modified kernel code, intrusive not allowed by some managed kubernetes providers.
- eBPF => less intrusive and safer because all the code is tested before execution

We can install falco as a service isolated from the cluster in the nodes or as a daemon set.

![[Kubernetes_-_CKS-56.png]]

![[Kubernetes_-_CKS-57.png]]

Falco implement several rules by default
![[Kubernetes_-_CKS-58.png]]

![[Kubernetes_-_CKS-60.png]]

Falco filters :
- fd.name : file descriptor name, used to match events agains specific file (read or write)
- evt.type : filter system call by name (execve, open, accept...)
- user.name : filter the user
- container.image.repository : filter specific images by name
- container.id : id of a container
- proc.name : name of the process

![[Kubernetes_-_CKS-61.png]]

Using a list : 

![[Kubernetes_-_CKS-62.png]]

Using macro :

![[Kubernetes_-_CKS-63.png]]

Falco configuration is located at `/etc/falco/falco.yaml`

![[Kubernetes_-_CKS-64.png]]

The order is important. Last rule will override others.

![[Kubernetes_-_CKS-67.png]]

The `/etc/falco/falco_rules.yaml` is the default file use by falco containing built-in rules, lists and macros.

To add new rules or overwrite existing one, the better way is to rewrite the rule with change in another file `/etc/falco/falco_rules.local.yaml` if not if we update falco it will overwrite our changes.

![[Kubernetes_-_CKS-69.png]]

We need to reload the configuration for changes to be taken account : 

![[Kubernetes_-_CKS-70.png|371]]

**Différence avec `systemctl restart falco` :**

- **`kill -1` (SIGHUP)** : le processus reste vivant, garde le même PID, et se contente de relire ses fichiers de config/règles en mémoire. Pas d'interruption du service, la surveillance continue pendant le rechargement (ou avec une coupure minimale, selon comment Falco implémente son handler SIGHUP).
- **`systemctl restart falco`** : systemd tue complètement le processus puis en lance un nouveau. Ça implique :
    - une vraie coupure de la détection le temps du redémarrage
    - la perte de tout état interne en mémoire (compteurs, buffers, etc.)
    - potentiellement le déclenchement des `ExecStartPre`/`ExecStopPost` du unit file
    - un nouveau PID
    - si Falco a un `StartLimitBurst` dans son unit systemd, des redémarrages répétés pourraient finir par être bloqués

![[Kubernetes_-_CKS-71.png]]

journalctl -fu falco-modern-bpf

[https://falco.org/docs/getting-started/installation/](https://falco.org/docs/getting-started/installation/)
[https://github.com/falcosecurity/charts/tree/master/falco](https://github.com/falcosecurity/charts/tree/master/falco)
[https://falco.org/docs/rules/supported-fields/](https://falco.org/docs/rules/supported-fields/)
[https://falco.org/docs/rules/default-macros/](https://falco.org/docs/rules/default-macros/)
[https://falco.org/docs/configuration/](https://falco.org/docs/configuration/)

### Ensure immutability of containers at runtime

By default we can make in place update to containers in kubernetes : 

![[Kubernetes_-_CKS-72.png]]

We can prevent it using securityContext :

```yaml
securityContext:
	readOnlyRootFilesystem: true
```

We can mount specific volumes needed by nginx to be write on : 
```yaml
	volumeMounts:
	- name: cache-volume
	  mountPath: /var/cache/nginx
	- name: runtime-volume
	  mountPath: /var/run
volumes:
- name: cache-volume
  emptyDir: {}
- name: runetime-volume
  emptyDir: {}
```

Now it should fail : 

![[Kubernetes_-_CKS-73.png]]

Danger of using privileged : 
![[Kubernetes_-_CKS-74.png]]

We could write on the container and it even change the host machine : 

![[Kubernetes_-_CKS-75.png]]

![[Kubernetes_-_CKS-76.png]]

Step to secure a pod :
1. set readOnlyRootFilesystem
2. verify the status of pod and check logs
```logs
AH00558: httpd: Could not reliably determine the server's fully qualified domain name, using 172.17.0.6. Set the 'ServerName' directive globally to suppress this message
AH00558: httpd: Could not reliably determine the server's fully qualified domain name, using 172.17.0.6. Set the 'ServerName' directive globally to suppress this message
[Mon Aug 24 21:12:37.915664 2026] [core:error] [pid 1:tid 1] (30)Read-only file system: AH00099: could not create /usr/local/apache2/logs/httpd.pid.ZXdb2r
[Mon Aug 24 21:12:37.915876 2026] [core:error] [pid 1:tid 1] AH00100: httpd: could not log pid to file /usr/local/apache2/logs/httpd.pid
```
1. update the pod with correct volumeMounts emptyDir 
```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    name: triton
  name: triton
  namespace: alpha
spec:
  containers:
  - image: httpd
    name: triton
    securityContext:
      readOnlyRootFilesystem: true
    volumeMounts:
    - mountPath: /usr/local/apache2/logs
      name: log-volume
  volumes:
  - name: log-volume
    emptyDir: {}
```

### Kubernetes Audit

A request to the api server pass to 4 different stages : 

![[Kubernetes_-_CKS-77.png]]

We do not want to log and audit everything because it will create too much noise.

There are different verbose level for audit logs : 
- None
- Metadata
- Request
- RequestResponse

All Operations on secrets on all namespaces :

![[Kubernetes_-_CKS-78.png]]

==By default audit logs are disabled ?== 

We can direct log to a file or to a remote webhook like falco

![[Kubernetes_-_CKS-79.png]]

![[Kubernetes_-_CKS-80.png]]

```yaml
apiVersion: audit.k8s.io/v1
kind: Policy
omitStages:
  - "RequestReceived"
rules:
  # 1) NONE: health checks + non-resource endpoints
  - level: None
    nonResourceURLs:
      - "/healthz*"
      - "/livez*"
      - "/readyz*"
      - "/version"
      - "/metrics"

  # 2) NONE: noisy watch/list
  - level: None
    verbs: ["watch", "list"]

  # 3) Deployment changes in citadel namespace at RequestResponse
  - level: RequestResponse
    namespaces: ["citadel"]
    verbs: ["create", "update", "patch", "delete"]
    resources:
      - group: "apps"
        resources: ["deployments"]

  # 4) Secrets + ConfigMaps at Metadata
  - level: Metadata
    resources:
      - group: ""
        resources: ["secrets", "configmaps"]

  # 5) Namespace interactions at Request
  - level: Request
    resources:
      - group: ""
        resources: ["namespaces"]

  # 6) Everything else at Metadata
  - level: Metadata
```

NOT WORKING

```yaml
kind: Policy
omitStages:
  - "RequestReceived"
rules:
- level: None
  resources:
  - nonResourceURLs:
      - "/healthz*"
      - "/livez*"
      - "/readyz*"
      - "/version"
      - "/metrics"

- level: None
  verbs: 
  - watch
  - list
- level: RequestResponse
  verb: 
  - create
  - update
  - patch
  - delete
  namespaces:
  - citadel
  resources:
    - group: "apps"
      resources:
        - deployments

- level: Metadata
  resources:
  - group: ""
    resources: 
    - secrets
    - confimaps

- level: Request
        resources:
      - group: ""
        resources: ["namespaces"]

- level: Metadata
```




---

![[Pasted image 20260825191558.png]]

Tu dois voir `Seccomp: 2` (mode filter actif).

```
sudo groupadd --system etcd
sudo useradd -s /sbin/nologin --system -g etcd etcd
```


```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sweeper
  namespace: automated
spec:
  replicas: 1
  selector:
    matchLabels:
      app: sweeper
  template:
    metadata:
      labels:
        app: sweeper
    spec:
      serviceAccountName: bot-sa    # Added
      automountServiceAccountToken: false  # Prevent auto-mount
      containers:
        - name: sweeper
          image: busybox:1.36
          command: ["sleep", "3600"]
          volumeMounts:    # Section added
            - name: sa-token
              mountPath: /var/run/secrets/tokens
              readOnly: true
      volumes:   # Section added
        - name: sa-token
          projected:
            sources:
              - serviceAccountToken:
                  path: bot-token
                  expirationSeconds: 3600
                  audience: default
```





## Points Chauds 

Voir les manifests avec oc explain + api resources

### User Namespaces (hostUsers)

Depuis Kubernetes 1.36, les **User Namespaces** sont **GA et activés par défaut** (KEP-127). Ils permettent à un pod de tourner dans son **propre namespace utilisateur Linux**, distinct de celui de l'hôte. Conséquence : un processus qui se croit `root` (UID 0) à l'intérieur du conteneur correspond en réalité à un UID non privilégié côté hôte. Une évasion de conteneur ne donne plus root sur le nœud.

Le champ s'écrit **`spec.hostUsers`** (au niveau pod, pas dans `securityContext`) :

```
apiVersion: v1kind: Podmetadata:  name: app-with-usernsspec:  hostUsers: false        # nouveau namespace utilisateur pour ce pod  securityContext:    runAsUser: 1000    runAsNonRoot: true  containers:  - name: app    image: myapp:1.0.0
```

| Valeur          | Effet                                                                                                                   |
| --------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `true` (défaut) | Le pod partage le namespace utilisateur de l'hôte (comportement historique)                                             |
| `false`         | Kubernetes crée un namespace utilisateur dédié et **map** les UIDs/GIDs du pod vers une plage non privilégiée de l'hôte |

Prérequis runtime

L'effet réel dépend du runtime conteneur : **containerd 1.7+ ou CRI-O 1.25+** sont requis. Sur des runtimes plus anciens, le pod démarre mais le mapping UID/GID n'est pas appliqué, un audit `crictl inspect` ou un lecteur de `/proc/<pid>/uid_map` sur le nœud confirme la prise en compte effective.

Certaines fonctionnalités sont **incompatibles** avec `hostUsers: false` : volumes `hostPath` partagés avec des processus hors du pod, `CAP_SYS_MODULE`, ou tout besoin d'agir sur le namespace utilisateur de l'hôte.


Le port de la policy est celui du conteneur, pas celui du Service

C'est le piège numéro un des NetworkPolicies. Le champ `port` d'une règle désigne le port sur lequel **le conteneur écoute**, c'est-à-dire le `targetPort` du Service, jamais le `port` publié par le Service.

### Netpols

Avec un Service qui expose `8080` vers un conteneur qui écoute sur `80`, écrire `port: 8080` dans la policy bloque tout le trafic : la traduction d'adresse a déjà eu lieu quand le paquet atteint le Pod, et le port vu par la policy est `80`. Le symptôme est trompeur, la policy semble correcte et rien ne passe. Vérifiez avec `kubectl get svc backend -o jsonpath='{.spec.ports[0].targetPort}'`.

Les networks policies sont appliqués à la sortie du pod pour l'egress et l'entrée pour l'ingress par le CNI.

ce filtrage est **distribué**, pas centralisé. Chaque nœud applique les policies pour les pods qui tournent dessus. Il n'y a pas de "pare-feu central" par lequel tout transite — chaque nœud (via son agent CNI, par exemple `calico-node` ou `cilium-agent`) traduit les objets NetworkPolicy en règles locales.

```yaml
  ingress:
    - from:
        - namespaceSelector:
            matchExpressions:
              - key: kubernetes.io/metadata.name
                operator: NotIn
                values:
                  - danger
        - podSelector: {}  # autorise aussi les pods du même namespace
```

Autorise le traffic ingress de tous les namespaces sauf de danger + le traffic intra-namespace.

### Sécuriser un cluster existant

Vous avez un cluster en production et voulez le durcir rapidement ?

1. **Évaluer la posture actuelle**
    Exécutez un audit avec `kube-bench` pour identifier les failles de configuration selon le CIS Benchmark.
2. **Restreindre les accès**
    Appliquez le principe du moindre privilège avec RBAC : limitez les permissions des ServiceAccounts et des utilisateurs.
3. **Isoler le réseau**
    Déployez des Network Policies `deny-all` par défaut, puis autorisez explicitement les flux nécessaires.
4. **Protéger les Secrets**
    Activez le chiffrement at-rest des Secrets dans etcd si ce n'est pas déjà fait.

### DEBUG API SERVER

```
tail -f /var/log/pods/kube-system_kube-apiserver-controlplane_c363a7038f4951f76fd174220564d664/kube-apiserver/*.log
```

```
crictl logs $(crictl ps -a --name kube-apiserver -q | head -n1)
```

```
ID=$(crictl ps -a --name kube-apiserver -q | head -n1) && crictl ps -a --id $ID && crictl logs $ID
```

Log locations to check:

- `/var/log/pods`
- `/var/log/containers`
- `crictl ps` + `crictl logs`
- `docker ps` + `docker logs` (in case when Docker is used)
- kubelet logs: `/var/log/syslog` or `journalctl`

```
tail -f /var/log/pods/kube-system_kube-apiserver-*/kube-apiserver/*
```


https://istio.io/latest/docs/reference/config/security/peer_authentication/


### Secrets

Secrets in volume are to be privileged instead of env variable.

| Aspect                             | Variable env | Volume |
| ---------------------------------- | ------------ | ------ |
| Visible dans `docker inspect`      | Oui          | Non    |
| Visible dans `/proc/<pid>/environ` | Oui          | Non    |
| Mise à jour automatique            | Non          | Oui    |
|                                    |              |        |

Un secret monté en volume est rafraichi toutes les 60 secondes sauf 
**Les exceptions où ça NE se met PAS à jour automatiquement**

- **Montage avec `subPath`**
- **Secret marqué `immutable: true`**
- **Secret injecté comme variable d'environnement** (`env` / `envFrom`) : **jamais**

L'application doit avoir un watch dessus si on ne veut pas relancer le pod.

### Service Account

Par défaut, un pod utilise le serviceAccount default du namespace et ce dernier est donc monté dans le pod.

Hors pour la pluspart des applications web de production, elles n'ont pas besoin d'accèder à l'api de kubernetes. Ainsi il faut désactiver l'automount de ce service account avec : 

```
automountServiceAccountToken
```

Si besoin d'un sa par le pod, il faudrait au mieux pour chaque application créer un service account dédié pour les raisons suivantes : 

| Problème             | Conséquence                                                                                                                                    |     |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | --- |
| Identité partagée    | Plusieurs workloads apparaissent sous la même identité vis-à-vis de l'API                                                                      |     |
| Traçabilité réduite  | La corrélation d'audit devient moins fine                                                                                                      |     |
| Permissions héritées | Tout RoleBinding sur `default` s'applique à tous les [Pods](https://blog.stephane-robert.info/docs/conteneurs/orchestrateurs/kubernetes/pods/) |     |
Le ServiceAccount **du pod** n'a besoin d'aucune permission RBAC particulière pour monter des volumes... 

**Qui fait quoi ?**

1. **Le kubelet** est celui qui va chercher le Secret et monte le volume/injecte la variable d'env. Il le fait via l'**autorisation Node** (Node authorizer), un mécanisme séparé du RBAC classique, indépendant de la ServiceAccount attachée au pod.
2. **La ServiceAccount du pod** (celle montée dans `/var/run/secrets/kubernetes.io/serviceaccount`) n'entre en jeu **que si le code applicatif dans le conteneur appelle lui-même l'API Kubernetes** (via ce token). Si ton appli ne fait pas d'appels à l'API server, le RBAC de la SA est complètement hors sujet ici.


Ça veut dire que l'on peut créer un pod en montant un secret et le lire dans le pod sans avoir la permission get sur ce secret car c'est le kubelet qui va créer le pod et monté le secret.

Il faut donc faire attention avec la permission de créer des pods. Par exemple si tout est gérer via gitops et des MR, on peut eviter la création de pod là où ce n'est pas nécessaire.

### Security Context

Voir les capabilities actives : 
```bash
kubectl exec -it cap-demo -- cat /proc/1/status | grep Cap
capsh --decode=0000000000000400
```

Un conteneur `privileged: true` peut potentiellement :

- Monter n'importe quel device de l'hôte
- Accéder à des parties sensibles du filesystem hôte
- Charger des modules kernel

Dans la pratique, cela rapproche fortement le conteneur des privilèges de l'hôte. Le risque exact dépend du runtime, des mounts et de l'isolement réel, mais considérez-le comme **extrêmement risqué**.

Utilisez-le **uniquement** pour des outils système très spécifiques (monitoring réseau bas niveau, agents de nœud) et jamais pour des applications.

### CSR

- [X] Comment mettre une CSR dans un fichier yaml en 1 ligne 
```bash
cat test.pem | tr -d "\n"
```
- Savoir générer une CSR, trouvable facilement dans la doc Kubernetes.

### Packets

- [X] apt-get vs apt ? [[apt vs apt-get]]
- [X] apt-get -y => commande sans demande interaction utilisateur

### PSA

- [X] PSA Exceptions ? Possible via AdmissionConfiguration https://kubernetes.io/docs/tasks/configure-pod-container/enforce-standards-admission-controller/#configure-the-admission-controller

### YAML

- [X] Voir les problèmes d'indentation yaml : `cat -A <file>`

### Admission Controller Kubernetes

- [X] Comment utiliser ? ImagePolicyWebhook fonctionnement qu'est ce que ça fait ? => ImagePolicyWebhook tape sur une webhook interne ou externe qui renvoi un obkect particulier à l'api server pour autoriser ou nom l'utilisation de l'image. Il suffit d'un kubeconfig avec l'url du webhook et les certs pour mTLS et d'ajouter çá dans AdmissionConfiguration ainsi que d'activer l'admission controller sur l'api server

### User Kubernetes

- [X] Comment créer un utilisateur sur Kubernetes ? Les différentes manières
	a) Certificats clients X.509 (méthode "manuelle" classique)
	b) ServiceAccounts (pour les workloads, pas les humains, mais souvent détournés pour des accès "utilisateur" simplifiés)
	c) OIDC (OpenID Connect) — méthode recommandée en production
	d) Fournisseurs cloud managés (IAM)
	e) Webhook Token Authentication
	f) Fichier statique de tokens/mots de passe (déprécié, à éviter)

- [X] Comment les lister et les trouvers ? **Kubernetes n'a pas d'objet natif "User"**. Contrairement aux `ServiceAccount` (qui sont de vrais objets API), les utilisateurs humains sont gérés en dehors du cluster — Kubernetes ne fait que faire confiance à une identité authentifiée par un moyen externe.
- [X] Permissions par défaut ? => aucune permission par défaut sans role binding (sur le user ou sur le group)

### Service Account

- [X] Permission par défaut ? => Aucune permission par défaut mais dangereux de laisser monter le token tout le temps dans les pods car d'autres personne peuvent faire des rolebindings dessus et le token sera monté partout

### Static-analysis

- [X] Kubesec vs Kube-linter => Kubesec est plus orienté sécurité avec un score a atteindre alors que kube-linter est plus bonnes pratiques

### Secrets

- [X] remplacer un secret as env var => as volume => il faut que l'application gère cela path au lien d'env var  
- [X] Modifier un secret sans erreur : `echo -n "valeur" | base64` => important pour ne pas avoir d'erreur de ligne en trop

### ReplicaSets

- [X] Version history limit garde les anciennes version du replicasets expliquant pourquoi on les voit encore dans Argo.

### Seccomp

- [X] Où est la conf seccomp ? Comment on charge un profile ? souvent dans `/var/lib/kubelet/seccomp/profiles/` c'est le CRI qui charge le profile pas besoin de redemmarer le kubelet 
- [X] Comment on vérifie qu'un profil est chargé ? et sur le pod ?
```bash
grep Seccomp /proc/<pid>/status 
# 0 = Unconfined, 1 = Strict, 2 = Filter (profil en place)
```
- [X] Différence entre pod et container ? defini soit pour tous les containers via pod soit individuellement via container

### Etcd

- [X] Quel user doit être utilisé pour les datas ETCD si on est en static pod ? Depend de l'implem root ou etcd
- [X] Comment rajouter l'encryption des secrets au repos ? https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/

### Audit

- [X] Ecrire une audit policy et la lire, ou sont les logs ? logs de l'apiServer defini dans la conf
- [X] Ecrire une policy Falco, ou la lire ? dans la sortie de falco ou sur un fichier dependamment de la conf
- [X] Si je modifie l'audit policy le fichier s'est mis à jour automatiquement dans le pod de l'api-server ? il faut redemarrer l'api server pour que les changements soient pris en compte apparement. Pour redemarrer l'apiServer ont deplace le manifest du static pod ailleurs, on attends que ce soit supprimé côté `crictl` et le remets à sa place pour recreer le pod.

### Network Policies Cillium

- [X] Comment en créer et comment elle fonctionnent ?

### Istio

- [X] Rajouter du mTLS obligatoire sur un namespace ? entre 2 pods ? sur tout le cluster ? => tout gérable via PeerAuthentication https://istio.io/latest/docs/reference/config/security/peer_authentication/

### Docker

- [X] Comment modifier la conf du daemon ? fichier `/etc/docket/daemon.json` ou service
- [X] Quel est le socket utilisé ? `/var/run/docker.sock` modifier les permissions
- [X] Sécuriser docker ? vérifier la conf ? 
- [X] Savoir comment lancer des conteneurs ?

### Nginx Ingress

- [X] Comment rajouter le ssl-redirect ? avec l'annotation ? Voir la doc nginx dispo à l'exam
- [X] Comment faire du rewrite juste du path ? => Voir la doc nginx dispo à l'exam

### Checksum verification

- [X] Comment verifier des checksums d'archive ? `sha256sum -b` ou `sha512sum -b` dépendamment de la demande
- [X] Savoir pourquoi sha256sum -b ? pourquoi binary ?
- [X] Comment vérifier et/ou récuperer le checksum d'une image ? skopeo digest

### Apparmor

- [X] Comment vérifier si des profiles sont loader ? ou les placer ? => commande apparmor
- [X] A placer sur tous les nodes ou forcer un node sur le déploiement
- [X] le chemin par défaut : /etc/apparmor.d/usr.shim.nginx ?

Les profiles sont ici généralement : 

```bash
# Profils disponibles 
ls /etc/apparmor.d/cat 
ls /sys/kernel/security/apparmor/profiles
```

Vérifier si apparmor est activé sur le node : 

```bash
aa-enabled
```

Chargé un profil sur un node : 

```shell
 apparmor_parser -q <fichier-avec-le-profile>
```

avec `-C` on passe en mode complaint et pas enforce par défaut

- [X] C'est toujours le cas si le node redémarre ? il faut que le profile soit dans `/etc/apparmor.d/`

Vérifier si le profile est chargé sur le node : 

```bash
aa-status | grep <nom-du-profile>
```

**ATTENTION** le nom du profile est différent du nom du fichier qui contient le profile.

Vérifier si le profile est chargé dans le pod :

```shell
kubectl exec hello-apparmor -- cat /proc/1/attr/current
```

### Kubelet

```yaml
# Activer l'autorisation 
webhookauthorization:  mode: Webhook
```

- [X] ça sert à quoi ça ? => délègue l'authorization à l'apiServer depuis le kubelet

### CIS Benchmark

- [X] Comment lancer un benchmark sur un node particulier ?

```bash
# Scan du kubelet uniquement
kube-bench run --targets node
```

IL FAUT LE LANCER SUR LE NODE SURLEQUEL ON DEMANDE

### Trivy

Deux options méritent une explication : `--ignore-unfixed` masque les CVE pour lesquelles aucun correctif n'est publié, utile pour ne pas bloquer un build sur un problème que personne ne peut résoudre, mais dangereux si vous l'activez sans suivre ces vulnérabilités par ailleurs. `--exit-code 1` est ce qui transforme le scan en **garde-fou** : sans lui, Trivy affiche les CVE et le job reste vert.

```bash
trivy image nginx:1.25.3
trivy image --ignore-unfixed nginx:1.25.3
trivy image --exit-code 1 --severity CRITICAL nginx:1.25.3
```

### JSONPATH

- [X] Refaire une passe dessus, comment ça marche ? Savoir rapidement comment récupérer des infos particulière.

### GatwewayAPI

Pas dans le scope de l'examen

### Telecharger binaire depuis Github

- [X] Comment faire ?

```bash
curl -L -O https://github/../<my-binary>.tar.gz
```

### API SERVER

- [X] Forcer le redemarrage ? => Deplacer le manifest et le remettre 
- [X] Acceder à l'api via curl dans un pods

```bash
curl https://kubernetes.default/api/v1/namespaces/restricted/secrets \
 -H "Authorization: Bearer $(cat /run/secrets/kubernetes.io/serviceaccount/token)" \
 -k
```

### Seccomp vs AppArmor

- **Secure computing mode (seccomp)**: Filter which system calls a process can make
- **AppArmor**: Restrict the access privileges of individual programs


### Linux Capabilities

- Each capability has a set of system calls (syscalls) that a process can make.

You can use Linux policy-based mandatory access control (MAC) mechanisms, such as AppArmor

For example, a root user in a privileged container might be able to use the `CAP_SYS_ADMIN` and `CAP_NET_ADMIN` capabilities on the node, bypassing the runtime seccomp configuration and other restrictions.

Additionally, you can run workloads in user namespaces by setting `hostUsers: false` in your Pod manifest. This lets you run containers as root users in the user namespace, but as non-root users in the host namespace on the node. This is still in early stages of development and might not have the level of support that you need. For instructions, refer to [Use a User Namespace With a Pod](https://kubernetes.io/docs/tasks/configure-pod-container/user-namespaces/)

### Cilium netpols

Si on met une règle deny explicite toute les règles allow sont bloqués.

Si on veut mettre du deny all par défaut il faut donc mettre seulement du deny implicite. Le deny implicite s'active meme quand la seule regle est une egressDeny.   

Comme ça : 

```yaml
apiVersion: cilium.io/v2
kind: CiliumClusterwideNetworkPolicy
metadata:
  name: cluster-deny-all
spec:
  endpointSelector: {}
  ingress:
    - {}
  egress:
    - {}
```
### Env vars Secrets

Please note that the environment variable method might be more prone to leakage due to crash dumps in logs and the non-confidential nature of environment variable in Linux, as opposed to the permission mechanism on files.

### Falco Exemple k8s audit log

```yaml
    - rule: Terminal shell in container
      condition: >
        spawned_process and container
        and shell_procs and proc.tty != 0
        and not k8s.ns.name in (debug-namespace, dev)
```

### Audit logs

```
`cat /var/log/kubernetes/audit.log | jq 'select(.verb=="create")'`
```

image digest : 

```
`skopeo inspect docker://nginx:1.25 | jq -r '.Digest'`
```
### Admission controller

Mutating et GitOps ? 

ValidattingAdmissionPolicy à l'examen, dans kube depuis 1.30 pas de mutating car kube 1.36 et l'exam est en kube 1.35.

3 resources :
- ValidatingAdmissionPolicy
- ValidatingAdmissionPolicyBinding
- Parameters => on défini le type de resource dans la polcy configmap ou CRD rule

### Image

- image used in production should not contain shells or debugging utilities, as an [ephemeral debug container](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/#ephemeral-container) can be used for troubleshooting.

- Avoid using image tags to reference an image, especially the `latest` tag, the image behind a tag can be easily modified in a registry. Prefer using the complete `sha256` digest which is unique to the image manifest. Th

### Scaling

**Le principe de base**

- `requests.memory` = ce que le pod est garanti d'avoir, utilisé par le scheduler pour placer le pod sur un nœud avec assez de ressources disponibles.
- `limits.memory` = le plafond que le pod ne peut pas dépasser (au-delà, le conteneur est tué par un OOM kill, spécifique à ce pod).

**Le problème quand `limit` > `request`**

Le scheduler réserve seulement la valeur du **request** sur le nœud, pas celle du **limit**. Ça veut dire qu'un nœud peut accueillir plusieurs pods dont la somme des _requests_ tient dans la mémoire disponible, mais dont la somme des _limits_ dépasse largement la capacité réelle du nœud.

Exemple concret :

- Nœud avec 8 Go de RAM
- 4 pods avec `request: 1Gi` / `limit: 4Gi` chacun
- Le scheduler accepte les 4 pods (4×1Gi = 4Gi ≤ 8Gi disponibles)
- Mais si les 4 pods montent tous en charge et consomment jusqu'à leur limite (4×4Gi = 16Gi), le nœud n'a plus assez de mémoire

**Conséquence**

Contrairement au CPU (compressible, throttling possible), la mémoire n'est pas compressible. Si le nœud entier manque de mémoire, le kubelet doit évincer des pods pour libérer de la place — et ça peut toucher **n'importe quel pod du nœud**, pas seulement celui qui a causé la surconsommation. C'est ce qu'on appelle l'exposition du nœud entier aux problèmes d'OOM (Out Of Memory) : au lieu d'un OOM kill ciblé et prévisible sur le conteneur fautif, on risque une instabilité globale du nœud.

**Bonne pratique**

Beaucoup d'équipes recommandent de fixer `request == limit` pour la mémoire (QoS class "Guaranteed"), justement pour éviter ce scénario de sur-souscription (overcommit) qui rend le comportement du nœud imprévisible sous charge.

Solutions :

- **HPA (Horizontal Pod Autoscaler)** : scale en nombre de pods, pas en resources par pod. Ça reste totalement compatible avec `request == limit` — en fait c'est même le combo classique en prod : chaque pod a une taille fixe et prévisible, et on ajuste le nombre de replicas selon la charge.
- **VPA (Vertical Pod Autoscaler)** : lui recalcule le request/limit dans le temps selon l'usage observé. C'est l'outil qui répond à ton problème — au lieu de laisser une marge manuelle "au cas où", VPA ajuste automatiquement le request pour coller à la conso réelle.
- **Cluster Autoscaler** : ajoute/retire des nœuds selon la pression sur les requests. Il ne résout pas le sur-provisionnement au niveau du pod, mais absorbe le fait que les requests sont fixes en ajustant la capacité du cluster.

## Questions Examens

1. Rajouter POD SECURITY CONSTRAINTS sur un namespace
2. Rajouter mTLS avec Istio : PeerAuthentication CRD + label sur namespace
3. Network Policy être très à l'aise !!!
4. Network Policy Cilium être très à l'aise + savoir rajouter mTLS via network policy
5. Falco : comment rajouter une règle et la monitorer
6. Audit logs kubernetes comment rajouter des règles 
7. Tester checksum image et binaire
8. SBOM génération avec bom et trivy et analyse avec trivy
9. Pod Security Context : Exemple un pod se lance pas car il ne respecte pas les security context => il faut juste adapter le pod
10. CIS Benchmark, ajuster un élément dans le contoleplane api server ou etcd (permissions des dossier...) Bien penser à rajouter les bon volumes dans le static pods
11. Erreur api serveur => a réparer, regarder les logs /var/logs/pods/kube-api_server*
12. Update version de node comme CKA classique
13. Signer et revoquer des certificate request et recupérer le certificat signé si accepté
14. Docker hardening et savoir lancer des conteneurs docker
15. Créer un Ingress, ajouté le https via tls certificate (API GATEWAY pas au programme)
16. RBAC => créer des roles, les attribuer, supprimer le montage automatique de token et monter le token du service account manuellement
17. Rajouter l'encryption etcd et savoir vérifier

## Resources

- https://killercoda.com/killer-shell-cks
- https://kodekloud.com
- https://notes.kodekloud.com
- https://killer.sh


## Docs

### Doc Officielle

La documentation officielle disponible est les éléments suivants : 

- **Kubernetes Documentation:** [**https://kubernetes.io/docs/**](https://kubernetes.io/docs/)
    Note that using the search function on [https://kubernetes.io/docs/](https://kubernetes.io/docs/) is allowed, but you must not open external search results.
- **Kubernetes Blog:** [https://kubernetes.io/blog/](https://kubernetes.io/blog/)
- **Falco** documentation [https://falco.org/docs/](https://falco.org/docs/)
- **Bom** documentation [https://kubernetes-sigs.github.io/bom/cli-reference/](https://kubernetes-sigs.github.io/bom/cli-reference/)
- **etcd** documentation [https://etcd.io/docs/](https://etcd.io/docs/)
- **NGINX Ingress Controller** Documentation [https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/)
- **Cilium** Documentation [https://docs.cilium.io/en/stable](https://docs.cilium.io/en/stable)
- **Istio** Documentation [https://istio.io/latest/docs/](https://istio.io/latest/docs/)

### Doc Utile

### NGINX
https://kubernetes.github.io/ingress-nginx/examples/rewrite/k

### AppArmor
https://kubernetes.io/docs/tutorials/security/apparmor/

### Seccomp
https://kubernetes.io/docs/reference/node/seccomp/

### Security Features
https://kubernetes.io/docs/concepts/security/linux-kernel-security-constraints/
https://kubernetes.io/docs/concepts/security/security-checklist/

### ServiceAccount
https://kubernetes.io/docs/concepts/storage/projected-volumes/#serviceaccounttoken

### AdmissionControllers
https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/
https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#imagepolicywebhook
https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/

### BOM
https://kubernetes-sigs.github.io/bom/cli-reference/bom_generate/

### PSA
https://kubernetes.io/docs/concepts/security/pod-security-admission/

### Cilium Policies
https://docs.cilium.io/en/latest/security/policy/layer3/