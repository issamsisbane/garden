Mischa use [[Renovate]] in a way that it create Pull Requests with his images updated. In the PR there are the changes of the versions and it's automatically changes by renovate.

To update, we juste have to merge the PR.

Renovate needs to access our github repo, so we need to create a token.

We need to create a secret with the token : 
``` bash
kubectl create secret generic renovate-container-env \
--from-literal=RENOVATE_TOKEN=my-token \
--dry-run=client \
-o yaml > renovate-container-env.yaml
```

Then we need to create a cronjob, a namespace and a configmap : 

``` yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: renovate
  namespace: renovate
spec:
  schedule: "@hourly"
  concurrencyPolicy: Forbid # Prevent 2 cronjob running at the same times
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: renovate
              image: renovate/renovate:latest
              args:
                - IssamSisbane/pi-cluster

              envFrom:
                - secretRef:
                    name: renovate-container-env
                - configMapRef:
                    name: renovate-configmap

          restartPolicy: Never
```

``` yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: renovate-configmap
  namespace: renovate
data:
  RENOVATE_AUTODISCOVER: "false"
  RENOVATE_GIT_AUTHOR: "Issam's Renovate Bot <bot@renovateapp.com>"
  RENOVATE_PLATFORM: "github"
```

We can use Flux to automate image update but it will commit directly. Apparently there are ways to use pull requests. But reconcile is very easy to setup.