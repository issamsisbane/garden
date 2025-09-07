# Contexte

On a un cluster de noeuds vault.
On veut pouvoir accèder à ce cluster de puis l'exterieur. 

On a donc un fqdn unique pour accèder aux cluster. Ainsi, il va falloir un load balancer pour rediriger les requêtes. 

On utilise HA proxy comme load balancer. 

# Health Check

Le load balancer doit savoir à chaque moment quel noeud du cluster vault est le leader pour rediriger les requêtes. Pour cela, il suffit de faire une requête d'api pour avoir le statut du noeud : 

```
https://{{ fqdn-noeud }}:8200/v1/sys/health
```

Selon la doc suivante : [/sys/health - HTTP API | Vault | HashiCorp Developer](https://developer.hashicorp.com/vault/api-docs/system/health)
Les heathchecks qui nous intéressent sont :
- `200` => Le noeud est le leader (Initialisé et unsealed)
- `429` => Le noeud est un noeud en StandBy (Initialisé et unsealed)

Il faut donc rediriger vers le noeud qui répond en 200.

Voici la conf HA Proxy pour le faire : 

```
global
  daemon
  maxconn 256
  log stdout format raw local0

defaults
  log global
  log-format "%ci:%cp [%tr] %ft %b/%s %Tt %ST %B \"%r\" %tsc"
  mode http
  timeout connect 5s
  timeout client  30s
  timeout server  30s
  option  httpchk GET /v1/sys/health
  http-check expect status 200

frontend vault_front
  bind *:443 ssl crt <cert-path-file>
  default_backend vault_cluster

backend vault_cluster
  balance first
  option httpchk GET /v1/sys/health
  http-check expect status 200

  server vault1 vault-node-01:8200 check ssl ca-file <ca-file-path>
  server vault2 vault-node-02:8200 check ssl ca-file <ca-file-path>
  server vault3 vault-node-03:8200 check ssl ca-file <ca-file-path>
```

Concrètement toutes les 2 secondes, HA proxy va émettre une heathcheck auprès des machines une par une jusqu'à obtenir un statut 200 et donc trouver le leader.


![[Pasted image 20250523183709.png]]
![[Pasted image 20250523183734.png]]

# Load Balancing
![[Pasted image 20250523183758.png]]

Finalement tout les requêtes sont envoyés au leader. Il n'y a pas d'histoire de mode performance où seulement tous les nœuds peuvent répondre aux requêtes de lecture et seulement le nœud leader peut répondre aux requête d'écriture.

C'est seulement avec le mode entreprise et il faudrait alors une configuration spéciale côté load balancer.

# TCP - Conf

Finalement il faudrait passer en tcp car c'est ce qui est fait
Voici la requete pour le faire : 
```
echo -e "GET /v1/sys/health HTTP/1.1\r\nHost: localhost\r\n\r\n" | openssl s_client -connect 172.21.69.11:8200 -quiet
```