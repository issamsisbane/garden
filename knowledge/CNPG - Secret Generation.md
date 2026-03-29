# CNPG - Secret Generation

[[CNPG - Secret Generation - External Secret]]


## InitDb
En créant un cluster CNPG simple comme cela : 

```
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: testcluster
  namespace: cnpg-test
spec:
  imageName: "cloudnative-pg/postgresql:17.4"
  instances: 1
  storage:
    size: 1Gi
```

On va avoir un conteneur initdb qui va créer un base de données app avec un utilisateur app et générer un secret avec toutes les infos pour se connecter à la bdd : password, host, url...

Le probleme avec cette approche c'est que l'on ne peut créer qu'une seule base de données.

## Database 

On peut aussi créer un [[CNPG - Database]] comme cela : 

```
apiVersion: postgresql.cnpg.io/v1
kind: Database
metadata:
  name: testdb
  namespace: cnpg-test
spec:
  name: testdb
  owner: issam
  cluster:
    name: testcluster
```

Si on crée la base de données tel quelle après avoir crée le cluster, on va avoir une erreur disant que le user `issam` n'existe pas. 

## Create User

Pour cela on peut donc crée le user à la création du cluster via : 
```
managed:
      roles:
        - name: issam
          ensure: "present"
          login: true
          superuser: false
```

Si on fait cela on ne pourra pas se connecter à la bdd via cet user, car on a pas fourni de secret contenant le mot de passe de ce dernier. Et dans secret CNPG ne genere pas automatiquement pour les users. 

Ainsi il faut ajouter : 

```
managed:
      roles:
        - name: issam
          ensure: "present"
          login: true
          superuser: false
          passwordSecret: 
	          name: mySecretName
```

Et maintenant en créant le base de données toute se passe bien !

On doit créer le secret avec le mot de passe de l'utilisateur mais aussi mettre les infos de connexion à la bdd à l'interieur. Comme ça il suffit juste de repliquer le secret dans le ns applicatif et pas besoin de transformation bizarre.

# Fonctionnement alternatif possible

On peut aussi dans notre database utiliser l'user `app` généré par l'initdb. Cela permet de ne pas avoir à generer un secret pour le mot de passe de l'utilisateur. 

Comme cela : 

```
apiVersion: postgresql.cnpg.io/v1
kind: Database
metadata:
  name: testdb
  namespace: cnpg-test
spec:
  name: testdb
  owner: app
  cluster:
    name: testcluster
```

Ensuite il faudrait repliqué le secret généré par CNPG dans le ns applicatif pour que l'application puisse se connecter à la bdd.

Le problème c'est que le secret généré par CNPG contient ces infos : 

![[Pasted image 20250724115728.png]]

Or les infos dbName, url... utilise app comme nom de base de données et pas testdb comme on voudrait.

Ainsi on peut pas juste utiliser le secret telquel. C'est pour cela que je pense que la meilleur solution est la précédente.

# Meilleure Solution

On peut utiliser la CRD Password de External Secret.

