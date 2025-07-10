# 🪝 Pre-commit Hook — Nettoyage des images non utilisées dans `3 - GARDEN/assets/`

Ce dépôt utilise un **hook Git personnalisé** qui s'exécute automatiquement à chaque commit. 

Il a pour but de **déplacer les images inutilisées** depuis `3 - GARDEN/assets/` vers `ASSETS/`, pour garder le répertoire `3 - GARDEN/assets/` propre.

J'utilise Obsidian et ce dernier permet de selectionner un dossier par défaut où les images et autres attachmenent vont être 

---

## ⚙️ Fonctionnement du hook

1. **Analyse tous les fichiers Markdown (`.md`)** dans le dossier `3 - GARDEN/` (et ses sous-dossiers).
2. **Détecte toutes les images référencées** via la syntaxe Obsidian : `! [[image.png]]`
3. **Parcourt tous les fichiers** présents dans `3 - GARDEN/assets/`
4. Si une image **n'est pas utilisée** dans les fichiers `.md` du Garden :
   - Elle est déplacée vers le dossier `ASSETS/`
   - Elle est automatiquement **ajoutée à l’index Git**

## 📦 Exemple

Si un fichier `3 - GARDEN/assets/chat.png` n'est référencé nulle part dans `3 - GARDEN/**/*.md`, il sera automatiquement déplacé vers : `ASSETS/chat.png`

## 🚀 Installation manuelle du hook

Copier le script dans `.git/hooks/pre-commit`

```bash
cp hooks/move-unused-images.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```