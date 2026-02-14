La synchronisation est possible et fonctionnel grâce a [[WebDav]].

J'ai testé en lançant ces conteneurs et ça fonctionne bien. On peut aussi activer la compression et encrypter les données. A voir si possible de recuperer la clé.

# Architecture

#ToThink

![[draw.io_280.png]]


> [!QUESTION]
> Where to put the webdav server ?
> How to backup ? 
> How to secure the backup ? 
> Where to put the backup ? S3 only ? Homelab and S3 ?

# Comment faire ? 

Le Readme du projet donne un docker compose avec les infos nécessaires : 

```yaml 
# webdav.yaml
address: 0.0.0.0
port: 2345

prefix: /
permissions: CRUD

# CORS configuration to allow all origins
cors:
  enabled: true
  credentials: true
  allowed_headers:
    - '*'
  allowed_hosts:
    - '*'
  allowed_methods:
    - GET
    - HEAD
    - POST
    - PUT
    - DELETE
    - OPTIONS
    - PROPFIND
    - PROPPATCH
    - MKCOL
    - COPY
    - MOVE
    - LOCK
    - UNLOCK
  exposed_headers:
    - '*'

users:
  - username: admin
    password: admin
    directory: /data
```

```yaml
# docker-compose.yaml
services:
  # Super Productivity app
  app:
    image: johannesjo/super-productivity:latest
    ports:
      - '8080:80'
    environment:
      # Pre-configured defaults for easier setup
      WEBDAV_BASE_URL: ${WEBDAV_BASE_URL:-http://localhost:2345/}
      WEBDAV_USERNAME: ${WEBDAV_USERNAME:-admin}
      WEBDAV_SYNC_FOLDER_PATH: ${WEBDAV_SYNC_FOLDER_PATH:-/}
      SYNC_INTERVAL: ${SYNC_INTERVAL:-15}
      IS_COMPRESSION_ENABLED: ${IS_COMPRESSION_ENABLED:-true}
      IS_ENCRYPTION_ENABLED: ${IS_ENCRYPTION_ENABLED:-false}

  # WebDAV sync server
  webdav:
    image: hacdias/webdav:latest
    ports:
      - '2345:2345'
    volumes:
      - ./webdav.yaml:/config.yml:ro
      - ${WEBDAV_DATA_DIR:-./data}:/data
    healthcheck:
      test: ['CMD', 'wget', '--quiet', '--tries=1', '--spider', 'http://localhost:2345/']
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 10s
```