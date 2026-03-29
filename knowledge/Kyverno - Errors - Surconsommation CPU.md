---
foam_template:
  filepath: "0 - INBOX/Kyverno - Errors - Surconsommation CPU.md"
  description: "New note"
created: "2026-03-26"
bloggable: true
---

# Kyverno - Errors - Surconsommation CPU

J'avais Kyverno qui consommait pour les deux pods reports controller 50 CPU et 10 CPU.

En plus de ça, il y avait beaucoup de restarts 2000 en quelques jours.

Le problème c'est qu'il y avait beaucoup d'ephemeralReports +900 qui n'étaient pas traité depuis 50 jours.

Dans les logs plein d'erreurs de requests vers l'api kubernetes.

C'est pas normal qu'on consomme autant car il n'y a rien sur le cluster.

## Réparations

1. Suppression des ephemerals reports à la main
2. Relancement des pods
3. Constations que les pods se font OOMKILLED car seulement 128Mi en limit RAM par défaut avec le chart
4. Montée des limits et requests RAM des pods reports controller

Et après ça plus de restart, plus d'erreurs dans les logs, et plus de surconsommation excessive de CPU on est en bien en dessous de 30m de CPU. C'est beaucoup mieux.

## Explications

La 128Mi était clairement la cause racine de toute la cascade :

OOMKill (128Mi trop petit)
    ↓
Redémarrage → re-discovery de toutes les APIs
    ↓
TLS timeouts pendant la discovery (connexions interrompues par le kill)
    ↓
Re-list complet de toutes les ressources → CPU explose
    ↓
OOMKill à nouveau → boucle infinie

Les "TLS handshake timeout" et "http2: client connection lost" dans les logs n'étaient pas un problème réseau — c'était juste les connexions orphelines laissées par les kills brutaux.


### CPU Élevé

Le CPU élevé était une conséquence de l'OOMKill, pas une cause indépendante
Quand un pod se fait OOMKill, il redémarre et doit tout recharger depuis zéro. Pour le reports controller, ça signifie :

1. La discovery API au démarrage
Démarrage → interroge TOUS les API groups du cluster
→ 20+ appels vers l'API server
→ Chacun doit répondre avant de passer au suivant
→ Pendant ce temps : CPU à fond

2. Le re-list complet de toutes les ressources
Après la discovery, le controller doit reconstruire son cache local en listant toutes les ressources qu'il surveille dans tous les namespaces — Pods, ConfigMaps, Deployments, etc. Avec un grand cluster OpenShift, ça représente potentiellement des dizaines de milliers d'objets à charger en mémoire.

3. Le retraitement de tous les EphemeralReports
Avec 970 EphemeralReports en attente, à chaque redémarrage il devait re-agréger tout depuis le début.

4. La boucle qui s'emballe
Tout ce travail consomme de la mémoire
→ Atteint 128Mi → OOMKill
→ Redémarrage → recommence depuis zéro
→ N'atteint jamais un état stable

En résumé : le CPU élevé c'était le controller qui recommençait indéfiniment le même travail intensif sans jamais pouvoir le terminer, faute de mémoire suffisante pour aller au bout.

### Pourquoi 50 cores de CPU ?

Tu as 2 pods en CrashLoopBackOff avec 2000+ restarts. La clé c'est le parallélisme des restarts.

Kubernetes ne redémarre pas un pod et attend qu'il soit stable — avec 2000 restarts, le backoff est certes long, mais pendant les phases de redémarrage rapide (les premiers centaines de restarts), les deux pods tournaient en même temps, chacun lançant ses workers en parallèle :
Pod 1 démarre → 8 goroutines de reconciliation → 25 cores
Pod 2 démarre → 8 goroutines de reconciliation → 25 cores
                                                = 50 cores

Et chaque goroutine de reconciliation fait des appels API en boucle serrée sans pouvoir terminer — donc elle consomme du CPU à 100% sans jamais se mettre en attente.

Pourquoi les reports ne pouvaient pas être traités ?

C'est là que c'est subtil. Le reports controller traite les EphemeralReports en mémoire — il charge l'objet, l'agrège, écrit le PolicyReport, puis supprime l'EphemeralReport.

Avec 128Mi, voilà ce qui se passait :
Charge 970 EphemeralReports en mémoire    → +60Mi
+ cache des ressources du cluster          → +40Mi  
+ discovery API                            → +20Mi
+ workers goroutines                       → +20Mi
                                           = ~140Mi → OOMKill

Il n'atteignait jamais l'étape "écrire le PolicyReport + supprimer l'EphemeralReport". Il mourait avant, laissant tous les EphemeralReports intacts, qui s'accumulaient restart après restart.

C'est pour ça que tu voyais 970 EphemeralReports vieux de 50 jours — ils n'avaient jamais pu être traités une seule fois.