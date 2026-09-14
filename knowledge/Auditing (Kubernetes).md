# Auditing (Kubernetes)

[[Auditing]] in kubernetes is mandatatory. We need to enable audit logs.

## Audit Logs

Exemple of a kubernetes audit log :

![[Kubernetes_-_CKS_12-1.png]]

## Policy Types

There are differents Audit policies : 
- **None**
- **Metadata** : Requests metadata to the api-server only
- **Request** : Requests metadata and request body but not the response
- **Response** : Requests metadata, requests body and the response

## Policies Exemple :

1. A policy to exclude log to get and list pods api call 

```yaml
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
  - level: None
    verbs: ["get", "list"]
	resources:
	  - group: ""
	    resources: ["pods"]
```

2. A policy to log metadata from events on pods :

```yaml
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
  - level: Metadata
    verb: ["get", "list", "create", "delete", "update"]
    resources:
      - group: ""
        resources: ["pods"]
```
![[Kubernetes_-_CKS_15.png]]

3. A policy to log all request from events on pods : 

```yaml
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
  - level:  Request
    verb: ["create", "delete", "update"]
    resources:
      - group: ""
        resources: ["pods"]
```
![[Kubernetes_-_CKS_14.png]]

4. A policy to log everything from events on pods : 

```yaml
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
  - level:  RequestResponse
    verb: ["create", "delete", "update"]
    resources:
      - group: ""
        resources: ["pods"]
```
![[Kubernetes_-_CKS_13.png]]