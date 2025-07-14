Use to gather and store timebased metrics.

Prometheus est une technologie open-source designé pour fournir monitoring et alerting pour des environnements cloud native.

### Qu'est-ce que Prometheus ?

**Prometheus** est un outil open-source de surveillance et d'alerte pour les systèmes distribués, initialement développé par SoundCloud en 2012. Il est maintenant un projet sous l'égide de la Cloud Native Computing Foundation (CNCF). Prometheus est principalement utilisé pour collecter, stocker et interroger des métriques de performance des systèmes et applications. Il est particulièrement populaire dans les environnements de cloud natif et d'orchestration de conteneurs, comme Kubernetes.

### Comment fonctionne Prometheus ?

Prometheus est basé sur un modèle "pull", c'est-à-dire qu'il interroge activement (scrape) des points d'extrémité exposant des métriques. Ces points d'extrémité sont généralement des services ou des applications qui fournissent des données sous forme d'API HTTP exposant les métriques dans un format spécifique (généralement au format texte).

Voici un aperçu de son fonctionnement :

1. **Scraping des métriques** :
   - Prometheus interroge périodiquement des points d'extrémité HTTP des applications ou des services qui exposent des métriques.
   - Ces métriques peuvent être des informations sur les performances du CPU, la mémoire, les requêtes HTTP, ou d'autres données spécifiques à l'application.
   - Les cibles peuvent être configurées statiquement ou découvertes dynamiquement à l'aide de mécanismes comme Kubernetes, Consul, etc.

2. **Stockage des données** :
   - Les métriques collectées sont stockées dans une base de données de séries temporelles interne (TSDB - Time Series Database). Cette base de données est optimisée pour la gestion de grandes quantités de données de métriques horodatées.

3. **Langage de requête (PromQL)** :
   - Prometheus fournit un langage de requête puissant appelé **PromQL** (Prometheus Query Language), permettant de faire des requêtes complexes pour analyser les métriques stockées.
   - PromQL permet, par exemple, de calculer des taux d'erreurs, des moyennes, des percentiles ou de comparer des séries de temps sur des périodes données.

4. **Alertes** :
   - Prometheus inclut un module d'alerte, **Alertmanager**, qui permet de définir des règles d'alerte basées sur les données collectées. Par exemple, vous pouvez définir une alerte si l'utilisation du CPU dépasse 80 % pendant plus de 5 minutes.
   - Alertmanager gère l'envoi d'alertes à divers canaux de notification, comme des e-mails, Slack, ou des systèmes d'incidents.

5. **Visualisation** :
   - Prometheus peut être utilisé avec des outils de visualisation comme **Grafana** pour créer des tableaux de bord interactifs et visualiser les métriques en temps réel.
   - Les métriques peuvent également être visualisées directement à l'aide de son interface utilisateur intégrée.

### Composants clés de Prometheus

- **Prometheus Server** : L'élément central qui collecte les métriques, les stocke et les rend disponibles pour interrogation.
- **Exporters** : Les applications ou services n'exposent pas toujours des métriques de manière native. Les "exporters" sont des petits programmes qui collectent des métriques à partir d'un service spécifique (comme une base de données) et les exposent au format attendu par Prometheus.
- **Alertmanager** : Gestionnaire d'alertes pour la définition et l'envoi d'alertes.
- **Pushgateway** : Utilisé dans certains cas où des applications ne peuvent pas être interrogées (push), elles envoient alors directement leurs métriques à Prometheus.

### Exemple de flux de travail de Prometheus

1. Une application expose un point d'extrémité `/metrics`, qui fournit des données sur l'utilisation du CPU, de la mémoire, etc.
2. Prometheus interroge régulièrement cet endpoint (scrape) et stocke les résultats dans sa base de données.
3. Vous pouvez écrire des requêtes PromQL pour analyser les performances de l'application sur une période donnée.
4. Si certaines conditions sont remplies (par exemple, la charge CPU dépasse un seuil), une alerte est envoyée via Alertmanager.

### Points forts de Prometheus
- **Indépendance** : Prometheus ne dépend pas de systèmes distribués externes comme Hadoop, ce qui le rend léger et facile à déployer.
- **Scalabilité** : Il est conçu pour être distribué et fonctionne bien dans les grands environnements de cloud natif.
- **Séries temporelles** : Il est spécifiquement optimisé pour les données de séries temporelles, ce qui le rend très performant pour ce type de données.

### Cas d'utilisation courants
- Surveillance des microservices.
- Collecte de métriques pour les applications dans des environnements Kubernetes.
- Surveillance de l'infrastructure cloud.
- Alertes basées sur des seuils définis.

Prometheus est donc un outil essentiel dans la surveillance des systèmes modernes, particulièrement dans les environnements à grande échelle où l'observation et les alertes proactives sont cruciales pour assurer la disponibilité des services.