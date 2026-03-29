Il peut arriver d'avoir l'erreur suivante : 
![[Pasted image 20250801193546.png]]

Pour la résoudre il faut supprimer les blobs problématiques. Et repush le contenu supprimés.

On peut retrouver les blobs problèmatiques dans les logs de nexus.

Pour résoudre le problème : 
1. Récupérer la liste des blobs
2. Se connecter à la bdd
3. Récuperer les ids des blobs depuis la table docker_asset_blob
4. Supprimer les reference aux blobs dans les tables docker_asset et docker_asset_blob

Se connecter à la bdd
1. On se connecte à l'user specifique de la machine
```
su - user
```
2. On se connecte avec psql avec l'user specifique
```
psql -U user
```
3. On se connecte à la bdd nexus
```
\c nexus
```

Au préalable, il faut stopper nexus.
```
systemct -u stop nexus-container
```

Les commandes à lancer :
```
SELECT * FROM docker_asset_blob WHERE blob_ref='s3-docker@5d12d284-7ebc-4a94-a04a-a08141cc4f96';
DELETE FROM docker_asset WHERE asset_blob_id = 2276;
DELETE FROM docker_asset_blob WHERE asset_blob_id = 2276;
```


# Sonatype ?

### Verify and Repair Data Consistency Tasks

NEW IN 3.83.0

These tasks restore missing data when an artifact that exist in storage is not in the database

## Case

Fred a mis juste le problème pour repousser dans la base de données et pas l'autre problème de manifest unknown.

En fait le premier problème est que on a manifest unknown quand on clique sur l'artefact. Et quand on tente de repousser l'artefact là on a une erreur 500 disant que le blob existe seulement dans la base de données.