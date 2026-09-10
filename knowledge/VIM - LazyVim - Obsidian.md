---
creation date: 2026-03-27-00:53:32
modification date: 2026-03-27-00:53:32
imageNameKey: VIM_-_LazyVim_-_Obsidian
---
H L to move from files

space + g + d to delete

```
bzip2 1.0.8
ca-certificates 2026-03-19
fzf 0.70.0
k9s 0.50.18
lazygit 0.60.0
libevent 2.1.12_1
libuv 1.52.1
lpeg 1.1.0_2
luajit 2.1.1772619647
luv 1.52.1-0
ncurses 6.6
neovim 0.11.6
openssl@3 3.6.1
pcre2 10.47_1
ripgrep 15.1.0
tmux 3.6a
tree-sitter@0.25 0.25.10
unibilium 2.1.2
utf8proc 2.11.3
zlib-ng-compat 2.3.3_1
```

```lua
return {
  "epwalsh/obsidian.nvim",
  version = "*",
  lazy = true,
  ft = "markdown",
  dependencies = {
    "nvim-lua/plenary.nvim",
  },
  opts = {
    note_id_func = function(title)
      return title:gsub(" ", "-"):gsub("[^a-zA-Z0-9-]", ""):lower()
    end,
    workspaces = {
      {
        name = "vault",
        path = "~/vault", -- adapte ce chemin
      },
    },
    daily_notes = {
      folder = "Journal",
      date_format = "%Y-%m-%d",
    },
    completion = {
      blink_cmp = true,
      min_chars = 2,
    },
    ui = {
    enable = true, -- rendu des checkboxes, liens, etc.
    },
  },
}
```