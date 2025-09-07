
- **1 - Enable Multi-Factor Authentication (MFA) for Root Account**:  
    The first step is to enable **Multi-Factor Authentication (MFA)** on the root account. This adds an extra layer of security, ensuring that only authorized users can access the account by requiring a second form of authentication in addition to the password.
    
- **2 - Limit Root Account Usage**:  
    For security best practices, the **root account should not be used for day-to-day operations**. Instead, the root account should only be accessed for critical tasks that require root-level permissions.
    
- **3 - Create an Admin User for Regular Operations**:  
    After securing the root account, create a **dedicated IAM user with administrative privileges**. This user will be used for all regular tasks, including managing resources and creating applications, while maintaining the security of the root account. We also need to enable MFA for this user.
    
- **4 - Set Budget Limits**:  
    To avoid unexpected charges on AWS, it's important to **set a budget** for your resources. AWS allows you to configure budgets that send alerts when your spending approaches a predefined limit, helping you keep costs under control.