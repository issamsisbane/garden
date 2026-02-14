---
title: "Enhancing my Cloud Skills - Week 6 - AWS Advanced"
description: "Week 6 of enhancing my Cloud Skills."
lang: "en"
pubDate: "Sept 21 2024"
heroImage: "/portfolio/blog/week6/week6.webp"
badge: "Enhancing my Cloud Skills"
tags: ["Cloud", "AWS", "Cloud Engineer Academy", "Architecture"]
---

*This week, I could learn a lot about AWS core services like **EC2**, **IAM**, and **S3**. I also used **Infrastructure as Code (IaC)** for the first time to deploy resources in the cloud. IaC has been a game-changer for me, especially compared to the more manual **ClickOps** approach, where I often felt overwhelmed trying to remember what I had deployed and where my resources were located. It was easy to lose track or miss something important. With IaC, everything is clearly defined in code, making it much easier to track, manage, and update resources.*

*To put what I learned into practice, I deployed an EC2 instance using **CloudFormation** to test and reinforce my understanding of these concepts.*



---
1 - **IaC** <br/> 
2 - **AWS CloudFormation** <br/>
3 - **AWS Compute** <br/>
4 - **NOTES/IAM** <br/>
5 - **EC2 Storage** <br/>
6 - **ELB** (Elastic Load Balancing) <br/>
7 - **S3** <br/>
8 - **RDS** (Relational Database Service) <br/>

---
# 1 - IaC

## What is IaC ?

**Infrastructure as Code (IaC)** is a practice that allows developers and operations teams to **manage and provision infrastructure** through **code** rather than manual processes. Instead of using a graphical interface like the AWS Web Portal (ClickOps) or Command-Line Interface (CLI) to set up resources, IaC allows you to **define your infrastructure in code**, which can be stored in version control, shared across teams, and automatically deployed.

There are many IaC Tools such as : AWS CloudFormation, Terraform, Pulumi...

## Key Benefits of IaC

### **Version Control**

Using IaC, infrastructure definitions can be stored in **version control systems** (like Git). This allows teams to track changes over time, collaborate more effectively, and revert to previous versions if issues arise.

### **Collaboration and Automation**

IaC facilitates **collaboration** across teams, enabling multiple developers to work on infrastructure changes simultaneously. Additionally, automation tools can integrate with IaC to **automatically deploy infrastructure** based on the code, reducing the need for manual intervention.

- **CI/CD Integration**: Infrastructure changes can be automatically applied as part of a **Continuous Integration/Continuous Deployment (CI/CD)** pipeline, streamlining the development and deployment process.

### **Consistency and Reliability**

IaC ensures that environments are **consistent** across development, testing, and production. Since the infrastructure is defined in code, the same infrastructure can be deployed across multiple environments without human error.

- **Example**: Whether you're deploying to a development environment or a production environment, IaC ensures that each environment is set up exactly the same, reducing inconsistencies and potential issues caused by manual configurations.

### **Faster Setup and Scaling**

IaC enables infrastructure to be **set up quickly**. With just a few lines of code, entire environments can be created, replicated, or scaled automatically. This is particularly useful for **auto-scaling** or deploying complex infrastructure with multiple services.

- **Automation**: Instead of manually setting up servers, databases, and networks one by one, you can define them in IaC and deploy them with a single command.

### **Integration with DevOps**

IaC integrates seamlessly with **DevOps practices**, making it easier to manage both code and infrastructure in a unified way. It allows for infrastructure changes to be tested and reviewed just like software code, aligning infrastructure management with the agile principles of continuous development and delivery.

---

# 2 - AWS CloudFormation
## Definition

**AWS CloudFormation** is Amazon Web Services' **native Infrastructure as Code (IaC)** solution. It allows you to define, provision, and manage AWS resources using code, providing a declarative way to set up infrastructure. By defining resources in a **CloudFormation template**, you can automate the process of infrastructure deployment in an AWS environment without manually configuring each service through the AWS Console or CLI.

In essence, CloudFormation acts as a **detailed blueprint** for your infrastructure, with the entire architecture defined in a single file using **JSON** or **YAML**.

## Key Concepts

###  Templates

A **template** is the file that contains the **configuration** for the AWS resources you want to create. The template specifies what resources are needed, how they should be configured, and the relationships between them. Templates are written in **JSON** or **YAML**, and they serve as the basis for creating and managing resources in AWS.

- **Template Structure**: Each template contains several sections, including:
    - **Resources**: The core of the template, specifying the AWS resources to be created (e.g., EC2 instances, S3 buckets, VPCs).
    - **Outputs** (optional): Return values from the stack, such as resource IDs or URLs.
    - **Parameters** (optional): Allow input values to customize the template at runtime.

### Stacks

A **stack** is a collection of AWS resources defined by a CloudFormation template. Stacks allow you to **group resources together** and manage them as a single unit. You can create, update, and delete entire stacks at once, which simplifies the process of managing multiple resources.

Instead of managing individual AWS services (like EC2, S3, and RDS) separately, you can define them all in one stack and create, update, or delete them in one action.

Deleting a stack will automatically delete all resources associated with it, making resource management much easier and ensuring nothing is left behind.

### ChangeSets

**ChangeSets** allow you to preview the impact of changes made to your infrastructure **before** they are applied. This feature is useful when updating stacks, as it provides an opportunity to review potential changes and avoid unintended consequences, such as resource deletion or configuration mismatches.

Before updating an existing stack to add a new EC2 instance, ChangeSets allow you to see how the update will affect the current infrastructure.

---

## How Does AWS CloudFormation Work?

Using AWS CloudFormation involves defining your infrastructure using code (templates), and then deploying that infrastructure as stacks. The workflow generally follows these steps:

It's possible to find the properties and the name of types by using the AWS CloudFormation [Documentation](https://docs.aws.amazon.com/cloudformation/). This is an example for [Subnets](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet.html).

### **Step 1 - Create a Template**

The first step in using CloudFormation is to define your infrastructure in a template. Below is an example of a simple CloudFormation template written in **YAML** to create an S3 bucket:

``` yaml
# CloudFormationTemplateVersion
# Description

AWSTemplateFormatVersion: "2010-09-09" # Supported version of the template
Description: "CloudFormation template to create an S3 bucket" # What this template does
Resources: # Resources to be created
  S3Bucket: # Logical name of the resource must be unique within the template
    Type: "AWS::S3::Bucket"
    Properties:
      BucketName: "my-issam-s3-bucket-yaml" # globaly lowercase unique name across AWS S3 buckets

```


### **Step 2 - Create a Stack**

Once the template is ready, you can deploy the infrastructure by creating a **stack**. This stack will provision all the resources specified in the template. You can create a stack using the AWS CLI:

``` bash
aws cloudformation create-stack --stack-name [name-of-the-stack] --template-body file://[name-of-the-file]
```

This command will take the template and create the resources defined in the CloudFormation stack.

### **Step 3 - Update the Stack**

When you need to change your infrastructure, you can modify the template and update the stack:

``` bash
aws cloudformation update-stack --stack-name [name-of-the-stack] --template-body file://[name-of-the-file]
```

This updates the resources in the stack to reflect the changes in the template.

### **Step 4 - Verify Stack Status**

After creating or updating a stack, you can check its status using the following command:

``` bash
aws cloudformation describes-stacks --stack-name [name-of-the-stack]
```

This will display the current status of the stack, such as **CREATE_COMPLETE** or **UPDATE_IN_PROGRESS**.

### **Step 5 - Delete the Stack**

To delete all resources associated with a stack, you can use the following command:

```
aws cloudformation delete-stack --stack-name [name-of-the-stack]
```

## Project - Deploy a VPC

### Deployment

The objective of this project was to redeploy an entire **VPC architecture** using AWS CloudFormation. The goal was to create a **Bastion Host** to securely access an EC2 instance in a private subnet and ping another EC2 instance in a different **private subnet** located in a different **Availability Zone (AZ)**. This setup was previously done using **ClickOps** (manual setup via the AWS Console), but now, the goal is to automate it using **CloudFormation** for more efficiency and reproducibility ([ClickOps Version](https://medium.com/@issam.sisbane/enhancing-my-cloud-skills-week-5-aws-networking-7a93a503d6d5)). 

![AWS_VPC_ARCHITECTURE_Bastion.png](/portfolio/blog/week6/AWS_VPC_ARCHITECTURE_Bastion.png)

You can find the complete CloudFormation template code [here](https://github.com/IssamSisbane/cea-cloudformation/blob/main/vpc.yaml).

For instance, this is how to deploy a VPC : 

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Description: "CloudFormation template to create a VPC"

Resources:
  MyVPC:
    Type: "AWS::EC2::VPC"
    Properties:
      CidrBlock: "172.16.0.0/16" # IP range for the VPC
      EnableDnsSupport: "true" # Allow how resources in the vpc to commnicate with the amazon dns servers
      EnableDnsHostnames: "true" # Allow how resources in the vpc to receive dns hostnames
      Tags:
        - Key: Name
          Value: MyVPC
```


This is how to deploy an ec2 instance : 

```yaml
  # Bastion Host EC2
  BastionHost:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: t2.micro # Instance type of our EC2 instance
      ImageId: ami-0cb0b94275d5b4aec # Amazon machine image ID, a template that contains the software configuration (OS). A blue print for our EC2 instance. An image that provides the software that is required to set up and boot an Amazon EC2 instanc
      KeyName: bastion # Key pair name to connect to the instance
      SubnetId: !Ref PublicSubnet1A
      SecurityGroupIds:
        - !Ref BastionSG
      Tags:
        - Key: Name
          Value: BastionHost
```

We need to get the keyname which reference a Key Pair we previously created and download. It's needed to ssh to our ec2 instances.

You can find the appropriate AMI ID for your instance by navigating to the EC2 dashboard and selecting the relevant Amazon Machine Image : 
![AMI_image_id.png](/portfolio/blog/week6/AMI_image_id.png)

### Testing the setup

Once the VPC and Bastion Host are deployed, the next step is to test whether the architecture functions as expected by accessing the private instances through the Bastion Host.

1. **Accessing the Bastion Host via SSH**
``` bash
ssh -i bastion.pem ec2-user@[public-ip-address-of-the-ec2-instance]
```

2. **Copy our Key Pair to use ssh**
``` sh
scp -i bastion.pem bastion.pem ec2-user@15.237.184.39:~/private.pem # must be launch from our pc terminal and not ec2
```

3. **Updating File Permissions**
If we can't use the private.pem file in a linux envrionment we need to update permissions : 
``` bash
chmod 400 private.pem
```

This is what we get : 

![bastion_project_terminal_screen.png](/portfolio/blog/week6/bastion_project_terminal_screen.png)

---

# 3 - AWS Compute

## What is AWS Compute ?

Compute is the power that computer use to performe task. In cloud environment, its the server or virtual machines that are the backbone of cloud systems.
AWS compute is the term use to describe using aws computers to run websites or applications.
## Compute services

There are 4 popular AWS compute services : 

**EC2 :** One of the most widely used compute services in AWS. It provides **resizable**, **secure** **compute** **capacity** in the cloud, allowing users to run virtual servers, or **instances**, on demand.

**Lambda :** **Serverless** **computing** **Service** which lets run our code without managing servers.
AWS will handle maintenance, scaling and logging. Lambda are **event-driven** which means it could respond to changes in Data in an AWS Service or to Incoming HTTP Requests.

**Beanstalk :** AWS Elastic Beanstalk **simplifies** the process of **deploying**, **managing**, and **scaling** applications in the cloud. Beanstalk **automatically** **handles** the infrastructure provisioning, load balancing, and scaling, leaving developers free to focus on coding.

**ECS :** Amazon ECS is a **container orchestration** service that enables you to **run** and **manage** containers at **scale**. Containers are lightweight, portable units that package an application’s code along with its dependencies, making it easy to deploy and run in any environment.

## Project - Deploy an EC2 Instance

This is how to deploy an ec2 instance  : 

```yaml
  # Bastion Host EC2
  BastionHost:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: t2.micro # Instance type of our EC2 instance
      ImageId: ami-0cb0b94275d5b4aec # Amazon machine image ID, a template that contains the software configuration (OS). A blue print for our EC2 instance. An image that provides the software that is required to set up and boot an Amazon EC2 instanc
      KeyName: bastion # Key pair name to connect to the instance
      SubnetId: !Ref PublicSubnet1A
      SecurityGroupIds:
        - !Ref BastionSG
      Tags:
        - Key: Name
          Value: BastionHost
```


---

# 4 - IAM (Identity Access Management)

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
## Project - Using IAM with CloudFormation

You can find the complete template [here](https://github.com/IssamSisbane/cea-cloudformation/blob/main/iam.yaml) : 

1. **Creating an IAM User with CloudFormation**

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: "IAM CloudFormation template"

Resources:
  MyIAMUser:
    Type: AWS::IAM::User
    Properties:
      UserName: IssamCFN
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AdministratorAccess #Administrator Access Policy - High level access tier
```

2. **Creating the CloudFormation Stack**

``` bash
aws cloudformation create-stack --stack-name my-iam-stack --template-body file://iam.yaml
```

3. **Debugging**

``` bash
An error occurred (InsufficientCapabilitiesException) when calling the CreateStack operation: Requires capabilities : [CAPABILITY_NAMED_IAM]e
```

This error occurs because creating IAM resources (like users, roles, or policies) requires explicit acknowledgment from the user to ensure they understand the security implications.

So we need to use this in the command : 

``` bash
aws cloudformation create-stack --stack-name my-iam-stack --template-body file://iam.yaml --capabilities CAPABILITY_NAMED_IAM
```

While the IAM user is created successfully with administrative privileges, note that this user does not have access to the **AWS Management Console**. This is because we didn’t specify a **password** in the CloudFormation template.

In general, **passwords** and other sensitive information are not hardcoded in **Infrastructure as Code (IaC)** for security reasons. Instead, best practices dictate that such credentials should be managed through:

- **AWS Secrets Manager**: For securely storing and managing sensitive information such as passwords or API keys.
- **IAM Policies**: That enforce MFA (multi-factor authentication) for console access.

---

# 5 - EC2 Storage

It exists 2 types of storage within EC2 instances : 
### Amazon EBS
Amazon Elastic Block Store is an external hard drive that we can connect to EC2.
If we terminate the instance associated to the EBS, our data remained intact.

**EBS Volumes types :**

| Types                    | Name | Usage                                                                          |
| ------------------------ | ---- | ------------------------------------------------------------------------------ |
| General Purpose SSD      | `gp2`  | Boot Volumes, Dev & Test Env, Low-latency Interactive Applications             |
| Provisioned IOPS SSD     | `io1`  | I/O-Intensive Workloads ==(Large Database and Mission-critical Applications)== |
| Throughput Optimized HDD | `st1`  | Throughput-intensive Workloads ==(Big Data, Data Warehouses, Log Processing)== |
| Cold HDD                 | `sc1`  | Less Frequently Accessed Workloads ==(Backups & archives)==                    |
To **choose** a volume type, we need to **consider** : 
- Performance Requirements
- Durability Needs
- Budget Constraints
### Instance Store

It's a temporary storage and provides fast access to the data.
If we terminate the instance associated to the EBS, our data will be lost.

---

# 6 - ELB (Elastic Load Balancing)

Elastic Load Balancing (ELB) is a service design to **automatically distributes incoming traffic** accross multiple **targets** such as EC2 instances, docker containers or IP Addresses.

It allows to distributes the traffic between differnet ec2 instances in different AZs. It increases the fault tolerance of our system.

## Types of Elastic Load Balancers

We choose the right type of load balancers according to : 
- Traffic type
- Performance
- Application Architecture
### ALB (Application Load Balancer)

**Application Load Balancer (ALB)** is optimized for **HTTP/HTTPS traffic** and is commonly used in modern web applications. It operates at **Layer 7** (the application layer), allowing for **advanced routing** based on the content of the request.

**Features** :
    - **Path-based Routing**: Routes traffic based on URL paths (e.g., `/images` to one service, `/videos` to another).
    - **Host-based Routing**: Routes traffic based on the domain name (e.g., `api.example.com` to a different service than `www.example.com`).
    - **Routing to Multiple Targets**: Can route requests to different services, containers, or load balancers based on defined rules.

**Ideal for **:
    - Content Management Systems
    - Microservices Architecture
    - Container-based Applications (e.g., Docker, Kubernetes)

**Advanced Features**: Fine-grained routing rules enable you to make routing decisions based on the **content** of the request.
### NLB (Network Load Balancer)

**Network Load Balancer (NLB)** is designed for **TCP traffic** and operates at **Layer 4** (the transport layer). It is built to handle **extreme performance requirements**, capable of handling millions of requests per second with **ultra-low latency**.

**Features**:
    - **Low Latency**: Ideal for applications requiring **millisecond-level** latency.
    - **Connection-level load balancing**: Routes connections based on **IP Protocol Data**.

**Ideal for**:
    
    - TCP, UDP, and TLS traffic
    - Web servers requiring high throughput
    - Cache servers and databases that need consistent, fast access

**Use Cases**:
    - High-performance applications such as real-time gaming, video streaming, and large-scale web servers.

## Auto Scaling

**Auto Scaling** is an AWS service designed to **automatically adjust** the number of EC2 instances in response to changes in **demand** or **resource utilization**. By dynamically increasing or decreasing the number of instances, Auto Scaling ensures that applications maintain **high availability** and **cost efficiency**.

### Benefits of Auto Scaling:

- **Cost Efficiency**: Automatically scales down during periods of low demand, saving costs.
- **Improved Fault Tolerance**: Auto Scaling can replace failed instances and maintain the desired number of healthy instances.
- **Seamless Load Handling**: Automatically adds more instances to handle increased traffic, ensuring high performance even during peak usage.

### Components 

#### Auto Scaling Groups

A **collection** of EC2 instances that share **similar** characteristics and treated as a **logical grouping** for scaling & management.

We define a minimum and a maximum of instances in the group allowing AWS to scale them.

#### Launch Configurations ==(Deprecated)==
This is a **deprecated** method for defining the settings for new EC2 instances launched in an Auto Scaling group. It includes parameters such as:
- Instance Type
- AMI ID
- Key Pair
- Security Groups
- Associated Block Storage

#### Launch Template

This is the **enhanced** version of the launch configuration, providing more flexibility and features. Launch templates allow for multiple versions and the ability to configure different instance types or settings under the same template ID.

#### Scaling policies

Scaling policies define how the Auto Scaling group should adjust the number of instances based on specific conditions or metrics, such as **CPU utilization** or **custom metrics**.

Differents types of policies : 
- Target Tracking Scaling : **Adjust the number of instances** automatically to maintain a target value for a specific metrtic ==e.g., keep average CPU utilization at 50%==
- Step Scaling : **Increase or deacrease the number of instances** basing on **scale** adjustments depending on the size of the alarm breach. ==For example, if CPU utilization is above 60%, add one instance.==
- Schedule Scaling : **Increase or decrease instances** on **schedule** **time** points. It's appropriate for predictable load changes. ==For example, at 9 am add 5 instances to handle peek hours 

### Combining Auto Scaling and ELB

By combining **Auto Scaling** with **Elastic Load Balancing (ELB)**, you ensure that traffic is **evenly distributed** across all EC2 instances in the Auto Scaling group. This not only enhances performance but also increases the **availability** of your application. As traffic increases, Auto Scaling adds new instances, and ELB automatically begins distributing traffic to these instances.

- **Enhanced Fault Tolerance**: If one instance fails, ELB automatically reroutes traffic to healthy instances, while Auto Scaling replaces the failed instance.
- **Improved Performance**: Scaling based on demand ensures that your application remains responsive and efficient during peak times.


## Project - Create an ALB with CloudFormation

We will create an ALB an a Auto Scaling Group. The diagram below shows what we wants to achieve : 

![ELB_Load_balancer_diagram.gif](/portfolio/blog/week6/ELB_Load_balancer_diagram.gif)

You can find the complete template [here](https://github.com/IssamSisbane/cea-cloudformation/blob/main/ec2.yaml).

The template to create a Load Balancer : 

``` yaml
# Application Load Balancer. We must create a Listener and target group.
  MyLoadBalancer:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      Name: MyLoadBalancer
      Subnets:
        - !Ref PublicSubnet1A
        - !Ref PublicSubnet2B
      SecurityGroups:
        - !Ref WebServerSecurityGroup
```

This our LoadBalancer in the AWS Console : 

![ELB_Load_balancer_Resource_map_screenshot.png](/portfolio/blog/week6/ELB_Load_balancer_Resource_map_screenshot.png)

Using the DNS name of our load balancer we can see that we are redirected to one of our instances we defined in target above :

![ELB_DNS_browser_screenshot.png](/portfolio/blog/week6/ELB_DNS_browser_screenshot.png)

## Project - Auto Scaling Group

Now we want to create an Auto Scaling Group. To be triggered to scales our Auto Scaling Group. We will create a cloudWatchAlarm. We will use the CPU Usage to scale out if necessary. If the CPU Usage is more than 70 % then we will need another instance to take care of the load.

![Pasted image 20240921165121.png](/portfolio/blog/week6/Pasted image 20240921165121.png)

You can find the complete template [here](https://github.com/IssamSisbane/cea-cloudformation/blob/main/asg.yaml).


---

# 7 - S3 

## What is S3 ?

**mazon S3 (Simple Storage Service)** is a highly scalable, **cloud-based object storage** service designed for storing and retrieving data from anywhere on the web. It provides an impressive **99.999999999% durability** (referred to as **11 nines** of durability) and **99.99% availability**, ensuring your data is **protected against loss** and **accessible** when needed. S3 is known for its **large capacity**, **security**, and **reliability**, making it one of the most widely used storage services in cloud computing.

## Components

### Buckets

**Buckets** are the top-level containers used to store objects (data) in S3. Each bucket has a **unique name** across all AWS accounts globally and serves as the organizational unit where data is stored.

**Key Features** :
    - Buckets can be organized with **folders** (virtual directories) to structure your data.
    - **Bucket name** must be unique globally, and by default, AWS allows the creation of up to **100 buckets per account**.
    - **Data governance** can be enforced at the bucket level using **Bucket Policies** (for access control).
### Objects

Objects are the fundamental entities stored in S3, consisting of **data** and associated **metadata**. Each object can range in size from **0 bytes to 5 terabytes** and is identified by a **unique key**.

**Components** :
    - **Actual File**: The data being stored (e.g., an image, video, document).
    - **Metadata**: Information about the object, such as its content type, creation date, and user-defined metadata.

### Keys 

A **key** is a unique identifier for each object within a bucket. It includes the **full path** to the object, similar to a file path in a traditional file system. For example, in the bucket `my-bucket`, the key for an object might be `images/photo.jpg`.

## Features
### Bucket Policies

**Bucket Policies** are **JSON-based access control policies** that allow fine-grained control over who can access your S3 resources and how they can interact with them.

- **Key Features**:
    - Allow or deny access to specific **AWS accounts**, **IAM users**, or **IP ranges**.
    - Grant permissions such as **read**, **write**, or **delete** for objects in the bucket.
    - Enforce **encryption requirements** for objects uploaded to the bucket.
    - Restrict access based on **HTTP referers** or require specific conditions for access.
### Versioning

**Versioning** allows you to **maintain multiple versions** of an object within a bucket. When versioning is enabled, S3 keeps previous versions of objects, allowing you to **recover** from accidental deletions or overwrites.

**Benefits** :
    - **Accidental Deletion Protection**: Restores objects to their previous state in case of deletion.
    - **Compliance**: Meets regulatory requirements for data retention.
    - **Enable or Suspend**: You can enable or suspend versioning at any time. When suspended, existing versions are retained, but new versions are no longer created.
### Lifecycle Policies

**Lifecycle Policies** help automate the management of objects stored in S3. Based on predefined rules, you can transition objects between different **storage classes** or delete them after a certain period.

- **Key Features**:
    - Transition objects to **lower-cost storage classes** (e.g., move data from **Standard** to **Glacier** after a certain period).
    - **Expire objects** after a specified time to free up space and reduce costs.
    - **Delete previous versions** of objects based on defined retention policies.

Lifecycle policies help **optimize costs** by automatically transitioning data to more cost-effective storage tiers as its usage decreases.
## S3 Storage Classes

### Standard

**Frequently** **Accessed** Data & Requires durability & availability

### Intelligent

**Unknown** or **changing** Access Patterns. It automatically moves the data to the most cost effective access tier.

### Infrequent Access (IA)

**Less Frequently accessed** data that requires rapid access when needed.

### One Zone-InfrequentAccess (IA)

Data is stored in a **Single Availability** Zone & Costs 20% less than Standard IA. **Infrequently Accessed** data that doesn't need to be replicated across multiple AZs.

### Glacier and Glacier Deep Archive

Lowest-cost Storage for **Data Archiving** & **Long term** Backup.
For **Infrequently accessed data** and when several hours of retrieval time is suitable.

## Use Cases

### Website Hosting

Amazon S3 can be used to **host static websites**. S3’s automatic scalability allows it to handle large amounts of traffic without requiring manual intervention.

### Backup & Restore

S3 is widely used as a **primary storage** solution for disaster recovery.

### Archive

With **S3 Glacier** and **S3 Glacier Deep Archive**, you can easily move data to **low-cost storage** for long-term data retention.

### Big Data Analytics

**Store** and **analyze** Massive Data Sets using AWS Athena or AWS Redshift.

### Media Files

Amazon S3 is ideal for storing and distributing **unstructured data** like media files (images, videos, and audio).

## Project - Static Website Deployment To S3

We will deploy a simple static webpage to S3. I just created an index.html page with an H1 tag saying : "HI THIS IS A WEBSITE HOSTED ON AWS". 

You can find the complete template [here](https://github.com/IssamSisbane/cea-cloudformation/blob/main/s3-static.yaml).

This is how to create a s3 bucket : 

``` yaml
MyS3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-static-website-is
      WebsiteConfiguration:
        IndexDocument: index.html
```

We had our index.html file into the bucket : 

```sh
aws s3 cp index.html s3://my-static-website-is 
```

If we try to access the file in the bucket we encounter an `Access Denied` : 

![S3_static_webpage_error.png](/portfolio/blog/week6/S3_static_webpage_error.png)

If we try to debug using the AWS Console we find this interesting setting : 

![S3_public_access_policies_2.png](/portfolio/blog/week6/S3_public_access_policies_2.png)

We need to update the bucket policies to allow public access.

``` yaml
MyS3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: my-static-website-is
      WebsiteConfiguration:
        IndexDocument: index.html
      PublicAccessBlockConfiguration:
        RestrictPublicBuckets: false
```

It's now working : 

![S3_static_webpage_success.png](/portfolio/blog/week6/S3_static_webpage_success.png)

---

# 8 - RDS (Relational Database Service)

The relational AWS managed  Database.
AWS take care of provisioning, configuration, patching and backups.

Under the hood RDS is built on top of EC2.
We can use many databases engines such as : 
* MySQL
* PostgresSQL
* MariaDB
* Oracle DB

### Benefits

#### Multi-AZ
Databases are **replicate** accross **multiple** **AZs**. It improves reliability and availability.
#### Automatic failover
There is an **automatic** failover **to** the standby instance which allows our database to still running.

#### Read Replicas
Allow to handle the **read-only workloads** to make the database less charge. Our master database would not become overloaded. We will have one databases for writing data and one for reading data. We can place read replicas in **other regions**.

#### Automatic Backups
It happens **once a day** and includes both : **RDS Instance** and **Transaction logs**. We can choose **Retention Period** (up to 35 days). If we want to keep it longer we have to create **manual snapshots** of our database. We can stored the backups in AWS S3.

## Project - Database Creation

This is a template to create a new RDS MySQL Database : 

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Description: CloudFormation template to create an RDS instance

Resources:
  # MyDB
  MyDb:
    Type: AWS::RDS::DBInstance
    Properties:
      DBInstanceIdentifier: MyNewRDS
      MasterUsername: admin # in prodcution we would use KMS to encrypt this
      MasterUserPassword: password # in prodcution we would use KMS to encrypt this
      DBInstanceClass: db.t3.micro
      Engine: mysql
      EngineVersion: 8.0.35
      AllocatedStorage: 20
      BackupRetentionPeriod: 7
```
# DynamoDB

The non relational AWS managed Database.

