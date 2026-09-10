https://artifacthub.io/packages/helm/forgejo-helm/forgejo#external-database


I wanted a lightweight forge for my homelab where I could tests things.

I have a notes setup using obsidian. I have different vaults and I store them in different places : 
- Personal => store in proton-drive
- Work General => stored in company account one-drive
- Work Client Specific => stored in the client shared drive

This currently works but I wanted to use git for my personal vault.

I already have a setup for my shared notes, you can find it here : 

But I wanted to have it in git and I have some personal stuff I don't want to be in a public github repo. 

Thats another reason why I wanted to setup a private registry.

For now I'm just experimenting, but later I will implement redundancy, backup strategy...

The critera where : 
- easy to use and install
- forge
- runner / actions
- FOSS
- well maintained

My first choice was gitea. I install it, but after a few research I found it it wasn't FOSS anymore. So alternative then is forgejo a fork of gitea totally FOSS. 

It has the same functionnality so perfect for me.

![[homelab-forgejo-architecture.excalidraw]]

I installed CNPG on my cluster previously so I set up a postgresql database for my forgejo instances.

I have only one forgejo instances because it just for me so I don't need a HA setup. But it would be interesting to see what is happening with an ha setup.

Firstly I started to follow this documentation https://forgejo.org/docs/latest/admin/installation/docker/ and adapt it to kubernetes. 

Finally, I found there was a maintained helm charts so it save some trouble to directly use it.

I did a pretty simple configuration at first and I will improve it with time and my needs.

The configuration is quite straighforward. I had some trouble with configuring the database tough.

Indeed, in the chart configuration there is a part dedicated to configure external database : 

![[Pasted image 20251111133156.png]]
https://artifacthub.io/packages/helm/forgejo-helm/forgejo#external-database

I created a cluster with CNPG and it generated for me the secret to connect to the database. So I juste specified it with `additionalConfigSources` just like show in the documentation. 
But I had errors with the deployment. I found out reading the whole documentation that the value of the secret must be in capital keys. But CNPG generate a secret with lower case caracters.

So I decided to set use the env variables instead : 
``` yaml
additionalConfigFromEnvs:
- name: FORGEJO__DATABASE__PASSWD
  valueFrom:
	secretKeyRef:
	  name: forgejo-cnpg-cluster-app
	  key: password
- name: FORGEJO__DATABASE__NAME
  valueFrom:
	secretKeyRef:
	  name: forgejo-cnpg-cluster-app
	  key: dbname
- name: FORGEJO__DATABASE__USER
  valueFrom:
	secretKeyRef:
	  name: forgejo-cnpg-cluster-app
	  key: user
- name: FORGEJO__DATABASE__HOST
  valueFrom:
	secretKeyRef:
	  name: forgejo-cnpg-cluster-app
	  key: host
- name: FORGEJO__DATABASE__DB_TYPE
  value: postgres
```
This solution worked !

# Access 

![[Pasted image 20251111133614.png]]

To test it, I used a portforward on port 3000 to verify the instance is accessible.

There is a secret in the namespace created by one of the initContainers for the admin user and its password.

I could connect successfylly to the instance !
![[Pasted image 20251111133746.png]]
# Mails

Sendmail is already in the gitea image.
![[Pasted image 20251111133545.png]]


# Storage

PVC + Backup using the forgejo dump command.