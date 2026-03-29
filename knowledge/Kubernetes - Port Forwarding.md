Port forwarding allow to associate a port from our computer to a the port of some pod. 

``` bash
kubectl port-forward pods/mealie 9000
```

We can also port forward to access a service.