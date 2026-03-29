On peut avoir des problèmes d'incohérences entre la base de données et nexus. 

Pour règler le problème, il faut supprimer les blobs qui posent problèmes mais aussi aller dans la DB et supprimer tout le contenu de la table du repo qui pose problème `helm_asset_blob` ainsi que ces références via la commande : 

``` sql
TRUNCATE TABLE helm_asset_blob CASCADE; # ou docker ou raw...
```

![[Pasted image 20250801185614.png]]

