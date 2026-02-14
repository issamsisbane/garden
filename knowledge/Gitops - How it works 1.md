# How it works 

![[Pasted image 20250201201612.png]]

We will install a Flux or Argo controller in our cluster. 
Which will constantly check in our Git Repo (containing our infrastructure template files) for changes. 

It's called **Reconciliation Loop**.

We just define the state and the GitOps operator will make sure the cluster reflect this state. If not it will make the necessary changes.

For example, if we changes the image of a deployment it will create new pods with the new images automatically.

We have then a full history of everything that happened on our Kubernetes Cluster.

# GitOps Workflow:

- Git repository holds all configuration for applications and infrastructure
- Cluster pulls changes and deployment information
- GitOps controller runs a constant loop to match Git state with cluster state