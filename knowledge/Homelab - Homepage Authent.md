---
creation date: 2026-03-17-22:18:04
modification date: 2026-03-17-22:18:04
imageNameKey: Homelab_-_Homepage
---
Je me suis souvenu que j'avais lu dans la documentation authentik qu'il était possible de proteger des apps sans authent.


Et je suis tombé sur cette issue github :
https://github.com/gethomepage/homepage/discussions/529

# Authentification Homepage avec Authentik sur Kubernetes

## Vue d'ensemble

Homepage ne supporte pas nativement l'authentification. Pour protéger l'accès, on utilise **Authentik** en mode **ForwardAuth** : Traefik intercepte chaque requête et demande à Authentik si l'utilisateur est bien connecté, avant de laisser passer vers Homepage.

```
Navigateur → Traefik → [ForwardAuth Middleware] → Homepage
                              ↓
                       authentik-server
                       (vérifie la session)
                       ✅ OK → laisse passer
                       ❌ KO → redirige vers login
```

---

## Concepts clés

### Middleware Traefik (ForwardAuth)

Un middleware est un plugin que Traefik applique à chaque requête HTTP **avant** de la transmettre à l'application. Le middleware `ForwardAuth` transfère la requête à un service d'authentification externe (ici Authentik) qui répond :

- `200 OK` → la requête est autorisée, Traefik la laisse passer
- `401/302` → l'utilisateur n'est pas connecté, Authentik redirige vers la page de login

L'application (Homepage) ne sait pas qu'il y a une authentification — elle reçoit juste les requêtes déjà validées.

### Outpost Authentik

L'outpost est le **composant Authentik qui répond aux requêtes du middleware**. Il expose un endpoint HTTP `/outpost.goauthentik.io/auth/traefik` que Traefik appelle à chaque requête.

Il existe deux types d'outpost :

- **Embedded** : intégré directement dans le pod `authentik-server`. Simple, suffisant pour un homelab. Pas de déploiement supplémentaire.
- **Dédié** : un Deployment Kubernetes séparé, pour plus de scalabilité.

Dans notre cas on utilise l'**outpost embedded**, accessible via le service `authentik-server` existant.

### ProxyProvider vs OAuth2Provider

||**OAuth2Provider (ex: Headlamp)**|**ProxyProvider (Homepage)**|
|---|---|---|
|L'app gère l'auth ?|✅ Oui (support OIDC natif)|❌ Non (Traefik la gère)|
|Blueprint|`authentik_providers_oauth2`|`authentik_providers_proxy`|
|Mode|Redirect + callback token|ForwardAuth à chaque requête|

Homepage n'ayant pas de support OIDC, on utilise un **ProxyProvider** en mode `forward_single`.

---

## Architecture déployée

```
┌─────────────────────────────────────────────────────┐
│ Kubernetes Cluster                                   │
│                                                      │
│  namespace: traefik                                  │
│  ┌──────────────────┐                               │
│  │ Traefik Gateway  │  main-gateway (HTTPS)         │
│  └────────┬─────────┘                               │
│           │ HTTPRoute                                │
│           ↓                                          │
│  ┌──────────────────────────────┐                   │
│  │ Middleware: ForwardAuth      │  namespace: homepage│
│  │ → authentik-server:80/      │                   │
│  │   outpost.goauthentik.io/.. │                   │
│  └────────┬─────────────────────┘                   │
│           │ si authentifié                           │
│           ↓                                          │
│  ┌────────────────┐    ┌──────────────────────┐     │
│  │ Homepage :3000 │    │ authentik-server :80  │     │
│  │ namespace:     │    │ namespace: authentik  │     │
│  │ homepage       │    │ (outpost embedded)    │     │
│  └────────────────┘    └──────────────────────┘     │
└─────────────────────────────────────────────────────┘
```

---

## Fichiers de configuration

### 1. Blueprint Authentik

Le blueprint crée automatiquement dans Authentik le Provider, l'Application et configure l'outpost embedded. Il est monté via un ConfigMap dans le worker Authentik.

```yaml
# configmap-blueprints.yaml  (ajouté à ton ConfigMap existant)
homepage.yaml: |
  version: 1
  entries:
    # ProxyProvider en mode ForwardAuth
    - model: authentik_providers_proxy.proxyprovider
      state: present
      identifiers:
        name: Homepage ForwardAuth
      attrs:
        name: Homepage ForwardAuth
        authorization_flow: !Find [authentik_flows.flow, [slug, default-provider-authorization-implicit-consent]]
        invalidation_flow: !Find [authentik_flows.flow, [slug, default-provider-invalidation-flow]]
        external_host: https://homepage.issamhomelab.org
        mode: forward_single
        cookie_domain: issamhomelab.org

    # Application Homepage
    - model: authentik_core.application
      state: present
      identifiers:
        slug: homepage
      attrs:
        name: Homepage
        slug: homepage
        provider: !Find [authentik_providers_proxy.proxyprovider, [name, Homepage ForwardAuth]]

    # Rattachement à l'outpost embedded existant
    - model: authentik_outposts.outpost
      state: present
      identifiers:
        name: authentik Embedded Outpost
      attrs:
        name: authentik Embedded Outpost
        type: proxy
        providers:
          - !Find [authentik_providers_proxy.proxyprovider, [name, Homepage ForwardAuth]]
        config:
          authentik_host: https://authentik.issamhomelab.org
          authentik_host_insecure: false
          kubernetes_namespace: authentik
```

> **Note** : le champ `invalidation_flow` est obligatoire depuis les versions récentes d'Authentik.

### 2. Middleware Traefik ForwardAuth

```yaml
# middleware-authentik-forwardauth.yaml
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: authentik-forwardauth
  namespace: homepage
spec:
  forwardAuth:
    # On pointe directement sur authentik-server (outpost embedded)
    # Pas de service outpost séparé nécessaire
    address: http://authentik-server.authentik.svc.cluster.local/outpost.goauthentik.io/auth/traefik
    trustForwardHeader: true
    authResponseHeaders:
      - X-authentik-username
      - X-authentik-groups
      - X-authentik-email
      - X-authentik-name
      - X-authentik-uid
      - X-authentik-jwt
      - X-authentik-meta-app
```

> **Important** : l'adresse pointe sur `authentik-server` directement (pas `ak-outpost-*`), car l'outpost embedded est servi par le même pod.

### 3. HTTPRoute Homepage

```yaml
# httproute-homepage.yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: homepage
  namespace: homepage
  annotations:
    external-dns.alpha.kubernetes.io/hostname: "homepage.issamhomelab.org"
    external-dns.alpha.kubernetes.io/cloudflare-proxied: "true"
spec:
  parentRefs:
    - name: main-gateway
      namespace: traefik
      sectionName: https
  hostnames:
    - "homepage.issamhomelab.org"
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /
      filters:
        - type: ExtensionRef
          extensionRef:
            group: traefik.io
            kind: Middleware
            name: authentik-forwardauth
      backendRefs:
        - name: homepage
          namespace: homepage
          port: 3000
```

> **Important** : avec Gateway API, les annotations `traefik.io/router.middlewares` sont **ignorées**. Il faut obligatoirement utiliser `filters.extensionRef` dans la HTTPRoute.

---

## Ordre de déploiement

```bash
# 1. Mettre à jour le ConfigMap des blueprints et redémarrer le worker
kubectl apply -f configmap-blueprints.yaml
kubectl rollout restart deployment/authentik-worker -n authentik

# 2. Vérifier que le blueprint s'est appliqué sans erreur
kubectl logs -n authentik deployment/authentik-worker | grep -i homepage

# 3. Appliquer le middleware Traefik
kubectl apply -f middleware-authentik-forwardauth.yaml

# 4. Appliquer la HTTPRoute
kubectl apply -f httproute-homepage.yaml
```

---

## Problèmes rencontrés et solutions

### Blueprint en doublon

```
IntegrityError: duplicate key value violates unique constraint
```

**Cause** : le blueprint avait déjà été détecté une fois (ConfigMap recréé ou renommé).  
**Solution** :

```bash
kubectl exec -it -n authentik deployment/authentik-worker -- bash
python manage.py shell
>>> from authentik.blueprints.models import BlueprintInstance
>>> BlueprintInstance.objects.filter(path__contains="homepage").delete()
>>> exit()
kubectl rollout restart deployment/authentik-worker -n authentik
```

### Champ `invalidation_flow` manquant

```
Serializer errors {'invalidation_flow': [ErrorDetail(string='This field is required.')]}
```

**Cause** : champ obligatoire depuis les versions récentes d'Authentik.  
**Solution** : ajouter dans le blueprint :

```yaml
invalidation_flow: !Find [authentik_flows.flow, [slug, default-provider-invalidation-flow]]
```

### Middleware ignoré (pas de redirection vers login)

**Cause** : l'annotation `traefik.io/router.middlewares` n'est pas prise en compte avec Gateway API.  
**Solution** : utiliser `filters.extensionRef` dans la HTTPRoute (voir fichier ci-dessus).

### Erreur 500 — service outpost introuvable

```
dial tcp: lookup ak-outpost-authentik-embedded-outpost.authentik.svc.cluster.local: no such host
```

**Cause** : l'outpost embedded ne crée pas de service Kubernetes séparé.  
**Solution** : pointer directement sur `authentik-server.authentik.svc.cluster.local` dans le middleware.

## Restreindre l'accès via roles

```
# Restreindre à un groupe spécifique (ex: "admins")
- model: authentik_policies_expression.expressionpolicy
  state: present
  identifiers:
    name: homepage-access-policy
  attrs:
    name: homepage-access-policy
    expression: |
      return ak_is_group_member(request.user, name="admins")

- model: authentik_policies.policybinding
  state: present
  identifiers:
    policy: !Find [authentik_policies_expression.expressionpolicy, [name, homepage-access-policy]]
    target: !Find [authentik_core.application, [slug, homepage]]
  attrs:
    policy: !Find [authentik_policies_expression.expressionpolicy, [name, homepage-access-policy]]
    target: !Find [authentik_core.application, [slug, homepage]]
    enabled: true
    order: 0
```

## Fonctionnement Authentik

## Comment fonctionne la session Authentik

### Le flow complet la première fois

```
1. Tu vas sur homepage.issamhomelab.org
2. Traefik → ForwardAuth → authentik-server
3. Authentik : pas de session → redirige vers authentik.issamhomelab.org/login
4. Tu te connectes (login/password)
5. Authentik crée un cookie de session dans ton navigateur
6. Authentik redirige vers homepage.issamhomelab.org
7. Traefik → ForwardAuth → authentik-server
8. Authentik : session valide ✅ → laisse passer
```

### Les requêtes suivantes

```
Tu vas sur homepage.issamhomelab.org
Traefik → ForwardAuth → authentik-server (cookie envoyé automatiquement)
Authentik : session valide ✅ → laisse passer immédiatement
```

Pas de redirect, pas de login, transparent.

---

## Durée des sessions

Il y a **deux durées distinctes** dans Authentik :

||**Session**|**Token ForwardAuth**|
|---|---|---|
|Configuré dans|Flow → Stage "User Login"|ProxyProvider `token_validity`|
|Durée par défaut|**30 jours**|**24 heures**|
|Effet si expiré|Doit se reconnecter|Redemande silencieusement à Authentik|

En pratique pour toi : **tu te reconnectes tous les 30 jours** — c'est la session navigateur qui compte. Le token ForwardAuth se renouvelle automatiquement en arrière-plan tant que la session est active, donc tu ne le vois jamais expirer.

---

## Modifier la durée de session via blueprint

```yaml
- model: authentik_stages_user_login.userloginstage
  state: present
  identifiers:
    name: default-authentication-login
  attrs:
    name: default-authentication-login
    session_duration: "days=30"    # ← changer ici
    # Exemples :
    # "hours=8"    → reconnexion chaque journée de travail
    # "days=7"     → reconnexion hebdomadaire
    # "days=365"   → reconnexion annuelle
    remember_me_offset: "days=30"  # durée du "se souvenir de moi"
```

Pour un homelab, `days=30` ou `days=90` est généralement suffisant.

