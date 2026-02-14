# Window Manager

Komorebi

# Status Bar

Yasb

# Shortcuts

whkd
# Stop win + L shortcut

https://superuser.com/questions/1059511/how-to-disable-winl-in-windows-10

# Disable windows shortcuts : 

Tu peux utiliser AutoHotkey pour rediriger ou bloquer ces raccourcis.

#### Étapes :

1. Installe [AutoHotkey](https://www.autohotkey.com/).
![[Pasted image 20250802125658.png]]

2. Crée un fichier texte avec l’extension `.ahk` (ex: `block_win_keys.ahk`).
    
3. Ajoute ce contenu :

```
#1::Return
#2::Return
#3::Return
#4::Return
#5::Return
#6::Return
#7::Return
#8::Return
#9::Return
```

> `#` = touche Win

4. Lance le script AutoHotkey (clic droit → "Run Script").