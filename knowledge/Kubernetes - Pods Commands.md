
# Kubernetes - Pods Commands

- [[Kubernetes - Create a yaml definition pod for cli]]
- [[VIM - Paste formatted YAML]]

## Display more information about pods
```
k get pods -o wide
```

## Launch a command inside a pod
```
k exec -it <pod-name> -- /bin/bash 
# or /bin/sh
```

## Create a sleeping pod

**Exemple pod sleep infinty**

```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: api-test
  name: api-test-pod
spec:
  serviceAccountName: node-viewer-service
  containers:
  - image: nginx
    name: api-test
    command: ["/bin/sleep", "infinity"]
    restartPolicy: "Never"
    resources: {}
  restartPolicy: "Never"
  dnsPolicy: ClusterFirst
status: {}
```
