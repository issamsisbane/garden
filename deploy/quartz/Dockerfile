# Build depuis la racine du repo garden :
#   docker build -f deploy/quartz/Dockerfile -t ghcr.io/issamsisbane/garden:latest .
# node:22-alpine ne marche pas : busybox `env` ne supporte pas `-S`,
# utilisé par le shebang du CLI Quartz. On reste sur une base Debian.
FROM docker.io/library/node:22-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Commit figé sur la branche v5 de Quartz (validé le 2026-09-11 via le repo
# notes). Sans ça, `git clone` récupère la branche par défaut du moment,
# qui peut casser le build ou changer de comportement sans qu'on ait
# touché à ce repo.
ARG QUARTZ_COMMIT=f1fba3fc55cbf60a60a5d09c95a49c042cdab63a

WORKDIR /quartz
RUN git init -q . \
    && git remote add origin https://github.com/jackyzha0/quartz.git \
    && git fetch --depth 1 origin "$QUARTZ_COMMIT" \
    && git checkout FETCH_HEAD \
    && npm ci

COPY deploy/quartz/quartz.config.yaml ./quartz.config.yaml

# Racine du repo garden (content/, knowledge/, resources/, assets/) devient
# le dossier content de Quartz.
COPY . /content

RUN npx quartz build --directory /content --output /output

FROM docker.io/library/nginx:1.27-alpine
COPY deploy/quartz/default.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /output /usr/share/nginx/html
EXPOSE 80
