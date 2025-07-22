Générer un certificat pour local host : 

``` sh
openssl req -x509 -newkey rsa:4096 -keyout keycloak.key -out keycloak.crt -days 365 -nodes -subj "/CN=localhost"
```

# TrustStore

# Key

# Cert