
Commands : 

`wc` : compter les lignes
`head`  : Afficher les premiers lignes d'un fichier
`cut`  : Ne garder que certaines colonnes d'un fichier
`grep` : Ne ressortir que ce qui contient le pattern mentionné
`sort` : Trie l'entrée
`uniq` : ne ressort que les éléments uniques (Adjacent)


## History

The size of history can be change by changing : 
env vars `HISTSIZE` and `HISTSIZEFILE`.

To avoid duplicate we can use HISTCONTROL=ignoredups

### History expansion

#### Run commands
The command will be executed directly : 
`!!` : last command
`!grep` : last grep command
`!?grep?` : last command with grep in it

To only print the command : 
`!?grep?:p` : print the command 

#### Deletion
`rm -i` : prompt files to be delete

`!$` : Last argument of the last command

Remove the files found by the ls :
```
# Allow to verify what is match before deletion
ls *.txt
rm !$
```

`!*` : All argument of the last command

#### Edition
`curl 8.8.8.8 443`
`^curl^telnet` : Launch the previous command by replacing curl with telnet
It would change only the last occurence of the word in the command.
`!!:s/curl/telnet/` : Replace all occurences of the word like a classic sed.

## Moving between directories faster

### CDPATH
We can use CDPATH which is like a PATH, that will search in it when hitting a cd.

### Stack

We can use pushd et popd to had and delete directories from the stack.

```
pushd
popd
dirs
pushd 
```