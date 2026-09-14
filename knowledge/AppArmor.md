# AppArmor

With Seccomp we can prevent or allow entire syscall but we do not have a finegrained control on the syscalls. 

For exemple if we want to prevent writing into a specific directory...

App Armor allow us to do this. It is a linux security module. It allow us to confine a program to limited set of resources.

It is installed by default on most linux machines. To check 

```bash
systemctl status apparmor
```

The appArmor kernel module must be applied on all nodes.

We can check like this : 

![[Kubernetes_-_CKS_38.png]]

App Armor is applied to an application through a profile.

The profile must be loaded into the kernel :

```bash
cat /sys/kernel/security/apparmor/profiles
```

![[Kubernetes_-_CKS_39.png]]

App Armor profiles are simple text files that define what resources can be used by an application (Linux capabilities, network resources, file resources...).

Deny write to all filestystem : 

![[Kubernetes_-_CKS_40.png]]

![[Kubernetes_-_CKS_41.png]]

List app armor profiles loaded : 

![[Kubernetes_-_CKS_42.png]]

Profiles can be loaded in 3 different modes : 
- **enforce** : App Armor will monitor and enforce the rules
- **complain** : No restriction, just log actions as events
- **unconfined** : No restrictions and no log

#### Creating rules

We can use apparmor-utils to easily create new rules : 

```bash
apt-get install -y apparmor-utils
```


We will use this script as an exemple : 

![[Kubernetes_-_CKS_43.png]]

App Armor will monitor the calls made by the script and ask question about what we want to allow or not.

![[Kubernetes_-_CKS_44.png]]

Once we launched the script on an another window we can type S.

![[Kubernetes_-_CKS_45.png]]

We also have the severity here :

![[Kubernetes_-_CKS_46.png]]

To allow we used I for Inherit.

Choices for Commands : 

- **(I)nherit** — le processus enfant (`mkdir`) **hérite du profil du parent** (`add_data.sh`). Pas de nouveau profil créé : `mkdir` tourne avec exactement les mêmes permissions que le script qui l'a lancé.
- **(C)hild** — crée un **profil enfant** (sous-profil, ou « hat ») spécifique à cette exécution. `mkdir` est confiné séparément mais reste rattaché hiérarchiquement au profil parent.
- **(N)amed** — attache l'exécution à un **profil nommé indépendant** (existant ou à créer), complètement séparé du profil parent. Utile si `mkdir` doit avoir ses propres règles réutilisables ailleurs.
- **(X) ix On** — bascule (toggle) l'option **« ix »**, c'est-à-dire le mode « inherit-execute » combiné au choix précédent (ex: Pix, Cix). En gros, ça active/désactive un repli automatique vers l'héritage si le profil dédié ne peut pas s'appliquer. C'est un modificateur, pas un choix de confinement en soi.
- **(D)eny** — **refuse** l'exécution de `mkdir` par ce script. Toute tentative future sera bloquée et loguée.
- **Abo(r)t** — **annule** le scan en cours sans enregistrer les modifications faites jusque-là.
- **(F)inish** — **termine** l'analyse et écrit le profil final dans `/etc/apparmor.d/`.

Choices for file access :
- **(A)llow** — autorise cet accès précis et l'ajoute au profil tel quel (ici `owner rw` sur `/dev/tty`).
- **(D)eny)** (option par défaut, entre crochets) — refuse l'accès. Toute tentative future sera bloquée et loguée.
- **(I)gnore** — ignore cet événement, ne l'ajoute pas au profil et ne le redemandera pas pendant ce scan. Le comportement réel du système (allow/deny) dépendra de ce qui existe déjà ou par défaut.
- **(G)lob** — généralise le chemin en remplaçant une partie par un **glob** (wildcard), par exemple `/dev/tty*` au lieu du chemin exact. Utile si le programme accède à plusieurs fichiers similaires.
- **Glob with (E)xtension** — pareil que Glob, mais en gardant l'extension du fichier fixe (utile pour des chemins du type `/var/log/*.log`).
- **(N)ew** — te permet de **saisir manuellement** un chemin ou motif personnalisé différent de celui proposé.
- **Audi(t)** — ajoute une règle d'**audit**, c'est-à-dire que l'accès sera autorisé mais chaque utilisation sera quand même journalisée (logguée) pour surveillance.
- **(O)wner permissions off** — retire la restriction « owner » (propriétaire uniquement). Par défaut la règle proposée est `owner rw` (seul le propriétaire du fichier a accès) ; cette option enlève cette contrainte pour autoriser plus largement.
- **Abo(r)t** — annule le scan sans sauvegarder.
- **(F)inish** — termine et écrit le profil.

AppArmor ne donne jamais **plus** de droits que les permissions Unix — il peut seulement **restreindre davantage** ce qu'un programme confiné a le droit de faire, même si Unix l'autoriserait. C'est du Mandatory Access Control (MAC) par-dessus le Discretionary Access Control (DAC) classique.

- Tant que tu ne mets pas O, AppArmor **ajoute** une contrainte : « en plus des permissions Unix normales, il faut que ce soit le propriétaire qui accède ».
- Unix `chmod`/`chown` reste inchangé dans les deux cas — AppArmor ne modifie jamais ça, il filtre juste ce que le processus confiné a le droit de faire par-dessus.

We can find our profile has been added running aa-status :

![[Kubernetes_-_CKS_47.png]]

The generated profiles are in `/etc/apparmor.d/` 

![[Kubernetes_-_CKS_48.png]]

If we launch again the script with `data_directory=/opt` it will failed : 

![[Kubernetes_-_CKS_49.png]]

To load an existing profile we use : 

```bash
apparmor_parser /etc/apparmor.d/root.add_data.sh
```

If nothing is printed it means the profile is already loaded.

To disable a profile we do : 

```bash
apparmor_parser -R /etc/apparmor.d/root.add_data.sh
ln -s /etc/apparmor.d/root.add_data.sh /etc/apparmor.d/disable/
```