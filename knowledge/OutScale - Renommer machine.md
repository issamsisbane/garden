Pour renommer des machines outscale sans supprimer les machines soutenus via Terraform. 

Il faut : 
1. Renommer la machine via cockpit (ihm outscale).
2. Ajouter à la main la machine et tout ce qui la compose dans le state de terraform sauf la keypair. 
3. Supprimer l'ancien nom de la machine du state
4. Lancer un apply qui devrait seulement créer une nouvelle keypair avec un nouveau nom. 

ça marche si la keypair est créer avec le nom de la vm. Si la keypair est déjà désigné dans le terraform pas besoin de faire cette étape.


> [!DANGER] IMPORTANT
> Pour que l'import fonctionne il faut déjà ajouter la conf dans terraform pour qu'il y ait l'ecart et faire un plan


Ensuite, il faut récupérer la keypair en local puis générer la clé publique associé pour l'ajouter dans les authorized hosts de la machine dont on a changé le nom. 

``` sh
ssh-keygen -y -f ./tomcat-public-int-kp > ./tomcat-public-int-kp.pub
```

Ensuite on supprime device et account de wallix et on relance et tout est ok !