Créer une pipeline github actions qui va build une image frontend et backend pour une application et rajouter une manifest dans un dépôt gitops pour créer un environnement de Dev.

Quand on fait une modif dans le code dev et que l'on push. Cela va automatiquement créer l''enviornnement sur kubernetes.

On peut faire en sorte qu'il faille créer une branche pour ça obligatoirement, pas sur la master. Et quand la branche est supprimé ça va supprimé l'application sur argo.