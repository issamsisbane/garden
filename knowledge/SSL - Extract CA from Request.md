---
foam_template:
  filepath: "0 - INBOX/SSl - Extract CA from Request.md"
  description: "New note"
created: "2025-12-06"
---

# SSl - Extract CA from Request

It's possible to extract the CA from a request to a website to add it to our truststore manually yo make sure communication are secure.

We can use this command to extract only the CA certificate : 

```bash
openssl s_client -connect exemple.com:443 -showcerts </dev/null 2>/dev/null \
  | awk '/-----BEGIN CERTIFICATE-----/,/-----END CERTIFICATE-----/'
```

Then we need to specify this CA when making a request using the client we want e.g aws-cli to request an S3 expose with a private PKI.