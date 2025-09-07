## 1 - Génération de la clé privée
```
openssl genpkey -algorithm RSA -out private_key.pem
```

## 2 - Génération de la demande de signature du certificat
```
openssl req -new -key private_key.pem -out certificate.csr
```

## 3 - Génération du certificat pour 1 an
```
openssl x509 -req -days 365 -in certificate.csr -signkey private_key.pem -out certificate.pem
```

## 4 - Vérification
```
openssl x509 -in certificate.pem -text -noout
```