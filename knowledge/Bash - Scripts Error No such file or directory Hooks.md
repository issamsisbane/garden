I has an error when using my git hooks scripts for my [[Project - Garden Automatic Translation]].

The error : 
![[screenshot-2025-07-10_23-42-20.png]]

I was editing this file on windows and it happens that there are some compatibility problems with the file encoding.

To resolve this problem I had to use the utilitary `dos2unix`.

```
pacman -S dos2unix
```

```
dos2unix .git/hooks/pre-commit
```
