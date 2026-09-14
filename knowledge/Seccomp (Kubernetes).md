# Seccomp (Kubernetes)

```bash
kubectl run amicontained --image docker.io/jess/amicontained amicontained -- amicontained
```

![[Kubernetes_-_CKS_32.png]]

Kubernetes doesn't implement Seccomp by default.

To enable it : 

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: amicontained
  namespace: default
spec:
  securityContext:
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: amicontained
    args:
      - amicontained
    image: "docker.io/jess/amicontained:latest"
    securityContext:
      allowPrivilegeEscalation: true
```

![[Kubernetes_-_CKS_32-1.png]]

We can see seccomp is enabled and there are more syscalls blocked.

By default kubernetes does this : 
```yaml
spec:
  securityContext:
   seccompProfile:
     type: Unconfined
```

We can use a custom seccomp profile : 

```yaml
spec:
  securityContext:
   seccompProfile:
     type: Localhost
	 localhostProfile: <path-to-custom-json-file>
```

The different types are : 
- Localhost - a profile defined in a file on the node should be used. The file's location relative to `<kubelet-root-dir>/seccomp` which is `/var/lib/kubelet/seccomp`.
- RuntimeDefault - the container runtime default profile should be used.
- Unconfined - no profile should be applied.

For exemple this would use a custom profile to just log all system calls made by the container : 

![[Kubernetes_-_CKS_33.png]]

![[Kubernetes_-_CKS_34.png]]

To associate syscall with their name we can use : 

```bash
grep -w 35 /usr/include/asm/unistd_64.h
```

We can also use the tracee tool to do the same : 

![[Kubernetes_-_CKS_35.png]]

We can disable all syscalls like this : 
![[Kubernetes_-_CKS_37.png]]

It will cause the container to not start, it's secure but we can do anything : 
![[Kubernetes_-_CKS_36.png]]

Another way is to firstly launch the container without restriction and use tracee to list all the system calls needed and then create a dedicated profile for the pod. But our application will need to do everything it can do to allow us to identify all the needed syscalls.

It is kind of difficult to use this because we need the policy on all the node. For all the pod to have a policy dedicated, it will be unmanageable.

- Le kubelet ne charge pas le contenu JSON du profil en mémoire lui-même. Il se contente de transmettre au runtime CRI (containerd, CRI-O) le chemin du profil (`localhostProfile` relatif à `/var/lib/kubelet/seccomp/`).
- C'est le runtime de conteneur (via runc en général) qui **lit le fichier sur disque au moment de la création du conteneur**, pour construire le filtre seccomp (BPF) qui sera appliqué au process.
- Une fois le filtre appliqué à un process au démarrage, il est **immuable** — un filtre seccomp ne peut pas être modifié à chaud sur un process déjà lancé (on ne peut que l'ajouter, pas le remplacer/assouplir).

https://kubernetes.io/docs/tutorials/clusters/seccomp/

[[Kubernetes - CKS - Seccomp automated]]