We first need to install [[Rancher Desktop]] in windows.
We have to add wsl in the settings. I ran into an error [[Rancher Desktop - Error Installation]]

Mischa installed [[brew]] as a package manager to have the same config between the mac and his ubuntu machine.

We need to install kubectl & [[K9S]] : 
```
brew install kubectl & k9s
```

he also install vim & tmux : 
```
sudo apt install vim tmux
```

he also show a configuration for .bashrc : 
```
alias k='kubectl'
source /etc/bash_completion
source <(kubectl completion bash)
complete -o default -F __start_kubectl k
```

It allows to add completion for [[Kubectl - Documentation]] and the use of the alias k instead of always typing kubectl.

We also created a config for vim by creating the file .vimrc : 
``` bash
" Ensure Vim uses filetype plugins
filetype plugin on

"Enable indentation
filetype indent on

" Set the default indentation to 2 spaces for all files
set tabstop=2
set softtabstop=2
set shiftwidth=2
set expandtab

" Highlight trailing whitespace in all files
autocmd BufRead,BufNewFile * match Error /\s\+$/

" Enable auto-indentation
set autoindent

" Turn on syntax highlighting
syntax on

" Set backspace so it acts more intuitively
set backspace=indent,eol,start
```