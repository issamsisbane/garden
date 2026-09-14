# Kubernetes - Pod Security Admission

It must be easy to use.

Advanced use case must go to PAC (policy-as-code) external solutions such as :
- k-rail
- kyverno
- OPA

Pod Security is a built-in admission controller enabled by default.

PSA : Pod Security Admission

PSA as namespaced scope. To enable it on a namesapce we need to add a label : 

```bash
kubectl label ns payroll pod-security.kubernetes.io/<mode>=<security standard>
```

There are builtins security profiles : 

| Security Standard | Description                  |
| ----------------- | ---------------------------- |
| Privileged        | Unrestricted policy          |
| Baseline          | Minimally restrictive policy |
| Restricted        | Heavily restricted policy    |

| Mode    | On Violation                |
| ------- | --------------------------- |
| enforce | Reject pod                  |
| audit   | Record in audit logs        |
| warn    | Trigger user-facing warning |
![[Kubernetes_-_CKS_55-2.png]]

We can add exceptions using a configmap for the validating webhook.

```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: AdmissionConfiguration
plugins:
  - name: PodSecurity
    configuration:
      apiVersion: pod-security.admission.config.k8s.io/v1
      kind: PodSecurityConfiguration
      defaults:
        enforce: baseline
        enforce-version: latest
        audit: restricted
        audit-version: latest
        warn: restricted
        warn-version: latest
      exemptions:
        usernames: []
        runtimeClassNames: []
        namespaces: [my-namespace]
```