# Before Kubernetes

Before Kubernetes we would have differentes VMs behind a Load Balancers. Each VMs would have docker containers. We would have the same VMs we the same containers in it. And so the load balancer will redirect the load to one of the VM. 

It was all provisionned using ansible, and we would have to do everything consciently. For exemple, if we have too much load on the current infrastructures we would have to create and provisionned more vms and so we will create and provisionned each VMs.
![[Before_Kubernetes.drawio.png]]

# After Kubernetes

Kubernetes is the Operating System of the cloud. It will replace the Load Balancer in the previous architecture to be a control plane. Then we wouldn't to do everything by hand. Indeed if we have too much load for the current infrastrucures we would just have to update a yaml and tel kubernetes we need more of that containers and it will add more automatically.

![[After_Kubernetes.drawio.png]] 

A VM is now called a node. 
We say to kubernetes what we want and then he will figure it out. For instance, if we want 3 instances of an application. If one fails then kubernetes will set up a new one to match the configuration we specified et then delete the failed one.

We can also scale up or down using metrics (cpu usage, number of users...).