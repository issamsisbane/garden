Si on veut utiliser un stockage S3 qui n'est pas AWS directement mais qui utiliser l'api de S3. On peut avoir une erreur à la configuration de `verification`.

Pour ça il faut desactiver cette verification pour S3 dans la conf de nexus.

```
nexus.s3.blobstore.verify...
```

Dans le chart Nexus HA, il faut activer l'override de la conf et mettre tel quel la propriété dans nexus.conf.data qui va creer le config map et le monter dans le pods.

Il faut aussi augmenter les connexions à postgres pour du HA.