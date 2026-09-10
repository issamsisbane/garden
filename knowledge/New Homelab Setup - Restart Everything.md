---
creation date: 2026-04-10-19:49:55
modification date: 2026-04-10-19:49:55
imageNameKey: New_Homelab_Setup_-_Restart_Everything
---
J'ai eu beaucoup de problème sur mon homelab.

Dernièrement, tout fonctionnait au ralenti. Je me suis rendu compte que c'était du a mon node master qui mettait trop de temps pour ecrire dans etcd.

Sur mon node master, c'est un vieux pc avec un HDD et avec trop d'applications (même si c'est peu pour moi, une dizaine d'app) ça commençait a ne plus aller.

J'ai essayer de mon côté de résoudre le problème, notamment en passant le node master sur mon raspberrypi qui lui a un ssd.

Mais etcd a fini corrompu et j'ai préféré tout supprimer pour repartir de 0.

## Uninstall total

J'ai utiliser Kubespray avec le playbook `reset` pour tout supprimer.
## Reinstall

J'ai juste modifier les vars pour tout reinstaller. J'avais des erreurs lors de l'installation du CNI. En fait, le playbook n'avais pas tout desinstaller le CNI totalement.

Je l'ai donc fait à la main.

```bash
rm -rf /run/cni/calico
```

## Tout reinstaller

