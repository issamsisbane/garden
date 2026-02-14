---
foam_template:
  filepath: "0 - INBOX/CNPG - PostInit Commands.md"
  description: "New note"
created: "2025-12-04"
---

# CNPG - PostInit Commands


Il y a une différence entre `postInitTemplateSQL` et `postInitApplicationSQL`.

`postInitTemplateSQL` s'applique à la bdd applicative crée via l'initdb mais aussi aux templates et donc à toutes les nouvelles bdd qui vont être crée.

`postInitApplicationSQL` ne s'applique que à la bdd applicative crée par CNPG lors de l'initDB.