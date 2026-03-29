Alloy only has builtin exporter for components of the grafana stack and not for other competitors such as elasticsearch. 

But it has an exporter called otel. This is for OpenTelemetry. It is a standard.
We can use this but Elasticsearch doen't understand by default otel so we need a brick between alloy and elastic. It's the otel collector.

https://github.com/issamsisbane/observability-alloy-to-elastic/tree/main

![[Pasted image 20250916091040.png]]

The logs are coming to elastic : 

![[Pasted image 20250912184201.png]]
