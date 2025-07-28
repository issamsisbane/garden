``` yaml
export GIT_REPO_URL=https://gitlab.url
export GIT_REPO_TOKEN=glpat-xxxxxxxxxxxxxxxxxxxx
export GIT_REPO_PROJECT=default
cat <<EOF | oc apply -f -
apiVersion: v1
kind: Secret
metadata:
  name: myrepo
  namespace: openshift-gitops
  labels:
    argocd.argoproj.io/secret-type: repository
type: Opaque
stringData:
  type: git
  url: ${GIT_REPO_URL}
  username: token
  password: ${GIT_REPO_TOKEN}
  project: ${GIT_REPO_PROJECT}
EOF
```

Un repo est binder a un projet. On ne peut pas utiliser un meme repo pour 2 projets. Il faut donc creer autant de ressource repo de projet qui l'utilise en spécifiant bien le bon projet à chaque fois.