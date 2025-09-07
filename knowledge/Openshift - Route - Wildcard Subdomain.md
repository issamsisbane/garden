[How to configure OpenShift ingress wildcard policy - Red Hat Customer Portal](https://access.redhat.com/solutions/5220631)

The Ingress Operator will use WildcardPolicy to configure the environment variable ROUTER_ALLOW_WILDCARD_ROUTES in the OpenShift Router.

Modify default ingresscontroller to allow wildcard policy. 

Below lines needs to be added under default ingresscontroller spec:

```
spec:
  replicas: 2
  routeAdmission:
	wildcardPolicy: WildcardsAllowed
```

Check ingress operator status. Ingress operator should be in Available state after making above change.

Create a DNSRecord resource with following resource definition:

```
apiVersion: ingress.operator.openshift.io/v1
kind: DNSRecord
metadata:
  labels:
	ingresscontroller.operator.openshift.io/owning-ingresscontroller: default
  name: hello-openshift
  namespace: openshift-ingress-operator
spec: 
  # openshift.example.com is my base domain and ocp45 is my cluster ID
  dnsName: '*.openshift.apps.ocp45.openshift.example.com.'
  recordTTL: 30
  recordType: CNAME
  targets:
	 # Target should be the ELB DNS and all worker and master instances should be added to this ELB
	- xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx-1111111111.us-west-2.elb.amazon.com
```

Deploy a sample application in your OpenShift cluster:

```
# oc new-project hello-openshift
# oc new-app httpd
```

Create a route resource with the following definition:

```
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: hello-openshift
spec:
  # I have created a wildcard DNSrecord ‘*.openshift.apps.ocp45.openshift.example.com’ earlier         
  host: data.openshift.apps.ocp45.openshift.example.com
  # wildcardPolicy should be ‘Subdomain’
  wildcardPolicy: Subdomain
  port:
	targetPort: 8080-tcp
  to:
	kind: Service
	name: httpd
	weight: 100
```

Check whether the route has been admitted or not:
```
# oc get route -oyaml | grep -A 5 'conditions'
```

Try to access the route:
```
# curl http://data.openshift.apps.ocp45.openshift.example.com 
```