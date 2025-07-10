# What is it ?

It defines source and destination to deploy group of [[Kubernetes]] resources.

The source is the git repository containing our manifests. 
The destination is the cluster and namespace where we wants to deploy.

# Sources Supported

- [[Helm Charts]]
- [[Kustomize]] application
- Directory of yaml files
- [[Jsonnet]]