
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


[[GIT - Worktree]]
