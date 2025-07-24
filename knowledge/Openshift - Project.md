# Creation d'un projet openshift

``` yaml
apiVersion: project.openshift.io/v1
kind: ProjectRequest
metadata:
	name: hello-openshift
	annotations:
		openshift.io/display-name: "Hello OpenShift"
	description: "This is an example project to demonstrate OpenShift v3"
```