Le **Vault Injector** (aussi appelé _Vault Agent Injector_) **ne crée pas de `Secret` Kubernetes** comme `Vault Secrets Operator` (VSO) peut le faire.  
Il agit différemment : il **injecte dynamiquement les secrets depuis Vault directement dans le Pod**, **sans créer d’objets `Secret` Kubernetes intermédiaires**. Et ne crée pas de Secret Kubernetes.

---

## 🔍 Fonctionnement du Vault Agent Injector (mode sidecar)

Quand tu actives l’injector via des **annotations** sur ton Pod, il :

1. **Ajoute un sidecar container** au Pod (le Vault Agent)
    
2. Le sidecar :
    
    - Authentifie le pod auprès de Vault (via ServiceAccount + Kubernetes auth)
        
    - Récupère les secrets depuis Vault (avec la policy associée)
        
    - Les **écrit dans un volume partagé** (souvent dans `/vault/secrets/`)
        
3. Ton application peut lire les secrets :
    
    - Sous forme de **fichiers montés dans un `emptyDir` partagé**
        
    - Ou en **variables d’environnement** (facultatif)
        

---

### ✅ Exemple YAML

```
apiVersion: v1
kind: Pod
metadata:
  name: my-app
  annotations:
    vault.hashicorp.com/agent-inject: "true"
    vault.hashicorp.com/role: "my-k8s-role"
    vault.hashicorp.com/agent-inject-secret-config: "secret/data/myapp/config"
spec:
  serviceAccountName: vault-auth
  containers:
  - name: my-app
    image: my-image
    volumeMounts:
    - name: vault-secrets
      mountPath: "/vault/secrets"
  volumes:
  - name: vault-secrets
    emptyDir: {}
```

Cela injectera les secrets dans `/vault/secrets/config`

---

### 🔄 Secrets mis à jour automatiquement ?

- Oui, **le sidecar peut faire du renouvellement automatique** si les secrets sont dynamiques (comme des DB credentials)
    
- Sinon, pour des secrets statiques, tu dois gérer le reload toi-même (ou utiliser un sidecar comme `consul-template`)