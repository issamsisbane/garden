---
foam_template:
  filepath: "0 - INBOX/CNPG - Plugin - PGBACKREST.md"
  description: "New note"
created: "2026-07-03"
---

# État des lieux — Problème plugin pgBackRest CNPG-I

- [État des lieux — Problème plugin pgBackRest CNPG-I](#état-des-lieux--problème-plugin-pgbackrest-cnpg-i)
  - [Contexte](#contexte)
  - [Erreur principale](#erreur-principale)
  - [Symptômes confirmés](#symptômes-confirmés)
    - [Variables d'environnement manquantes](#variables-denvironnement-manquantes)
    - [Erreur secondaire (v0.0.2 et v0.0.3)](#erreur-secondaire-v002-et-v003)
    - [Erreur pgBackRest sans config S3](#erreur-pgbackrest-sans-config-s3)
  - [Architecture du plugin (pour rappel)](#architecture-du-plugin-pour-rappel)
  - [Ce qui a été vérifié et éliminé](#ce-qui-a-été-vérifié-et-éliminé)
    - [Configuration de la Stanza](#configuration-de-la-stanza)
    - [Correspondance stanzaRef / metadata.name](#correspondance-stanzaref--metadataname)
    - [Namespace](#namespace)
    - [RBAC du ServiceAccount](#rbac-du-serviceaccount)
    - [Présence de l'objet Stanza](#présence-de-lobjet-stanza)
    - [Image du sidecar](#image-du-sidecar)
    - [Modification du Secret](#modification-du-secret)
    - [Versions testées](#versions-testées)
  - [Issues Github](#issues-github)
  - [Pistes restantes](#pistes-restantes)


## Contexte

Les tests ont été réalisés sur un cluster openshift dans le namespace test-grafana.
Il n'y a pas netpol dans ce namespace.

Pour mes tests, j'ai créer les ressources suivantes :
- Cluster CNPG
- Stanza (CRD pgbackrest plugin)
- PluginController (CRD pgbackrest plugin)
- Secret : nommé `minio` pour matcher exactement ce qu'il y a dans la doc du plugin mais le vrai secret avec la conf pour utiliser le compte S3 de emap est `aws-credentials-secret`.

Une fois toutes les ressources crées, les pods du cluster CNPG montent bien et passent en ready. On se retrouve juste avec des erreurs dans les logs.

| Élément | Valeur |
|---|---|
| Opérateur CNPG | v1.29.1 (testé aussi en v1.29.0) |  
| Plugin pgBackRest (Dalibo) | v0.0.2 (testé aussi en v0.0.3) |

## Erreur principale

L'erreur suivante apparait dans le container `postgres` du cluster CNPG lancé et dans le pog `pgbackrest-plugin`.

```log
stanza creation failed: can't determine if stanza exists,
error can't parse pgbackrest JSON: invalid character 'P' looking for beginning of value
```

Cette erreur est la conséquence d'une cause racine : **les variables d'environnement S3 ne sont pas injectées dans le sidecar `plugin-pgbackrest`**. pgBackRest tourne donc avec sa configuration locale par défaut (`/var/lib/pgbackrest`), produit des logs texte préfixés `P00 WARN:` sur stdout, ce qui corrompt le JSON attendu par le plugin.

## Symptômes confirmés

### Variables d'environnement manquantes

La commande `kubectl exec -it <pod> -c plugin-pgbackrest -- env | grep PGBACKREST` ne retourne **aucune variable PGBACKREST_** autre que celle du pod, alors que les variables attendues d'après la doc sont :

```
PGBACKREST_STANZA=main
PGBACKREST_LOCK_PATH=/controller/tmp/pgbackrest-cnpg-plugin.lock
PGBACKREST_LOG_LEVEL_FILE=off
PGBACKREST_REPO1_PATH=/repo-01
PGBACKREST_REPO1_S3_BUCKET=...
PGBACKREST_REPO1_S3_ENDPOINT=...
PGBACKREST_REPO1_S3_KEY=...
PGBACKREST_REPO1_S3_KEY_SECRET=...
PGBACKREST_REPO1_S3_REGION=...
PGBACKREST_REPO1_S3_URI_STYLE=...
PGBACKREST_REPO1_S3_VERIFY_TLS=...
```

Même les variables ajoutées manuellement via `customEnvVar` dans la CRD `Stanza` **ne sont pas injectées**.

### Erreur secondaire (v0.0.2 et v0.0.3)

En plus de l'erreur ci-dessus, on peut trouver l'erreur suivante dans les logs au démarrage du cluster. Ce qui laisse penser à un problème de CRD.

```log
stanza maintenance failed:
v1.GetOptions is not suitable for converting to "postgresql.cnpg.io/v1" in scheme
```

Erreur Go dans `StanzaMaintenanceRunnable.Start / maintenance.go:38` — le sidecar ne peut pas lire les types CNPG depuis l'API Kubernetes car `postgresql.cnpg.io/v1` n'est pas enregistré dans le scheme du sidecar. Cette erreur est une conséquence de l'absence de config, pas la cause initiale.

### Erreur pgBackRest sans config S3

```
Permission denied: unable to list file info for path '/var/lib/pgbackrest/backup'
```

pgBackRest utilise son repo local par défaut car aucune config S3 n'est présente.

## Architecture du plugin (pour rappel)

Le plugin pgbackrest Dalibo fonctionne de la manière suivante :

1. L'opérateur CNPG appelle le `pgbackrest-controller` via **gRPC** (port 9090, protocole CNPG-I) lors de la création de chaque Pod
2. Le `pgbackrest-controller` lit la `Stanza` et le `Secret` S3, construit les env vars, et renvoie la configuration du sidecar à CNPG
3. CNPG injecte le sidecar avec les env vars dans le Pod PostgreSQL

Le sidecar est bien présent dans le pod → le controller répond à l'appel gRPC. Mais il renvoie un sidecar **sans env vars**, ce qui indique qu'il n'arrive pas à lire la Stanza ou à en extraire la configuration.

## Ce qui a été vérifié et éliminé

### Configuration de la Stanza

Le YAML de la Stanza est correct :
- `bucket`, `endpoint`, `region`, `repoPath` renseignés
- `secretRef` pointant vers `aws-credentials-secret` avec les bonnes clés
- `uriStyle: host`, `verifyTLS: false`

### Correspondance stanzaRef / metadata.name

Le `stanzaRef` dans `spec.plugins` du Cluster correspond exactement au `metadata.name` de l'objet Stanza — vérifié par `kubectl get stanza`.

### Namespace

La Stanza et le Cluster sont dans le même namespace.

### RBAC du ServiceAccount

```bash
kubectl auth can-i get secret aws-credentials-secret \
  --namespace test-grafana \
  --as=system:serviceaccount:cnpg-system:pgbackrest-controller
# Résultat : yes
```

Le ServiceAccount `pgbackrest-controller` a bien accès aux Secrets dans le namespace applicatif.

### Présence de l'objet Stanza

`kubectl get stanza -n <namespace>` retourne bien l'objet.

### Image du sidecar

L'image injectée dans le pod est bien `dalibo/cnpg-pgbackrest-sidecar:0.0.2` — confirmé via `kubectl get pod -o jsonpath='{.spec.containers[?(@.name=="plugin-pgbackrest")].image}'`.

### Modification du Secret

J'ai remarqué que si je met un nom de secret qui n'existe pas il y a une erreur et pareil avec une clé de secret qui n'existe pas.

J'ai donc essayé de modifier le secret référencer dans Stanza pour les identifiants du S3 en en ne gardant que des mots sans tiret dans le nom du secret et dans les valeurs pour l'id et le secret.

Aucune amélioration.

### Versions testées

Testé en v0.0.2 et v0.0.3 du plugin pgbackrest avec CNPG 1.29 et 1.29.1 — même comportement dans tous les cas.

## Issues Github

La version v0.0.3 du plugin pgbackrest est sorti il y a une semaine. Dans cette version il y a des tests automatisé avec la version 1.29.1 de CNPG.

Cependant, il n'y a qu'une seule issue qui pointe vers cette version. Je pense que cette version n'a pas encore été vraiment utilisé.

Il y a cette issue qui a la même erreur que l'on a. Mais pourtant ils arrivent bien quand même à créer des backup et à restorer.

https://github.com/dalibo/cnpg-plugin-pgbackrest/issues/151

Il y a aussi les issues suivantes qui sont pourtant cloturés :

https://github.com/dalibo/cnpg-plugin-pgbackrest/issues/115
https://github.com/dalibo/cnpg-plugin-pgbackrest/issues/51

J'ai bien testé en host aussi pour `uriStyle`


## Pistes restantes

1. Tester sur le cluster d'anteprod pour vérifier qu'on a la même erreur
2. **Ouvrir une issue sur le repo Dalibo** en documentant le comportement sur OpenShift + CNPG 1.29 : https://github.com/dalibo/cnpg-plugin-pgbackrest/issues/new
3. **Tester avec le fork Opera Software** (`operasoftware/cnpg-plugin-pgbackrest` v0.6.0) qui a une compatibilité CNPG 1.29 documentée et une architecture différente (objet `Archive` au lieu de `Stanza`) https://github.com/operasoftware/cnpg-plugin-pgbackrest