
# Install Options

There are 3 differents options to install ArgoCD.

## Non HA setup

For evaluation dev/testing envs.

## HA setup
For production. Requires 3 worker nodes.

## Light installation "Core"
Used by admin only, UI and API not installed for end users.
Non-HA by default?

# Privileges options

## Cluster admin privileges

ArgoCD has the cluster-admin access to deploy into the same cluster that runs in.

## Namespaces level privileges

ArgoCD will not be able to deploy applications in the same cluster that runs in.