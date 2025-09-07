Voici quelques commandes de base pour utiliser `iwctl` :

1. **Lancer iwctl** :
    

- `iwctl`
    
- **Lister les périphériques sans fil disponibles** :
    
- `device list`
    
- **Scanner les réseaux sans fil disponibles** :
    
- `station <device> scan station <device> get-networks`
    
    Remplacez `<device>` par le nom de votre périphérique sans fil.
    
- **Se connecter à un réseau sans fil** :
    
- `station <device> connect <SSID>`
    
    Remplacez `<device>` par le nom de votre périphérique sans fil et `<SSID>` par le nom du réseau sans fil auquel vous souhaitez vous connecter.
    
- **Quitter iwctl** :
    

1. `quit`
    