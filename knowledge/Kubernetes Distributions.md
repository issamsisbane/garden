# Kubernetes Distribution Options for Home Lab

Kubernetes is a set of binaries running on a Linux distribution.

Several options exist for setting up a Kubernetes cluster.

## A Kubernetes distribution is a packaged version of Kubernetes that:

- Bundles the core Kubernetes components

- Provides its own installation and management methods

- May modify or optimize certain components

- Often includes additional tools/features

### Kubeadm:

- Used in CKA certification

- Good for deep learning but challenging for long-term management

- Requires manual certificate and CNI management

### MicroK8S:

- Developed by Canonical

- Easy to install but has an opinionated approach

- Bundled add-ons with limited configuration options

### Talos Linux:

- Production-grade, secure, and hardened Kubernetes

- Immutable OS that takes over entire disk

- No SSH access, only API communication

- Considered more advanced and abstracts away installation details

### K3S (chosen for this course):

- Strikes a balance between ease of use and learning opportunities

- Single binary installation on existing Linux systems

- Allows for OS-level troubleshooting and exploration

- Optimized for ARM (good for Raspberry Pi)

- Lightweight and easy to install (one command)

- Powers Rancher, relevant for enterprise Kubernetes management

- Easy to upgrade and add nodes

- Flexible for networking plugins and customization

- K3S is recommended for beginner Kubernetes home labs

- Future courses will cover more advanced options like Talos Linux

- GitOps approach will make it easy to transfer setups between distributions