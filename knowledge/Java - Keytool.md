---
foam_template:
  filepath: "0 - INBOX/Java - Keytool.md"
  description: "New note"
created: "2026-01-07"
---

# Java - Keytool

## Keystore

### Lister le contenu d'un Keystore


```bash
keytool -list -keystore truststore.p12 -storepass changeme -v
```

### Ajouter un CA au keystore


``` bash
keytool -importcert -file ca-certificate.crt \
  -alias nouveau-ca -keystore truststore.p12 \
  -storetype PKCS12 -storepass changeit -noprompt
```

### Extract Certs & Keys

```bash
openssl pkcs12 -in truststore.p12 -out combined.pem -nodes
```

### Export

Ensuite on peut intégrer le keystore dans un secret par exemple.

Il faut utiliser la commande suivante pour recuperer le configmap en base64 et l'integrer dans un secret.


```bash
base64 -w 0 truststore.p12
```





Monter un pod pour utiliser keytool sur kubernetes avec un certificat et un trustore de monté : 


```
# pod-keytool.yaml
apiVersion: v1
kind: Pod
metadata:
  name: keytool-pod
  namespace: test-keytool
  labels:
    app: keytool
spec:
  imagePullSecrets:
    - name: imagepullsecret
  containers:
  - name: keytool
    image: eclipse-temurin:17-jdk
    command: ["/bin/sh"]
    args: ["-c", "sleep infinity"]
    volumeMounts:
    - name: certs-volume
      mountPath: /certs
  volumes:
  - name: certs-volume
    configMap:
      name: certificates-configmap
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: certificates-configmap
  namespace: test-keytool
binaryData:
  truststore.p12: |
    base64
data:
  # Placez vos certificats ici en base64 ou texte
  ca-certificate.crt: |
    -----BEGIN CERTIFICATE-----
    # Votre certificat CA ici
    -----END CERTIFICATE-----
```
