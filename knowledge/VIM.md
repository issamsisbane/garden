# Concepts
## word

A word consists of a sequence of letters, digits and underscores, or a sequence of other non-blank characters, separated with white space (spaces, tabs, EOL). An empty line is also considered to be a word.

Use 'w', 'e', and 'b' to navigate WORDs.

![[Pasted image 20241220162516.png]]

## WORD

A WORD consists of a sequence of non-blank characters, separated with white space. An empty line is also considered to be a WORD.

Use 'W', 'E', and 'B' to navigate WORDs.

![[Pasted image 20241220162652.png]]

# Movements 

## Simple Movements

`h`: move left
`j`: move down
`k`: move up
`l`: move right

`w`: move forward by beginning of the words 
`e`: move forward by ending of the words
`b`: move backward by beginning of the words ("aren't" isn't a single word)

`W`: move forward by beginning of the WORDS 
`E`: move forward by beginning of the WORDS
`B`: move backward by beginning of the WORDS ("aren't" is a single word)

## Precise Movements

`f[character]` : move to the next occurences of the character (same line as soon as the line continue)
`F[character]` : move to the previous occurences of the character (same line as soon as the line continue)

`t[character]` : move to character just before the next occurences of the character (same line as soon as the line continue)
`T[character]` : move to character just before the previous occurences of the character (same line as soon as the line continue)

`;`: continue in the same direction
`,`: continue in the opposite direction

## Horizontal Movements

`0` : move to the start of the line
`$` : move to end of the line
`^`: Moves to the **first non-blank character of a line**
`g_`: Moves to the **non-blank character at the end of a line**

## Vertical Movements

 `}` : jumps entire paragraphs **downwards**
`{` : similarly but **upwards**
`CTRL-D` : lets you **move down half a page** by scrolling the page
`CTRL-U` : lets you **move up half a page** also by scrolling

## Search

`/{pattern}` : to search **forward**
`?{pattern}` : to search **backward**

`n` : continue in **same** **direction**
`N` : continue in the **opposite** **direction**

`/<enter>` : previous search **forward**
`?<enter>` : previous search **backward**

`*` : **search** for the word **under** the cursor **forward**
`#` : **search** for the word **under** the cursor **backward**

## Counts

**`{count}{motion}`** to multiply a motion **`{count}`** times.

## Semantical Movements

**`gd`** to jump to definition of whatever is under your cursor.
**`gf`** to jump to a file in an import.

## Big Movements

**`gg`** to go to the top of the file.
**`{line}gg`** to go to a specific line.
**`G`** to go to the end of the file.
**`%`** jump to matching **`({[]})`**%%  %%.

## Operations

`x`: Delete [count] characters under and after the cursor in the current line [into a register if specified]. Does the same as 'dl'.
`r`: Replace a character
`d`: Delete text that {motion} moves over [into a register if specified].
	`dw`: delete the current word
	`db`: delete previous word
	`d7l`: delete 7 letters in the current word to the right

# Edit

To edit texts in VIM we will combine the motions we already learned to operators.

{operator}{count}{motion}
Perform an action with a number of times to a bit of text
![[Pasted image 20250129233051.png]]

`u` : undo
`ctrl` + `r` : redo

## Operators

- **`c`** (**c**hange): Change deletes a piece of text and then sends you into _Insert mode_ so that you can continue typing, changing the original text into something else. The change operator is like the **`d`** and **`i`** commands combined into one[two](https://www.barbarianmeetscoding.com/boost-your-coding-fu-with-vscode-and-vim/editing-like-magic-with-vim-operators/#fn-two). This duality makes it the most useful operator
- **`y`** (**y**ank): Copy in Vim jargon
- **`p`** (**p**ut): Paste in Vim jargon
- **`g~`** (switch case): changes letters from lowercase to uppercase and back. alternatively, use **`gu`** to make something lowercase and **`gu`** to make something uppercase
- **`>`** (shift right): Adds indentation
- **`<`** (shift left): Removes indentation
- **`=`** (format code): Formats code
- **`~`** (switch case): Switch case of selection

## Examples

- Use **`d5j`** to delete 5 lines downwards
- Type **`df'`** to delete everything in the current line from the cursor until the first occurrence of the **`'`** character (including the character itself)
- Or type **`dt'`** to do like the above example but excluding the character (so up until or just before the **`'`** character)
- Use **`d/hello`** to delete everything until the first occurrence of **`hello`**
- Type **`ggdG`** to delete a complete document

### Modes de Vim

1. **Mode Normal** : Le mode par défaut, pour naviguer et manipuler le texte.
2. **Mode Insertion** : Pour insérer du texte (`i` pour entrer en mode insertion).
3. **Mode Commande** : Pour exécuter des commandes (`:` pour entrer en mode commande).
4. **Mode Visuel** : Pour sélectionner du texte (`v` pour entrer en mode visuel).

### Commandes de base en mode Normal

- **`i`** : Passer en mode insertion avant le curseur.
- **`I`** : Passer en mode insertion au début de la ligne.
- **`a`** : Passer en mode insertion après le curseur.
- **`A`** : Passer en mode insertion à la fin de la ligne.
- **`o`** : Insérer une nouvelle ligne sous la ligne actuelle et entrer en mode insertion.
- **`O`** : Insérer une nouvelle ligne au-dessus de la ligne actuelle et entrer en mode insertion.
- **`Esc`** : Revenir en mode Normal depuis le mode Insertion ou Visuel.

### Déplacements de base

- **`h`** : Aller à gauche.
- **`j`** : Aller en bas.
- **`k`** : Aller en haut.
- **`l`** : Aller à droite.
- ==**`0`** : Aller au début de la ligne (même si caractère blanc).==
- ==**`^`**: Aller au premier caractère non espace de la ligne==
- ==**`$`** : Aller à la fin de la ligne (possible de rajouter un compteur).==
- **`gg`** : Aller au début du fichier (avec [count] pour aller a la ligne count].
- **`G`** : Aller à la fin du fichier.
- **`w`** : Aller au début du mot suivant.
- **`b`** : Aller au début du mot précédent.
- **`e`**:  Aller à la fin du mot suivant
- ==**`f`**: Aller à la prochaine occurence de lettre sur la lettre (F pour backward)==
- ==**`t`**: Aller à la prochaine occurence de lettre avant la lettre (T pour backward)==
- ==**`,`**: Repete le dernier `t` ou `f` dans la direction opposée==
- ==**`;`**: Repete le dernier `t` ou `f` dans la même direction==
- ==**`%`**: Renvoi vers le délimiteur fermant ( => ) et inversement==
- ==**`*`**: Renvoi à la première occurence suivante du premier mot entier près du curseur==
- ==**`#`**: Renvoi à la première occurence précédente du premier mot entier près du curseur==
- ==**`n`**: Repete la dernière recherche (marche avec * et #)

![[Pasted image 20250325181912.png]]

### Édition de texte

- **`x`** : Supprimer le caractère sous le curseur.
- **`dd`** : Supprimer (couper) la ligne courante.
- **`yy`** : Copier (yanker) la ligne courante.
- **`p`** : Coller après le curseur ou sous la ligne courante (selon le contexte).
- **`u`** : Annuler la dernière action.
- **`Ctrl + r`** : Rétablir (redo) une action annulée.
- **`Ctrl + d`** : Supprime la ligne actuelle.
- **`Ctrl + u`** : Se déplacer vite en haut.
- **`cw`** : Changer le mot sous le curseur.
- ==**`r`** : Remplacer un caractère sous le curseur.==
- ==**`~`**: Changer de case (min to maj ou inverse)==
- ==**`d$`**: Supprime tout depuis le curseur jusqu'a la fin de la ligne==
- ==**`d0`**: Supprime tout du debut de la ligne jusqu'au curseur==
- ==**`dG`**: Supprime tout jusqu'à la fin du fichier
- ==**`d%`**: Supprime tout le bloc ({ifelse})

dfp => supprime jusqu'au caractère p

### Déplacement de la fenetre

- ==**`zt`**: Déplace la fenètre pour avoir le cursor en haut==
- ==**`zz`**: Déplace la fenètre pour avoir le cursor au milieu==
- ==**`zb`**: Déplace la fenètre pour avoir le cursor en bas==

### Mode Visuel (pour sélectionner du texte)

- **`v`** : Entrer en mode visuel pour une sélection de texte.
- **`V`** : Sélectionner la ligne entière.
- **`y`** : Copier (yanker) la sélection.
- **`d`** : Supprimer (couper) la sélection.

### Commandes en mode Commande (après `:`)

- **`:w`** : Sauvegarder le fichier.
- **`:q`** : Quitter Vim.
- **`:wq`** : Sauvegarder et quitter Vim.
- **`:q!`** : Quitter sans sauvegarder.
- **`:x`** : Sauvegarder et quitter (comme `:wq`).
- **`:e filename`** : Ouvrir un fichier.
- **`:set nu`** : Afficher les numéros de ligne.
- **`:set nonu`** : Masquer les numéros de ligne.

# Command lines

### Open 2 file in vertical splitted mode
```
vim -O file otherfile
```
to switch right : `ctrl`+`w`+`l` 

to switch left : `ctrl`+`w`+`h`

# Commands

Copy env variables inside vim : 
```
:r! echo $ENV
```

# Comments

Pour commenter un ensemble de lignes séléctionné en visual mode :

```
norm I#
```

Pour décommenter un ensemble de lignes séléctionné en visual mode :

```
norm ^x
```