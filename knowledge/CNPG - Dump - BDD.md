---
foam_template:
  filepath: "0 - INBOX/CNPG - Dump - BDD.md"
  description: "New note"
created: "2026-03-12"
bloggable: true
---

# CNPG - Dump - BDD

## Creation du dump

Créer un Dump de BDD manuellement


Pour des dumps ponctuels, il est possible de le faire manuellement.

### CLI

Via la cli oc, on peut se connecter au pod CNPG et utiliser les commandes suivantes pour créer et récupérer un dump en local :

```bash
kubectl exec cluster-example-1 -c postgres \
  -- pg_dump -d app > app.sql
```


### PGAdmin

Via PGAdmin, il est très simple de créer un dump d'une base de données.

## Chargement du dump Automatique

Il est possible d'utiliser les mecanismes CNPG pour faire des dumps et les restorer. [[CNPG - Backup]]

## Chargement du dump Manuel

### 1.	Accès au pod CNPG

Pour accéder au pod CNPG, il faut passer par kubectl ou oc.

Depuis la machine de rebond il faudra donc d’abord se login au préalable via oc au cluster :

```bash
oc login --server="$server" --username="$USERNAME" --password="$pass"
```

Il est aussi possible de se connecter sur l’UI Openshift et de récupérer la commande connexion directement depuis l’UI.

### 2.	Copie et chargement du dump sur le pod CNPG

Tu peux effectivement copier le dump de la bdd dans le répertoire /var/lib/postgresql/data, cela ne devrait pas poser de problème. Seul point à prendre en compte, le pvc fait 1Gb par défaut donc il faudra peut-être l’augmenter si le dump est lourd ou bien créer un pvc dédié pour ce dump (qui sont des actions de mon côté).

Voici la commande pour copie le dump dans le pod : 

```bash
oc cp ./dump.sql $namespace/$pod:/var/lib/postgresql/data/dump.sql
```

Une fois le dump copié, pour lancer les commandes psql, il faut se connecter directement sur le pod via oc avec la commande suivante : 

```bash
oc rsh -c postgres $pod -n $namespace
```

Une fois connecté sur le pod, tu peux te connecter à la bdd avec la commande suivante et entrer le mot de passe (trouvable dans le secret Openshift cnpg-emp-db-secret): 

```bash
psql -U <my-user> -d <my-db> -h localhost
```

### 3.	Alternative sans copie du dump dans le pod

Sinon, il est aussi possible de charger le dump de la bdd directement depuis la machine de rebond sans le copier sur le pod au préalable avec la commande suivante :

```bash
kubectl exec -I $pod -n $namespace -- psql "postgresql://<my-user>:<my-password>@localhost/<my-db>" < dump.sql
``` 