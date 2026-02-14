Openshift assigne par défaut un utilisateur dans un pod. 
Cet utilisateur est attribué selon un certain range d'id fourni pour le project. Ce range peut être trouvé dans les annotations du project :

![[Pasted image 20250811103003.png]]

Il peut arriver que l'image que l'on va utiliser, configure déjà un utilisateur. Il faudra donc le modifier pour utiliser un id du range.

The UID and GID range follow the format <first_id>/<id_pool_size> or <first_id>-<last_id>
