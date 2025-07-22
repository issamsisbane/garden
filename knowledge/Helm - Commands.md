Manages the repository and list helm packages : 

``` sh
helm repo [Command]
```

Install or Uninstall a helm chart : 

``` sh
helm install/uninstall 
	[release-name] [chart-location] 
	--version [version]
	--keep-history (uninstall)
	--values ./values.yaml
	-f ./values-dev.yaml
```

Gives details of a helm installation : revision #, deployment time, current status ...

``` sh
helm status [release-name]
```

List our helm releases in your envrionment :

``` sh
helm list [flags]
helm ls --all-namespace
helm ls --all-namespace -a (see even uninstalled release)
```

Change the version of the release : 

``` sh
helm upgrade [release-name] [chart-location] --version [version] --namespace [namespace]
```

Rollback to a previously installed release version : 

``` sh
# Show all versions
helm history [release-name] -n [namespace]

# Rollback
helm rollback [release-name] [revision-number] -n [namespace]
``` 
