https://fluxcd.io/flux/get-started/

We are going to install [[Flux]] in our [[K3S]] Cluster.

# Create a classic GitHub Token

We need to create a GitHub personal access token with repo permissions. 
We need to export these variables : 

```sh
export GITHUB_TOKEN=<your-token>
export GITHUB_USER=<your-username>
```


I created a script to load them because if we just export it. We would lose it when closing the shell. I don't know if I will need it earlier. For sure I don't commit it to git.

We install the flux cli tool : 
```
brew install fluxcd/tap/flux
```

# Install flux onto the cluster
```
flux bootstrap github \
  --owner=$GITHUB_USER \
  --repository=pi-cluster \
  --branch=main \
  --path=./clusters/staging \
  --personal
```

This command allow to configure in which repository and branch we wants flux to monitor. Then Flux will create the manifest file in the repo to manage itself.

We can manage several clusters with the same GitOps repostiory (production, staging..)

# Results

- Flux creates necessary manifests in the GitHub repository

- New namespace 'flux-system' is created on the cluster with Flux components

- GitOps controller is now active on the cluster
From now the GitOps Controller is installed in our cluster. And We can start deploying things.