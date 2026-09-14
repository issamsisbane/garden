---
creation date: 2026-08-26-22:32:42
modification date: 2026-08-26-22:32:42
imageNameKey: Users_(Kubernetes)
---
# Users

Kubernetes manage users using : 
- File
- LDAP
- Certificate

So we can create users directly from kubernetes.

All user access is managed by the api server.

User can authenticate using :
- **Static Token File** (Not Recommended):
	- We have users described with token and group in a file read by the api-server. 
	- We must specify the token with each request to access the api.
	- We must configure the api-server static pod to use our file via volumeMount and --basic-auth-file
- **Certificates**
- **Identity Services External**

