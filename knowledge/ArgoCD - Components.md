There are 3 differents components in ArgoCD. 

# API/Web Server

Its a gRPC /REST server exposing the API consumed by the web ui and cli. The only component we will be interacting with.

It allows to : 
- Manage applications : 
	- Create
	- Delete
	- Update

- Operate applications
	- Rollbak
	- Sync
- Authentication
# Repo Server

Internal service responsible of cloning remote git repos and generate the needed kubernetes manifests

# Application controller

Its a Kubernetes controller which continuously monitors running applications and compares the current, live state against the desired target state. 

- It communicates with Repo Server to get the generated manifests.
- It communicates with the API to get actual cluster state. And make the necessary changes
- Deploy to destination clusters
- Detects OutofSync Apps and take corrective actions
- Invokes user-defined hooks for lifecycle events (PreSync, Sync, PostSync)

# Additional components

**Redis** for caching
**Dex** for identity service to integrate with external identity providers.
**ApplicationSet** Controller which autmates the generation of Argo CD Applications.