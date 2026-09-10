Tracing
Traces tempo

Monitoring
Metrics prometheus

Logging
Logs loki


k8s-monitoring-helm
example : https://github.com/grafana/k8s-monitoring-helm/tree/main/charts/k8s-monitoring/docs/examples

[[Loki]]
[[Kube Prometheus Stack]]

loki filter
![[Pasted image 20251116164611.png]]

https://prometheus.io/docs/prometheus/latest/querying/api/

```
## Remote Write Receiver[](https://prometheus.io/docs/prometheus/latest/querying/api/#remote-write-receiver)

Prometheus can be configured as a receiver for the Prometheus remote write protocol. This is not considered an efficient way of ingesting samples. Use it with caution for specific low-volume use cases. It is not suitable for replacing the ingestion via scraping and turning Prometheus into a push-based metrics collection system.

Enable the remote write receiver by setting `--web.enable-remote-write-receiver`. When enabled, the remote write receiver endpoint is `/api/v1/write`. Find more details [here](https://prometheus.io/docs/prometheus/latest/storage/#overview).
```