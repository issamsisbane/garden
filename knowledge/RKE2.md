---
tags: TECHNOS
state: to_complete
---

[[K3S vs RKE2]]
# Definition
**RKE2** (Rancher Kubernetes Engine 2) est une [[Distribution Kubernetes]] développée par Rancher Labs. Il est conçu pour être sécurisé par défaut, léger et facile à déployer. Voici une brève description de ses principales caractéristiques :

### Caractéristiques clés de RKE2 :

1. **Sécurité renforcée :**
    
    - Livré avec **SELinux**, des politiques **PodSecurityPolicy** activées par défaut et le chiffrement des données sensibles.
    - Intègre **CIS Benchmarks** pour Kubernetes, facilitant la conformité aux normes de sécurité.
2. **Léger et modulaire :**
    
    - Basé sur le projet **K3s**, il conserve une approche minimaliste.
    - Inclut uniquement les composants essentiels pour exécuter Kubernetes, comme **containerd** au lieu de Docker pour la gestion des conteneurs.
3. **Compatibilité complète avec Kubernetes :**
    
    - Conserve toutes les fonctionnalités de Kubernetes standard (API complète, CRD, etc.).
    - Prêt pour les charges de travail en production.
4. **Adapté aux environnements hybrides :**
    
    - Optimisé pour fonctionner sur des environnements cloud, sur site ou en périphérie (edge computing).
    - Prend en charge les clusters multi-noeuds et les environnements distribués.
5. **Facilité d'administration :**
    
    - Simplifie le déploiement et la gestion des clusters Kubernetes avec des outils et une documentation claire.
    - Peut être intégré dans l'écosystème **Rancher** pour une gestion centralisée.

### Cas d'utilisation :

- Déploiement Kubernetes sécurisé en production.
- Scénarios nécessitant une conformité stricte (sécurité, audits).
- Environnements distribués, tels que les infrastructures hybrides ou périphériques.

# Nodes
## Master Nodes

## Agent Nodes