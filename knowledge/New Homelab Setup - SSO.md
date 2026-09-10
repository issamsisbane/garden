---
creation date: 2026-04-12-15:51:21
modification date: 2026-04-12-15:51:21
imageNameKey: New_Homelab_Setup_-_SSO
---
## Authentik

## Authelia

### LLDAP

https://github.com/Evantage-WS/lldap-kubernetes/tree/main

I decided not to use the chart because it's just a deployment, a service and a pvc.

I had an error of rights documented on the repo 

```bash
│ [entrypoint] Copying the default config to /data/lldap_config.toml
│ [entrypoint] Edit this file to configure LLDAP.
│ > Setup permissions..
│ chown: /data: Operation not permitted
│ chown: /data/lldap_config.toml: Operation not permitted
│ stream closed EOF for lldap-second/lldap-chart-deployment-5c877d4667-74vd2 (lldap)
```

The solution was to use a rootless image and add security context to use 1001 and fsgroup. 

### Authelia installation