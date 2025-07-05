---
title: "Pipeline CI/CD pour une Fonction Lambda"
description: "Ce projet a pour but de mettre en place un pipeline CI/CD pour une fonction AWS Lambda."
lang: "fr"
pubDate: "Oct 06 2024"
heroImage: "/portfolio/projects/cea-cicd-lambda/cea-cicd-lambda-cover.png"
badge: "PERSONNEL"
tags: ["Cloud", "DevOps", "GitHub Actions", "AWS", "CICD", "Cloud Engineer Academy"]
---

*Ce projet m’a permis de découvrir GitHub Actions et AWS ensemble. Franchement très intéressant, et étonnamment simple à mettre en place !*

---

1 — **Vue d’ensemble** </br>
2 — **Étapes** </br>
3 — **Vérification** </br>

---

## 1 - Vue d’ensemble

L’objectif ici est de mettre à jour une fonction Lambda existante dès qu’on pousse du code dans un repo GitHub. On utilise des secrets pour authentifier GitHub Actions auprès d’AWS et déployer la fonction automatiquement.

![](/portfolio/projects/cea-cicd-lambda/GitHub_Actions_Workflow_Lambda_project.png)

Le runner GitHub fait les étapes suivantes :
1. Récupère le code depuis le repo
2. Met en place l’environnement Python et installe les dépendances
3. Configure les identifiants AWS
4. Emballe le code de la Lambda
5. Déploie la fonction Lambda sur AWS

On crée la fonction Lambda via la console AWS pour aller plus vite.

## 2 - Étapes

### 1 - Créer un nouveau repo GitHub

Depuis l’interface GitHub.

### 2 - Ajouter un secret dans les Actions

Il faut stocker nos identifiants AWS de manière sécurisée pour que notre pipeline puisse s’authentifier correctement.

![](/portfolio/projects/cea-cicd-lambda/GitHub_secrets.png)

### 3 - Créer la fonction Lambda

![](/portfolio/projects/cea-cicd-lambda/CI_CD_lambda.png)

### 4 - Ajouter le code de la Lambda dans le repo

Au début, la fonction affiche juste un `"Hello from Lambda"` en réponse à une requête HTTP. On veut changer ce comportement via notre pipeline.

```python
import json

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
```

**Bonne pratique** : toujours inclure un fichier `requirements.txt` pour les dépendances Python.

![](/portfolio/projects/cea-cicd-lambda/lambda_python_directory_structure.png)

On ajoute le fichier de pipeline `.github/workflows/lambda.yaml`

```yaml
name: Deploy AWS Lambda
on:
  push:
    branches:
      - main
    paths:
      - "lambda/*"

jobs:
  deploy-lambda: # Job name
    runs-on: ubuntu-latest # Specify the runner
    steps:
      # 1 - Checkout and get the code in the runner environment
      - uses: actions/checkout@v2

      # 2 - Set up Python environment
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: "3.12"

      # 3 - Install dependencies
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r lambda/requirements.txt

      # 4 - Setup AWS credentials
      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: eu-west-3

      # 5 - Zips the lambda code and updates the lambda function
      - name: Deploy Lambda
        run: |
          cd lambda
          zip -r lambda.zip .
          aws lambda update-function-code --function-name my-test-cicd-lambda --zip-file fileb://lambda.zip
```

On met à jour le code comme ceci : 

``` python
import json

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda changes made from vscode!')
    }
```

### 5 - Commit & Push
On commit et on push, ce qui déclenche automatiquement le pipeline :

![](/portfolio/projects/cea-cicd-lambda/GitHub_actions_push_project_logs.png)

## 3 - Verification

Et là, si on va dans la console AWS, on peut voir que le code de la fonction a bien été mis à jour :

![](/portfolio/projects/cea-cicd-lambda/CI_CD_lambda_updated.png)

C’est un succès ! Notre fonction Lambda a été mise à jour grâce au pipeline GitHub Actions. On peut la supprimer maintenant si on veut.