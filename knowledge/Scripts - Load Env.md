Ce script permet de directement exporter toutes les variables d'envrionnements nécessaires pour un environnement en particulier. 

# Utilisation

```
load pel
```

# Configuration

## Ajout d'envrionnement

Il suffit d'aller dans `/home/issam/.outscale` et d'ajouter un fichier env_{nom_de_lenvrionnement} et d'ajouter les exports nécessaires à l'intérieur. 

## Améliorations

Il serait intéressant de rendre l'outil plus globale que juste outscale car finalement on peut l'utiliser pour tout. 

Je devrais déplacer le script qui dans `.outscale` actuellement dans TOOLS et ajouter peut être le type d'envrionnement que je veux load pour avoir : 

```
load outscale oniam
```