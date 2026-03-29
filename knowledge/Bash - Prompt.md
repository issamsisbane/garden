It is possible to change bash prompt by editing the variable PS1 in .bashrc.

This website facilitate the process : 
https://bash-prompt-generator.org/

``` bash
PROMPT_COMMAND='PS1_CMD1=$(__git_ps1 " (%s)")'; PS1='\[\e[38;5;155m\]\u@\h\[\e[97m\]:\[\e[38;5;45m\]\w\[\e[38;5;220;1m\]${PS1_CMD1}\[\e[0m\] \a\[\e[2m\]\t\n\[\e[0;38;5;155m\]\$\[\e[0m\] '
```