---
foam_template:
  filepath: "0 - INBOX/Postgres - Psql.md"
  description: "New note"
created: "2025-12-04"
---

# Postgres - Psql

[[SQL - Boilerplates]]

Connection to psql :

```bash
psql -h localhost -U username -d database
```

List roles and attributes of users

```bash
\du
```

List databases :

```bash
\l
```

Navigate to database :

```bash
\c database
```

List tables :

```bash
\dt
```

List schemas : 

```bash
\dn
```

List extensions :

```bash
\dx
```

List locales :

```bash
\l+
```

