
Minikube allows to use kubernetes locally.

Creating a minikube cluster
```
minikube start --driver=docker
```

without this command we nekubected to activate something in the bios.

Add ingress to the cluster : 
```
minikube addons enable ingress
```

https://minikube.sigs.k8s.io/docs/start/?arch=%2Fwindows%2Fx86-64%2Fstable%2F.exe+download#Ingress

To Access a Nodeport using the docker driver : 

```
minikube service [service-name] --url
```

If we have an app using env variables we set in the values.yaml of the helm chart, if we want to update it using helm upgrade we have to restart the pod of the app to apply the changes