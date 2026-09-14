# App Armor (Kubernetes)

Prerequisities : 
- k8s version > 1.4
- AppArmor Kernel module enabled on all nodes
- AppArmor Profile loaded in the Kernel
- Container Runtime should be supported

Exemple : 

![[Kubernetes_-_CKS_50.png]]

To specify the apparmor rule we do : 

```yaml
spec:
  securityContext:
    appArmorProfile:
      type: Localhost
      localhostProfile: apparmor-deny-write
```

![[Kubernetes_-_CKS_51.png]]
