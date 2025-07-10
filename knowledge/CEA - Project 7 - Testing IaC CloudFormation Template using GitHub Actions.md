---
state: published
tags: ["Cloud Academy"]
---
## 1 - Overview

This project is focused on creating a **GitHub Actions Workflow** that automates the process of creating an **S3 bucket** using a **CloudFormation** template and testing it within a **Pull Request (PR)**. The goal is to validate if the CloudFormation template is correctly written and functional before merging the PR into the main branch.
![[GitHub_Actions_Workflow_PR_project.png]]
- Once the developer creates a pull request to merge into the main branch, the workflow will:
    - Use the CloudFormation template to create an **S3 bucket**.
    - Post the result of the CloudFormation operations in the **PR** discussion, along with the **bucket name**.
    - Upon merging the PR, the workflow will **delete the stack** (and the S3 bucket), cleaning up the resources.

This workflow allows us to test the CloudFormation code within the **pull request** before it's merged into the main branch. It ensures that the infrastructure code is working properly and prevents errors from being deployed in production.

In a **production** environment, a separate workflow triggered on the main branch would handle deploying the stack to the **production environment**.

We will be using the GitHub repository as our [previous project]().

## 2 - Steps

### Step 1: Creating a Pull Request

Once a new branch is created, the developer will create a **pull request (PR)**. This triggers the workflow to start, which will attempt to create an S3 bucket using the provided **CloudFormation** template.

### Step 2: Error Handling

During the first run of the workflow, an error was detected in the CloudFormation template due to **incorrect indentation**.

![[GitHub_actions_pull_pr_project_logs_error.png]]

- The error logs indicated a problem in the template’s structure, and after fixing the indentation issue, the workflow was triggered again.

### Step 3: Successful Validation and Creation

After correcting the error, the pipeline executed smoothly. The **S3 bucket** was successfully created, and the PR discussion was updated with the validation results, including the name of the bucket created.

![[GitHub_actions_pull_pr_project_passed_validation.png]]

- **CloudFormation Stack** created successfully:

![[GitHub_actions_pull_pr_project_cloudformation_stack_created.png]]

- **S3 Bucket** created as expected:

![[GitHub_actions_pull_pr_project_s3_bucket_created.png]]

### Step 4: Cleanup Process Fails to Trigger

However, we noticed that after merging the pull request, the **cleanup job** (responsible for deleting the stack and the S3 bucket) did not run. To resolve this, we had to update the workflow configuration.

### Step 5: Workflow Configuration Update

To fix the issue and ensure that the cleanup job runs after merging the PR, we added the following configuration to the workflow file:

``` yaml
on:
  pull_request:
    paths:
      - "cloudformation/**"
    types: [opened, synchronize, reopened, closed]
```

This ensures that the workflow triggers on specific PR events (opened, synchronized, reopened, and closed) and only for files in the `cloudformation/` directory.

### Step 6: Preventing the Validation Job from Running on Merge

Additionally, we updated the **validate-cfn job** to avoid running the CloudFormation validation when the PR is merged. We added the following condition to skip this step when the PR is merged:


``` yaml
jobs:
  validate-cfn:
    if: github.event.pull_request.merged == false
```

This ensures that the validation job only runs for unmerged PRs, preventing unnecessary execution after the code is already merged.

### Step 7: Successful Cleanup Job Execution

After applying the fixes, the workflow executed correctly, and the cleanup job successfully ran after merging the PR. The stack and S3 bucket were deleted as expected.

![[GitHub_actions_pull_pr_project_cleanup_job.png]]

Finally, everything worked as intended, and the resources were cleaned up once the pull request was merged.
After creating a new branch and create a pull request, our workflow started and found an error in our Cloudformation template. 

## 3 - Conclusion 

This project showcases the power and flexibility of **GitHub Actions** when combined with **CloudFormation** for automating infrastructure tasks. By integrating this workflow into the development process, we can:

- **Validate infrastructure code** within pull requests.
- **Ensure infrastructure correctness** before merging into the main branch.
- Automatically **create and delete resources**, keeping the environment clean.

In a real production environment, we would likely use a more robust deployment strategy with separate workflows for staging and production environments, ensuring a smooth and reliable infrastructure deployment process.

This setup also demonstrates how automating **infrastructure validation** and **cleanup** processes can help ensure that infrastructure changes are safe, repeatable, and manageable across different environments.

It was interesting to see how we can validate IaC before merging to the main branch. I never thought of this way before.