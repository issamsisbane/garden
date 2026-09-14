---
creation date: 2026-08-26-22:35:02
modification date: 2026-08-26-22:35:02
imageNameKey: TLS_Certificate_(Kubernetes)
---
# TLS Certificate (Kubernetes)

## Users

![[Kubernetes_-_CKS_2.png]]


Generer la clé privée de l'user admin
```bash
openssl genrsa -out admin.key 2048
```

Generer la csr
```bash
openssl req -new -key admin.key -subj "/CN=kube-admin/OU=system:masters" -out admin-csr
```

Signer le certificat signé par le CA du cluster
```bash
openssl x509 -req -in admin.csr -CA ca.crt -CAkey ca.key -out admin.crt
```

Kube-api server 

![[Kubernetes_-_CKS_3.png]]


### Certificate API

0. User generate a key and a csr with his name as CN and sent it to an admin
	CN=username O=groups
	
	```bash
	openssl genrsa -out user.key 2048
	openssl req -new -key user.key -out user.csr -subj "/CN=alice/O=devs"
	```
0. Admin take the csr and create CertificateSigningRequest Object
1. Review Requests (admin)
2. Approve Requests (admin)
3. Share certs to Users


View the certificate :
```bash
kubectl get csr jane -o yaml
```

The controller manager is responsible for : 
- CSR-APPROVING
- CSR-SIGNING

![[Kubernetes_-_CKS_4.png]]

The CSR :

```yaml
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: akshay  
spec:
  expirationSeconds: 3600
  request:  LS0tLS1CRUdJTiBDRVJUSUZJQ0FURSBSRVFVRVNULS0tLS0KTUlJQ1ZqQ0NBVDRDQVFBd0VURVBNQTBHQTFVRUF3d0dZV3R6YUdGNU1JSUJJakFOQmdrcWhraUc5dzBCQVFFRgpBQU9DQVE4QU1JSUJDZ0tDQVFFQXRTdWkwMDhnQU94b0ZWbkZQcTcwVWJMT29na204cGR2aXR4ZnNGU0JUWjQ1CkJvQS9ObzFMd0dhYnovU0laUU9DN2ZDT3o5dU1qRDNjdGlzU1VaVHZENzJKVGhhekRpWnpXaDJBRjFNMWJmQ3EKWDYwN3VnendvSUtoMjgyUnVIQzNwQmlFNGtSOFlLZyt3K3hjZ1duVDZZRGV1cms4dEt5TDlDZHdRcERlUHpIUgpiM2dkOXd6UzM1WkdXUkJqb3kyTVEyeHVNQktZNUdhanVrUWwvWEJhNWRQOCttcGtXZDd4ekpyamZmbUc3eUlJCmpVVmg1M0ZRWUhENFBWaGh3allCNmhHekNDdlpIUEdhWUpMSnM0UENLTG1CRUVQN2hYZnpvWXp0T2psRXhuMjUKaThmVWN6MUJrNzRYTjlqZHlLWWU2L3NWU1FBWW5ZaUtvekdCYThLckZRSURBUUFCb0FBd0RRWUpLb1pJaHZjTgpBUUVMQlFBRGdnRUJBSno1Tnlac05MdXdNVEQrblJTblNybDhiRTQ5UXZkU2hiU0RzK2pYaThoMS83VVF0YzljCng3ejBiWmlUREpwS0xWK2FrNFdrc0ROeFk2NFVwUW5zd2R1QzhUMnhUSzZhcHVtdC9FakZQaDdaMkxkb01aZWUKRGdWdCsrY2JvbFJwazZYaDkzOHpTaFRFYWFiREw1VFlqYmxsTUd4VU5wb2NzYzdnN0VIam5HOWVxbnRFYlFwNwo4K0I3R0xmQ3JidkdRMzhzdklvNWlXYUhNVy9NQjJGQkt1VXJDV2phdzNnZFV4T3RYZXNDR3JVMDJnV2Q3S3pNCmcyMC9MMkMvR0t0NVVUeWdUR290SDV1OTVNYU9URy9TSjM2QWpYcGw3ZU4xd04zM1dGUkFEMzQ0MVhxbFlWU28KTG52S2RXdTRsb2NVMFpxNGxzTFRIMnNxY01EcWxXM1N0RWc9Ci0tLS0tRU5EIENFUlRJRklDQVRFIFJFUVVFU1QtLS0tLQo=
  usages:
      - "client auth"
  username: akshay
  signerName: "kubernetes.io/kube-apiserver-client"
```

Approve a csr :
```bash
kubectl certificate approve akshay
```

![[Kubernetes_-_CKS_5.png]]

![[Kubernetes_-_CKS_6.png]]

In context we can specify a namespace.

```bash
kubectl config view
```