To push a chart using the helm push dependency 

Add the registry :
```sh
helm registry login [registryName]
```

Push the packaged chart :
```sh
helm push chart.tgz oci://[registryName]
```