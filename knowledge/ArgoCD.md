https://www.youtube.com/watch?v=MeU5_k9ssrs
 
# Without ArgoCD

![[Pasted image 20250112160101.png]]

## Challenges with this approach : 
* Install and setup tools (kubetcl)
* Configure access to Kubernetes
* Configure access to cloud platforms
* Security Challenge
* No Visibility of deployment status (What is the state of the infra, did it work ? did it failed ?)

![[Pasted image 20250112164927.png]]

The CD part can be improved a lot.

ArgoCD was build as a CD tool for Kubernetes based on GitOps.

ArgoCD is a part of K8s cluster
ArgoCD agent pulls K8s manifest changes and applies them
We are in a Pull workflow and no longer to a Push workflow like before.

As best practices, we separate **App Source Code Git Repos** and **App Configuration Git Repos**

![[Pasted image 20250112165825.png]]

![[Pasted image 20250112170003.png]]
We would always update the infra using the git repositories by commiting. 
But it's possible to configure argoCD to not sync manual cluster changes automatically but just send an alert instead.

![[Pasted image 20250112170342.png]]
![[Pasted image 20250112170516.png]]
![[Pasted image 20250112170531.png]] 