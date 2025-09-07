Pour mettre à jour des volumes de vms sur outscale il a deux méthodes : 
1. Supprimer et recréer les machines avec une snapshot et terraform
	* Cela prends du temps et peut poser problème (interruption de service)
2. Update le volume via l'api d'Outscale

J'ai decidé d'utiliser l'api de outscale car ça posait moins de problème. 

# BASH

> [!ATTENTION] Utilisation du bash
> Il est plus simple d'utiliser l'api que de se battre avec la cli osc
> J'ai créer un script pour faire ça plus facilement

## 1 - On arrête la machine

## 2 - On load l'envrionnement

```
load oniam
```

##  3 - On lance le script

Le script se situe : `~/SCRIPTS/outscale/api`
On modifie le script avec les variables demandé et on le lance. 

# Installation du command line d'outscale
[Installing and Configuring OSC CLI – OUTSCALE Public Documentation](https://docs.outscale.com/en/userguide/Installing-and-Configuring-OSC-CLI.html)

# Vérification du bon fonctionnement de l'API
``` sh
osc-cli api ReadVolumes --profile "default"
```

# Update du volume
[Augmenter la taille d’un volume – Documentation publique OUTSCALE](https://docs.outscale.com/fr/userguide/Augmenter-la-taille-d-un-volume.html#_Instance_Windows)

### 1. Arreter la VM

On arrete la vm via cockpit et on attends qu'elle s'arrete.

### 2. Lancer le script

On lance ce code  :

``` sh
osc-cli api UpdateVolume --profile "default" \
  --VolumeId "vol-12345678" \
  --Size 200
```

### 3. Relancer la VM

On relance la VM via Cockpit.

### 4. Configurer l'utilisation du volume 
On accède à la vm via RDP et on accède à diskmgmt.msc depuis le menu démarrer. On doubleclick sur notre volume puis etendre volume et on suit les étapes jusqu'a la fin. 
Notre volume est bien configuré !


