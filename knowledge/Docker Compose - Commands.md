# Lancer les conteneurs

### Lancer les conteneurs en arriere plan
```
docker compose up -d
```

si on fait une modif on peut relancer et ça ne va recréer que les conteneurs modifié.
### Lancer seulement une partie

```
docker compose up -d --build <nom>
```

# Lister

```
docker-compose ps
```

# Logs

### Affiche les logs en continu

```
docker-compose logs -f    # 
```
# Stopper les conteneurs

```
docker-compose down
```