𝐇𝐨𝐰 𝐞𝐭𝐜𝐝 𝐭𝐮𝐫𝐧𝐬 𝐦𝐲 𝐭𝐢𝐧𝐲 𝐡𝐨𝐦𝐞𝐥𝐚𝐛 𝐢𝐧𝐭𝐨 𝐚 𝐫𝐞𝐚𝐥-𝐰𝐨𝐫𝐝 𝐊𝐮𝐛𝐞𝐫𝐧𝐞𝐭𝐞𝐬 𝐜𝐥𝐮𝐬𝐭𝐞𝐫
  
A production-grade Kubernetes environment must run as a cluster of several nodes to ensure resilience. If one node goes down, the others take over the workload.  
  
𝗡𝗼𝗱𝗲 𝗮𝘄𝗮𝗿𝗲𝗻𝗲𝘀𝘀  
  
For this to work, the nodes in the cluster need to always be aware of the current state of the system :  
  
• Which resources exist in the cluster?  
• Which workloads are running on which nodes?  
• What is the health of each node and its pods?  
  
𝗪𝗵𝗮𝘁 𝗶𝘀 𝗲𝘁𝗰𝗱?  
  
This is where etcd comes in. Etcd is a distributed key-value store that holds all the information about a cluster and its state.  
  
Etcd uses the Raft consensus algorithm, which means it runs as a cluster of nodes (quorum).  
  
A leader is elected to handle writes, while the other members acknowledge and replicate the data. If the leader node goes down, the remaining members automatically elect a new leader, ensuring the cluster keeps running consistently.  
  
𝗠𝘆 𝗘𝘅𝗽𝗲𝗿𝗶𝗲𝗻𝗰𝗲  
  
In my homelab, I first started with a single-node cluster using k3s, which defaults to SQLite as the datastore. But when I expanded to a 3-node cluster, I migrated to etcd to make the cluster resilient and closer to a production-grade setup.  
  
---  
  
You can read the whole article here : [https://lnkd.in/enEBA9xM](https://lnkd.in/enEBA9xM)  
  
Homelab - 2 / 2

![[1757572804546.jpg]]