On veut que notre container [[Podman - Commands]] nexus se relance au démarrage de notre machine.

Pour ça il y avait cette documentation : [Running Podman Pods and Containers on Boot – Qubits & Bytes](https://qubitsandbytes.co.uk/containers/running-podman-pods-and-containers-on-boot/)

Mais on utilise la commande suivante qui est deprecated : 

```
podman generate systemd
```

Ainsi dorénavant, c'est fait différement comme le montre les deux documentations suivantes : 
- [podman-systemd.unit — Podman documentation](https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html)
- [Make systemd better for Podman with Quadlet](https://www.redhat.com/en/blog/quadlet-podman)

On va utiliser quadlet qui a partir d'un fichier de configuration va nous générer un fichier service pour systemd. Ce service va lancer notre conteneur avec tous les paramètres nécessaires.

On va lancer toutes ces commandes en tant qu'utilisateur non-root et rootless.
## 1 - Activation du démarrage automatique

Il faut lancer cette commande pour activer le linger pour que les services puissent démarrer sans forcément de session utilisateur active.

``` bash
loginctl enable-linger $(whoami)
```
## 2 - Création du fichier nexus.container

On doit créer le fichier suivant : `$HOME/.config/containers/systemd/nexus.container`.
A l'intérieur, il faut ajouter la configuration de notre container : 

``` bash
[Unit]
Description=The Nexus Container
After=network.target

[Container]
Image=localhost/sonatype/nexus3:3.76.1
PublishPort=80:8081
PublishPort=5000-5010:5000-5010
Volume=/opt/sonatype/nexus:/nexus-data
Volume=/opt/sonatype/nexus/log:/nexus-data/log
Pull=never
PodmanArgs=--cgroups=enabled --log-driver=journald # nécessaire sinon au redemarrage on a des erreurs

[Service]
Restart=always
RestartSec=10s
TimeoutStartSec=900

[Install]
WantedBy=multi-user.target default.target
```

## 3 - Activation du service

```
systemctl --user daemon-reload
systemctl --user status nexus # Verifier que le service existe bien
systemctl --user enable nexus
systemctl --user start nexus
```

Quand on fait un `daemon-reload` ça va trigger `/usr/lib/systemd/system-generators/podman-system-generator` qui va convertir notre fichier .container en .service pour systemd.
Ensuite il suffit de lancer le service pour que tout fonctionne et que le container se crée.