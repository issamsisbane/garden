---
foam_template:
  filepath: "0 - INBOX/Linux - APT - Proxy.md"
  description: "New note"
created: "2026-04-07"
---

# Linux - APT - Proxy

To use a proxy for apt :

`/etc/apt/apt.conf.d/90curtin-aptproxy`

```bash
Acquire::http::Proxy "http://proxy";
Acquire::https::Proxy "http://proxy";
```
