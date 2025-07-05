In Kubernetes, we don't really define pods directly. 

We would prefer to use deployment in order to define a certain state we want to achieve. 

And so if we delete a pod attached to the deployment the pod would be recreated. If we had only deploy the pod only then it would be gone .

It exists differents [[Deployment Strategy]]