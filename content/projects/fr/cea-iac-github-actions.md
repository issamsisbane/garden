---
title: "Tester un Template CloudFormation avec GitHub Actions"
description: "Ce projet vise à créer un pipeline GitHub Actions pour tester un template CloudFormation IaC avant fusion dans la branche main."
lang: "fr"
pubDate: "Oct 05 2024"
heroImage: "/portfolio/projects/cea-iac-github-actions/actions.png"
badge: "PERSONNEL"
tags: ["Cloud", "DevOps", "GitHub Actions", "AWS", "CICD", "Cloud Engineer Academy"]
selected: true
---
*Ce projet m’a énormément appris. C’était super intéressant de voir qu’on pouvait valider du code IaC **avant** de le fusionner dans la branche main. Franchement, je n’y avais jamais pensé avant. Le code du projet est dispo ici.*

---

1 — **Vue d’ensemble** </br>
2 — **Étapes** </br>
3 — **Conclusion** </br>

---

## 1 - Vue d’ensemble

L’objectif de ce projet est de créer un **workflow GitHub Actions** qui automatise la création d’un **bucket S3** à l’aide d’un **template CloudFormation**, et de tester ce déploiement au sein d’une **Pull Request (PR)**. Le but, c’est de valider le template **avant** qu’il ne soit mergé dans la branche principale.

![](/portfolio/projects/cea-iac-github-actions/GitHub_Actions_Workflow_PR_project.png)

- Lorsqu’un dev crée une PR pour merger vers `main`, le workflow va :
    - Utiliser le template CloudFormation pour créer un **bucket S3**.
    - Poster le résultat dans la PR avec le **nom du bucket**.
    - Une fois la PR mergée, le workflow va **supprimer la stack** (et le bucket), ce qui nettoie les ressources automatiquement.

Ce mécanisme nous permet de **tester notre code IaC** dans la PR, donc avant qu’il parte en prod. Super pratique pour éviter d’introduire des erreurs dans l’environnement principal.

En **prod**, un autre workflow (déclenché depuis la branche main) pourrait se charger du déploiement final dans un environnement dédié.

On utilise ici le repo GitHub du [projet précédent]().

---

## 2 - Étapes

### Étape 1 : Création d’une Pull Request

Une fois qu’une nouvelle branche est créée, le dev ouvre une **pull request**. Ça déclenche le workflow qui tente de créer un bucket S3 via le template CloudFormation.

### Étape 2 : Gestion des erreurs

Dès le premier run, le workflow a levé une erreur à cause d’une **mauvaise indentation** dans le template CloudFormation.

![](/portfolio/projects/cea-iac-github-actions/GitHub_actions_pull_pr_project_logs_error.png)

- Les logs ont pointé vers la structure incorrecte du template. Une fois corrigée, on a relancé le pipeline.

### Étape 3 : Validation réussie et création des ressources

Après la correction, le pipeline s’est déroulé sans souci. Le **bucket S3** a bien été créé, et un message de validation a été posté dans la PR, avec le nom du bucket.

![](/portfolio/projects/cea-iac-github-actions/GitHub_actions_pull_pr_project_passed_validation.png)

- **Stack CloudFormation** créée avec succès :

![](/portfolio/projects/cea-iac-github-actions/GitHub_actions_pull_pr_project_cloudformation_stack_created.png)

- **Bucket S3** bien créé :

![](/portfolio/projects/cea-iac-github-actions/GitHub_actions_pull_pr_project_s3_bucket_created.png)

### Étape 4 : Le job de cleanup ne s’exécute pas

Après merge de la PR, on a remarqué que le **job de nettoyage** (suppression du bucket et de la stack) **ne s’était pas déclenché**. Il a donc fallu revoir la config du workflow.

### Étape 5 : Mise à jour du workflow

Pour corriger ça, on a mis à jour la config avec ce bloc :

``` yaml
on:
  pull_request:
    paths:
      - "cloudformation/**"
    types: [opened, synchronize, reopened, closed]
```

Ce bloc permet de déclencher le workflow sur des événements PR spécifiques (opened, synchronized, reopened, and closed) et uniquement quand les fichiers `cloudformation/` sont modifiés.

### Étape 6 : Éviter la validation lors du merge

On ne veut pas que la validation du template se fasse après le merge. On a donc ajouté une condition dans le job `validate-cfn` :


``` yaml
jobs:
  validate-cfn:
    if: github.event.pull_request.merged == false
```

Comme ça, la validation ne tourne que si la PR n’est pas encore mergée.

### Étape 7 : Cleanup automatique réussi

Une fois les corrections appliquées, tout a bien fonctionné : le job de nettoyage s’est lancé après le merge, et la stack + le bucket ont bien été supprimés.

![](/portfolio/projects/cea-iac-github-actions/GitHub_actions_pull_pr_project_cleanup_job.png)

Et voilà : on a pu valider le template dans la PR, merger en toute confiance, et nettoyer les ressources juste après.
Après la création d'une nouvelle branche et d'une pull request, notre workflow a trouvé une erreur dans notre template cloudformation.

## 3 - Conclusion 

Ce projet montre bien **la puissance de GitHub Actions** couplée à **CloudFormation** pour automatiser les tâches infra.

Avec ce workflow, on peut :

- **Valider le code IaC** dès les pull requests.
- **Assurer la validité du template** avant qu’il parte en production.
- **Créer et supprimer automatiquement** les ressources, gardant un environnement propre.

En prod, ce genre de setup serait encore plus costaud, avec des workflows séparés pour le staging et la prod.

Et surtout : automatiser la **validation** et le **nettoyage** d'infrastructure rend les changements bien plus sûrs, reproductibles et simples à gérer, peu importe l’environnement.

Honnêtement, je ne m’étais jamais dit qu’on pouvait tester de l’IaC comme ça dans une PR. Super découverte !