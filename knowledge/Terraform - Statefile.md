---
creation date: 2026-03-21-15:11:42
modification date: 2026-03-21-15:11:42
imageNameKey: Terraform_-_Statefile
---
Quand on utilise terraform (ou opentofu), on doit gérer un statefile.

Ce statefile liste tous ce qui a été déployé par terraform et donc utilisé pour savoir ce qui doit etre modifié supprimé...

Le statefile est un fichier qu'il faut proteger car il peut contenir des credentials. Mais il doit aussi être partagé par toutes les personnes qui doivent exécuté le code terraform.

Cela étant dit, on arrive à un problème. Le problème de l'oeuf de de la poule.
Habituellement, le statefile est stocké dans un S3. C'est ce qui est le plus courant.

Mais ce stockage S3 sur un cloud provider, il doit bien être crée au préalable. En plus très souvent il faut d'autre éléments avec le S3 (DynamoDB, Policies IAM pour AWS...)

Mais comment utiliser terraform alors que le stockage pour le S3 n'est pas encore disponible ?

### Solution 1 : Bootstrap local

La première solution est d'écrire le code terraform pour créer le bucket S3 dans un dossier bootstrap avec un statefile en local.

Une fois le S3 crée, le statefile peut être poussé sur le S3.

Parcontre il faut faire attention à ne pas faire un terraform destroy qui viendrait tout supprimer ce bucket avec tous nos statefile.

### Solution 2 : Bootstrap manuel

L'autre solution est d'accépter que tout ne peut pas être automatisé. Et que ce bootstrap initial doit se faire à la main (où via cli) mais pas en as code.

Il est aussi possible pour AWS par exemple d'utiliser Cloudfront qui ne nécessite pas de statefile pour cette partie boostraping.

### Solution 3 : Bootstrap Externe

Une autre solution est de stocké le statefile dans un autre endroit. Par exemple dans un vault ou openbao ou un serveur http. 

Mais dans ce cas le serveur doit aussi exister au préalable.

### Mauvaise idée : Stockage via GIT

J'ai pensé à un moment de stocké mon statefile sur git. 
Le statefile de base est un fichier plain-text qui peut contenir des credentials, on ne peut donc pas le stocker comme cela sur Github ou Gitlab.

Par contre il est possible d'encrypter ce fichier. Opentofu le permet par exemple ou bien des solutions externes comme sops ou pgp.

Ainsi on pourrait pousser le statefile sur Git et tout le monde aurait accès au statefile avec le code directement.

Cependant cela pose un problème, car le principe de lock du statefile ne serait pas applicable.

En effet, lorsque developer1 lance clone le repo et lancer un terraform apply, on ne veut pas que developer2 puisse aussi le faire. Sinon les 2 peuvent avoir un statefile différent selon les modifs apportés et on se retrouve avec des conflits au final.

Une solution sera de ne permettre l'execution des commandes terraform uniquement depuis une pipeline ci/cd sur une branche précise. Ce qui forcera une execution à chaque fois et donc le lock du statefile par la même occasion.