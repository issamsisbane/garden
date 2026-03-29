[Kubernetes Myth #09: ClusterIP Services Always Use Round-Robin Load Balancing - DEV Community](https://dev.to/rajeshdeshpande02/kubernetes-myth-09-clusterip-services-always-use-round-robin-load-balancing-139o)

With many pods selected by a service the load-balancing isn't using round-robin but a random statistically based algorithm to redistribute the traffic.

[Load Balancing in Kubernetes. Services In Kubernetes | by Natarajan | Medium](https://medium.com/@natrajrams4/load-balancing-in-kubernetes-53bfb7b842be)

It exists two mode : 
- kube-proxy - iptables : by default we can alter behavior
- kube-proxy - ipvs : we can alter behavior

By default its random : [kubernetes - How openshift service loadbalance between pods? - Stack Overflow](https://stackoverflow.com/questions/68334574/how-openshift-service-loadbalance-between-pods)