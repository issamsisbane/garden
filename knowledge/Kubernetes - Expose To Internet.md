# Alternatives

* [[Kubernetes - Expose a Port From Router]]
* [[Cloudflare Tunnels]]

# Create a Cloudflare Tunnel

https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/get-started/create-local-tunnel/

https://developers.cloudflare.com/cloudflare-one/tutorials/many-cfd-one-tunnel/

## Requirements

We need to have a cloudflare domain to be able to use cloudflare tunnels for free.

## Setup

### Install cloudflared

We follow the process to add the apt repo for cloudflare and we launch : 

``` bash
sudo apt-get update && sudo apt-get install cloudflared
```

### Authentication

``` bash
cloudflare tunnel login
```

This command will redirect to our browser where we can login to cloudflare to authenticate. It will install the account certificate in our host in our home directory at `.cloudflared`.

### Create the tunnel

We run : 
```
cloudflared tunnel create ldpi
```

We need to keep the id : 
```
57a6c4c8-2e61-4b27-b5ef-3859a9f6b755
```

It will create a json file in the `.cloudflare` directory with : 
- AccountTag
- TunnelSecret
- TunnelID

We will need the secret for our deployment in kubernetes. But we don't want it to be set as it is in our deployment because we are using gitops and it's push to github so no secret.

So we will create a kubernetes secret for this.

For now we will create the secret manually using : 
``` bash
kubectl create secret generic tunnel-credentials 
\ -n linkding
\ --from-file=credentials.json=/home/issam/.cloudflared/file.json
```

### Associate the tunnel with a DNS Record

![[Pasted image 20250202144421.png]]

We need to add in target : 
```
57a6c4c8-2e61-4b27-b5ef-3859a9f6b755.cfargotunnel.com
```
And make sure proxy is enabled.

### Link the Tunnel to our cluster

We will create a config file for the config of cloudflare.
And we will add in it our secret containing our credentials.json.
For this we will mount the secret as a volume and config file.

Then after commiting and pushing. We can connect to our application at : 
https://ldpi.issamhomelab.org

We can see there is already HTTPS & SSL certificate. This is taken care by cloudflare.