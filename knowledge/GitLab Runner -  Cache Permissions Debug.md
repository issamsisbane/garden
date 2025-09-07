# Contexte

En utilisant des runners gitlab sur openshift avec des PVC pour le cache il y avait des erreurs d'ecriture et de lecture lorsque l'on voulait ecrire dans le cache.
# Solution

Il faut deja verifier la SCC pour qu'elle autorise bien l'ajout de fsgroup.

Ensuite, Il faut ajouter un fsgroup dans la config du gitlab : 

``` yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: cpj-runner-config
data:
  config.toml: |
    concurrent = 200
    log_level = "debug"
    log_format = "json"
    shutdown_timeout = 0
    [session_server]
      session_timeout = 10800
    [[runners]] 
      name = "cpj"
      url = "https://ulj-git-dc1-001.forge.tbot.dc.justice.gouv.fr"
      executor = "kubernetes"
      cache_dir = "/cache" 
      environment = ["NO_PROXY=.justice.gouv.fr", "HTTP_PROXY=http://proxy.dc.justice.gouv.fr:8080", "HTTPS_PROXY=http://proxy.dc.justice.gouv.fr:8080"]
      [runners.cache]
        Shared = false
      [runners.kubernetes]
        privileged = false
        namespace = "ulj-cpj"
        pull_policy = "if-not-present"
      # quelques limites pour encadrer l'utilisation des ressources par les conteneurs du runner
      # build
        cpu_limit = "2"
        memory_limit = "6Gi"
      # service
        service_cpu_limit = "1"
        service_memory_limit = "1Gi"
      # helper
        helper_cpu_limit = "1"
        helper_memory_limit = "1Gi"
        [runners.kubernetes.pod_security_context]
          fs_group = 1000
          
      # un pvc pour gérer le cache
        [[runners.kubernetes.volumes.pvc]]
          name = "cpj-runner"
          mount_path = "/cache"
          mount_propagation = "HostToContainer"
 
        # un secret contenant l'autorité de certification de la plateforme afin que les pods helpers
        #des runners puissent se connecter en https aux API des autres outils d'ULJ : Nexus, SonarQube, Vault etc..
        [[runners.kubernetes.volumes.secret]]
          name = "cpj-runner-ca"
          mount_path = "/etc/gitlab-runner/certs/"
          read_only = true
      [runners.kubernetes.build_container_security_context]
      [runners.kubernetes.build_container_security_context.capabilities]
        add = ["SETFCAP"]
```

# Solution Provisoire

Finalement la solution est d'ajouter dans les pipelines, un before_script au premier job qui fait : 

```
chmod 777 /cache
```

Cette commande n'est à lancer qu'a la création d'un nouveau pvc. Après les permissions sont bien set et plus besoin d'y toucher.

Mais pour être sûr on va garder la ligne. Il faudra trouver une solution plus élégante par la suite. 

On a essayer d'ajouter la commande au prescript dans le config file du runner mais ça ne marche pas.

## Erreurs
### Erreur avec Podman

![[2025-01-13 10_12_21-Centre de notifications.png]]

### Erreur cache
![[2025-01-13 10_11_58-Centre de notifications.png]]

## Lancement des commandes

On utilise les manifest définis dans le repo git suivant pour le déploiement du runner : 
[2sa / ulj / Gitlab Runner · GitLab](https://code.dea.intranet.justice.gouv.fr/2sa/ulj/gitlab-runner/-/tree/dc1/ocp-4.14/)

On va clone le repo et on peut utiliser oc pour intéragir avec le Cluster OpenShift d'ici.

![[2025-01-16 12_06_58-Centre de notifications.png]]

## Debug Kevin, Jerome & Romain 16/01/2024

Ce que l'on a fait : 
* Modifier le chemin du /cache vers /home/gitlab-runner
* Modifier le chemin du /cache vers /var/tmp
* Modifier SCC
* Supprimer SCC
* Utiliser Kaniko au lieu de podman (besoin d'accès route)
* Utiliser buildah au lieu de podman (pas besoin d'accès root)

## Capture d'écran Debug
![[2025-01-16 10_34_53-Centre de notifications.png]]

![[2025-01-16 11_03_39-Démarrer.png]]

![[2025-01-16 11_03_48-Démarrer.png]]

![[2025-01-16 11_04_03-Démarrer.png]]

![[2025-01-16 11_04_25-Démarrer.png]]

![[2025-01-16 11_06_39-Démarrer.png]]

![[2025-01-16 11_08_10-Démarrer.png]]

![[2025-01-16 11_12_23-Démarrer.png]]

![[2025-01-16 11_27_18-Centre de notifications.png]]

![[2025-01-16 11_30_00-Centre de notifications.png]]