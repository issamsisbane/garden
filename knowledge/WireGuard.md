WireGuard est une solution VPN beaucoup plus **récente** et **moderne** que Strongswan. Elle a été conçue pour être simple, rapide et efficace, tout en offrant des niveaux élevés de sécurité.

# Caractéristiques principales de WireGuard

- **Protocole :** WireGuard n'utilise pas IPSec, mais un protocole VPN personnalisé, qui fonctionne au niveau de la couche réseau (couche 3), plus simple et optimisé pour les performances.
- **Chiffrement :** WireGuard repose sur des algorithmes modernes de cryptographie comme **ChaCha20** pour le chiffrement, **Poly1305** pour l'authentification, **Curve25519** pour les échanges de clés, et **Blake2s** pour le hachage.
- **Authentification :** WireGuard utilise un modèle d'authentification par **clés publiques**. Chaque pair a une clé privée et une clé publique. L'authentification se fait en partageant les clés publiques, ce qui simplifie la gestion par rapport à IPSec.
- **Performances :** WireGuard est très performant. Il est conçu pour être léger, rapide et efficace, avec un code base minimaliste par rapport à IPSec. Cela le rend particulièrement adapté pour des applications à faible latence ou des environnements embarqués.
- **Simplicité :** WireGuard est réputé pour sa **facilité de configuration**. Quelques lignes suffisent pour configurer un VPN fonctionnel, ce qui contraste avec la complexité des solutions IPSec.
- **Système d'exploitation :** WireGuard est disponible sur **Linux**, **Windows**, **macOS**, **Android**, et **iOS**. Il est intégré nativement dans le noyau Linux depuis la version 5.6.

# Avantages

- **Performance et légèreté :** WireGuard est extrêmement performant par rapport à IPSec, en partie grâce à son implémentation simple et efficace. Il consomme également moins de ressources CPU.
- **Simplicité d’utilisation :** WireGuard est facile à installer et à configurer, même pour des utilisateurs avec peu d'expérience.
- **Sécurité moderne :** Il utilise des algorithmes de chiffrement récents et éprouvés, ce qui assure une sécurité de pointe.

# Inconvénients

- **Moins mature :** WireGuard est relativement jeune par rapport à IPSec. Il n'a pas encore le même niveau de déploiement dans des environnements critiques (même s'il est rapidement adopté).
- **Fonctionnalités limitées :** WireGuard est simple et minimaliste, mais cela signifie qu'il n'a pas certaines des fonctionnalités avancées que Strongswan ou IPSec peuvent offrir, comme la gestion de politiques complexes de sécurité ou d'authentification multi-facteurs.
- **Confidentialité des adresses IP :** Contrairement à IPSec, WireGuard ne masque pas complètement les adresses IP des pairs, ce qui peut poser des problèmes de confidentialité dans certains cas spécifiques.