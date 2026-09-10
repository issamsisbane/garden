https://www.youtube.com/watch?v=hf6j3oiomi4

Outil d'infra-as-code pour définir des ressources avec des CRDs kubernetes pour qu'elles soient crée dans le cloud.

Fonctionne comme Terraform mais directement depuis kube.

Cela permet de tous gerer directement depuis kube et de ne pas avoir a jongler entre kube et terraform.

Quand on crée une ressource dans kube ça l'a crée sur le cloud provider et quand on la supprime de kube ça va aussi la supprimer dans le cloud provider.

On peut donc tout gérer en GitOps.