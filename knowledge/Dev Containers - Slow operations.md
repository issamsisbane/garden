En lançant un devcontainer angular depuis windows, les commandes étaients très longues à se lancer +1-2 min à chaque fois (npm install + ng test).

La Solution est d'envoyer les fichiers dans la WSL et de relancer VS Code depuis là. 

C'est un problème connu que WSL a du mal a travailler avec les fichiers sur le fs de windows lorsqu'ils sont volumineux.