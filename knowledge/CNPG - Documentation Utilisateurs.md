# CNPG Defintion

Cloud Native PostgresSql est un Operateur Kubernetes qui permet de créer simplement et rapidement des clusters de bases de données sur Kubernetes

# Ressources

Il existe deux ressources importantes activés par l'operateur CNPG. 

## Cluster

La seule ressource nécessaire à déployer est le Cluster. Cela va créer un cluster dans le namespace spécifié qui va pouvoir contenir une ou plusieurs base de données.

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

En appliquant ce Manifest. CNPG va automatiquement créer une base de données `app` avec un user `app` ainsi qu'un secret `testcluster-cluster-app` avec le mot de passe utilisateur et toutes les informations utiles pour se connecter à la base de données.

Tout cela se fait par le biais d'un initContainer gérer par l'operateur CNPG. Il est possible de modifier le comportement de cet initContainer : 

```
initdb:
	database: mybdd
	owner: myuser
	secretName: my-user-secret  # Specification du secret avec le mot de passe user
	postInitTemplateSQL:        # Lancement de commande post création
	  - "CREATE SCHEMA gap;"
```

Il est possible de fournir un secret avec le mot de passe directement plutôt que de laisser CNPG le générer.

Pour plus d'informations voir la [API Reference Cluster - CloudNativePG v1.26](https://cloudnative-pg.io/documentation/1.26/cloudnative-pg.v1/#postgresql-cnpg-io-v1-Cluster) 
## Database

La ressource Database permet de créer une base de données dans le Cluster en plus de celle crée par initDB. 

Cela permet d'avoir notre base de données comme une ressource kubernetes et donc de pouvoir la gérer comme telle plutôt que de reposer entierement sur initDb qui nous restreint en plus à seulement une seule base de données.

Voici un exemple de manifest qui peut-être utilisé : 

```
apiVersion: postgresql.cnpg.io/v1
kind: Database
metadata:
  name: testdb
  namespace: cnpg-test
spec:
  name: testdb
  owner: test
  cluster:
    name: testcluster
```

La différence avec initDb est qu'ici l'utilisateur doit déjà exister sinon la base de données ne se déploiera pas.

Ainsi deux choix sont possibles : 
1. Créer l'utilisateur via initDb et profiter de la génération de mot de passe
2. Créer l'utilisateur via la ressource Cluster mais prendre la responsabilité de création du mot de passe.

### Création utilisateur via initDb

Cela peut-être intéressant si l'on ne va créer qu'un seule base de données ou si toutes nos bases de données vont utiliser le même utilisateur.

Il suffit de reprendre le template de la section précédente et d'utiliser le même owner  : 

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
	initdb:
		owner: myuser    # On spécifie seulement le user
```

### Création d'un utilisateur via roles

Cela peut-être intéressant si l'on veut créer un utilisateur par base de données. Dans ce cas dans la ressource Cluster on aura : 

```
spec: 
	managed:
      roles:
        - name: bestuser
          ensure: "present"
          login: true
          superuser: false
          passwordSecret: 
	          name: mySecretName
```

Il est obligatoire de spécifié un secret lors de la création d'un utilisateur appelé `role` dans le contexte de PostgreSQL.

On peut en créer autant que l'on veut et on peut aussi aller plus loin dans la personnalisation.

Pour plus d'informations voir :
- [API Reference RoleConfiguration - CloudNativePG v1.26](https://cloudnative-pg.io/documentation/1.26/cloudnative-pg.v1/#postgresql-cnpg-io-v1-RoleConfiguration)
- [PostgreSQL Database Management - CloudNativePG v1.26](https://cloudnative-pg.io/documentation/1.26/declarative_database_management/)
- [PostgreSQL Role Management - CloudNativePG v1.26](https://cloudnative-pg.io/documentation/1.26/declarative_role_management/)

# Chart

Il faut ainsi définir ses ressources applicatives dans le values et definir la base de données.

Ainsi le code serait réduit à : 

```
namespace:
  name: mytestnamespace

shared:
  database:
    clusterName: mytestcluster
    instances: 1

    databases:
    - name: mydatabase1 
      owner: 
        name: myuser1 
    - name: mydatabase2
      owner: 
        name: myuser2 
```

Le cluster de base de données sera crée dans le namespace mytestnamespace-cnpg. Les secrets pour accèder au deux bases de données sont automatiquement repliqués dans le namespace applicatif `mytestnamespace`. 

Le secret contient les informations suivantes :
- dbname
- host
- jdbc-uri
- password
- pgpass
- port
- uri
- user
- username

## Variables

Voici toutes les variables qui peuvent être utilisées :

```
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: {{ $database.clusterName }}
spec:

  database:
    clusterName: mytestcluster
    instances: 1 

	imageName: {{ $database.image | default "ghcr/cloudnative-pg/postgresql:17.4" }}
  instances: {{ $database.instances | default 2 }}

  postgresql:
    parameters:
      max_connections: "{{ $database.parameters.maxConnections | default 100 }}"
  storage:
    storageClass: {{ $storage.storageClass }}
    size: {{ $storage.size | default "1Gi" }}

    databases:
    - name: mydatabase1 
      owner: 
        name: myuser1
		ensure
		login
		superuser
		connectionLimit
```

## Exemple

Un exemple d'utilisation du chart peut-être trouvé ici :