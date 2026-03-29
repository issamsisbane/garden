Le Scheduler va décider ou un pod va être déployé. Le choix est fait selon les nodes disponibles. 

Il est possible d'influencer ce choix avec des annotations sur le node et sur le pod : 

```sh
kubectl label node <nom-du-node> disktype=ssd
```

Sur le pod : 
``` yaml
spec:
  nodeSelector:
    disktype: ssd
```