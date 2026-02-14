
## Best Practices

### Least Privilege Principle

The **Least Privilege Principle** is a security best practice that states users should only have the minimum permissions necessary to complete their tasks. This reduces the risk of unintended or malicious use of resources.

### IAM Groups

Instead of managing permissions for individual users, it's recommended to organize users into **groups**. This simplifies management by applying permissions at the **group level** rather than the user level. Groups allow you to manage access for multiple users simultaneously.

### Rotate and ReIssue credentials
To minimize the risk of compromised credentials, regularly rotate passwords and access keys.

- **Password Policy**: For example, enforce a password change every 60 days.
- **Monitor User Activity**: AWS provides logs and metrics to monitor user activity, such as the last login and the last usage of access keys. Regularly review this to identify inactive users or abnormal activity.

### Use Customer Managed Policies

If you need custom policies, use **Customer Managed Policies** rather than inline policies because they are easier to manage, reuse, and audit. 