Claude code c'est un assistant IA sous forme d'application de terminal. On l'installe via nodeJS. 

# Installation

[Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview#configure-claude-code)



J'ai donc installé nodejs sur la WSL :

``` bash
# Download and install fnm:
curl -o- https://fnm.vercel.app/install | bash

# Download and install Node.js:
fnm install 22

# Verify the Node.js version:
node -v # Should print "v22.14.0".

# Download and install pnpm:
corepack enable pnpm

# Verify pnpm version:
pnpm -v
```

Pour installer claude code il faut juste lancer : 

``` bash
npm install -g @anthropic-ai/claude-code

# Pour le container il faut ajouter le sudo (non recommandé par la doc de claude code)
```

Ensuite il on peut tester en lançant claude dans le terminal. 
Il faudra aussi ajouter du crédit sur son compte anthropic.

## Devcontainers
je l'ai installé dans un premier temps dans un devcontainer pour tester et ça marche bien mais ce n'est pas vraiment pratique puisqu'il faut refaire la configuration à chaque fois. 

[Repo Devcontainers officiel](https://github.com/anthropics/claude-code/tree/main/.devcontainer)

# Utilisation

## Terminal 

| Command  | Description | Example |
|---|---|---|
|`claude`|Start interactive REPL|`claude`|
|`claude "query"`|Start REPL with initial prompt|`claude "explain this project"`|
|`claude -p "query"`|Run one-off query, then exit|`claude -p "explain this function"`|
|`cat file \| claude -p "query"`|Process piped content|`cat logs.txt \| claude -p "explain"`|
|`claude config`|Configure settings|`claude config set --global theme dark`|
|`claude update`|Update to latest version|`claude update`|
|`claude mcp`|Configure Model Context Protocol servers|[See MCP section in tu](https://docs.anthropic.com/en/docs/agents/claude-code/tutorials#set-up-model-context-protocol-mcp)|

- `--print`: Print response without interactive mode
- `--verbose`: Enable verbose logging
- `--dangerously-skip-permissions`: Skip permission prompts (only in Docker containers without internet)

|Command|Purpose|
|---|---|
|`/bug`|Report bugs (sends conversation to Anthropic)|
|`/clear`|Clear conversation history|
|`/compact`|Compact conversation to save context space|
|`/config`|View/modify configuration|
|`/cost`|Show token usage statistics|
|`/doctor`|Checks the health of your Claude Code installation|
|`/help`|Get usage help|
|`/init`|Initialize project with CLAUDE.md guide|
|`/login`|Switch Anthropic accounts|
|`/logout`|Sign out from your Anthropic account|
|`/pr_comments`|View pull request comments|
|`/review`|Request code review|
|`/terminal-setup`|Install Shift+Enter key binding for newlines (iTerm2 and VSCode only)|
|`/vim`|Enter vim mode for alternating insert and command modes|

## Automated Context

Claude peut-être utilisé dans des pipelines et contexte automatisé. 
Par exemple dans un pipeline gitlab on peut demander à claude de mettre à jour le README avec les derniers changements qui ont été apporter au repo git via les commits.

``` bash
export ANTHROPIC_API_KEY=sk_...
claude -p "update the README with the latest changes" --allowedTools "Bash(git diff:*)" "Bash(git log:*)" Edit
```

