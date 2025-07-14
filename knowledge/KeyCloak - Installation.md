## Mode Developpement
[OpenJDK - Keycloak](https://www.keycloak.org/getting-started/getting-started-zip)

Cette installation correpond à un environnement de developpement.

Les étapes sont simple : 
1. Installer OpenJDK 21
2. Télécharger et extraire KeyCloak
3. Créer un utilisateur pour KeyCloak
4. Définir les permissions pour l'utilisateur KeyCloak
5. Créer un fichier de service systemd pour KeyCloak
6. Démarrer et activer le service KeyCloak

## Mode Production
[Configuring Keycloak for production - Keycloak](https://www.keycloak.org/server/configuration-production)
On fait les mêmes étapes que ci-dessus cependant, il y a plusieurs choses a prendre en compte pour setup un environnement de production.

#### 1. Utiliser une base de données
[Configuring the database - Keycloak](https://www.keycloak.org/server/db)

Plutôt que d'utiliser la base de données InMemory par défaut de KeyCloak, il faut utiliser une base de données comme : 
![[Pasted image 20241022151112.png]]

Bien faire attention de donner les droits a l'utilisateur pour editer le schéma public.

#### 2. Configurer SSL
[Configuring TLS - Keycloak](https://www.keycloak.org/server/enabletls)

Il faut ajouter un hostname et le certificat ainsi que la clé associé.

#### 3. Configure Outgoing HTTP Requests
[Configuring outgoing HTTP requests - Keycloak](https://www.keycloak.org/server/outgoinghttp)

Keycloak fait des requêtes aux services qu'ils gèrent, on peut configurer ces requêtes notamment en ajoutant un truststore avec les certifcats associés.

#### 4. Configuer le Hostname
[Configuring the hostname (v2) - Keycloak](https://www.keycloak.org/server/hostname)
