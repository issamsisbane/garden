---
title: "A la recherche d'un outil d'analyse du traffic web"
description: "Comment analyser le traffic d'un site web pour avoir une idée du nombre d'utilisateurs ?"
lang: "fr"
pubDate: "Apr 24 2024"
heroImage: "/portfolio/blog/analytics/analytics.png"
badge: "AZURE"
tags: ["Cloud", "Azure", "Analyse"]
---

## Problématique

Après avoir développé et déployé quelques sites web, notamment mon portfolio, j'étais curieux d'obtenir des informations sur les visiteurs. Notamment, je partageais plusieurs liens vers mon portfolio, que ce soit sur LinkedIn, GitHub ou mon CV.

Je voulais connaître le trafic sur mon site, en particulier le **nombre de visiteurs uniques**.

## Backend fait maison

Dans un premier temps, j'ai envisagé de créer ma propre solution. J'ai pensé à un backend simple où chaque visite déclencherait une requête. Cependant, j'ai rapidement rencontré des obstacles. En adoptant cette approche, il serait impossible de compter précisément le nombre d'utilisateurs uniques. Par exemple, les actualisations de page seraient comptées comme de multiples visites plutôt qu'une seule. 

Pour résoudre ce problème, j'ai exploré l'utilisation de cookies pour suivre les utilisateurs uniques, ainsi que les informations contenues dans les en-têtes de requêtes. Cependant, les données disponibles dans les en-têtes étaient limitées, ne fournissant que le navigateur et sa version, ce qui ne permettait pas d'identifier de manière fiable un utilisateur unique. Étant donné que mon portfolio est un site statique, je suis limité dans la gestion des en-têtes et je ne peux pas récupérer, par exemple, l'adresse IP. 

Même en récupérant l'adresse IP, il serait difficile de garantir l'unicité de l'utilisateur, car celle-ci peut changer. Les cookies ne sont pas non plus fiables car les utilisateurs peuvent les supprimer. Par conséquent, j'ai décidé de rechercher une autre solution sans modifier le type de rendu de mon site ou apporter des modifications majeures.

## Transition vers Google Analytics

Confronté à ces défis, je me suis tourné vers Google Analytics, un outil bien établi dans le domaine de l'analyse web. L'intégration des scripts google à mon site était très simple. IL faut juste ajouter un script dans toutes les pages que l'on veut monitorer. Or comme j'utilise Astro qui permet l'utilisation de layout sur toutes les pages j'ai seulement du ajouter le script dans ma page layout.

![google analytics tag](/portfolio/blog/analytics/analytics_0.png)

Cependant, malgré son intégration avec mon projet Astro, j'ai rencontré des difficultés à accéder aux données collectées, limitant ainsi mon analyse du trafic du site. Initialement, aucune donnée n'était disponible sur le tableau de bord. Après quelques minutes, les données n'étaient toujours pas disponibles. Par conséquent, j'ai décidé d'explorer d'autres options.

![Tableau de bord vide](/portfolio/blog/analytics/analytics_1.png)

## Adoption d'Azure Application Insight

Après avoir évalué différentes options, je me suis souvenu d'Azure [Application Insight](https://learn.microsoft.com/fr-fr/azure/azure-monitor/app/app-insights-overview), un outil qui permet de voir et de gérer, en temps réel, les performances d'une application ou d'une API

J'ai également réalisé qu'il était possible de lier Application Insight à une application même si elle n'est pas hébergée sur Azure (mon portfolio étant hébergé sur GitHub Pages).

Le processus de connexion de l'application à Azure était similaire à celui de Google Analytics, simplement en intégrant la balise JavaScript d'Application Insight. Cependant, après l'intégration et le redéploiement de mon application, aucune donnée n'était visible dans Application Insight. 

Après des recherches en ligne, j'ai découvert que l'extension `uBlock Origin` de mon navigateur bloquait les scripts d'Azure identifiés comme des traqueurs. En désactivant cette extension ou en utilisant un autre navigateur, j'ai pu enfin voir les données dans le portail Azure.

J'ai ainsi pu créer un [dashboard](https://learn.microsoft.com/en-us/azure/azure-portal/azure-portal-dashboards) pour obtenir des informations sur les visiteurs de mon site et un [workbook](https://learn.microsoft.com/en-us/azure/azure-monitor/visualize/workbooks-overview) pour des informations plus précises et des visualisations détaillées.

![Azure Users Dashboard](/portfolio/blog/analytics/analytics_2.png)

## Résultats et conclusion

Grâce à l'utilisation d'Application Insight, j'ai pu obtenir des informations détaillées sur les utilisateurs de mon site, telles que le nombre d'utilisateurs uniques, leur provenance géographique et les pages consultées. Bien que les données ne soient pas parfaitement précises, l'outil s'est révélé être une solution fonctionnelle et pertinente pour les besoins du projet.

NB.

24 heures plus tard, les données sont apparues sur le tableau de bord de Google Analytics. Il était en effet mentionné qu'il pouvait y avoir un délai de propagation maximal de 48 heures et que les extensions pouvaient bloquer les scripts de Google.

![Google Analytics Dashboard](/portfolio/blog/analytics/analytics_3.png)

## A retenir:

- Besoin initial d'analyser le trafic d'un site portfolio.
- Difficultés rencontrées avec la mise en place d'outils personnalisés et Google Analytics.
- Adoption réussie d'Application Insight pour obtenir des données plus précises sur les utilisateurs du site.
- Importance de tester la compatibilité des outils avec les configurations existantes pour assurer la collecte efficace des données.