---
created: "2026-08-13"
---

# Keycloak - LDAP


Par défautP tous les rôles du LDA sont récupérés.

Pour modifier le filtre appliqué il faut se rendre sur keycloak. 

On se place dans le realm, puis dans l'onglet mapper on clique sur groups. Le filtre peut être modifié dans le champs LDAP Filter et doit être une expression LDAP valide.

Exemple : (|(cn=*groupe1)(cn=groupe2)(cn=groupe3))