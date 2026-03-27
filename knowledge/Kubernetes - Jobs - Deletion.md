---
foam_template:
  filepath: "0 - INBOX/Kubernetes - Jobs - Deletion.md"
  description: "New note"
created: "2026-03-10"
bloggable: true
---

# Kubernetes - Jobs - Deletion

## Le problème

J'avais des jobs qui failaient directement et qui supprimaient les pods sans possibilité d'accèder aux logs.
J'avais `restartPolicy: onFailure`

## La solution

La différence vient du composant qui fait le “redémarrage” et de la façon dont le contrôleur de Job gère les Pods selon leur état.

Comportement de restartPolicy: OnFailure
Avec OnFailure, c’est le kubelet sur le nœud qui redémarre le conteneur à l’intérieur du même Pod quand il échoue (exit code ≠ 0). Le Pod reste donc le même objet Kubernetes, il change seulement d’état (RestartCount qui augmente, etc.).

Tant que le Job n’a pas atteint son backoffLimit, le Pod est considéré comme “actif”. Quand le Job est finalement marqué en échec, le contrôleur de Job supprime les Pods encore actifs pour nettoyer, ce qui fait disparaître le Pod que tu voulais inspecter.
​

Comportement de restartPolicy: Never
Avec Never, le kubelet ne redémarre pas le conteneur. Si le conteneur échoue, le Pod passe en phase Failed et est considéré comme “terminé”.
​

Le contrôleur de Job ne redémarre pas le Pod existant : il crée un nouveau Pod pour la nouvelle tentative, en incrémentant les compteurs de tentatives dans le status du Job.

Les Pods échoués ne sont plus “actifs”, donc le contrôleur ne les nettoie pas lorsqu’il marque le Job comme Failed, ce qui explique pourquoi tu peux encore voir les Pods en échec et consulter leurs logs.
​

En résumé pratique
OnFailure → redémarrage du conteneur dans le même Pod par le kubelet, puis nettoyage des Pods actifs par le Job quand celui‑ci échoue, donc moins de Pods “restes” pour les logs.

Never → chaque tentative crée un nouveau Pod, les Pods échoués restent visibles (tant qu’aucune autre politique de rétention/TTL n’est configurée), ce qui est pratique pour débugger et regarder les logs après coup.

Si ton objectif principal est de garder les Pods en échec pour debug, restartPolicy: Never est le bon choix ou bien tu peux mettre en place un pipeline de logs centralisé pour ne plus dépendre de la durée de vie des Pods.
​