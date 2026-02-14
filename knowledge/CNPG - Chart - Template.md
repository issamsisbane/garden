```
{{/* vim: set filetype=mustache: */}}

{{- define "common.databasecluster.tpl" -}}
{{- $top := first . }}
{{- $database := index . 1 }}
{{- $databases := $database.databases }}
{{- $initdb := $database.initdb }}
{{- $namespace := $top.Values.namespace | default dict }}
{{- $storage := $database.storage | default dict }}
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: {{ $database.clusterName }}
  namespace: {{ $namespace.name | default $top.Release.Namespace }}-cnpg
spec:
  imageName: {{ $database.image | default "ghcr.nexus.ulmj.intranet.justice.gouv.fr/cloudnative-pg/postgresql:17.4" }}
  instances: {{ $database.instances | default 2 }}

  inheritedMetadata:
    annotations:
      replicator.v1.mittwald.de/replication-allowed: "true"
      replicator.v1.mittwald.de/replication-allowed-namespaces: {{ $namespace.name | default $top.Release.Namespace }}

  {{- if and $database.parameters $database.parameters.maxConnections }}
  postgresql:
    parameters:
      max_connections: "{{ $database.parameters.maxConnections | default 100 }}"
  {{- end }}
  storage:
  {{- if $storage.storageClass }}
    storageClass: {{ $storage.storageClass }}
  {{- end}}
    size: {{ $storage.size | default "1Gi" }}

  {{- if $initdb }}
  bootstrap:
    initdb:
      database: {{ $initdb.database }} 
      owner: {{ $initdb.owner }} 
      {{- if $initdb.secretName}}
      secret: 
        name: {{ $initdb.secretName }} 
      {{- end }}
      {{- if $initdb.postInitTemplateSQL }}
      postInitTemplateSQL:
        {{- range $query := $initdb.postInitTemplateSQL}}
        - "{{ $query }}"
        {{- end }}
      {{- end }}


    {{- if $initdb.postInitTemplateSQL }}
  enableSuperuserAccess: false
    {{- end }}

  {{- end }}
  {{- if $databases }}
  managed:
    roles:
    {{- $processedOwners := dict }}
    {{- range $db := $databases }}
      {{- if $db.owner }}
        {{- $ownerName := $db.owner.name }}
        {{- if $ownerName }}
          {{- if not (hasKey $processedOwners $ownerName) }}
            {{- $_ := set $processedOwners $ownerName true }}
      - name: {{ $ownerName }}
        ensure: {{ $db.owner.ensure | default "present" }}
        login: {{ $db.owner.login | default true }}
        superuser: {{ $db.owner.superuser | default false }}
        passwordSecret:
          name: cnpg-{{ $db.name }}-db-secret
        connectionLimit: {{ $db.owner.connectionLimit | default 100 }}
          {{- end }}
        {{- end }}
      {{- end }}
    {{- end }}
  {{- end }}
     

{{- if (and $database.backup $database.backup.enabled) -}}
  backup:
    barmanObjectStore:
      destinationPath: {{ $database.backup.path }} 
      endpointURL: {{ $database.backup.endpointURL }} 
      s3Credentials:
        accessKeyId:
          name: database-backup
          key: ACCESS_KEY_ID
        secretAccessKey:
          name: database-backup
          key: ACCESS_SECRET_KEY
        region:
          name: database-backup
          key: ACCESS_REGION
{{- end }}

{{ if $database.databases -}}
{{- include "common.utils.merge" (list $top $database "common.database.tpl") }}
{{- include "common.utils.merge" (list $top $database "common.databasecluster.secret")}}
{{- end }}
{{- end }}

{{- define "common.databasecluster.secret" -}}
{{- $top := first . }}
{{- $cluster := index . 1 }}
{{- $namespace := $top.Values.namespace | default dict }}
{{- $ns := $namespace.name | default $top.Release.Namespace }}
{{- $port := "5432" }}
{{- range $db := $cluster.databases -}}
{{- $host := printf "%s-rw" $db.name }}
{{- $password := randAlphaNum 32 }}
---
apiVersion: v1
kind: Secret
type: kubernetes.io/basic-auth
metadata:
  name: cnpg-{{ $db.name }}-db-secret # TODO secret name
  namespace: {{ $ns }}-cnpg
  annotations:
    replicator.v1.mittwald.de/replication-allowed: "true"
    replicator.v1.mittwald.de/replication-allowed-namespaces: {{ $ns }}
data: 
  dbname: {{ $db.name | b64enc | quote }}
  host: {{ $host | b64enc | quote }}
  jdbc-uri: {{ printf "jdbc:postgresql://%s.%s-cnpg:%s/%s?password=%s&user=%s" $host $ns $port $db.name $password $db.owner.name | b64enc | quote  }}
  password: {{ $password | b64enc | quote }} 
  pgpass: {{ printf "%s:%s:%s:%s:%s" $host $port $db.name $db.owner.name $password | b64enc | quote }}
  port: {{ $port | b64enc | quote }}
  uri: {{ printf "postgresql://%s:%s@%s.%s-cnpg:%s/%s" $db.owner.name $password $host $ns $port $db.name | b64enc | quote }}
  user: {{ $db.owner.name | b64enc | quote }}
  username: {{ $db.owner.name | b64enc | quote }}
---
apiVersion: v1
kind: Secret
type: kubernetes.io/basic-auth
metadata:
  name: cnpg-{{ $db.name }}-db-secret # TODO secret name
  namespace: {{ $ns }}
  annotations:
    replicator.v1.mittwald.de/replicate-from: {{$ns}}-cnpg/cnpg-{{ $db.name }}-db-secret # TODO secret name
data: 
  username: test  # Mandatory for basic auth will be overriden
  password: test  # Mandatory for basic auth will be overriden
{{- end }}
{{- end }}

{{- define "common.databasecluster" -}}
{{- include "common.utils.merge" (append . "common.databasecluster.tpl") }}
{{- end }}
```

# Users

Il faut verifier que l'on ne crée qu'une seul fois le user meme si il est defini dans plusieurs database afin de ne pas avoir d'erreur coté CNPG. On va mettre les users traité dans un dict et verifier ce dict à chaque fois.

# Secrets

Pour les secrets on va créer un secret via les templates avec toutes les infos de connexion à la bdd selon le modele de cnpg qui sera dans le ns `projet-cnpg`

En plus de ça on générer un autre secret pour la replication dans le ns applicatif `projet` . Cela permet de faire une replication en pull via [[Kubernetes Replicator]]

On a bien verifié à avoir un mot de passe différent pour chaque user.

Il fallait aussi rajouter une vérification pour que tous les secrets crée ait le même mot de passe si jamais le user était le même.

# InitDB

J'ai laissé quand même l'init DB au cas ou mais la replication ne va pas marcher car je ne l'ai pas ajouter. A voir.