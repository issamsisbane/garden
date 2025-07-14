
[Vault with integrated storage reference architecture | Vault | HashiCorp Developer](https://developer.hashicorp.com/vault/tutorials/day-one-raft/raft-reference-architecture)
## Consul
Solution backend pour les données de Vault pour gérer la réplication...
## RAFT
[Raft (algorithm) - Wikipedia](https://en.wikipedia.org/wiki/Raft_(algorithm))
RAFT est un algorithme de consensus permettant le stockage distribué des données de vault entre les différentes nodes du cluster.
### Comment RAFT gère les données entre les nœuds
1. **Leader et réplicas** :
		- Un nœud est élu comme **leader**, et les autres sont des **réplicas**.
	- Les écritures sont toujours dirigées vers le leader, qui les réplique ensuite vers les autres nœuds.
2. **Tolérance aux pannes** :
		- Avec 3 nœuds, le cluster peut tolérer la perte d'un nœud et continuer à fonctionner (majorité/quorum de 2 nœuds).
3. **Volumes indépendants** :
		- RAFT réplique les données entre les nœuds via le réseau, donc chaque nœud a une copie indépendante des données.

