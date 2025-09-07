This capstone project aims to deploy an application following everything that I learned in mischa's courses. 

The application to deploy is [audiobookshelf](https://www.audiobookshelf.org/docs#docker-compose-install)

# STAGE 1 - Deployment

## Create the deployment

To generate a default deployment file we use : 

``` bash
k create deployment audiobookshelf --image=test:latest --dry-run=client -o yaml > deployment.yaml
```

I just created a simple deployment with the image name.

Then I created a namespace and all the kustomization files needed in order to have something like this : 

![[Pasted image 20250215190748.png]]

Then I tested using port-forwarding : 

```
k port-forward -n audiobookshelf pod/audiobookshelf-9d6495885-c498z 8080:80
```

This means we map the port 8080 of our computer to port 80 of the pod container. I tried to use port 80 of my computer but apparently I already have some nginx running ??? We can use any ports (unused) we want.

## Change the port

We want to change the port use by the container and listen by the audiobookshelf app. 

Reading the docs we can see there is an environnement variables called PORT allowing to change it :

![[Pasted image 20250215193512.png]]
https://github.com/audiobookshelf/audiobookshelf-web/blob/master/content/docs/configuration/1.configuration.md

### Direct 
We can directly set the variable : 

```
env: 
	name: "PORT"
	value: "3005"
```

it's important to use "" for the numbers.

### ConfigMap

Or we can use a config map : 

``` yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: configmap-env
data:
  PORT: "3005"

```

```yaml
envFrom:
        - configMapRef:
            name: configmap-env
```

We can test again via a port-forward to ensure everything works fine.

# STAGE 2 - Persistent Volumes

The goal is to add persistent volumes in order to persist configurations and the audiobook we add in the app.

## Needed volumes

In the documentation we can find some volumes to add (docker compose): 

``` yaml
services:
  audiobookshelf:
    image: ghcr.io/advplyr/audiobookshelf:latest
    ports:
      - 13378:80
    volumes:
      - </path/to/audiobooks>:/audiobooks
      - </path/to/podcasts>:/podcasts
      - </path/to/config>:/config
      - </path/to/metadata>:/metadata
    environment:
      - TZ=America/Toronto

```

## Create a PVC

I just need to create a pvc : 

``` yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: audiobookshelf-pvc
spec:
  accessModes:
    - ReadWriteOnce
  volumeMode: Filesystem
  resources:
    requests:
      storage: 1Gi
```

## Configure the deployment

Then I can use this pvc and map every folder to persist to the pvc :
``` yaml
volumeMounts:
          - mountPath: "/audiobooks"
            name: audiobookshelf-storage
          - mountPath: "/podcasts"
            name: audiobookshelf-storage
          - mountPath: "/config"
            name: audiobookshelf-storage
          - mountPath: "/metadata"
            name: audiobookshelf-storage
         
      volumes:
        - name: audiobookshelf-storage
          persistentVolumeClaim:
            claimName: audiobookshelf-pvc
```

Now when I create a library and upload a file, if I delete the pod the eveything is still there. 

It's possible to download some audiofiles here : https://librivox.org/

![[Pasted image 20250215201924.png]]

## Reflexion - Many PVC ?

Mischa decided to create a pvc for each path to mounth. This could be a good solution because it provides : 
- better isolation for data (own backup and restore process)
- effcient storage (ssd for config and hdd for audiobooks)
- quotas handling and different size or CSI

# STAGE 3 - Internet and Non-root

## Non-root

We want to launch our container as non-root to be more secure.

I investigate in the container and saw that the user is `node` with `/etc/passwd`. 

So i change the user in the container by setting : 
``` yaml
spec:
      securityContext:
        fsGroup: 1000
        runAsUser: 1000
        runAsGroup: 1000
```

But I ran into an error : 

![[Pasted image 20250215204020.png]]

These are permissions errors due to the fact that our volume and folders were initialized by root. Indeed, we just created a new pod but as we have the volumes the folders has the same permissions as before. And so our `node` user doesn't have the rights to access it which generate an error and our pod could'nt start.

The solution is to delete and restart everything related to audiobookshelf in the cluster (volumes and pods). We could set manually the permissions but it's not very clean.  

Finally, by relaunching our application. Everyhting works fine.

## Expose to Internet

### Create a cloudflare tunnel

``` bash
cloudflared tunnel create abs
```

It will create a .json file in `.cloudflared`.

### Create a secret

``` bash
k create secret generic tunnel-credentials.yaml -o yaml --from-file=credentials.json=/home/issam/.cloudflared/1f1cbd27-3a5e-4d0e-af85-425d2038787d.json --dry-run=client > tunnel-credentials.yaml
```

We need to sops it, with the same key as before : 

``` bash
export AGE_PUBLIC=''
sops --age=$AGE_PUBLIC --encrypt --encrypted-regex '^(data|stringData)$' --in-place tunnel-credentials.yaml
```

### Create the cloudflare resource

``` yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cloudflared
spec:
  selector:
    matchLabels:
      app: cloudflared
  replicas: 2 # You could also consider elastic scaling for this deployment
  template:
    metadata:
      labels:
        app: cloudflared
    spec:
      containers:
      - name: cloudflared
        image: cloudflare/cloudflared:latest
        args:
        - tunnel

        # Points cloudflared to the config file, which configures what
        # cloudflared will actually do. This file is created by a ConfigMap
        # below.
        - --config
        - /etc/cloudflared/config/config.yaml
        - run
        livenessProbe:
          httpGet:
            # Cloudflared has a /ready endpoint which returns 200 if and only if
            # it has an active connection to the edge.
            path: /ready
            port: 2000
          failureThreshold: 1
          initialDelaySeconds: 10
          periodSeconds: 10
        volumeMounts:
        - name: config
          mountPath: /etc/cloudflared/config
          readOnly: true
        # Each tunnel has an associated "credentials file" which authorizes machines
        # to run the tunnel. cloudflared will read this file from its local filesystem,
        # and it'll be stored in a k8s secret.
        - name: creds
          mountPath: /etc/cloudflared/creds
          readOnly: true
      volumes:
      - name: creds
        secret:
          secretName: tunnel-credentials

      # Create a config.yaml file from the ConfigMap below.
      - name: config
        configMap:
          name: cloudflared
          items:
          - key: config.yaml
            path: config.yaml
---
# This ConfigMap is just a way to define the cloudflared config.yaml file in k8s.
# It's useful to define it in k8s, rather than as a stand-alone .yaml file, because
# this lets you use various k8s templating solutions (e.g. Helm charts) to
# parameterize your config, instead of just using string literals.
apiVersion: v1
kind: ConfigMap
metadata:
  name: cloudflared
data:
  config.yaml: |
    # Name of the tunnel you want to run
    
    tunnel: abs

    credentials-file: /etc/cloudflared/creds/credentials.json

    # Serves the metrics server under /metrics and the readiness server under /ready
    metrics: 0.0.0.0:2000
    no-autoupdate: true

    ingress:
    - hostname: abs.issamhomelab.org
      service: http://audiobookshelf:3005

    # This rule sends traffic to the built-in hello-world HTTP server. This can help debug connectivity
    # issues. If hello.example.com resolves and tunnel.example.com does not, then the problem is
    # in the connection from cloudflared to your local service, not from the internet to cloudflared.
    - hostname: hello.example.com
      service: hello_world
    # This rule matches any traffic which didn't match a previous rule, and responds with HTTP 404.
    - service: http_status:404
```

## Configure the CNAME

We need to create a cname for our tunnel : 
![[Pasted image 20250215213112.png]]

We just add in the target the id of our tunnel and we add `.cfargotunnel.com` at the end.

It wouldn't work because I forgot to add it at the end.