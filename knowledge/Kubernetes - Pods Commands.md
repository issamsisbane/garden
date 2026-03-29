
#### Display more information about pods
```
k get pods -o wide
```

#### Launch a command inside a pod
```
k exec -it <pod-name> -- /bin/bash 
# or /bin/sh
```

[[Kubernetes - Create a yaml definition pod for cli]]
[[VIM - Paste formatted YAML]]