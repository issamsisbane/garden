Apache mellon est un module pour le serveur apache qui implémente le protocole SAML 2.0, permettant à apache de jouer le rôle de Service Provider (SP). 

Il externalise la gestion de l'authentification vers un Identity Provider (IdP) externe utile pour le SSO.

# Fonctionnement

1. Redirection vers l'IdP: Lorsqu'un utilisateur tente d'accèder à une ressource protégée. Mellon redirige la requête vers l'IdP
2. Authentification par l'IdP: L'utilisteur s'autentifie auprès de l'IdP, qui génére alors une assertion SAML contenant les informations d'autentification.
3. Retour vers le SP: L'assertion est renvoyée à Mellon. Mellon la valide (verification signature et certificats) et accord l'accès à la ressource.

Le Service Provider et l'Identity Provider doivent échanger des métadonnées pour se faire confiance mutuellement. Ces métadonnées contiennent entre autres les URL des endpoints et certificats utilisés.

# Configuration

Certains fichiers sont nécessaires pour faire configurer apache mellon

## IDP Metadata

Le fichier idp-metadata.xml renseigne toutes les métadonnées décrivant l'IdP : 
- Endpoints (SSO / SLO)
- Certificat Public (pour signature)

```
MellonIdPMetadataFile /chemin/vers/idp-metadata.xml
```

## SP Metadata

Le fichier sp-metadata.xml renseigne toutes les métadonnées décrivant le SP :
- Endpoints
- Certificat Public

```
MellonSPMetadataFile /chemin/vers/sp-metadata.xml
```

# Certs

```
MellonCertificateFile /chemin/vers/certificat.crt
MellonCertificateKey /chemin/vers/cle.key
```