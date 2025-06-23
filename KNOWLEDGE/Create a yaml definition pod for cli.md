```
k run nginx --image=nginx --dry-run=client -o yaml > nginx.yaml
```

The --dry run allow to not execute the command in the cluster.