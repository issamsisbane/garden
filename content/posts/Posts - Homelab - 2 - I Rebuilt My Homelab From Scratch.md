𝐈 𝐑𝐞𝐛𝐮𝐢𝐥𝐭 𝐌𝐲 𝐇𝐨𝐦𝐞𝐥𝐚𝐛 𝐅𝐫𝐨𝐦 𝐒𝐜𝐫𝐚𝐭𝐜𝐡  
  
My first homelab worked. K3s was running, Flux was deploying applications, everything was stable.  
  
And yet I felt like I was cheating.  
  
K3s is opinionated by design. Indeed, it bundles the datastore, the load balancer, the CNI, all of it into a single binary. That's great for getting started and for small infrastructure.  
  
But after a while I realised I couldn't tell you what kubeadm actually does, how etcd is bootstrapped, or why a CNI plugin makes the choices it makes. I was operating a cluster without really understanding it.  
  
I had this realization just after passing the CKA certification. My homelab is by definition the place where I can learn and break things. So it wasn't a good choice for me to use K3S directly.  
  
𝗧𝗵𝗲 𝗗𝗲𝗰𝗶𝘀𝗶𝗼𝗻  
  
I wiped everything and started over. The new stack:  
  
- kubeadm for cluster bootstrapping  
- Kubespray to automate the deployment across all three nodes with Ansible  
- Calico as the CNI, explicitly configured, not bundled  
  
The goal wasn't to make it harder. It was to make it legible. Every component visible, every choice deliberate.  
  
𝗪𝗵𝗲𝗿𝗲 𝗧𝗵𝗶𝘀 𝗦𝗲𝗿𝗶𝗲𝘀 𝗦𝘁𝗮𝗿𝘁𝘀  
  
Before getting to Kubernetes, there's a step most tutorials skip: actually installing the OS on three different machines, headlessly, reproducibly. That's what this article covers.  
  
How I went from three blank laptops to three identical, network-reachable Ubuntu nodes using a single cloud-init file.  
  
It's less glamorous than deploying workloads. But if you ever have to rebuild a node at 11pm, you'll be glad you automated this part.  
  
---  
  
Read the full article here : [https://lnkd.in/dp7gAD8a](https://lnkd.in/dp7gAD8a)

Homelab - 2 / 3

![[homelab-migration.png]]