```sh
skopeo --insecure-policy copy docker://source docker://destination
```

``` sh
skopeo --insecure-policy copy --dest-tls-verify=false docker://source docker://localhost:5000/argocd/dex:v2.41.1 --dest-creds username:$
(oc whoami -t)
```