In order to manage our kubernetes secrets, we will be using [[SOPS]] cli tool.

# Setup
https://fluxcd.io/flux/guides/mozilla-sops/

## Install cli tools
We need to install sops & [[Age]] : 
```
brew install sops age
```

## Generate Age key

```
age-keygen -o age.agekey
```

It will create a private & a public key.

## Create a test secret


## Encrypt the secret

We export the public key to an env variable : 
```
export AGE_PUBLIC=publickey
```
We launch : 
``` bash
sops --age=$AGE_PUBLIC --encrypt --encrypted-regex '^(data|stringData)$' --in-place test-secret.yaml
```
It will encrypt everything inside data or stringData in our test-secret.yaml.

``` yaml
apiVersion: v1
data:
    password: ENC[AES256_GCM,data:FI2pre7NH10=,iv:myvkP/7wL9gVLt899xC/DJmlt55NPex1HMtTEk4Lv2A=,tag:Izw/ExaaVYwHtlb6AOPQ7A==,type:str]
    user: ENC[AES256_GCM,data:qYKfMFh5jeE=,iv:DVp8HU7Ai7QYfgIC85uWnjmcAStPKFLs+fZ1MQptckk=,tag:yL7RHGGfQkMIM1IUJB0CPg==,type:str]
kind: Secret
metadata:
    creationTimestamp: null
    name: test-secret
sops:
    kms: []
    gcp_kms: []
    azure_kv: []
    hc_vault: []
    age:
        - recipient: age12fqpm05rsmgfcdsys68kna8afmwcwyuwuv6h8enp242dg5fmu40q3hu3ln
          enc: |
            -----BEGIN AGE ENCRYPTED FILE-----
            YWdlLWVuY3J5cHRpb24ub3JnL3YxCi0+IFgyNTUxOSBOVzJXbElDNjBiZHVtWmto
            ZVBmaG05Q2VTYVZibzBzSlQ5ZXV1VzBMcVc4CnIzeGpBTU8xZVJOOENHNExIV1lG
            ZUN3Y2JUUTNLSWdySkx2U2VUQisvQm8KLS0tIDFVa1JhZ2I2RCtaZHpNNkNJYUxy
            b3MvTkRvRlozaWMrUWpKdUlIckllYXcK372z1Jexh26AkqKBSkei0C06XXR2X3jO
            +FpkENSpqPMKBhmCxAs9uyaO6wudlsFaaTEQwXwUVZZEAj4+EM6GLw==
            -----END AGE ENCRYPTED FILE-----
    lastmodified: "2025-02-02T14:35:24Z"
    mac: ENC[AES256_GCM,data:pmuLYp+OkLgibUClxUw+cpVCmO/DcvzavCSJ5IA3nn4RqpLAJOEwfg/AQcPulgTKm0h1ZNPRqomQyISvdQkx3k+8RYnrN4Nqmp6UKpKF3CZTfQCjlNH+JXFISc22H1hrbVWlOYdddbrMgs2og/6Vm4iqYHlOmguXARkKgYpiVvc=,iv:xxN7uLz1Y334U5tLqqVj5419Xxk9i8Zo+y03OjtONbM=,tag:kUiTUX2rG5YR1WdWFsinLg==,type:str]
    pgp: []
    encrypted_regex: ^(data|stringData)$
    version: 3.9.4
```

We can now safely commit the file in github because to decrypt it we need the secretkey.

## Allow flux to decrypt secrets

We create secret with the content of our age file : 
``` bash
 cat age.agekey | kubectl create secret generic sops-age 
 --namespace=flux-system --from-file=age.agekey=/dev/stdin
```

We will need to do this manually. It will then not be commited to git.

Now we need to tell flux where the key is located in `/clusters/staging/apps.yaml` :
``` yaml
decryption:
    provider: sops
    secretRef:
      name: sops-age
```

Now if we push an encyrpted secrets to GitHub. If we print it with kubectl it will be automatically decrypted by flux.

# Cons

By using this technique to encrypt secrets, we have to always launch the command to encrypt the secret before commiting it to github. We can forget it. [[Verify Secret SOPS]]

# Secret Env Container

We can add a secret or config map as env variables for containers using : 
``` yaml
envFrom:
  - configMapRef:
      name: linkding-configmap
  - secretRef:
      name: linkding-container-env
```

the command to create a secret from scratch in a file is : 

``` bash
kubectl create secret generic linkding-container-env \
--from-literal=LD_SUPERUSER_NAME=mykola \
--from-literal=LD_SUPERUSER_PASSWORD=avramuk \
--dry-run=client \
-o yaml > linkding-container-env-secret.yaml
```

We want to follow [[Twelve Factors App]]

```
Flux reconcile with source
```