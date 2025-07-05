---
title: "Sécuriser vos applications Azure : Guide pas à pas pour utiliser Azure Key Vault avec Azure Functions"
description: "Découvrez comment renforcer la sécurité de vos applications Azure en utilisant Azure Key Vault avec Azure Functions. Suivez notre guide pas à pas pour protéger vos secrets et clés de manière efficace et sécurisée dans le cloud."
lang: "fr"
pubDate: "Apr 22 2024"
heroImage: "/portfolio/blog/function_kv/function_kv.png"
badge: "AZURE"
tags: ["Cloud", "Azure", "Function", "KeyVault"]
---

Lorsqu'on utilise Azure Cloud et que l'on déploie des applications, qu'elles soient des Functions, des Conteneurs ou des Web Apps, la plupart du temps l'application va nécessiter des variables d'environnement pour fonctionner. 

Il est assez simple d'ajouter des variables d'environnement en passant par le portail web Azure, et cela fonctionne très bien. Cependant, dans certains cas, les variables d'environnement sont sensibles et ne doivent pas être accessibles en clair directement depuis le portail Azure depuis la page de l'application.

C'est dans ce genre de cas qu'intervient **Azure Key Vault**. **Azure Key Vault** est un service de gestion des **secrets** des **clés** et des **certificats** dans **Microsoft Azure**. Il permet de stocker de manière sécurisée et de gérer les informations sensibles telles que les mots de passe, les clés d'API, les certificats et d'autres données confidentielles. 

Partons du principe que nous avons déjà créé un Key Vault et une Function App (voir les crédits pour plus de détails). Nous utiliserons Function App, mais la démarche est sensiblement la même pour les autres ressources Azure.

## 1 - Ajouter un secret dans notre Key Vault

![Image1](/portfolio/blog/function_kv/function_kv_0.png)

![Image2](/portfolio/blog/function_kv/function_kv_1.png)

## 2 - Activation de la `managed identity` dans la Function App.

Une `managed identity` dans Azure est un service qui simplifie et sécurise l'authentification des ressources Azure en leur fournissant une identité gérée par la plateforme, éliminant ainsi le besoin de gérer manuellement des informations d'identification. En d'autres termes cela permet de donné une identité à nos applications et leur accorder des droits à nos différentes ressources Azure.

![Image3](/portfolio/blog/function_kv/function_kv_2.png)

## 3 - Ajouter un rôle à notre application

Il faut que nous ajoutions un rôle à notre application. Pour cela, il faut retourner dans notre Key Vault. On se rend dans IAM et on clique sur `add role assignment`.

![Image4](/portfolio/blog/function_kv/function_kv_3.png)

Il faut choisir un rôle adapté à nos besoins. Tous les rôles qui donnent un accès en lecture au secret peuvent être utilisés. Cependnat cela ne respecte pas le principe du moindre privilège en matière de sécurité du cloud. Il faudrait donc plutôt choisir le rôle qui ne donne que les accès nécessaires, soit ici uniquement un accès en lecture aux secrets.

Ainsi, nous allons choisir le rôle `Key Vault Secrets User` :

![Image5](/portfolio/blog/function_kv/function_kv_4.png)

Il faut maintenant choisir la `managed identity` correspondant à notre application et ajouter l'application à laquelle nous voulons accorder l'accès :

![Image6](/portfolio/blog/function_kv/function_kv_5.png)

## 4 - Ajouter les secrets dans l'application

On choisit le secret que l'on veut ajouter dans notre application :

![Image7](/portfolio/blog/function_kv/function_kv_6.png)

On choisit la version désirée et on copie le `Secret Identifier` :

![Image8](/portfolio/blog/function_kv/function_kv_7.png)

On retourne dans notre Function App dans l'onglet configuration. Il suffit d'ajouter ceci : `@Microsoft.KeyVault(SecretUri=YourSecretIdentifier)`

![Image9](/portfolio/blog/function_kv/function_kv_8.png)

## Conclusion

Et voilà ! Vous venez d'ajouter une variable d'environnement à votre application depuis votre KeyVault !

## Crédits

Créer une identité managée : [https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/tutorial-windows-vm-access-nonaad](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/tutorial-windows-vm-access-nonaad)

Créer un Key Vault : [https://learn.microsoft.com/en-us/azure/key-vault/secrets/quick-create-portal](https://learn.microsoft.com/en-us/azure/key-vault/secrets/quick-create-portal)