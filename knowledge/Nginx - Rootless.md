# Problème

Dans le dockerfile de bonjour-angular. On utilisait à la base l'image du dockerhub nginx:latest.

Or lorsque j'ai déployé l'application, je me suis rendu compte que le pod ne voulait pas démarrer. En vérifiant les logs, j'ai vu que c'était à cause d'un problème de permission. 
# Solution

Pour pouvoir lancer des conteneurs dans openshift, il faut que ces derniers soit rootless. Or ce n'est pas le cas de cette image. Apparement, on peut gérer cela en utilisant une [[SCC]] mais je n'avais pas trop envie de faire cela, je voulais une vraie image rootless. 

J'ai fini par trouver une image sur le dockerhub `nginxinc/nginx-unprivileged` qui est bien rootless et promu par le repo officiel nginx.

J'avais toujours des problèmes avec le conteneur qui ne voulait pas se lancer. 
Finalement, il fallait bien choisir le port 8080 et ajouter cela dans la description du deployment dans le manifest yaml :

``` yaml
containers:
        - name: module-frontend
          image: ""
          imagePullPolicy: Always
          ports:
            - name: http
              containerPort: 8080
              protocol: TCP
          securityContext:
            capabilities:
              drop:
                - NET_RAW
            runAsNonRoot: true
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
          volumeMounts:
          - mountPath: /tmp
            name: tmp
      volumes:
        - emptyDir: {}
          name: tmp
          livenessProbe:
            httpGet:
              path: /
              port: http
          readinessProbe:
            httpGet:
              path: /
              port: http
```

En fait, on monte un volume emptyDir qui sera supprimé à la suppression du pod pour pouvoir écrire dans le répertoire /tmp sans problème.

# FINALEMENT

Il faut le le volumes tmp et il faut ajouter ça dans le fichier de conf nginx.conf qui est ajouté via un config file : 

```
pid /tmp/nginx.pid;
```

Et le dockerfile doit ressembler à ça : 
``` docker
FROM dockerhub.nexus-primaire.integration.ulmj.intranet.justice.gouv.fr/nginxinc/nginx-unprivileged
COPY docker/build/nginx/default.conf /etc/nginx/conf.d/default.conf
COPY dist/cpj-mai-frontend /usr/share/nginx/html
WORKDIR /srv/www
EXPOSE 8080
```

le chemin a utilisé est forcément /usr/share/nginx/html