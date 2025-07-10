For now our linkding pod is running as root. This is not an expected behavior for production workload because if someone manage to access the container he would be able to do everything.

So we want to restrict this by running as a non root user and disable privileges escalation. 

# Set the user

## Find the user

We need to find the user needed for the particular image. 

For this a good int is to take a look at `/etc/passwd` : 
![[Pasted image 20250202111406.png]]

We can see different users that are not the linux default ones. So it must be one of those. 

Moreover, when we look at the dockerfile of the application, we can see : 
![[Pasted image 20250202111507.png]]

Also if we do :

``` bash
kubectl logs linkding | grep id
```
We can see  :

![[Pasted image 20250202112527.png]]

So the user to user must be www-data with the id of 33.

## Add a Security Context

In our deployment we have to add a [[Security Context]] : 

```yaml
spec:
      securityContext:
        fsGroup: 33 # group ID - Volume Permissions
        runAsUser: 33 # user ID
        runAsGroup: 33 # group ID
```

The fsGroup mean that any files created in that volume will be Group ID.

## Privilege Escalation

We also need to prevent privilege escalation. It's the default setting can be override : 
```
containers:
	securityContext:
            allowPrivilegeEscalation: false
```
## Verification
![[Pasted image 20250202113118.png]]