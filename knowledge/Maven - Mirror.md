---
foam_template:
  filepath: "0 - INBOX/Maven - Mirror.md"
  description: "New note"
created: "2026-01-19"
---

# Maven - Mirror


Dans le fichier `settings.xml`, on peut configurer un mirror.

En configurant un mirror, on demande à maven de passer par ce mirror pour dl les dépendances.

Il faut faire attention cependant à la configuration.

https://maven.apache.org/guides/mini/guide-mirror-settings.html

Si on met ça : 

```xml
<mirrors>
    <mirror>
        <!--This sends everything else to /public -->
        <id>nexus</id>
        <mirrorOf>*</mirrorOf>
        <url>https://${env.MAVEN_GLOBAL_REGISTRY_SERVER_FQDN}/repository/group-maven-public/</url>
    </mirror>
</mirrors>
```

Toutes les dépendances seront télécharger depuis Nexus.

On peut avoir des repository particulier que l'on veut utiliser.
Dans ce cas il faut ajouter le repository en dessous dans `<repositories>` et jouer avec le **mirrorOf** selon ce que l'on veut pour ignorer le mirror pour des dépots en particulier.


```xml
<mirrors>
        <mirror>
            <!--This sends everything else to /public -->
            <id>nexus</id>
            <mirrorOf>*,!jst-maven-release</mirrorOf>
            <url>https://${env.MAVEN_GLOBAL_REGISTRY_SERVER_FQDN}/repository/group-maven-public/</url>
        </mirror>
    </mirrors>
```

