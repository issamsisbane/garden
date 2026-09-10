Use keycloak to setup SSO for applications int our kubernetes cluster.

https://www.youtube.com/watch?v=-DQCiaOSlqs

il faut mapper le role admin de keycloak au role Admin de grafana. Cela se fait via les values du chart kube-prometheus-stack

https://github.com/rslim087a/keycloak-sso-kubernetes-oidc-tutorial