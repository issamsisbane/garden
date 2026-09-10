On peut naviguer des dossiers avec netrw l'exporateur de fichier natif directmeent intégré à vim.

https://vonheikemen.github.io/devlog/tools/using-netrw-vim-builtin-file-explorer/

On peut l'utilsier pour naviguer dans notre system, crée des dossiers, les modifier et les supprimer.

On peut meme avoir des vues differences dont un tree ou on peut parcourir tous les dossier depuis une page avec la commande i.

On accède à ça via : 
```
vim . (un dossier)
```

ou 

```
:e . (avec vim d'ouvert)
```

On peut utilsier : 
```
:Lexplore
:Le
```

Pour toggler netrw dans un window a gauche ça va ouvrir un fichier à droite et on peut refaire la commande pour fermer la tab window

Monter d'un repertoire : 
```
-
```

Revenir au repertoire precedent : 
```
u
```

Creer un fichier (il faut l'enrengistrer pour qu'il soit créer) : 
```
%
```

Toggle Hidden files : 
```
gh
```

- `R`: Renames a file
    
- `mt`: Assign the "target directory" used by the move and copy commands.
    
- `mf`: Marks a file or directory. Any action that can be performed on multiple files depend on these marks. So if you want to copy, move or delete files, you need to mark them.
    
- `mc`: Copy the marked files in the target directory.
    
- `mm`: Move the marked files to the target directory.
    
- `mx`: Runs an external command on the marked files.
    
- `D`: Deletes a file or an empty directory. vim will not let us delete a non-empty directory. I'll show how to bypass this later on.
    
- `d`: Creates a directory.