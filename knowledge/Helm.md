Helm is install on our machine and not on the cluster directly. It will connect to the [[Kubernetes]] cluster to make commands.  

Helm is a packet manager for kubrenetes. We can use it to Install, Update or Rollback Kubernetes Application. 

[Helm and Helm Charts Explained](https://www.youtube.com/watch?v=w51lDVuRWuk)

[[Helm - Using Charts]]
[[Helm - Charts]]
[[Helmfile]]
[[Helm - Creating Charts]]
[[Helm - Commands]]
# Helm Versions

Helm provides 2 versions that are currently used by organizations. Most use the v3 but some use the v2. 


| Helm v2                             | Helm v3                           |
| ----------------------------------- | --------------------------------- |
| Client/Server model                 | Client only                       |
| Depends on the 'Tiller' Service     | Uses 'Secrets' as storage driver  |
| Uses 'ConfigMaps' as storage driver | Uses User Namespace               |
| Uses Tiller Namespace               | Improved Chart Upgrade Strategies |
| More Dependencies / More Complex    | Less Dependencies / Less Complex  |


The key difference between those 2 versions are the removal of Tiller in version v3. Tiller was an additional server used to manages changes to Kubernetes. In v3, Helm cli directly use the Kubernetes API to manages changes and resources providing more granularity for access control and removing additional unnecessary complexity.

# Helm Commands
# Plugins

[[Helm - Datree]]