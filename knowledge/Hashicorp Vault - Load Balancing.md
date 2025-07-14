
Il est important de configurer un load balancer pour l'accès au nodes de Vault. 

On doit passer par le leader pour toutes les opérations d'écriture mais par n'importe quel node pour les opérations de lecture. 

On peut donc repartir la charge sur les différents nodes. Cela va aussi permettre de gérer les redirections en cas d'indisponibilité d'un node. 

> If you choose to terminate TLS at your load balancer, it is also strongly recommended to use TLS for the connection from the load balancer to Vault as well to minimize the exposure of secret content on your network.

Il suffit d'utiliser l'endpoint `/v1/sys/health`  pour récupérer l'etat d'un node :
- **200** : Le nœud est actif et **leader**.
- **429** : Le nœud est en mode standby.
- **503** : Le nœud est scellé ou indisponible.

Puis on rediriger le trafic selon le type de requête : 
- Rediriger les requêtes d’écriture (`POST`, `PUT`, `DELETE`, etc.) vers le **leader**.
- Répartir les requêtes en lecture (`GET`) entre les **standby**.
- 