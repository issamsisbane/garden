
## Commands
### Initialise a new git repository

```bash
git init
```

### Clone a existing git repository

``` bash
git clone url
```

### Staging and commiting changes

**Check status of changes :** 

``` bash
git status
```

**Stage a file for commit :** 

``` bash
git add [file]
```

**Commit staged changes with a descriptive message :**

``` bash
git commit -m "message"
```

### Branching and merging

**List branch :** 

``` bash
git branch
```

**Create a new branch :**

``` bash
git branch [branch-name]
```

**Switch to a different branch :**

``` bash
git checkout [branch-name]
```

**Merge a specified branch into the current branch :

``` bash
git merge [branch]
```

### View git changes

**View commit history :**

``` bash
git log
```

**Show changes between commits and branches :**

``` bash
git diff
```

### Undo changes

**Create a new commit that undoes changes from a specific commit :**

``` bash
git revert [commit]
```

**Reset current HEAD to a specified state :**

``` bash
git reset
```

### Remote

**Get newest changes from the repo :**

``` bash
git push [remote-name] [branch-name]
```

**Push newest changes to the repo :***

``` bash
git pull [remote-name] [branch-name]
```

# Garder les fichiers lors d'un changement de branche

``` bash
# Sauvegarder les changements
git stash

# Récupérer les changemetns
git stash pop
```

# Supprimer les changements non suivies

``` bash
# Supprimer les changements non ajoutés avec git add
git checkout -- .
```

# Arreter de suivre un fichier

``` bash
# Supprimer un fichier ajouter avec git add
git reset <nom-fichier>
```

# GIT Rebase

Permet de refaire l'intégrale d'une arborescence git

```
git rebase -i HEAD~<nombre de commit à prendre en compte de puis le HEAD
```

Ensuite on va avoir une liste comme cela :
```
pick .......
pick .......
pick .......
pick .......
```

Chaque ligne represente un commit.
On remplace pick par squash pour les lignes que l'on veut fusionner.

On sauvegarde.

Ensuite une editeur du nom du commit qui va être fait s'ouvre. De base il y a le nom de tous les commits.
On peut tout supprimer et juste ajouter le nom que l'on veut donner a notre commit.

# Modifier l'origin

```
# Voir l'URL actuelle
git remote -v

# Changer l'URL
git remote set-url origin https://nouveau-lien-du-repo.git
```

# Ajout une nouvelle origin

```
# Ajoutez un nouveau remote 2
git remote add new-origin https://nouveau-repo-url
```


# Supprimer les branches en local qui ne sont pas sur le repo distant

```
# Récuperer les derniers maj 
git fetch --prune

# Afficher les branches distantes qui n'existent pas
git branch -vv | grep ': gone]' | awk '{print $1}'
git branch -vv | grep ': disparue]' | awk '{print $1}'

# Supprimer les branches
git branch -vv | grep ': gone]' | awk '{print $1}' | xargs git branch -D

```