# Kubernetes Distribution Options for Home Lab

Kubernetes is a set of binaries running on a Linux distribution.

Several options exist for setting up a Kubernetes cluster.

Une **distribution Kubernetes** est une version empaquetée, modifiée ou configurée de Kubernetes, conçue pour faciliter son déploiement et sa gestion dans des contextes spécifiques. Ces distributions incluent généralement Kubernetes (le système de base) ainsi que des outils, des plugins ou des configurations pré-intégrées pour répondre à des besoins particuliers.
## A Kubernetes distribution is a packaged version of Kubernetes that:

- Bundles the core Kubernetes components

- Provides its own installation and management methods

- May modify or optimize certain components

- Often includes additional tools/features

### Kubeadm:

- Used in CKA certification

- Good for deep learning but challenging for long-term management

- Requires manual certificate and CNI management

### MicroK8S:

- Developed by Canonical

- Easy to install but has an opinionated approach

- Bundled add-ons with limited configuration options

### Talos Linux:

- Production-grade, secure, and hardened Kubernetes

- Immutable OS that takes over entire disk

- No SSH access, only API communication

- Considered more advanced and abstracts away installation details

### K3S (chosen for this course):

- Strikes a balance between ease of use and learning opportunities

- Single binary installation on existing Linux systems

- Allows for OS-level troubleshooting and exploration

- Optimized for ARM (good for Raspberry Pi)

- Lightweight and easy to install (one command)

- Powers Rancher, relevant for enterprise Kubernetes management

- Easy to upgrade and add nodes

- Flexible for networking plugins and customization

- K3S is recommended for beginner Kubernetes home labs

- Future courses will cover more advanced options like Talos Linux

- GitOps approach will make it easy to transfer setups between distributions


# Pourquoi des distributions Kubernetes ?

Kubernetes est un projet open source, mais son installation et sa configuration "brutes" peuvent être complexes. Une distribution simplifie l'expérience utilisateur en :

- Préconfigurant Kubernetes pour différents environnements (cloud, sur site, périphérie).
- Intégrant des outils additionnels (monitoring, stockage, réseau).
- Garantissant une compatibilité et des mises à jour sécurisées.

---

# Caractéristiques communes des distributions Kubernetes :

1. **Kubernetes de base** :
    
    - Inclut les composants essentiels de Kubernetes : API Server, Scheduler, Controller Manager, kubelet, etc.
    - Offre des fonctionnalités standard comme le déploiement d'applications, la gestion des ressources et l'autoscaling.
2. **Intégrations supplémentaires** :
    
    - Ajout d'outils pour la gestion réseau (CNI), le stockage (CSI), et la sécurité (RBAC, PodSecurityPolicies).
    - Intégration souvent avec des solutions de monitoring (Prometheus, Grafana) ou de logging.
3. **Support d'installation simplifiée** :
    
    - Scripts, installateurs ou outils pour réduire les efforts nécessaires au déploiement.
4. **Support technique et mises à jour** :
    
    - Fournies par l'entreprise ou la communauté qui développe la distribution.

---

# Exemples populaires de distributions Kubernetes :

1. **RKE (Rancher Kubernetes Engine)** :
    - Fournit une installation simplifiée pour Kubernetes, adaptée aux environnements cloud et sur site. [[RKE2]]
2. **EKS (Elastic Kubernetes Service)** :
    - Distribution gérée par AWS, optimisée pour fonctionner sur leur infrastructure.
3. **GKE (Google Kubernetes Engine)** :
    - Distribution gérée par Google Cloud, hautement intégrée avec les services GCP.
4. **OpenShift** :
    - Distribution développée par Red Hat, orientée vers les entreprises avec des fonctionnalités avancées comme CI/CD intégré. [[3 - GARDEN/knowledge/Openshift]]
5. **K3s** :
    - Version allégée de Kubernetes pour les environnements edge ou les petits clusters.

---

# Cas d'utilisation d'une distribution Kubernetes :

- **Production** : Distributions comme OpenShift ou EKS sont souvent choisies pour leur stabilité et leur support.
- **Test et développement** : Minikube ou Kind sont des distributions légères idéales pour tester Kubernetes localement.
- **Cloud** : GKE, EKS, et AKS (Azure Kubernetes Service) offrent une gestion simplifiée dans les environnements cloud.
- **Edge computing** : K3s ou MicroK8s sont adaptés pour des environnements légers ou distribués.
# Tools

[[Minikube]]
[[Rancher Desktop]]