[[Quartz]]
Il n'y a pas de conteneur tout simple pour lancer obsidian comme un site web accessible via une url. 

Il existe des conteneurs qui font du docker in docker et qui permette d'acceder au conteneur avec obsidian via un protocol particulier. J'ai pas envie de faire ça sur tout que dans kubernetes ça va être trop de permissions à donner.

Ducoup la meilleur option c'est de convertir obsidian en plain markdown et de balancer ça à un site static. Il faut obligatoirement convertir pour repasser au markup mardown classique et rebuild tous les liens. Il y a des outils pour faire ça pas besoin de le reecrire apparement. Après je l'ai déjà plus ou moins fait dans mes pipelines github actions donc bon...

https://jacobian.org/til/hugo-obsidian/