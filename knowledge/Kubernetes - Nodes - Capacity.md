Les nodes kubernetes ont des limites de CPU, de RAM mais aussi de nombre de pods. 

Pour voir le nombre de pod deployé par node : 
``` sh
kubectl get pods -o wide --all-namespaces | awk '{print $8}' | sort | uniq -c
```

Pour voir les limites par node : 
```
oc describe nodes | grep -i "pods" -A 2
```

```
kubectl get nodes -o custom-columns=NAME:.metadata.name,PODS:.status.capacity.pods
NAME
```