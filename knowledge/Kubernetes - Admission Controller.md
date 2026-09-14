# Kubernetes Admission Controller

![[Kubernetes_-_CKS_54-1.png]]

By default there are admission controllers in the cluster : 
- AlwaysPullImages
- DefaultStorageClass
- EventRateLimit
- NamespaceExists
- NamespaceAutoProvision (disabled by default)
- ...

We can see admission controllers enabled by default :

```bash
kube-apiserver -h | grep enable-admission-plugins
```

![[Kubernetes_-_CKS_55-1.png]]

To add or disable admission controllers we need to update the flag in the kube-apiserver manifest : 

![[Kubernetes_-_CKS_57.png]]

**NamespaceAutoProvision** and **NamespaceExists** are deprecated and replaced by **NamespaceLifecycle** : prevent resources creation in no existing namespace and prevent the deleting of default namespace.

Exemple of webhook that validate image before running it by a scan using an admission controller built-in kubernetes but not enabled yet.

![[Kubernetes_-_CKS_58.png]]

![[Kubernetes_-_CKS_59.png]]

`admission-configuration.yaml`
```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: AdmissionConfiguration
plugins:
- name: ImagePolicyWebhook
  path: /etc/kubernetes/imgvalidation/imagepolicy-conf.yaml
```

`imagePolicy-conf.yaml`
```yaml
imagePolicy:
  kubeConfigFile: /etc/kubernetes/imgvalidation/kubeconf.yaml
  allowTTL: 50
  denyTTL: 50
  retryBackoff: 500
  defaultAllow: false ## If true, if the webhook fail it allows the creation of the pod
```

`kubeconf.yaml`
```yaml
apiVersion: v1
kind: Config
clusters:
- cluster:
    certificate-authority: /etc/kubernetes/imgvalidation/webhook.crt
    server: https://image-checker-webhook.default.svc:1323/image_policy
  name: checker_webhook
contexts:
- context:
    cluster: checker_webhook
    user: api-server
  name: checker_validator
current-context: checker_validator
preferences: {}
users:
- name: api-server
  user:
    client-certificate: /etc/kubernetes/pki/front-proxy-client.crt
    client-key: /etc/kubernetes/pki/front-proxy-client.key
```

To add it to the kube-apiserver : 

Edit `/etc/kubernetes/manifests/kube-apiserver.yaml`:

```bash
cp /etc/kubernetes/manifests/kube-apiserver.yaml /opt/kube-apiserver.yaml.bak
vi /etc/kubernetes/manifests/kube-apiserver.yaml
```

**1. Enable the admission plugin:**

```yaml
    - --enable-admission-plugins=NodeRestriction,ImagePolicyWebhook
```

**2. Add the admission control config file:**

```yaml
    - --admission-control-config-file=/etc/kubernetes/imgvalidation/admission-configuration.yaml
```

**3. Mount the imgvalidation directory:**

Add to `volumes`:

```yaml
    - name: imgvalidation
      hostPath:
        path: /etc/kubernetes/imgvalidation
        type: Directory
```

Add to `volumeMounts`:

```yaml
    - name: imgvalidation
      mountPath: /etc/kubernetes/imgvalidation
      readOnly: true
```

**4. Verify the API server is running:**

```bash
kubectl get pods -n kube-system
```

**5. Test an Image**

![[Kubernetes_-_CKS_60.png]]

#### Types of Admission controllers

- Validating Admission controller : only perform checks (NamespaceExists)
- Mutating Admission controller : Can update the ressource before creation (DefaultStorageClass)

Mutating A C are ran before Validating A C.

#### Custom Admission Controller

There are special admission controller allowing us to create customs : 
- MutatingAdmissionWebhook
- ValidatingAdmissionWebhook

It will point to an external admission Webhook server inside or outside the cluster.

The request in the api-server will go through all enabled builtin admission controller and the to our custom ones.

The apiserver pass an AdmissionReview object to our Admission Webhook Server and it respond with and Admission Review object.

![[Kubernetes_-_CKS_52-1.png]]

We just need to create this resource no need to touch the manifest of the apiserver.

If it is a service inside the cluster : 

![[Kubernetes_-_CKS_53-1.png]]

Instead it will be just :
```yaml
clientConfig:
  url: https://my-webhook-server
```