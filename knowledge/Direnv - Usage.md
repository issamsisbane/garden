---
creation date: 2026-03-21-23:30:15
modification date: 2026-03-21-23:30:15
imageNameKey: Direnv_-_Usage
---
Edition

Edit and allow .envrc

```bashrc
direnv edit .envrc
```

Good practice

The .envrc should be committed and the secrets and sensitive file should be added via the import of a .env file.

```bash
dotenv_if_exists .env.private
```