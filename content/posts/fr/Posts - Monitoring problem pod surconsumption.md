---
lang: fr
---

𝐌𝐨𝐧 𝐩𝐨𝐝 𝐜𝐨𝐧𝐬𝐨𝐦𝐦𝐚𝐢𝐭 𝟏𝟑𝟓 % 𝐝𝐞 𝐬𝐚 𝐥𝐢𝐦𝐢𝐭𝐞 𝐑𝐀𝐌... 𝐬𝐚𝐧𝐬 𝐞̂𝐭𝐫𝐞 𝐎𝐎𝐌𝐊𝐢𝐥𝐥𝐞𝐝. 𝐕𝐨𝐢𝐜𝐢 𝐩𝐨𝐮𝐫𝐪𝐮𝐨𝐢.

Aujourd'hui, j'ai rencontré un problème assez particulier sur Kubernetes.

𝐋'𝐚𝐥𝐞𝐫𝐭𝐞
Je reçois une alerte concernant certains pods ArgoCD et leur consommation de RAM. En l'analysant, je me rends compte que le pod application-controller d'ArgoCD, sur un cluster en particulier, consommerait 135 % de sa limite RAM.

𝐀𝐧𝐚𝐥𝐲𝐬𝐞
Je me rends donc sur le cluster et je constate que le pod tourne toujours. Dans l'UI OpenShift, il affiche une consommation de 12 GB, alors que sa limite est de 9 GB. Or, ce n'est pas censé être possible : si un pod dépasse la limite définie dans son manifest Kubernetes, il est tué et finit en OOMKilled.

Je me connecte donc directement dans le pod pour vérifier la consommation réelle via le cgroup, et là, surprise : le pod ne consomme que 6 GB, bien en dessous de la limite, et pas du tout les 12 GB affichés.

Je retrouve cette même valeur de 12 GB sur Grafana, où je constate que depuis midi, toutes les métriques ont doublé.

𝐃𝐢𝐚𝐠𝐧𝐨𝐬𝐭𝐢𝐜
Sur Grafana, en jouant un peu avec les requêtes, je me rends compte que chaque métrique remontée par Prometheus pour un pod est comptabilisée en double. La seule différence entre les deux séries de métriques est le nom du service :

kubelet
prometheus-kubelet

𝐋𝐞 𝐩𝐫𝐨𝐛𝐥è𝐦𝐞
Avec un k get servicemonitor, je découvre qu'une nouvelle instance de Prometheus a été déployée, accompagnée d'un second ServiceMonitor. Résultat : toutes les métriques sont scrapées deux fois, ce qui impacte les valeurs visibles sur l'UI OpenShift comme sur Grafana, toutes multipliées par deux.

Grâce au dépôt GitOps, j'ai pu rapidement identifier quand et par qui cette modification avait été faite, et résoudre le problème sans perdre de temps.

𝐂𝐨𝐧𝐜𝐥𝐮𝐬𝐢𝐨𝐧
Ce diagnostic m'a pris un certain temps et m'a même fait douter de ce que je voyais. Il illustre bien l'importance du monitoring dans les clusters, mais aussi le fait qu'une mauvaise configuration peut considérablement compliquer les diagnostics. En revanche, il montre aussi à quel point le GitOps rend tout beaucoup plus lisible et rapide à investiguer : sans le dépôt Git contenant toute la stack de monitoring, identifier cette modification aurait été bien plus compliqué.