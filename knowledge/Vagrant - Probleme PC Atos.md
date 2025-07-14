
Lors d'un vagrant up, j'étais bloqué ici : 

```
Clearing any previously set network interfaces
```

J'ai résolu le problème en ajoutant cette ligne : 

```
# AVANT
node.vm.network "private_network", type: "dhcp" # ip: "192.168.33.1#{i}"

# APRES
node.vm.network "private_network", ip: "192.168.56.10#{i}", name: "VirtualBox Host-Only Ethernet Adapter"
```

Enfaite j'ai déjà in adapter VirtualBox qui existait, il suffit de seulement l'utiliser.

![[Pasted image 20250114114424.png]]