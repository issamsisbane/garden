
# CMO


[Monitoring stack architecture - Monitoring | Observability | OKD 4.17](https://docs.okd.io/4.17/observability/monitoring/about-ocp-monitoring/monitoring-stack-architecture.html)
[Cluster Monitoring Operator vs User Workload Monitoring](https://www.linkedin.com/pulse/cluster-monitoring-operator-vs-user-workload-dhinesh-kumar-d0xje
[Monitoring stack architecture - Monitoring | Observability | OKD 4.17](https://docs.okd.io/4.17/observability/monitoring/about-ocp-monitoring/monitoring-stack-architecture.html)

![[Pasted image 20250908192452.png]]

These tools operate across two domains:

- **Cluster Monitoring:** Monitors OpenShift’s internal components and infrastructure
- **User Workload Monitoring:** Allows developers to monitor their applications independently

![[Pasted image 20250908192728.png]]

# COO

[Brief overview of Cluster Observability Operator | Red Hat Developer](https://developers.redhat.com/articles/2024/12/13/brief-overview-cluster-observability-operator?ref=dailydev)

![[Pasted image 20250908192431.png]]

![[Pasted image 20250908192423.png]]

# COO vs CMO

|                                |                                                                                                                                                                  |                                                                                                                                                           |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Aspect**                     | **OpenShift default monitoring stack**                                                                                                                           | **Cluster Observability Operator (COO)**                                                                                                                  |
| **Scope**                      | Limited to core components within the cluster (e.g., API server, ETCD) and OpenShift-specific namespaces. Provides basic monitoring suitable for standard needs. | Offers comprehensive monitoring and analytics for enterprise-level needs, covering cluster and workload performance.                                      |
| **Functional Goals**           | Focuses on infrastructure health, using Prometheus and Alertmanager for basic monitoring and alerting.                                                           | Provides in-depth insights, focusing on granular performance and trend analysis. Supports historical analysis and capacity forecasting.                   |
| **Configuration Management**   | Built-in configurations offer limited customization. Users can set alerting and notification methods but lack options to adjust storage or retention policies.   | Broader configuration options, including data retention periods, storage methods, and collected data types. High customization and extensibility via COO. |
| **Data Retention and Storage** | Shorter data retention times, designed for short-term monitoring and real-time detection.                                                                        | Supports long-term data retention, enabling historical data analysis and capacity planning.                                                               |
| **Use Cases**                  | Suitable for basic needs, like tracking cluster component status and application health checks.                                                                  | Ideal for advanced monitoring scenarios, such as trend forecasting and anomaly detection, suited for larger enterprises.                                  |
| **Integration**                | Much more integrated into OpenShift Container Platform. For instance, WebConsole dashboard and alert management.                                                 | Lacks direct integration with OpenShift Container Platform and typically requires an external Grafana instance for dashboards.                            |
- **Operations teams in multi-tenant environments**: With multi-tenancy support, COO allows different teams to configure monitoring views for their projects and applications, making it suitable for teams with flexible monitoring needs.
- **Development and operations teams**: Teams that need fine-grained monitoring and customizable observability views for in-depth troubleshooting, anomaly detection, and performance tuning during development and operations.

# Thanos 

Thanos est une solution open source qui **complète Prometheus** en résolvant plusieurs de ses limitations natives, notamment en matière de **scalabilité**, de **rétention longue durée des données** et de **requêtage global** sur plusieurs instances Prometheus

|Composant|Rôle|
|---|---|
|Thanos Sidecar|Upload les données de Prometheus vers le stockage objet.|
|Thanos Store|Lit les données depuis le stockage objet.|
|Thanos Querier|Aggrège les requêtes vers plusieurs Prometheus/Sidecar/Store.|
|Thanos Compactor|Applique le downsampling et la compaction des données.|
|Thanos Ruler|Évalue les règles d’alerte et les enregistre dans le stockage.|