# Istio

## Istio Components

**`istiod`** — le control plane d'Istio (fusion depuis Istio 1.5 de Pilot, Citadel et Galley). Il s'occupe de :

- **Configuration/distribution** : traduit les CRDs Istio (VirtualService, DestinationRule, Gateway, etc.) en configuration Envoy (xDS) et la pousse vers tous les sidecars proxy (Envoy) injectés dans les pods du mesh.
- **Sécurité (PKI)** : agit comme autorité de certification interne, délivre et fait tourner les certificats mTLS pour chaque workload.
- **Validation** : valide les ressources Istio via un webhook avant leur admission dans le cluster.
- **Injection des sidecars** : gère le webhook mutant qui injecte automatiquement le conteneur `istio-proxy` (Envoy) dans les pods des namespaces labellisés pour l'injection.

**`istio-ingressgateway`** — une passerelle Envoy dédiée qui gère le trafic **entrant** depuis l'extérieur du cluster vers les services du mesh. C'est le point d'entrée typique, exposé en général via un `LoadBalancer` ou `NodePort`, configuré via des ressources `Gateway` + `VirtualService`. Il remplace/complète un Ingress Controller classique avec des fonctionnalités plus riches (routage L7, TLS, mTLS, etc.).

**`istio-egressgateway`** — une passerelle Envoy symétrique qui gère le trafic **sortant** du mesh vers des services externes. Elle permet de centraliser et contrôler tout le trafic qui quitte le cluster (politiques de sécurité, logging, chiffrement TLS vers l'extérieur, contrôle des destinations autorisées), plutôt que de laisser chaque pod sortir directement.