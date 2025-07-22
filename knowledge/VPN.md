---
tags: TECHNOS
state: to_complete
---

[[Tunnel IPSec]]

# Technos

[[WireGuard]]
[[Strongswan]]

|Critère|**Strongswan (IPSec)**|**WireGuard**|
|---|---|---|
|**Protocole**|IPSec (IKEv1/IKEv2)|Protocole VPN propriétaire|
|**Simplicité**|Complexe à configurer|Très facile à configurer|
|**Chiffrement**|Algorithmes classiques (AES, 3DES)|Algorithmes modernes (ChaCha20, Poly1305)|
|**Performances**|Moins performant|Très performant|
|**Authentification**|Certificats, PSK, EAP|Clés publiques (simples)|
|**Utilisation typique**|Entreprises, VPN complexes|Utilisation personnelle, petits VPN, performance critique|
|**Support système**|Principalement Linux, mais support multi-plateforme|Support multi-plateforme avec intégration native Linux|