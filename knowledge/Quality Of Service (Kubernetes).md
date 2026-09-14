# Quality Of Service (Kubernetes)

- **Guaranteed** : If we define requests and limits the same and every container of the pod.
- **Burstable** : The second to get delete in case of node resource pressure. Request < Limits
- **Best Effort** : The first to get deleted in case of node resource pressure. No requests or limits set.

If we set limit, then request is automatcally set equal to limit

### Quality of Service - Network

Using Cillium, we can limit throughput of namesapce using netpols : 

![[Kubernetes_-_CKS-14.png]]

![[Kubernetes_-_CKS-15.png]]

### Quality Of Service - Storage


![[Pasted image 20260822221047.png]]