---
state: to_complete
tags: ["TECHNOS"]
---

[What is an SSH Bastion? | SSH Bastion host setup](https://goteleport.com/blog/ssh-bastion-host/)

# Qu’est-ce qu’un bastion SSH ? 

Un bastion SSH est un serveur Linux standard accessible via Internet. Ce qui le distingue, c’est qu’il est le **seul** à accepter les connexions **SSH externes**. Pour accéder à une autre machine, un utilisateur doit **d’abord** se connecter au bastion, puis établir une **nouvelle connexion SSH** depuis ce bastion vers la **machine cible**. Ce processus est parfois appelé **saut** et les bastions SSH sont également connus sous le nom de **jump hosts**.

Le **saut** peut être automatisé, ce qui signifie qu’un client SSH peut être configuré pour effectuer ce saut automatiquement.

# Exemples

[[Wallix]]
[[Teleport]]
# Stop using SSH Key ?!

[How to manage SSH keys?](https://goteleport.com/blog/ssh-key-management/)