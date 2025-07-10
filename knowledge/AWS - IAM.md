[[AWS - IAM - Best Practices]]
[[AWS - IAM - MFA]]

IAM supports the security best practice known as the [[Least Privilege Principle]]
## What is IAM ?

**AWS Identity and Access Management (IAM)** is a service that enables secure control over access to AWS services and resources. It allows you to manage **users**, **groups**, **roles**, and **policies** to define **who** has access to what resources and under what conditions.

## IAM User

An **IAM user** can represent a **human** (like an individual user), an **organization**, or an **application** that interacts with AWS services. Each IAM user has a unique set of **credentials** (combination of username + password + MFA) used for authentication and to perform specific actions on AWS resources.

## IAM Groups

An IAM Group is a **collection** of users that allows you to **manage permissions** for **multiple** users simultaneously. Instead of attaching policies to each user individually, you can **attach** a **policy** to a group and **all** users in the group **inherit** those **permissions**.

## IAM Policies

**IAM Policies** are JSON documents that define what actions are **allowed** or **denied** for specific resources. Policies can be applied to **users**, **groups**, and **roles** to control access to AWS resources.

### Key Elements of a Policy:

- **Actions**: The specific actions allowed or denied (e.g., `s3:PutObject`, `ec2:StartInstances`).
- **Resources**: The specific AWS resources the policy applies to (e.g., a specific S3 bucket, an EC2 instance).
- **Conditions**: Optional restrictions under which the policy applies (e.g., only allowing access from a specific IP address or during certain hours).

### Types of Policies:

1. **Managed Policies**
    
    - **AWS Managed Policies**: Pre-built policies created by AWS for common use cases, like full access to S3 or EC2. AWS manages and updates these policies, ensuring they stay secure and up-to-date.
    - **Example**: `AdministratorAccess`, `AmazonS3ReadOnlyAccess`.
2. **Inline Policies**
    
    - **Inline Policies** are policies that are **attached directly** to a single user, group, or role and are not reusable elsewhere. These policies are specific to a particular entity and **cannot be reused** by other users or groups.
3. **Customer Managed Policies**
    
    - **Customer Managed Policies** are policies that you **create and manage** yourself. These policies can be attached to multiple users, roles, or groups, making them much more versatile and reusable.

## IAM Roles

An **IAM Role** is an IAM entity that can be **temporarily assumed** by trusted users, applications, or AWS services. Roles allow you to **delegate permissions** to resources without assigning long-term access credentials like access keys.

- **Temporary Permissions**: Roles grant temporary permissions for performing specific tasks. Once the role is assumed, the entity gains the permissions assigned to the role for a limited time.
- **No Access Keys**: Roles don’t require permanent access keys, making them more secure for delegation of permissions.

# Integration and Federation
IAM can integrate with existing identity systems, such as Microsoft Active Directory (AD), allowing organizations to use their existing infrastructure for access control. It also supports **Identity Federation**, enabling users to authenticate using existing identities from external systems (e.g., corporate directories or Single Sign-On (SSO) solutions) without creating separate IAM accounts.