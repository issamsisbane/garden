# Helm - Repo vs OCI Repo

The main diffrences is the protocol and the usage of the index.yaml.

Legacy Repo use and index.yaml referencing all the charts and versions. 

It could be a problem if the repo has a huge list of chart. And you have to reDownload it using helm `helm repo update` in order to get the new versions of charts or the new chart.

OCI Repos don't have a index.yaml. It more efficient and reduces data bandwidth a lot.
But it lacks a search function. Using OCI repo you can't use helm search anymore.

OCI repos are the cloud native way to use helm charts and we are moving to global use of it.

[Medium Article](https://medium.com/@idan441/migrating-to-oci-based-helm-chart-repositories-in-order-to-reduce-cloud-costs-fc9f492fdffe)