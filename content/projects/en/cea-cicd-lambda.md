---
title: "CI/CD Pipeline For a Lambda Function"
description: "This project aims to create a CI/CD pipeline for an AWS Lambda Function."
lang: "en"
pubDate: "Oct 06 2024"
heroImage: "/portfolio/projects/cea-cicd-lambda/cea-cicd-lambda-cover.png"
badge: "PERSONAL"
tags: ["Cloud", "DevOps", "GitHub Actions", "AWS", "CICD", "Cloud Engineer Academy"]
---

*This project allowed me to discover GitHub Actions and AWS Together. It was very interesting and surprisingly very simple to setup.*

---

1 — **Overview** </br>
2 — **Steps** </br>
3 — **Verification** </br>

---

## 1 - Overview

The goal of this project is to update an existing lambda Function when code is push in a repository. Secrets will be used to authenticate github actions to AWS to deploy our lambda function.

![](/portfolio/projects/cea-cicd-lambda/GitHub_Actions_Workflow_Lambda_project.png)

**Runner** : 
1. Checks out the code from the repository
2. Setup python envrionement and install dependencies
3. Configure aws credentials
4. Package up our lambda
5. Deploy the lambda to aws

We will create the lambda from aws console to speed up things.

## 2 - Steps 

### 1 - Create a new GitHub repo

Using GitHub website.

### 2 - Create a new actions secret

We need to securely store our aws credentials to authenticate our pipeline with aws.

![](/portfolio/projects/cea-cicd-lambda/GitHub_secrets.png)

### 3 - Create the lambda function

![](/portfolio/projects/cea-cicd-lambda/CI_CD_lambda.png)

### 4 - Add code to our repo for the lambda

Initially, the code of the lambda simply print "Hello from Lambda" in response of HTTP Request. We want to change this behavior using our pipeline to update the code.

``` Python
import json

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
```

**Best practice** is to always include a requirements.txt file for python dependencies.

![](/portfolio/projects/cea-cicd-lambda/lambda_python_directory_structure.png)

We add the code for our pipeline in `.github/workflows/lambda.yaml`

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

We can update our code to : 

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
We commit and  pushes the changes which will trigger the pipeline : 

![](/portfolio/projects/cea-cicd-lambda/GitHub_actions_push_project_logs.png)
## 3 - Verification

Then if we go to the aws console we can seen that the code has been updated :

![](/portfolio/projects/cea-cicd-lambda/CI_CD_lambda_updated.png)

It's a success, we updated our function using GitHub Actions Pipeline. We can now delete our function.
