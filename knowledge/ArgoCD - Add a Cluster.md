Pour se connecter à un cluster, il faut créer un service account avec les bonnes permissions dans le cluster cible puis recuperer le token lié à ce service account. Dans le cluster qui heberge argo dans le ns d'argo on envoi ce secret : 

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: cluster-secours
  namespace: gitops-prod
  labels:
    argocd.argoproj.io/secret-type: cluster
type: Opaque
stringData:
  name: cluster-secours
  server: "https://url:6443"
  config: '{"bearerToken": "","tlsClientConfig": {"insecure": false, "caData": ""}}'
```


``` yaml
export ARGOCD_CLUSTER_NAME="anteprod"
export ARGOCD_CLUSTER_API_URL="https://api.cop"
export ARGOCD_CLUSTER_BEARER_TOKEN="sha256~..."
export ARGOCD_CLUSTER_CA='
-----BEGIN CERTIFICATE-----
...
-----END CERTIFICATE-----
'
export ARGOCD_CLUSTER_CONFIG='
{
  "bearerToken": "$ARGOCD_CLUSTER_BEARER_TOKEN",
  "tlsClientConfig": {
    "insecure": false,
    "caData": "$(echo $ARGOCD_CLUSTER_CA | base64 -w0)"
  }
}
'
cat <<EOF | oc apply -f -
apiVersion: v1
kind: Secret
metadata:
  name: mycluster
  namespace: openshift-gitops
  labels:
    argocd.argoproj.io/secret-type: cluster
type: Opaque
stringData:
  name: "${ARGOCD_CLUSTER_NAME}"
  url: "${ARGOCD_CLUSTER_API_URL}"
  config: "${ARGOCD_CLUSTER_CONFIG}"
EOF
```