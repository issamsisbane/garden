[[CNPG - Chart - Template]]

# Theorie avec Christopher 

Finalement avec Christopher on est partis sur 
- Utiliser le initdb pour creer l'admin du cluster
- Utiliser Database pour créer une ou plusieurs base de données
- Chaque Database aurait le meme utilisateur qui serait le seul sur le cluster
- S'il veulent un autre utilisateur, il faut creer un autre cluster.
- De plus pour chaque db 
	- un secret avec les informations de connexion généré par le chart
	- un secret avec le mot de passe généré par CNPG

## Problèmes

Avec cette théorie, vu qu'on crée un secret autant ajouté le mot de passe directement pour avoir un secret complet et enlever de la complexité.

De plus, ça pose un problème car on ne peut plus gérer l'utilisateur comme je le faisais avec ça : 

```
managed:
    roles:
    {{- range $db := $databases }}
      - name: {{ $db.owner.name }}
        ensure: {{ $db.owner.ensure | default "present" }}
        login: {{ $db.owner.login | default true }}
        superuser: {{ $db.owner.superuser | default false }}
        passwordSecret: 
          name: {{ $db.owner.passwordSecretName }}
        connectionLimit: {{ $db.owner.connectionLimit | default 100 }}
```

Et on ne peut donc plus gérer la connectionLimit (nécessaire pour nexus par exemple)

## Solution

Je pense donc que le mieux serait de reabandonner completement initdb et de n'utiliser que roles et Database.

On a donc :
- On utilise Database pour definir une database
- Chaque base de données peut avoir un user différent ou le même
- s'il on met le même il faut mettre toutes les options au moins sur le premier car seulement le premier sera crée

```
namespace:
  name: nexusrepo

shared:
  database:
    clusterName: oui
    instances: 1

    databases:
    - name: oui 
      owner: 
        name: oui 
        connectionLimit: 10000
    - name: test
      owner: 
        name: oui 
```

On met dans un dict les users déjà traités pour ne pas avoir deux fois le même sinon on a une erreur : 

```
managed:
    roles:
    {{- $processedOwners := dict }}
    {{- range $db := $databases }}
      {{- if $db.owner }}
        {{- $ownerName := $db.owner.name }}
        {{- if $ownerName }}
          {{- if not (hasKey $processedOwners $ownerName) }}
            {{- $_ := set $processedOwners $ownerName true }}
      - name: {{ $ownerName }}
        ensure: {{ $db.owner.ensure | default "present" }}
        login: {{ $db.owner.login | default true }}
        superuser: {{ $db.owner.superuser | default false }}
        passwordSecret:
          name: cnpg-{{ $db.name }}-db-secret
        connectionLimit: {{ $db.owner.connectionLimit | default 100 }}
          {{- end }}
        {{- end }}
      {{- end }}
    {{- end }}
  {{- end }}
```

## Tests

### Replication des secrets

J'ai testé la replication des secrets et ça fonctionne bien.

J'ai testé avec un type de secret `Opaque` et avec un type de secret `basic-auth` les deux fonctionnent. 

Juste basic-auth il faut rajouter :

```
data:
  username: test 
  password: test
```

Cela va etre overrider après donc aucun problème. 

SI DUCOUP PROBLEME IL FAUT REMETTRE UN SECRET OPAQUE.

J'ai decidé de rester avec basic-auth car c'est ce qui est généré par cnpg par soucis de cohérence.

### Creation bdd avec users

#### 1 User et 1 DB
Avec un seul user et une db ça marche très bien

#### 2 User et 2 DB
