---
foam_template:
  filepath: "0 - INBOX/CNPG - Schema.md"
  description: "New note"
created: "2025-12-04"
---

# CNPG - Schema

## Commande SQL

[[CNPG - PostInit Commands#CNPG - PostInit Commands]]

Pour créer un schema il faut utiliser postInitApplicationSQL si on veut que ça s'applique uniquement à la BDD applicative.

## CRD Database

Avec la CRD database il est possible de créer des schemas :

```yaml
spec:
  schemas:
  - name: my-schema
    ensure: present
    owner: owner 
```