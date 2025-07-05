
We define the volume at the pod level and we use the volumeMounts to attache the volume to the container.

# Types

## EmptyDir
Several containers in the pod can access the same storage.
When the pod is deleted, the volume will also be deleted.

## Persistent Storage

### Persistent Volume

It place of storage. 
Example : 500gb

### Persistent Volume Claim

Its a claim of a certain amount of a persistent volume.
Example : I need 20 gb of the pv 500gb

#### Create only a pvc
We can also create a claim and kubernetes will provision automatically the pv.
In order to do this, it will be using a StorageClass. If we don't specify one then it will use the default one.
We need to be using the pvc to have a pv provision by kubernetes in this case

### Storage class

It exists many storage class depending of our infrastructure and what we want to do.
local path for [[Rancher Desktop]]

### Access mode

Define what access the pods has to the pvc/