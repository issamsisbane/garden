
# Why Partitionning

Partitionner un disque dur offre plusieurs avantages par rapport à l'utilisation d'un seul espace de stockage non partitionné. Voici quelques raisons pour lesquelles le partitionnement est utile :

1. **Organisation** :
    
    - **Séparation des données** : Différents types de fichiers peuvent être stockés dans différentes partitions. Par exemple, vous pouvez avoir une partition pour le système d'exploitation, une autre pour les documents personnels, et une autre pour les applications.
    - **Gestion simplifiée** : Cela facilite la gestion et la sauvegarde des données, car vous pouvez cibler des partitions spécifiques.
2. **Performance** :
    
    - **Optimisation des accès disque** : En séparant les fichiers fréquemment utilisés de ceux qui le sont moins, vous pouvez réduire la fragmentation et améliorer les performances.
    - **Utilisation de différents systèmes de fichiers** : Différentes partitions peuvent utiliser différents systèmes de fichiers optimisés pour des types spécifiques de données ou d'usages.
3. **Sécurité et stabilité** :
    
    - **Isolement des problèmes** : Si une partition est corrompue ou infectée par un virus, les autres partitions peuvent rester intactes.
    - **Protection des données** : Vous pouvez chiffrer des partitions spécifiques pour protéger les données sensibles.
4. **Installation de plusieurs systèmes d'exploitation** :
    
    - **Dual-boot** : Le partitionnement permet d'installer plusieurs systèmes d'exploitation sur le même disque dur, chacun ayant sa propre partition.
5. **Gestion de l'espace disque** :
    
    - **Allocation flexible** : Vous pouvez allouer de l'espace disque en fonction de vos besoins spécifiques, ce qui peut aider à éviter les problèmes de manque d'espace sur une partition critique.
    - **Quotas de disque** : Vous pouvez définir des limites d'espace pour différentes partitions, ce qui est utile dans les environnements multi-utilisateurs.
6. **Sauvegarde et récupération** :
    
    - **Sauvegardes ciblées** : Il est plus facile de sauvegarder et de restaurer des partitions spécifiques plutôt que l'ensemble du disque.
    - **Récupération de données** : En cas de problème, la récupération de données peut être plus simple et plus rapide si les données sont organisées en partitions.

# Ways of Partitionning

Il existe deux façon de partitionner : 
## Méthode Traditionnelle de Partitionnement

1. **Partitionnement** :
    
    - Un disque dur est divisé en partitions, chacune étant une section distincte du disque.
    - Chaque partition est formatée avec un système de fichiers (comme ext4, XFS, etc.).
    - Les partitions sont montées à des points spécifiques dans l'arborescence des fichiers (par exemple, `/`, `/home`, `/var`, etc.).
2. **Outils Utilisés** :
    
    - `fdisk` ou `gdisk` : pour créer et manipuler les partitions.
    - `mkfs` : pour formater les partitions avec un système de fichiers.
    - `mount` : pour monter les partitions.
3. **Avantages** :
    
    - Simplicité et facilité de mise en place.
    - Bonne performance car directement lié au matériel.
4. **Inconvénients** :
    
    - Manque de flexibilité : redimensionner les partitions peut être difficile et risqué.
    - Espace disque sous-utilisé : si une partition est pleine et une autre a de l'espace libre, il n'est pas facile de réallouer l'espace.

## Méthode avec LVM (Logical Volume Manager)

1. **Concepts de Base** :
    
    - **Volume Physique (PV)** : Un disque physique ou une partition est initialisé comme un volume physique.
    - **Groupe de Volumes (VG)** : Plusieurs volumes physiques sont combinés pour former un groupe de volumes.
    - **Volume Logique (LV)** : Un groupe de volumes est divisé en volumes logiques, qui peuvent être formatés et montés comme des partitions traditionnelles.
2. **Processus** :
    
    - Initialiser les disques ou partitions comme volumes physiques avec `pvcreate`.
    - Créer un groupe de volumes avec `vgcreate`.
    - Créer des volumes logiques dans le groupe de volumes avec `lvcreate`.
    - Formater les volumes logiques avec un système de fichiers et les monter.
3. **Avantages** :
    
    - Flexibilité : les volumes logiques peuvent être redimensionnés dynamiquement.
    - Gestion simplifiée de l'espace disque : possibilité d'ajouter de nouveaux disques à un groupe de volumes existant.
    - Instantanés : possibilité de créer des instantanés pour la sauvegarde et le test.
4. **Inconvénients** :
    
    - Complexité accrue par rapport au partitionnement traditionnel.
    - Légère surcharge due à la couche d'abstraction supplémentaire.

## Comparaison

- **Flexibilité** : LVM offre une bien meilleure flexibilité pour la gestion de l'espace disque.
- **Performance** : Le partitionnement traditionnel peut offrir de meilleures performances car il est plus direct.
- **Complexité** : LVM est plus complexe à configurer et à gérer, mais offre des fonctionnalités avancées.

En résumé, si vous avez besoin d'une configuration simple et directe, le partitionnement traditionnel peut suffire. Cependant, pour des environnements où la flexibilité et la gestion dynamique de l'espace disque sont cruciales, LVM est souvent la meilleure option.