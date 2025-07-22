J'ai utiliser pour cette exemple un conteneur avec le client gpg installe.
### Clés GPG

#### Création de clés GPG

Pour signer un chart helm une clé GPG est nécessaire.

Il faut que la machine ou le conteneur dispose d'un client gpg.

Le script suivant perment de générer une clé gpg.

``` bash
#!/bin/bash

# Génération de la clé GPG
gpg --batch --generate-key <<EOF
Key-Type: RSA
Key-Length: 4096
Name-Real: 2SA
Name-Email: 2SA@email.com
Expire-Date: 0
%no-protection
%commit
EOF

# Export de la clé privée dans un fichier
gpg --armor --export-secret-keys your@email.com > /root/private.key

# Export de la clé publique dans un fichier
gpg --armor --export your@email.com > /root/public.key
```

Il suffit ensuite de récupérer la private.key et la public.key et les ajouter dans un vault/ pour ne pas les perdre.

C'est la clé privée (private.key au format file) ainsi que le nom de la clé (Name-Real) qu'il faudra ajouter dans les secrets GitLab et ajouter via les inputs du composant : 
 -  `helm_component-gpg-private-key-name`
 -  `helm_component-gpg-private-key`

#### Utilisation de la clé GPG pour signer un chart

Il faut que la machine ou le conteneur dipose d'un client gpg et de helm.
Il est recommandé d'utiliser l'image cdsh qui contient toutes les outils requis.

Il suffit de lancer le script suivant : 

``` bash
# Import la clé privée gpg dans le store du client gpg
gpg --batch --import /root/private.key

# Export des stores dans un format gpg utilsable par helm
gpg --export >~/.gnupg/pubring.gpg
gpg --export-secret-keys >~/.gnupg/secring.gpg

# Signature du chart
helm package --sign --key "2SA" --keyring ~/.gnupg/secring.kbx .
```

#### Verification de la signature d'un chart

Il faut bien avoir la clé publique dans le keyring publique.
Il faut que la machine ou le conteneur dipose d'un client gpg et de helm.
Il est recommandé d'utiliser l'image cdsh qui contient toutes les outils requis.

```bash
# Import la clé publique gpg dans le store du client gpg
gpg --batch --import /root/public.key

# Export des stores dans un format gpg utilsable par helm
gpg --export >~/.gnupg/pubring.gpg

# Verification de la signature du chart
helm verify mon-chart-1.0.0.tgz
```