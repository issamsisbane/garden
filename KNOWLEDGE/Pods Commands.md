
#### Display more information about pods
```
k get pods -o wide
```

#### Launch a command inside a pod
```
k exec -it <pod-name> -- /bin/bash 
# or /bin/sh
```

[[Create a yaml definition pod for cli]]
[[Paste formatted YAML]]