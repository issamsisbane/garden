# Contexte

Il peut arriver un use-case où on a besoin de mettre des fichiers dans les secrets vault. Pour mettre des fichiers il faut qu'ils soient encodés en base64. 

Le problème c'est que VSO de base prends les valeurs des secrets définis dans vault mais les encode en base64 pour créer les secrets kubernetes. 

Donc avec le comportement normal on se retrouve pour notre fichier avec un secret avec le base64 réencoder en base64.

Donc on ne peut plus utiliser le fichier directement depuis le secret et il faut faire une transformation en plus.

# Solutions

## Bricolage

Une solution est d'avoir un init conteneur qui va decoder le base64 du secret avant que ce soit passé au pod.

Je n'aime pas cette solution car ça fait toucher au code du pod, deploiement et je n'ai pas envie de toucher à ça sachant que je suis dans une logique de helm chart qui porte toute la configuration.

## Transformation

VSO permet de faire des transformations sur les secrets qui vont être crée dans le cluster kube.

Il existe deux façon de faire.

### Transformation à la volée

Dans le manifest de notre `VaultStaticSecret` on va définir des transformations comme cela : 

``` yaml
apiVersion: secrets.hashicorp.com/v1beta1  
kind: VaultStaticSecret  
metadata:  
name: vault-kv-app  
namespace: cpj  
spec:  
type: kv-v2  
  
# mount path  
mount: kvv2  
  
# path of the secret  
path: dev/app-secret  
version: 2  
# dest k8s secret  
destination:  
   name: secretkv  
   create: true  
   transformation:  
     excludes:  
       - .*  
     templates:  
       username:  
         text: |  
           {{ b64dec (get .Secrets "username") }}  
       password:  
         text: |  
           {{ b64dec (get .Secrets "password") }}  
refreshAfter: 30s  
  
# Name of the CRD to authenticate to Vault  
vaultAuthRef: static-auth
```
### Transformation réutilisable

Au lieu de devoir redéfinir nos transformations dans chaque vaultStaticSecret, on peut créer une ressource `SecretTransformation` qui va permettre de reutiliser la transformation dans plusieurs `VaultStaticSecret`.

Il faut créer une `SecretTransformation` : 

``` yaml
apiVersion: secrets.hashicorp.com/v1beta1
kind: SecretTransformation
metadata:
  name: decode-base64-all
  namespace: cpj
spec:
  # Pas d'exclusion ici, on veut tout décoder
  excludes:
    - .*
  sourceTemplates:
    - name: helpers
      text: |
        {{- range $k, $v := .Secrets -}}
        {{ $k }}: {{ $v | b64dec | quote }}
        {{- end -}}
 
```

Puis la référencer dans le `VaultStaticSecret` : 

``` yaml
apiVersion: secrets.hashicorp.com/v1beta1
kind: VaultStaticSecret
metadata:
  name: vault-kv-app
  namespace: cpj
spec:
  type: kv-v2

  # mount path
  mount: kvv2

  # path of the secret
  path: dev/app-secret
  version: 2
  # dest k8s secret
  destination:
    name: secretkv
    create: true
    transformation:
      transformationRefs:
        - name: decode-base64-all
  # static secret refresh interval
  refreshAfter: 30s

  # Name of the CRD to authenticate to Vault
  vaultAuthRef: static-auth
```

### Conclusion

La solution fonctionne mais elle a une limite. Il faut définir à la main les clés qui vont être décodés. Dans le context d'un heln chart il faudra definir dans les values les clés. 

J'avais pensé à faire quelquechose comme cela : 

``` yaml
apiVersion: secrets.hashicorp.com/v1beta1
kind: SecretTransformation
metadata:
  name: decode-base64-all
  namespace: cpj
spec:
  # Pas d'exclusion ici, on veut tout décoder
  excludes:
    - .*
  templates:
    decoded:
    - name: helpers
      text: |
        {{- range $k, $v := .Secrets -}}
        {{ $k }}: {{ $v | b64dec | quote }}
        {{- end -}}
```

ça ne fonctionne pas la sortie dans le secret est une seule clé decoded avec tous les contenu dedans.

On ne peut donc pas itérer et modifier la valeur des clés de manière dynamique. Il faut définir à la main chaque clé et la transformation que l'on veut appliquer.