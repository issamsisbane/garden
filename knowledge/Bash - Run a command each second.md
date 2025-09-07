``` sh
watch -n 1 "kubectl get pods"
```

We have to write the full command because it will be executed in another shell where .bashrc is not available.

We can also use the `--watch` to continuously monitor a command for changes : 

```
kubectl get pods --watch
```