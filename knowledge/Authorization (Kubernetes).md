# Authorization (Kubernetes)

## Cluster

### Roles

```
kubectl api-resources --namespaced=true
```

### ABAC

```
  --authorization-policy-file=/path/to/abac-policy.jsonl
  --authorization-mode=Node,RBAC,ABAC
```

```json
{"apiVersion": "abac.authorization.kubernetes.io/v1beta1", "kind": "Policy", "spec": {"user": "system:serviceaccount:default:john", "namespace": "default", "resource": "pods", "apiGroup": "*" , "readonly": true}}
```

## Kubelet Authorization