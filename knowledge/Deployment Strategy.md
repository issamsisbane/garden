Strategy defines how a Deployment will replace pods. 

# Rolling Update

Recreate pods, pod by pod. Users can still use the application.
```yaml
spec:
	strategy:
		type: RollingUpdate
		rollingUpdate:
			maxUnavailable: 1
			maxSurge: 1
			
```

It will only create 2 pods at a time if we change the image of the deployment for example.

If there is an error, it will not go further in the update. It will just stop and we have a **CrashLoopBackOff**

# Recreate

Recreate all the pod at the same time.

https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#strategy