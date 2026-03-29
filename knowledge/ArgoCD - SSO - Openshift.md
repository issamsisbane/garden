---
foam_template:
  filepath: "0 - INBOX/ArgoCD - SSO - Openshift.md"
  description: "New note"
created: "2026-02-25"
---

# ArgoCD - SSO - Openshift

Il créer une route en edge et qui redirige en http.
Il faut aussi parametrer ARGO pour etre en insecure comme la terminaison SSL se fait au niveau de la route.

```yaml
kind: Route
apiVersion: route.openshift.io/v1
metadata:
  name: argocd-server
  namespace: argocd
spec:
  host: argocd-fqdn
  to:
    kind: Service
    name: argocd-server
    weight: 100
  port:
    targetPort: http
  tls:
    termination: edge
    insecureEdgeTerminationPolicy: Redirect
  wildcardPolicy: None
```

```yaml
kind: ConfigMap
apiVersion: v1
metadata:
  name: argocd-cmd-params-cm
  namespace: argocd
data:
  server.insecure: 'true'
```

Pour la conf SSO :

```yaml
kind: ConfigMap
apiVersion: v1
metadata:
  name: argocd-cm
  namespace: argocd
data:
  resource.customizations.ignoreResourceUpdates.apps_ReplicaSet: |
    jqPathExpressions:
      - '.metadata.annotations."deployment.kubernetes.io/desired-replicas"'
      - '.metadata.annotations."deployment.kubernetes.io/max-replicas"'
      - '.metadata.annotations."rollout.argoproj.io/desired-replicas"'
  resource.exclusions: |
    ### Network resources created by the Kubernetes control plane and excluded to reduce the number of watched events and UI clutter
    - apiGroups:
      - ''
      - discovery.k8s.io
      kinds:
      - Endpoints
      - EndpointSlice
    ### Internal Kubernetes resources excluded reduce the number of watched events
    - apiGroups:
      - coordination.k8s.io
      kinds:
      - Lease
    ### Internal Kubernetes Authz/Authn resources excluded reduce the number of watched events
    - apiGroups:
      - authentication.k8s.io
      - authorization.k8s.io
      kinds:
      - SelfSubjectReview
      - TokenReview
      - LocalSubjectAccessReview
      - SelfSubjectAccessReview
      - SelfSubjectRulesReview
      - SubjectAccessReview
    ### Intermediate Certificate Request excluded reduce the number of watched events
    - apiGroups:
      - certificates.k8s.io
      kinds:
      - CertificateSigningRequest
    - apiGroups:
      - cert-manager.io
      kinds:
      - CertificateRequest
    ### Cilium internal resources excluded reduce the number of watched events and UI Clutter
    - apiGroups:
      - cilium.io
      kinds:
      - CiliumIdentity
      - CiliumEndpoint
      - CiliumEndpointSlice
    ### Kyverno intermediate and reporting resources excluded reduce the number of watched events and improve performance
    - apiGroups:
      - kyverno.io
      - reports.kyverno.io
      - wgpolicyk8s.io
      kinds:
      - PolicyReport
      - ClusterPolicyReport
      - EphemeralReport
      - ClusterEphemeralReport
      - AdmissionReport
      - ClusterAdmissionReport
      - BackgroundScanReport
      - ClusterBackgroundScanReport
      - UpdateRequest
  resource.customizations.ignoreResourceUpdates.ConfigMap: |
    jqPathExpressions:
      # Ignore the cluster-autoscaler status
      - '.metadata.annotations."cluster-autoscaler.kubernetes.io/last-updated"'
      # Ignore the annotation of the legacy Leases election
      - '.metadata.annotations."control-plane.alpha.kubernetes.io/leader"'
  resource.customizations.ignoreResourceUpdates.Endpoints: |
    jsonPointers:
      - /metadata
      - /subsets
  url: 'https://myargo-route'
  resource.customizations.ignoreResourceUpdates.all: |
    jsonPointers:
      - /status
  dex.config: |
    issuer: https://myargo-route/api/dex
    connectors:
    - config:
        clientID: system:serviceaccount:argocd:argocd-dex-server
        clientSecret: $oidc.dex.clientSecret
        groups: []
        insecureCA: true
        issuer: https://kubernetes.default.svc
        redirectURI: https://myargo-route/api/dex/callback
      id: openshift
      name: OpenShift
      type: openshift
  resource.customizations.ignoreResourceUpdates.discovery.k8s.io_EndpointSlice: |
    jsonPointers:
      - /metadata
      - /endpoints
      - /ports
  resource.customizations.ignoreResourceUpdates.argoproj.io_Application: |
    jqPathExpressions:
      - '.metadata.annotations."notified.notifications.argoproj.io"'
      - '.metadata.annotations."argocd.argoproj.io/refresh"'
      - '.metadata.annotations."argocd.argoproj.io/hydrate"'
      - '.operation'
  oidc.tls.insecure.skip.verify: 'true'
  resource.customizations.ignoreResourceUpdates.argoproj.io_Rollout: |
    jqPathExpressions:
      - '.metadata.annotations."notified.notifications.argoproj.io"'
  resource.customizations.ignoreResourceUpdates.autoscaling_HorizontalPodAutoscaler: |
    jqPathExpressions:
      - '.metadata.annotations."autoscaling.alpha.kubernetes.io/behavior"'
      - '.metadata.annotations."autoscaling.alpha.kubernetes.io/conditions"'
      - '.metadata.annotations."autoscaling.alpha.kubernetes.io/metrics"'
      - '.metadata.annotations."autoscaling.alpha.kubernetes.io/current-metrics"'
```