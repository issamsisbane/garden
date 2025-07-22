The steps to install something using helm are : 
### 1 - Add the repo
```
helm repo add
```
### 2 - Update helm repo
```
	helm repo update
```
### 3 - Install
```
helm install homarr homarr-labs/homarr --namespace homarr --create-namespace -f values.yaml
```
Do the same thing : 
```
helm install homarr homarr-labs/homarr --namespace homarr --create-namespace --values values.yaml
```
homarr-labs is the repo.
homarr is the thing we want to install.
We want to install in namespace and create one if necessary

Helm use [[Helm - Charts]]


If we just want to update we can : 
```
helm upgrade
```

Display installed repo : 
```
helm repo ls
```

Display installed charts : 
```
helm ls
```

Display values of the chart that can be overloaded in `values.yaml` : 
``` 
helm show values
```