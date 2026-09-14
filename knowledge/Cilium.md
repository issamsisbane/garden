# Cilium

Open-source software for providing and securing network connectivity between container applications.

Designed for modern microservices, it provides network security through extended Berkeley Packet Filter (eBPF).

Pod-to-pod encryption is one of its standout features.

![[Kubernetes_-_CKS-20.png|206]]
![[Kubernetes_-_CKS-21.png|198]]

![[Kubernetes_-_CKS-22.png|268]]

## Architecture

Cillium use eBPF technology which operates directly in the linux kernel.
Cillium controls how pods communicate with each other within the cluster.

![[Kubernetes_-_CKS-23.png|327]]

![[Kubernetes_-_CKS-24.png|326]]
![[Kubernetes_-_CKS-25.png|327]]

We can follow the documentation. The cillium cli does everything for us. Configuring the cni and install cillium through helm.

## Validate the Setup

- Check connectivity between the pods, **in a new terminal window run the following command**:
    
    ![](https://imgur.com/cdxKtvO.png)
    
    ```
    watch kubectl exec -it curlpod -- curl -s http://nginx
    ```
    
    The watch curl command should return the HTML content of the NGINX welcome page, indicating that the client pod can access the NGINX pod.
    
- Run a bash shell in one of the Cilium pods with `kubectl -n kube-system exec -ti ds/cilium -- bash` and execute the following commands:
    
- Check that WireGuard has been enabled (number of peers should correspond to a number of nodes subtracted by one):
    
    ```
    cilium-dbg status | grep Encryption
    ```
    
- Install tcpdump
    
    ```
    apt-get update
    apt-get -y install tcpdump
    ```
    
- Check that traffic is sent via the `cilium_wg0` tunnel device is encrypted:
    
    ```
    tcpdump -n -i cilium_wg0 -X
    ```
    
    - Here we are using `tcpdump`` to capture and display detailed network packets on the cilium_wg0 interface.
        
    - The -n option avoids DNS lookups, and the -X option shows packet content in both hexadecimal and ASCII format.
        
    - Via tcpdump, you should see the traffic between the pods.
        
    - We see requests from `curlpod` to `nginx` and responses from `nginx` to `curlpod` in `tcpdump` output.
        
        ![](https://i.imgur.com/RHcazJ0.png)


![[Kubernetes_-_CKS-27.png]]

We can install tcpdump on it and verify the traffic is encrypted.
