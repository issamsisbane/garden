## Grafana

Grafana était super long au démarrage, j'avais ça dans les logs : 
```
Error checking server process execution privilege. error: could not get current OS user to detect pr │
│ ocess privileges                                                                                     │
│ logger=migrator t=2026-08-12T19:34:18.418628243Z level=warn msg="Skipping migration: Already execute │
│ d, but not recorded in migration log" id="drop unique orgID index on alert_configuration if exists"  │
│ logger=migrator t=2026-08-12T19:34:29.676022415Z level=warn msg="Skipping migration: Already execute │
│ d, but not recorded in migration log" id="drop index UQE_dashboard_public_config_uid - v1"           │
│ logger=migrator t=2026-08-12T19:34:29.776225531Z level=warn msg="Skipping migration: Already execute │
│ d, but not recorded in migration log" id="drop index IDX_dashboard_public_config_org_id_dashboard_ui │
│ d - v1"
```

C'était les migrations qui étaient trop longues. Mais j'utilisais la bdd sqlite par défaut d'où le problème et la lenteur car j'ai des hdd pas opti.

Ducoup j'ai switcher sur une base postgres et ça va beacoup mieux. On est passé de 3 min au lancement du pod à 20 secondes.
## Else
**cAdvisor** → déjà présent via kubelet  
✅ **Node Exporter** → ~~peut être remplacé par **Alloy**~~ 
Kube-state-metrics → ~~peut être remplacé par **Alloy**~~ 
✅ **Promtail** → peut être remplacé par **Alloy**  
✅ **Prometheus + Loki + Grafana** → restent les backends centraux

- **Grafana** → visualisation
- **Prometheus** → collecte & stockage de métriques
- **Loki** → collecte & stockage des logs
- **Alloy** → agent unifié d’observabilité de Grafana Labs



alloy-metrics : definit les composants qui va recup les metrics
cluster-metrics : definit comment, quels metrics sont recuperer et où elles sont envoyée

Si on definit les destinations globalement dans le chart elles sont automatiquement attribués au différents types de valeurs : logs, metrics ou events

https://github.com/grafana/k8s-monitoring-helm/blob/main/charts/k8s-monitoring/docs/destinations/README.md

J'ai eu une erreur avec la derniere version du chart loki, je ne pouvais pas utiliser le stockage minio, il ya une erreur dans le chart qui renvoi une erreur disant qu'il manque des variables pour definir les buckets s3. Je suis passé à une version anterieur en attendant que ce soit reglé.

J'avais une erreur avec mon chart alloy car j'essayais de deployer avec les values du nouveau chart k8s-monitoring mais avec le chart alloy.... normal que ça ne fonctionnait pas

j'essaie d'ecrire dans loki mais il faut utiliser le service gateway et pas le write directement. Le gateway sert de point d'entrée pour tout.

J'essaie d'ecrire dans prometheus mais ça ne marche aps car pas possible d'ecrire dans prom il peut juste ecrire lui meme.

Mauvaise idée d'utilsier que alloy et  prometheus en mode push. Ce n'est pas recommandé.

Pour loki si on veut utiliser SimpleScalable avec 1 replicas de chaque il faut ajouter :
```
loki:
  commonConfig:
    replication_factor: 1
```
Sinon il faut au moins 3 backend ou on aura une erreur : 
failed to call resources:  too many unhealthy instances in the ring