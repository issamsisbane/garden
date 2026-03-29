C'est un operateur kubernetes qui perment de faire le lien entre une source externes et les secrets kubernetes.

On l'installe via un helm chart
![[ms-teams_0gX8WRkEnk.png]]

# Composants

## Secret Store

Etablit le lien et la connexion entre le cluster kube et la solution externe de gestion de secret (
[[Hashicorp Vault]], azurekeyvault...)
C'est une ressource Kubernetes.
Un SecretStore correspond à un Domain Applicatif (cpj, emp...)
![[ms-teams_iAagTPkIyW.png]]
## ExternalSecret

Fait le Mapping entre un secret du vault et un Secret kubernetes. Cela va crée un secret kubernetes qui va être alimenté par le secret dans le vault.

On crée un ExternalSecret par secret que l'on veut.