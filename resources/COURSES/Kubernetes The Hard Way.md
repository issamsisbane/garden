https://github.com/kelseyhightower/kubernetes-the-hard-way/tree/master

# 1 - Setup

On va créer des machines virtuelles avec Vagrant. On a besoin de : 

| Name    | Description            | CPU | RAM   | Storage |
| ------- | ---------------------- | --- | ----- | ------- |
| jumpbox | Administration host    | 1   | 512MB | 10GB    |
| server  | Kubernetes server      | 1   | 2GB   | 20GB    |
| node-0  | Kubernetes worker node | 1   | 2GB   | 20GB    |
| node-1  | Kubernetes worker node | 1   | 2GB   | 20GB    |

La jumpbox va être mon laptop.

[[Kubernetes - Fonctionnement]]

