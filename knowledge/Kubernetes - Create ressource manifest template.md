We can use this command to create pod directly without writing by hand : 

```
kubectl run pod-nginx --image=nginx:latest --labels="app=nginx" -o yaml --dry-run=client > nginx.yaml
```

Then we can overrides the manifest created.

https://kubernetes.io/docs/reference/kubectl/generated/kubectl_run/