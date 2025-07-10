[[Flux]] allow to use [[Helm]].

There are CRD defining :
- HelmRepository which replace the command `helm repo add`
- HelmRelease which replace the command `helm install`

```
flux get helm releases
```

In flux folder structure, we have the `infrastructure` folder which will contains everything infrastructure related such as : 
- ingress controller
- monitoring
- vault

But to be a bit cleaner we can use a folder for monitoring only.
In that folder, we will have two others folders : 
- `configs` : The configuration of the tools we deployed is in this folder (Custom Dashboard for grafana, prometheus rules...)
- `controllers` : The actuel defintion of the controllers which enable the CRDs

For the helm release we can specify version: "66.x" which will pull the last version each time the interval. We maybe don't want that behavior.

For the kube-prometheus-stack, there are some CRDs included with the chart that need to manage manually. We need to apply them before creation or update. We can automate this by adding : 
```
spec:
	install:
		crds: Create
	upgrade:
		crds: CreateReplace
```

The `driftDetection` will detect every change which is different than the specification of the chart and revert to the defined state. 

This behavior is what we expect from GitOps but we may need to ignore some things.

The values is the equivalent of the values.yaml file.