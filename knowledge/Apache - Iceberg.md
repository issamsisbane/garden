# Apache Iceberg

Question d'un opérateur de l'Etat : Faut-il remettre en cause le concept de bases de données modélisées et prendre le virage de la virtualisation des données et d'Iceberg ?

### **Qu'est-ce que la virtualisation des données ?**

La virtualisation des données est une technologie qui permet de créer une couche d'abstraction entre les applications et les sources de données. Cela signifie que les données restent à leur emplacement source (par exemple, dans un stockage _big data_), mais sont rendues accessibles à travers une couche logique.

  

### **La virtualisation des données est une avancée du modèle des _lakehouses_**

Dans les années 2010s, les entreprises ont migré (ou dupliqué) de gros volumes de données dans des _data lakes_. Cependant, si le _datalake_ permet de centraliser les données, il ne casse en rien les silos entre elles puisqu'elles restent dans des formats fragmentés issus de _pipelines_ différentes.

Le _lakehouse_ (Databricks et Snowflake) a cherché à résoudre ce problème en homogénéisant la gestion des métadonnées et en facilitant les transactions ACID. La virtualisation des données s'est accélérée grâce aux _lakehouses_. Désormais la question peut se poser, pour des SI ne manipulant que des bases de données (i.e. pas ou peu de contenus multimédia), de se tourner vers la virtualisation.

  

### **Qu'est-ce qu'Iceberg ?**

Iceberg est une solution au problème de fragmentation des _datalakes_ ayant fleuri dans les années 2010s, et qui sont des pots-pourris de documents multi-media, dans des formats divers (d'où le pastiche : _dataswamp_). Iceberg a d'ailleurs été créé chez Netflix en 2017, dans un contexte de forte volumétrie + formats multimédia + peu de transformations complexes nécessaires.

Iceberg est un **format de table**, pas un format physique : les données sont toujours techniquement écrites dans des fichiers Parquet. Iceberg oriente l'accès aux fichiers sous-jacents contenant les données. Cela permet par exemple de faire des partitions dynamiques, des transactions ACID (i.e. sans interrompre des pipelines/requêtes en cours), de faire évoluer les _schemas_ et de faire du _time-travel_ (i.e. rejouer des transformations pour voir l'état des données à un moment précis).

**Avantages/inconvénients d'Apache Iceberg**

|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Avantages**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | **Inconvénients**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| - Eviter la duplication des données dans des tables à chaque étape de la transformation  <br>- Gérer des données volumineuses avec des besoins de gestion avancée des métadonnées  <br>- Caractère natif (contrairement à Hive-Parquet) des transformations ACID, évolutions du _schema_, partitions et _time-travel_  <br>- Permet un requêtage universel de différents formats de données : cela est pertinent si l’on possède de nombreuses sources de données, avec des formats de données divers  <br>- Permet de centraliser la gestion des permissions sur les données | - Complexe de gérer des processus très lourds (ex : transformations avancées, calculs complexes) sans une couche persistante intermédiaire pour limiter la charge  <br>- _Debugging_ compliqué sans accès aux transformations intermédiaires  <br>- Réécriture de toute la code base dans le cas d'une migration  <br>- Besoin d'embaucher du personnel ayant de l'expertise dans les équipes, expertise rare également dans les ESN  <br>- Complexité de maintenance de la solution, avec des coûts importants (des solutions managées existent, comme Denodo, mais sont coûteuses également) |

**Conclusion**

Iceberg est un outil qui gagne en popularité, dans un écosystème qui change rapidement.

Un système 100% virtuel, basé sur des technologies comme Apache Iceberg, est théoriquement possible et efficace pour des flux simples ou modérément complexes, où les transformations sont peu nombreuses ou légères. Cependant, pour des transformations avancées ou des besoins spécifiques (audit, _debugging_), conserver une capacité à gérer des étapes intermédiaires sous forme persistante reste essentiel.

Si les données sont principalement transactionnelles et nécessitent des transformations complexes, alors on ne peut pas faire l'impasse sur les bases de données. **Iceberg n'est pas conçu pour remplacer les bases de données classiques, mais pour remplacer certains workloads analytiques.** En pratique, les mondes "transactional/RDMS" et "analytics/lakehouse" restent très distincts.

Le choix de mettre en place de la virtualisation de données avec Iceberg doit être justifié par un bon rapport avantage/coût, Iceberg étant particulièrement complexe et coûteux à mettre en œuvre et à maintenir.  
  
 **Questions à se poser :**

Quelle est la part de données transactionnelles ? Comment se décompose la pipeline ?

Quelle est la probabilité de pouvoir recruter / former des _data engineers_ avec une expertise sur Iceberg ?

Effectuer une analyse coûts-avantages préalable est indispensable : quel est le coût de refaire cette partie du SI décisionnel et d'embaucher des experts pour quelle valeur ajoutée en sortie ?