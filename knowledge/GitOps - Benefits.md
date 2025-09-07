
1. **Uniformité des configurations** : Assure que tous les clusters ont un état similaire pour la **configuration**, la **surveillance** et le **stockage**.
2. **Récupération et recréation rapide** : Permet de restaurer ou recréer des clusters à partir d’un état connu.
3. **Contrôle des changements** : Applique ou annule facilement les modifications de configuration sur plusieurs clusters.
4. **Gestion d’environnements multiples** : Associe des configurations **modélisées** et **paramétrables** pour différents environnements (développement, test, production).
5. **Plus sécurisé** car on peut seulement donner accès pour faire des actions sur nos environnements (cloud, machines ou kubernetes) à nos CD et plus aux personnes directement. Tout le monde peut proposer des changements via une PR mais celle-ci doit être validée pour ensuite être appliquée. 
