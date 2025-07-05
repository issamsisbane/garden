An Image Stream allow to facilitate the update of images inside [[Openshift]] Containers. 

Indeed, inside our container, we will reference an image stream. The image stream contains the following : 
``` yaml
apiVersion: image.openshift.io/v1
kind: ImageStream
metadata:
  name: mon-app
  namespace: mon-projet
spec:
  tags:
    - name: latest
      from:
        kind: DockerImage
        name: quay.io/mon-compte/mon-app:latest
      importPolicy:
        scheduled: true
```

We reference an image from a container registry. The image stream will notify the container when a new Image is available within the registry which will trigger or not a new pod depending of what we want. 

In the deployment, we will have : 

``` yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mon-app
  namespace: mon-projet
spec:
  replicas: 2
  selector:
    matchLabels:
      app: mon-app
  template:
    metadata:
      labels:
        app: mon-app
    spec:
      containers:
        - name: mon-app
          image: mon-app:latest  # <--- Référence à l'ImageStreamTag
          imagePullPolicy: Always
          ports:
            - containerPort: 8080
```

It's quite similar to what [[Renovate]] does.
