Flux offers a clear structure as a Monorepo for repositories.
https://fluxcd.io/flux/guides/repository-structure/

# Start
Everything start with the kustomization.yaml file which then imports others file :
![[Pasted image 20250201222946.png]]
![[Pasted image 20250201223003.png]]



We can create [[Kubernetes - Custom Resource Definition]] enabled by the flux operator.

# Synchronization & Deployment

In the gotk-sync. Flux already has created a GitRepository Custom Resource for our repo which he watch every 1m0s.
Flux is also configured in the same file to look at the specified path staging directory.
![[Pasted image 20250201224007.png]]

We will create a new file called apps.yaml This will reference the GitRepository resource defined by flux in the gotk-sync file.

![[Pasted image 20250201224250.png]]

The first one will scrape our github repo for changes every minutes and will create artifact for the next job.
But the deployment will only happen every 10 minutes

In short, the repository is 'monitored' very frequently (every 1 minute) to always know if there is something new to deploy, but deployment is not always rushed (every 10 minutes). This approach helps strike a balance between responsiveness and stability (or the load on the cluster).

For each change in the git repos, it will send a notification to flux to update the cluster. 
We have an interval of 10 min, which is just a safety. Indeed, if something change we would not wait 10 min we make the changes directly. The 10 interval act as a periodical forced verification to be sure that the cluster is still in the same state as the git repo. The state may have been change id someone has touched the cluster directly using kubectl.

# Define the apps folder
The file apps.yaml. Will be pick by Flux because it's configure to check the path /clusters/staging where we put our file.

``` yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: apps
  namespace: flux-system
spec:
  interval: 10m0s
  retryInterval: 1m
  timeout: 5m
  sourceRef:
    kind: GitRepository
    name: flux-system
  path: ./apps/staging
  prune: true
~                                
```

We are telling flux to sync everything that lives to path /apps/staging every minutes.

![[Pasted image 20250201230310.png]]

We will have all our configuration in the base directory that will be overloaded in the different environments. 
For example staging environments will look at the files in base and modify the configurations depending on their needs.

We need to add our application manifest files : 
![[Pasted image 20250201233627.png]]

# Push & Verification

Once we have push our modifications to GitHub, we can verifiy that flux has done the job by checking : 
```
flux get kustomizations
```
![[Pasted image 20250201233721.png]]

It's bound to the commit id. So once we see our commit id here with the ready flag. It means that everything was done successfully

We can check the application by port-forwarding : 
``` bash
k -n linkding port-forward pod/linkding-7b8cc7cb8c-bklh4 8081:9090
```

http://localhost:8081
![[Pasted image 20250201234053.png]]

# Flux Workflow
1. Flux reads the clusters/staging directory
2. Finds and applies our apps.yaml file
3. Looks at the apps/staging directory
4. Finds our Linkding kustomization file
5. Applies the resources we defined in the base configuration

# Add Storage
We just have deploy our Linkding Application but there is not data persistence yet. 

We need to create a pvc and add it to the deployment. Then we push the code and flux will handle the rest.

We also need to add the new file to the kustomization file.

We need to launch this command to create a super user to access linkding : 
```
k exec -it -n kubectl podname -- python manage.py createsuperuser --username=mischa --email=mischa@example.com
```