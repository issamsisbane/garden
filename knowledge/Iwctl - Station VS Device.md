# Station vs Device

Dans le contexte de `iwctl`, les termes `station` et `device` ont des significations spécifiques et sont utilisés pour des fonctions différentes :

### Device (Périphérique)

- **Définition** : Un `device` (périphérique) fait référence à l'interface matérielle sans fil elle-même, comme une carte Wi-Fi.
- **Utilisation** : Lorsque vous utilisez la commande `device list`, vous obtenez une liste des interfaces sans fil disponibles sur votre système.
- **Exemple** :
    

`device list`

Cela pourrait retourner quelque chose comme :

- `Name        Type      Powered   Adapter   Address ------------------------------------------------ wlan0       wifi      on        phy0      00:11:22:33:44:55`
    
    Ici, `wlan0` est le nom du périphérique sans fil.

### Station

- **Définition** : Une `station` fait référence à une instance logicielle qui gère la connexion d'un périphérique sans fil à un réseau. Elle est associée à un périphérique spécifique.
- **Utilisation** : Les commandes `station` sont utilisées pour effectuer des opérations spécifiques à la connexion réseau, comme scanner les réseaux disponibles, se connecter à un réseau, etc.
- **Exemple** :
    

- `station wlan0 scan station wlan0 get-networks station wlan0 connect MonReseau`
    
    Ici, `wlan0` est le nom du périphérique sans fil, et `station wlan0` est utilisé pour effectuer des opérations de connexion sur ce périphérique.

### Différence Clé

- **Device** : Représente le matériel physique (la carte Wi-Fi).
- **Station** : Représente l'instance logicielle qui gère la connexion réseau pour un périphérique spécifique.

En résumé, `device` est utilisé pour identifier et lister les interfaces matérielles sans fil, tandis que `station` est utilisé pour gérer les connexions réseau sur ces interfaces.