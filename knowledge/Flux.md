Flux is a [[GitOps]] tool more cli-focused than [[ArgoCD]]. 
It use [[Kustomize]].

We never update the flux manifest files by hand.

[[Flux Force Reconciliation]]

With flux we can see everything done by flux directly in the cluster. We can interact with the helm releases directly. It's not the case with Argo.