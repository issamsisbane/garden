---
creation date: 2026-03-18-00:02:01
modification date: 2026-03-18-00:02:01
imageNameKey: Homelab_-_Homepage_Setup
---
J'avais un soucis dans network je voyais custom.css vide alors que sur le pod l'api sortait bien le fichier.

Il s'avere que c'etait cloudflare qui avait mis en cache le fichier.

J'ai du rajouter une règle pour éviter ça :
![[Homelab_-_Homepage_Setup.png]]

![[Homelab_-_Homepage_Setup2.png]]

Il faudrait que je rajoute un system pour relancer le pod quand je modifie le configmap pour reload automatiquement.