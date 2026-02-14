Il faut simplement utiliser le serverside apply qui n'utilise pas par défaut last-applied-configuration et qui ne genere donc pas le probleme.

A l'avenir le server-side apply va devenir le standard.

[Fixing Argo CD "Too long must have at most 262144 bytes" error](https://www.arthurkoziel.com/fixing-argocd-crd-too-long-error/)

```
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
spec:
  syncPolicy:
    syncOptions:
    - ServerSideApply=true
```
```