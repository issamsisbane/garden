---
foam_template:
  filepath: "0 - INBOX/Openshift - Route - TLS.md"
  description: "New note"
created: "2025-12-09"
---

# Openshift - Route - TLS

On peut rajouter un certificat spécifique pour la termiaison de la route (en edge) :

```yaml
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: frontend
spec:
  host: www.example.com
  to:
    kind: Service
    name: frontend
  tls:
    termination: edge
    key: |-
      -----BEGIN PRIVATE KEY-----
      [...]
      -----END PRIVATE KEY-----
    certificate: |-
      -----BEGIN CERTIFICATE-----
      [...]
      -----END CERTIFICATE-----
    caCertificate: |-
      -----BEGIN CERTIFICATE-----
      [...]
      -----END CERTIFICATE-----
```
