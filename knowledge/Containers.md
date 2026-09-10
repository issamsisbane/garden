Sur Linux quand on crée des conteneurs ça se fait nativement.

Parcontre sur windows et macOs on a besoin d'une couche de virtualisation pour pouvoir creer des conteneurs. C'est ce que fait rancher desktop ou docker desktop.

Cela peut donc créer des problème. Par exemple sur un conteneurs créer sur macOS avec une archi ARM brew ne fonctionne pas. 

Une solution est de créer le conteneurs dans une VM via un provider [[DevPod]]