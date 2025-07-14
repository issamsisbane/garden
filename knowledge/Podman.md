Podman is a free & open-source alternative to [[Docker]].

Every pod run an infra container. It's a light-weight container used as an admin layer for the health of our pod.

We can define kubernetes yaml manifest to deploy pods. Which is really useful because when we want to deploy it to a kubernetes cluster we just use the file directly.

https://www.youtube.com/watch?v=Z5uBcczJxUY
Podman est un outil permettant de lancer des conteneurs comme [[Docker]].
L'avantage de podman c'est qu'il est gratuit et open-source et constitue donc une excellente alternative à Docker.

# Fonctionnement

Podman peut être installé sur windows via Podman Desktop. La configuration permet de créer une VM WSL fedora linux dédié à podman pour pourvoir lancer des conteneurs. C'est d'ici que l'on va faire toute nos commandes.

Lors de l'installation un tunnel a été créer entre windows et cette vm. On peut donc directement depuis powershell éxecuter des commandes podman.

## Accès depuis WSL Ubuntu
Il est aussi possible d'utiliser podman depuis WSL Ubuntu en faisant quelques configuration.

[Accessing Podman from another WSL distribution (Windows) | Podman Desktop](https://podman-desktop.io/docs/podman/accessing-podman-from-another-wsl-instance)