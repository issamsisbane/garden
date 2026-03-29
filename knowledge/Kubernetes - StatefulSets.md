> "In Kubernetes, several types of workload controller primitives exist, one of which is the [StatefulSet](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/). 
> 
> A StatefulSet manages the deployment and scaling of a set of Pods, and provides guarantees about the ordering and uniqueness of those Pods. 
> 
> Like a Deployment, a StatefulSet manages Pods that are based on an identical container spec, but unlike a Deployment, a StatefulSet maintains a sticky identity for each of its Pods. These Pods are created from the same spec, but are not interchangeable; each has a persistent identifier that it maintains across rescheduling."

https://developer.hashicorp.com/vault/tutorials/kubernetes/kubernetes-raft-deployment-guide