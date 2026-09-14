# Linux Capabilities (Kubernetes)

Even with seccomp disable we can't change the date on a container : 

![[Kubernetes_-_CKS_52.png]]

This is because of linux Capabilies.

![[Kubernetes_-_CKS_53.png]]

Before we had just privileged process with full right on kernel ran as root user 0 and unprivileged process.

Today permissions are separated as different capability which give a more granular control over **linux Capabilities**.

![[Kubernetes_-_CKS_54.png]]

To get capability needed for a command we do 

```bash
getcap /usr/bin/ping
/usr/bin/ping = cap_net_raw+ep
```

To get capability of a process :

```bash
ps -ef | grep /usr/sbin/sshd | grep -v grep
getpcaps 779
```

![[Kubernetes_-_CKS_55.png]]

By default a container even launch as root user is started with limited Capabilites.

To adjust the system clock we need the SYS_TIME capability.

To add capability we need to add this to the **CONTAINER**

```yaml
spec:
  containers:
  - name: test
    securityContext:
      capabilities:
        add: ["SYS_TIME"]
		drop: ["CHOWN"]
```