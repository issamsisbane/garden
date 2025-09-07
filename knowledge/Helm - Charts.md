Helm charts are a collection of kubernetes manifests template with variables in it that have been bundled together. 

Helm Charts allow us to use templating to customize application to our needs.

[[Helm - Templating]]
# Repos

It exists public and private repositories to get artifact for known applications we want to use (Prometheus, Graphana...).

The most used and known public repo is [Artifact Hub](https://artifacthub.io/) to find OpenSource Helm Charts. It's built in the helm cli using the `helm search hub` command.

We can used private a public repo using the `helm repo add` command.
# Values and Charts

The variables we have within the template can be overridden with the values.yaml file.

If we dont overload a variables form the values.yaml file it will just use the default values from the default values.yaml. 

Helm Charts works in a way that it take the default values as a base and override only the values specified in other values files we specify.

To create the values.yaml file, we can do : 
```
helm show values repository/name | vim
```

We can specify a values name :
```
helm template -f values-dev.yaml .
```
# Key Components

## Helm Charts

The yml files we would write like a classic kubernetes application.
We wrote the files in the ==template folder== where we can use a particular syntax to use Templating.

#### Service

``` yaml
apiVersion: v1
kind: Service
metadata: 
	name: {{ .Values.appName }}
	namespace: {{ .Values.namespace }}
	labels:
		app: {{ .Values.appName }}
spec:
	ports:
	- port: 80
	  protocol: TCP
	  name: myName
	selector:
		app: {{ .Values.appName }}
	type: LoadBalancer
```

#### Deployment

``` yaml
apiVersion: apps/v1
kind: Deployment
metadata: 
	name: my-app-01
	namespace: {{ .Values.namespace }}
spec:
	replicas: {{ .Values.replicas }}
	selector:
		matchLabels:
			app: my-app-01
	template:
		metadata:
			labels:
			
				app: my-app-01
		spec:
			containers:
				- name: my-app-01
				  image: "{{ .Values.image.name }}:{{ .Values.image.tag }}"
```


## Config Values

We use config values, to set variables we use in the templates. To Configure Deployment of our Helm Charts. We put the values in a ==values.yaml== file. We can also defined different files for different environnement we would just have to specify which one we want to use when deploying the chart : 

* ==values-dev.yaml==
* ==values-test.yaml==
* ==values-prod.yaml==

``` yaml
appName: myhelmapp
namespace: default

configmap:
	name: helmappconfigmapv1.1
	data:
		CUSTOM_HEADER: "This app was deployed with Helm"

image:
	name: my-image-name
	tag: latest
```

## Releases

This is the running instance of a helm deployment combined with a specific configuration (values file).
Managing releases allow to create, update or rollback our helm deployment.

# File Structure

![[helm_chart_file_structure.png]]

#### chart.yaml

Contains information about our chart (metadata).

``` yaml
apiVersion: v2
name: webapp
description: A Helm chart for Kubernetes

type: application

version: 0.1.0
appVersion; "1.16.0"
```

#### templates/files

All the files describe our application for the helm chart

#### templates/NOTES.txt

Contains not about the deployment which will be printed once the chart is installed or if the helm status command is launched.

#### values.yaml
Contains the values of the variables used in the template files.