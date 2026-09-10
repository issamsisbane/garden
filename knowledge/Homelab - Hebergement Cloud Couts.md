[[Kubernetes - FinOps]]

Je reflechissais à déployer un cluster dans le cloud et je me suis renseigné sur les couts.

# Comparatif 

Coûts mensuels pour un cluster Kubernetes HA avec 3 nœuds maîtres (2 vCPU, 4 Go de RAM) et 2 nœuds workers (4 vCPU, 8 Go de RAM) sur différents fournisseurs cloud, en tenant compte des tarifs standards pour une utilisation en France.

| Fournisseur           | Type de machine                           | Tarif par machine               | Total pour 5 machines | Remarques                                 |
| --------------------- | ----------------------------------------- | ------------------------------- | --------------------- | ----------------------------------------- |
| **[[Hetzner Cloud]]** | CX22 (2 vCPU, 4 Go, 40 Go SSD)            | 3,79 € / mois                   | 18,95 € / mois        | Très compétitif pour des besoins basiques |
| **OVHcloud**          | Essential DB1-4 (2 vCPU, 4 Go, 80 Go SSD) | 51,26 € / mois                  | 256,30 € / mois       | Offre robuste, mais plus chère            |
| **AWS EC2**           | t3.medium (2 vCPU, 8 Go)                  | ~0,0416 $ / h (~30,08 $ / mois) | ~150,40 $ / mois      | Tarifs On-Demand, plus élevés             |
| **Azure**             | D2s v3 (2 vCPU, 8 Go)                     | ~0,096 $ / h (~69,12 $ / mois)  | ~345,60 $ / mois      | Tarifs standard, plus élevés              |
# Comparatif Avec Spot instances

### ✅ AWS (règion EU West 1 / Paris ou Dublin équivalent)

On prend l’exemple des types utilisés auparavant :

- **t3.medium** (2 vCPU / 4 Go, pour masters). Spot = ~ 0,015 $/h soit ~ 10,95 $/mois ([Reddit](https://www.reddit.com/r/aws/comments/t33kf4?utm_source=chatgpt.com), [sparecores.com](https://sparecores.com/server_prices?page=4&regions=eu-west-2&utm_source=chatgpt.com)).
    
- **t3a.medium** (2 vCPU / 4 Go, workers éventuellement ARM) : Spot = ~ 0,0148 $/h soit ~ 10,70 $/mois ([GitHub](https://github.com/YakDriver/aws-ec2-instance-types/blob/main/results/eu-west-1.md?utm_source=chatgpt.com)).
    

|Rôle|Spot $/h|Spot €/mois (≈730h)|
|---|---|---|
|Master (3×)|0,015 $/h|~ 3 × 10,95 $ = 32,85 $ → ~31 €|
|Worker (2×)|0,0148 $/h|~ 2 × 10,70 $ = 21,40 $ → ~20 €|
|**Total**|—|**≈ 51 €/mois**|

Comparé au coût On‑Demand (≈150 $ ≈≈137 €), tu peux économiser jusqu’à **60 % de réduction** sur AWS via Spot.

---

### ✅ Azure (West Europe, VM d’environ 2 vCPU / 4 Go, type E2 ou B)

- Exemple : **E2d_v4/v5 spot** : ~0,026 $/h soit environ **19 $/mois** ([sparecores.com](https://sparecores.com/server_prices?page=11&regions=westeurope&utm_source=chatgpt.com), [Reddit](https://www.reddit.com/r/aws/comments/t33kf4?utm_source=chatgpt.com), [Reddit](https://www.reddit.com/r/aws/comments/bp2p7b?utm_source=chatgpt.com)).
    
- Cela reste environ **2 à 3× plus cher** qu’AWS spot pour la même configuration, mais reste bien inférieur au tarif On‑Demand d’Az

Voici une estimation du **coût mensuel sur Outscale** pour un cluster Kubernetes HA (3 nœuds maîtres + 2 nœuds workers), d'après les tarifs publics disponibles en Europe (region eu‑west‑2) [Reddit+13en.outscale.com+13fr.outscale.com+13](https://en.outscale.com/pricing/aws-compatible-vm-pricing/?utm_source=chatgpt.com) :

---

### ⚙️ Tarification horaire des VM Outscale (Europe)

- **t2.medium** (2 vCPU / 4 Go RAM) : **0,060 €/h**
    
- **c4.large** (2 vCPU? erreur — en fait 4 vCPU / 8 Go RAM) : **0,100 €/h** [F6S+8en.outscale.com+8lemondeinformatique.fr+8](https://en.outscale.com/pricing/aws-compatible-vm-pricing/?utm_source=chatgpt.com)
    

---

### 💳 Estimation des coûts mensuels (~730 heures par mois)

|Rôle|Config VM|Tarif €/h|Coût mensuel par VM|Quantité|Total mensuel|
|---|---|---|---|---|---|
|Masters|t2.medium|0,060 €|~43,8 €|3|~131,4 €|
|Workers|c4.large|0,100 €|~73 €|2|~146 €|
|**Cluster total**|—|—|—|—|**~277 € / mois**|