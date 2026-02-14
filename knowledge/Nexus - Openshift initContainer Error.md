# Erreur 

Lors du lancement du pod nexus installe via helm chart : 

Il y a une erreur lors de la creation de fichier dans /nexus-data/etc/....

nexus-data est un empty-dir mounté en tant que volume dans le pod.

# Résolution
Pour résoudre ça plusieurs solutions pas ouf : 
1. Utiliser la scc anyuid => trop de droit
2. Utiliser la scc gitlab-runner-prod => droit privilege escalation
3. Utiliser une scc custom nexus-scc => il faut ajouter dans le template du statefulset pour le pod 

```
securityContext:
	fsGroup: 2000
```

Le problème c'est que c'est pas possible via le chart ce n'est pas dans le template on ne peut que mettre la securityContext au niveau du conteneur donc obligé de passé à la main.

La scc que j'ai créer à la main : 
```
apiVersion: security.openshift.io/v1
kind: SecurityContextConstraints
metadata:
  name: nexus-scc
allowPrivilegeEscalation: false
runAsUser:
  type: RunAsAny
fsGroup:
  type: RunAsAny
supplementalGroups:
  type: RunAsAny
volumes:
  - configMap
  - downwardAPI
  - emptyDir
  - persistentVolumeClaim
  - projected
  - secret
  - hostPath
allowHostDirVolumePlugin: true
seLinuxContext:
  type: MustRunAs
```

Application de la scc au ns nexusrepo : 
```
oc adm policy add-scc-to-user nexus-scc -z default -n nexusrepo
```


Il faudrait aussi utiliser un pvc plutôt que le empty-dir plustard.

