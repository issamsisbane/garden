# Create Argo Application

We need to specify the listening directory and the git repos to watch :

``` yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata: 
  name: guestbook
  namespace: argocd
spec: 
  destination: 
    namespace: guestbook
    server: "https://kubernetes.default.svc"
  project: default
  source: 
    path: guestbook
    repoURL: "https://github.com/mabusaa/argocd-example-apps.git"
    targetRevision: main
  syncPolicy:
    syncOptions:
      - CreateNamespace=true
```

# Create the manifest for the application

We need to create the manifest we need (service & deployment) in the specified path to allow argo to deploy them.

``` yaml
apiVersion: v1
kind: Service
metadata:
  name: guestbook-ui
spec:
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: guestbook-ui
```

``` yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: guestbook-ui
spec:
  replicas: 1
  revisionHistoryLimit: 3
  selector:
    matchLabels:
      app: guestbook-ui
  template:
    metadata:
      labels:
        app: guestbook-ui
    spec:
      containers:
      - image: gcr.io/heptio-images/ks-guestbook-demo:0.2
        name: guestbook-ui
        ports:
        - containerPort: 80
```

# Error

I had an error first because I has master branch in the application yaml instead of main.

# Results

## Before Sync

![[Pasted image 20250202175724.png]]

We can see that our manifest was detected. We need to sync it. By default, the auto-sync is not active.

## After Sync

![[Pasted image 20250202175733.png]]
We have our application and service deployed.