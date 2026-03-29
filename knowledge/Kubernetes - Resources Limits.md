```
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: httpd-pod
  name: httpd-pod
spec:
  containers:
  - image: httpd:latest
    name: httpd-container
    resources: 
      limits:
        cpu: 100m
        memory: 20Mi
      - [ ] requests:
        cpu: 100m
        memory: 15Mi 
  dnsPolicy: ClusterFirst
  restartPolicy: Always
```