
# CI Pipelines
* Valider les fichiers de configurations
* Lancer des tests automatisés

Les changements doivent être approuvés avant application.

# CD Pipelines
## Push Deployment
On aura des pipelines dans des CI/CD Servers qui vont push les changements dans l'environnement de déploiement.

## Pull Deployment
On aura des outils comme [[FluxCd]] ou [[ArgoCD]] qui ont un agent installé dans l'envrionnement de déploiement. Ce dernier va monitorer et comparer le state actuel de l'infra et celui défini dans le dépôt Git et applique les changements nécessaires si jamais il y a écart.

L'avantage de ce type de déploiement est que l'on peut rollback très facilement à une version antérieur si il y problème, juste en faisant un git revert. 