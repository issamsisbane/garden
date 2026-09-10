---
creation date: 2026-03-25-22:46:16
modification date: 2026-03-25-22:46:16
imageNameKey: New_Homelab_Setup_-_Prises_connectés
---
## Besoin Initial

Utiliser des prises connectées **NOUS Zigbee** pour suivre la consommation électrique de 3 machines constituant un cluster Kubernetes homelab :
- 2 laptops
- 1 Raspberry Pi
 
L'antenne Zigbee (Sonoff Zigbee 3.0 USB Dongle Plus V2) est branchée en USB sur le Raspberry Pi.

## Architecture

![[zigbee_k8s_architecture.svg]]
Tous les composants tournent dans le namespace `domotic`.

## Tests

### Tests avec deployment

J'ai remarqué juste après avoir fait le déploiement de mon côté qu'il y avait un chart.
Je pensais que le chart n'était pas officiel mais en fait si c'est le meme nom que l'image.

Après c'est un ingress, un service, un deployment, un configmap et un pvc. C'est pas tant nécessaire d'avoir un chart pour ça.
#### Faire rejoindre une prise

On active depuis le frontend `permit join`.
Il faut cliquer quelques secondes sur le boutton jusqu'à ce qu'il clignote.
Une fois fait, on va voir notre prise directement s'afficher et se connecter.
#### Fixer le nom de la device

![[New_Homelab_Setup_-_Prises_connectes-1.png]]

## Problèmes rencontrés et résolutions
 
### 1. Mauvais stack adapter (zstack vs ember)
 
**Problème** : Zigbee2MQTT configuré avec le stack `zstack` échouait avec `SRSP - SYS - ping after 6000ms`. Le dongle ne répondait pas.
 
**Cause** : Le Sonoff Dongle Plus V2 utilise un chip **EFR32MG21** avec firmware **EmberZNet**, pas un chip Texas Instruments CC2652. Il faut donc le stack `ember` et non `zstack`.
 
**Résolution** : Passer l'adapter sur `ember` dans la configuration Zigbee2MQTT.
 
---
 
### 2. ModemManager bloquait le port série
 
**Problème** : Même avec le bon stack, le port `/dev/ttyUSB0` ne répondait pas.
 
**Cause** : `ModemManager` est un service Linux qui tente d'identifier tous les ports série au démarrage (pour détecter des modems 4G). Il bloquait `/dev/ttyUSB0` pendant 15-20 secondes, interférant avec Zigbee2MQTT.
 
**Résolution** :
```bash
sudo systemctl stop ModemManager
sudo systemctl disable ModemManager
```
Sans impact car le Pi n'utilise pas de modem mobile.
 
---
 
### 3. ConfigMap en lecture seule
 
**Problème** : En montant le ConfigMap directement sur `/data/configuration.yaml`, Zigbee2MQTT échouait au démarrage avec `EROFS: read-only file system` car il tente d'écrire des fichiers de migration dans `/data`.
 
**Cause** : Les volumes ConfigMap sont montés en lecture seule dans Kubernetes.
 
**Résolution** : Utiliser un **initContainer** qui copie le ConfigMap vers un `emptyDir` accessible en écriture avant le démarrage du container principal :
 
```yaml
initContainers:
  - name: copy-config
    image: busybox
    command:
      - sh
      - -c
      - cp /config-ro/configuration.yaml /data/configuration.yaml
    volumeMounts:
      - name: config
        mountPath: /config-ro
      - name: data
        mountPath: /data
```
 
Le ConfigMap reste la source de vérité, et Zigbee2MQTT peut écrire ses fichiers internes (`devices.yaml`, `coordinator_backup.json`, logs de migration) dans l'`emptyDir`.
 
---
 
### 4. Permissions sur le device USB
 
**Problème** : Le pod ne pouvait pas ouvrir `/dev/ttyUSB0` sans `privileged: true`.
 
**Cause** : Le device appartient au groupe `dialout` (GID 20) sur le Pi. Le pod n'avait pas ce groupe dans son contexte de sécurité.
 
**Résolution** : Ajouter `supplementalGroups: [20]` au `securityContext` du pod et supprimer `privileged: true` :
 
```yaml
spec:
  securityContext:
    supplementalGroups: [20]
  containers:
    - securityContext:
        allowPrivilegeEscalation: false
        capabilities:
          drop: ["ALL"]
          add: ["SETUID", "SETGID"]
```
 
---
 
### 5. Mauvaise adresse MQTT
 
**Problème** : `MQTT failed to connect mqtt://localhost:1883`
 
**Cause** : La config pointait vers `localhost` au lieu du service Kubernetes `mosquitto`.
 
**Résolution** : Utiliser le nom du service Kubernetes dans la config MQTT :
```yaml
mqtt:
  server: mqtt://mosquitto:1883
```
 
---
 
### 6. Namespace différent entre les pods
 
**Problème** : Zigbee2MQTT cherchait `moquitto.domotic.svc.cluster.local` (mauvais namespace et faute de frappe).
 
**Cause** : Mosquitto avait été déployé dans un namespace différent, et une faute de frappe s'était glissée dans le nom du service.
 
**Résolution** : Déployer tous les composants dans le même namespace `homelab-monitoring`. Les services du même namespace se trouvent par leur nom court sans FQDN.
 
---
 
## Points de configuration clés
 
| Paramètre | Valeur |
|---|---|
| Adapter type | `ember` |
| Port série | `/dev/ttyUSB0` |
| Baudrate | `115200` |
| rtscts | `false` |
| Node K8s | `ih-node-3` (le Raspberry Pi) |
| Namespace | `homelab-monitoring` |
| MQTT server | `mqtt://mosquitto:1883` |
 
---
 
## Ce qu'il reste à faire
 
- [ ] Appairer les 3 prises NOUS et leur assigner des `friendly_name` dans le ConfigMap
- [ ] Déployer `mqtt2prometheus`, Prometheus et Grafana
- [ ] Configurer les alertes Prometheus (seuil de consommation, prise hors ligne)