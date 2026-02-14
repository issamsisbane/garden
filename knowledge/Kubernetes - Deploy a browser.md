# Contexte

J'avais besoin d'utiliser les developers tools du navigateur EDGE pour recuperer l'assertion SAML renvoyée par un server SSO.

Or avec le PC du client je n'avais pas accès au devtools du navigateur (bloqué par l'organisation).

# Solution

Ainsi, pour contourner cela j'ai déployé un navigateur sur firefox via un openshift que j'ai exposé via une route.

Il y avait des flux a ouvrir mais j'ai donc pu utiliser les devtools depuis ce pod. C'est un pod en temps réel ça veut dire que la session perdure peut importe d'ou je me connecte pc 1 ou pc 2 c'est pareil. La connexion se fait depuis un naviagateur via la route (un navigateur dans un navigateur) : BROWSERCEPTION

# Copie 

Par contre il y avait un problème, je ne pouvais pas copier coller depuis le navigateur, apparement c'est censé être un probleme avec l'image mais étant un peu préssé je n'ai pas eu le temps de changer d'image et d'en trouver une qui marche. 

Comme j'ai toujours accès à Openshift, je peux déployé ce que je veux donc j'ai déployé un autre pod. Cette fois c'est codeserver (un fork de vscode) qui permet d'avoir un liveserver de code. Je m'en suis servi pour copier coller l'assertions SAML entre mon PC et le navigateur. J'ai pensé à la copier à la main mais c'était trop long...

# Manifests
## Firefox

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: firefox
spec:
  replicas: 1
  selector:
    matchLabels:
      app: firefox
  template:
    metadata:
      labels:
        app: firefox
    spec:
      serviceAccountName: bjr-runner
      containers:
      - name: firefox
        image: dockerhub/jlesage/firefox
        ports:
        - containerPort: 5800
        volumeMounts:
        - name: firefox-config
          mountPath: /config
        securityContext:
          runAsUser: 0
          privileged: true
          capabilities:
            drop:
            - "ALL"
      volumes:
      - name: firefox-config
        emptyDir: {}
---
apiVersion: v1
kind: Service
metadata:
  name: firefox
spec:
  selector:
    app: firefox
  ports:
    - protocol: TCP
      port: 5800
      targetPort: 5800

---
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: firefox
spec:
  host: firefox.apps.ocp-otc-dc1-t11.ocp01.tbot.dc.justice.gouv.fr
  to:
    kind: Service
    name: firefox
  port:
    targetPort: 5800
  tls:
    termination: edge
    insecureEdgeTerminationPolicy: Redirect


```
## Codeserver

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: code-server
spec:
  replicas: 1
  selector:
    matchLabels:
      app: code-server
  template:
    metadata:
      labels:
        app: code-server
    spec:
      serviceAccountName: bjr-runner
      containers:
      - name: code-server
        image: dockerhub/codercom/code-server:latest
        env:
        - name: PASSWORD
          value: "test" # Changez ceci pour sécuriser l'accès
        ports:
        - containerPort: 8080
        volumeMounts:
        - name: code-server-data
          mountPath: /home/coder
        securityContext:
          runAsUser: 0
          privileged: true
          capabilities:
            drop:
            - "ALL"
      volumes:
      - name: code-server-data
        emptyDir: {}
---
apiVersion: v1
kind: Service
metadata:
  name: code-server
spec:
  selector:
    app: code-server
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
---
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: code-server
spec:
  host: codeserver.apps.ocp-otc-dc1-t11.ocp01.tbot.dc.justice.gouv.fr
  to:
    kind: Service
    name: code-server
  port:
    targetPort: 8080
```
``