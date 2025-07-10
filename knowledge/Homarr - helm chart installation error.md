I wanted to install homarr in my rancher desktop cluster but I had an error saying that the key was too small. 

```
# generate keys
openssl rand -hex 32 | base64
```

I just forgot how secret worked in [[Kubernetes]]. 
Indeed, if you put something in data it must be base64 encoded and be aware of space.

If you want to put directly the value you have to use stringData.

``` yaml
apiVersion: v1
stringData:
  db-encryption-key: 73ce8d7a72f37643d130f45ecd6a0e993d15ac3c9ccbc004bb9735098d4f9685
kind: Secret
metadata:
  name: db-secret
  namespace: homarr
type: Opaque
```