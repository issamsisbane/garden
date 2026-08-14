---
created: "2026-08-12"
---

# Kubernetes - Debug Flux Sortant

Recuperer tous les flux sortants en faisant pointer vers ce proxy :

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: netdebug
  namespace: nexus
  labels: { app: netdebug }
spec:
  containers:
    - name: netdebug
      image: docker.io/nicolaka/netshoot
      command: ["sh", "-c", "while true; do nc -lk -p 9000; done"]
---
apiVersion: v1
kind: Service
metadata:
  name: netdebug
  namespace: nexus
spec:
  selector: { app: netdebug }
  ports:
    - port: 9000
      targetPort: 9000
```

Pour des flux dédié HTTP : 

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: http-echo-debug
  namespace: nexus
  labels: { app: http-echo-debug }
spec:
  containers:
    - name: echo
      image: docker.io/mendhak/http-https-echo:31
      ports: [{ containerPort: 8080 }]
```

Dans une conf NGINX on peut utiliser le mirror pour dupliquer le flux reçu et l'envoyer vers une autre destination : 

```json
location / {
                mirror /mirror-capture;
                client_body_buffer_size 20m;   # ajuste selon la taille max de tes layers Docker
                mirror_request_body on;

                proxy_pass <url-to-forward>
                proxy_set_header Host <host-to-forward>
                proxy_set_header Transfer-Encoding "";
                proxy_set_header Content-Length $safe_content_length;

                proxy_http_version 1.1;

                # TLS vers le vrai stockage S3-compatible
                proxy_ssl_trusted_certificate /etc/nginx/ca/ca.crt;
                proxy_ssl_verify on;
                proxy_ssl_verify_depth 2;
                proxy_ssl_server_name on;
            }

            location = /mirror-capture {
                internal;
                proxy_pass <other-url-to-forward>
            }
```