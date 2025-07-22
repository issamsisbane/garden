[Helm | General Conventions](https://helm.sh/docs/chart_best_practices/conventions/#:~:text=This%20part%20of%20the%20Best%20Practices%20Guide%20explains,nor%20underscores%20can%20be%20used%20in%20chart%20names.)

On nous dit ça : 

> **Chart** names must be lower case letters and numbers. Words may be separated with dashes (-): Examples: nginx-lego aws-cluster-autoscaler Neither uppercase letters nor underscores can be used in **chart** names.

Mais en meme temps on nous dit ça : 

> Variable names should begin with a lowercase letter, and words should be separated with camelcase and no dash.

C'est contradictoire...

Il y a une issue github pour ça : 
[Accessing values of the subchart with dash in the name · Issue #2192 · helm/helm](https://github.com/helm/helm/issues/2192)

En fait ca pose probleme quand on a des sous-charts et que veut leur envoyer des valeurs dans le chart parent. 

Il faut mettre comme cle le nom du sous-chart mais ducoup il y aura des dash.

Il est possible de modifier le nom des cle qui seront utiliser mais il faudrait modifier tous les charts, je ne veux pas trop faire ca.

Donc je decide de quand meme utiliser des dash dans les values mais uniquement pour les sous charts.