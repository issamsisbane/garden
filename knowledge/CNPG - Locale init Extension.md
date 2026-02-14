---
foam_template:
  filepath: "0 - INBOX/CNPG - Locale init Extension.md"
  description: "New note"
created: "2025-12-04"
---

# CNPG - Locale init Extension

On peut initialiser dans le initDB les locales et extensions qui seront répercutés sur les templates `template0` et `template1`.

Comme ça à la création de nouvelles bases de données tout sera ajoutés directement.

![[CNPG - Locale init Extension_2025-12-04-16-50-04.png]]

## Extensions 

Pour les extensions on peut faire cela : 

```yaml
spec:
  bootstrap:
    initdb:
        postInitTemplateSQL:
        - "CREATE EXTENSION IF NOT EXISTS pg_trgm;"
        - "CREATE EXTENSION IF NOT EXISTS pg_buffercache;"
        - "CREATE EXTENSION IF NOT EXISTS pg_prewarm;"
        - "CREATE EXTENSION IF NOT EXISTS btree_gist;"
        - "CREATE EXTENSION IF NOT EXISTS btree_gin;"
        - "CREATE EXTENSION IF NOT EXISTS pgstattuple;"
        - "CREATE EXTENSION IF NOT EXISTS pg_visibility;"
        - "CREATE EXTENSION IF NOT EXISTS pg_freespacemap;"
```

Om peut aussi ajouter des extensions pour chaque CRD `Database` comme cela : 

```yaml
spec:
    extensions:
    - name: pg_trgm
    - name: pg_buffercache
    - name: pg_prewarm
    - name: btree_gist
    - name: btree_gin
    - name: pgstattuple
    - name: pg_visibility
    - name: pg_freespacemap
```

## Locales 

Les locales que l'on ajoute dans initDB s'applique aux templates et donc à toutes les nouvelles bases qui seront crée.

```yaml
spec:
  bootstrap:
    initdb:
        encoding: UTF8
        locale: fr_FR.UTF-8
        localeCType: fr_FR.UTF-8
        localeCollate: fr_FR.UTF-8
```

Pour la CRD `Database` si l'on veut modfifier le localeCType, il faut utiliser le `template0` qui est modifiable comparé au par défaut `template1`.

Si on fait ça parcontre il faut laisser les extensions car elles ne seront pas copiées.

```yaml
spec:
  template: "template0"
  encoding: "UTF8"
  locale: "fr_FR.UTF-8"
  localeCType: "fr_FR.UTF-8"
  localeCollate: "fr_FR.UTF-8"
  extensions:
    - name: pg_trgm
    - name: pg_buffercache
    - name: pg_prewarm
    - name: btree_gist
    - name: btree_gin
    - name: pgstattuple
    - name: pg_visibility
    - name: pg_freespacemap
```

Le mieux c'est de ne laisser le choix que dans le initdb et donc avoir la même chose dans tous le cluster.

J'ai donc décidé de ne pas laisser la possibilité de modifier les locales dans la CRD Database.

On devrait à mon avis faire pareil pour tout les clusters.