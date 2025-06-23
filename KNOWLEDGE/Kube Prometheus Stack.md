This a stack of monitoring for [[Kubernetes]] Cluster.

It uses [[Prometheus]] to gathers metrics and [[Grafana]] to display it.

It responsible for gathering [[Metrics]] and visualize them.

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

It's compose of :
- [[Prometheus]] : Gather and store time-based metrics
- [[Alert manager]] : Allow to send alerts based on metrics threshold
- [[Grafana]] : Allow to visualize metrics using dashboard
- Prom [[Operator]] : Simplify the deployment and configuration of Prometheus
- Kube state metrics : Listen the kube api server and generate metrics about the state of object and exposes them to prometheus. 
- Node Exporter : Collect metrics about the node itself.

The default password for grafana is `prom-operator`.
If we enter a bad password it will lock the database and we will need to reinstall everything.