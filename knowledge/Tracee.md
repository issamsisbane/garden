# Aquasec Tracee

Opensource Tool to trace syscalls on a container using eBPF (Extended Berkeley Packet Filter) to trace the system at runtime. It can run programs directly in the kernel space without interfering with the kernel source code or loading any kernel modules.

eBPF programs are used to create tools such as tracee that can monitor the OS and detect suspicious behaviour.

We can run tracee as a container.

## Prerequisites

We need to mount these volumes : 


| Bind Mounts                   | Purpose           |
| ----------------------------- | ----------------- |
| /tmp/tracee                   | Default Workspace |
| /lib/modules (Read Only Mode) | Kernel Headers    |
| /usr/src (Read Only Mode)     | Kernel Headers    |

We also need to run the container as privileged because tracee needs additional capabilities.

## Exemple of use

Trace syscalls from a single command : 

![[Kubernetes_-_CKS_26.png]]

Trace syscalls from all new processes : 
![[Kubernetes_-_CKS_27.png]]

Trace syscalls from all new containers : 
![[Kubernetes_-_CKS_28.png]]