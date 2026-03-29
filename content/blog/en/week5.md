---
title: "Enhancing my Cloud Skills - Week 5 - AWS Fundamentals"
description: "Week 5 of enhancing my Cloud Skills."
lang: "en"
pubDate: "Sept 17 2024"
heroImage: "/portfolio/blog/week5/week5.webp"
badge: "Enhancing my Cloud Skills"
tags: ["Cloud", "AWS", "Cloud Engineer Academy", "Architecture"]
---


_Coming from an Azure background, I had never fully explored AWS and its components until now. This was my first deep dive into the core networking architecture of AWS. Given the similarities to what I already knew from Azure, the learning curve wasn’t too steep, allowing me to grasp the concepts more easily._

> As I mentioned in my previous articles, I come from a background in **cloud computing** and **software engineering**, so throughout my learning journey, I will be marking new concepts with the hashtag **#new**. This will help highlight what’s new to me and offer readers a clearer idea of where they might find additional value — whether they’re revisiting familiar concepts or encountering fresh material themselves.

> Stay tuned as I continue to document my learning process and share practical takeaways from each module!

--- 

1 - **AWS Global Architecture** <br/>
2 - **VPC** <br/>
3 - **NOTES/CLOUD ACADEMY/Content/IAM** <br/>
4 - **Project - 4 - Design a VPC** <br/>
5 - **Set up a Bastion Host** <br/>

---

# 1 - AWS Global Architecture

**AWS Regions** are a global network of clusters of data centers located in specific geographic areas. Each region is designed to be **completely independent** of others, providing resilience and fault isolation. This means if one region experiences an issue, it does not affect the others. Regions are identified using specific naming conventions, such as `eu-west-2` for the London region. This independence ensures that applications and services can remain available even in the event of a regional failure.
![AWS_Regions.png](/portfolio/blog/week5/AWS_Regions.png)



**AWS Availability Zones (AZs)** are isolated locations within an AWS region, each consisting of one or more discrete data centers with their own redundant power, networking, and connectivity. By being **physically separate** (typically up to 100 km apart), AZs provide enhanced fault tolerance and stability. They allow you to run services across multiple zones, ensuring that if one data center encounters an issue, the other zones can continue to operate without interruption, thereby maintaining high availability for your applications.

**Local Zones** are smaller, more localized extensions of AWS regions that bring compute, storage, and other AWS services closer to end-users. They are designed for **latency-sensitive applications** that require ultra-low latency by reducing the physical distance between the user and the cloud services. This is particularly useful for use cases like gaming, media streaming, and real-time simulations, where every millisecond counts.
![AWS_Local_zones.png](/portfolio/blog/week5/AWS_Local_zones.png)

**Edge Locations** are part of AWS's global Content Delivery Network (CDN), Amazon CloudFront. They **cache data** closer to end-users, ensuring even lower latency and faster delivery of content. By positioning data at the "last mile" between AWS and the client, edge locations significantly enhance the user experience by reducing the time it takes to load content, regardless of the user's geographic location.

### Service Availability Across Regions

Not all AWS services are available in every region. Services are launched in regions based on factors like demand, regulatory requirements, and infrastructure capabilities. However, some services, such as **IAM (Identity and Access Management)** and **S3 (Simple Storage Service)**, are considered **global services** and are accessible from any region.

### Reliability and Performance

AWS's vast and highly reliable global infrastructure ensures that your applications can be **highly available and performant** from anywhere in the world. By leveraging regions, availability zones, local zones, and edge locations, AWS enables you to build robust, low-latency applications that can withstand failures and deliver consistent performance to users globally.
# 2 - VPC

A VPC is a **logically isolated private network** within the AWS cloud, providing the flexibility to design and manage your cloud environment in a secure and controlled manner.

### CIDR Blocks

CIDR (Classless Inter-Domain Routing) blocks define the IP address range assigned to your VPC. This range determines the number of resources you can deploy, as it sets the upper limit on the number of IP addresses available within the network. Carefully planning the CIDR block is crucial to ensure sufficient IP addresses for current and future needs.

### Subnets

A VPC is a virtual network, and subnets are subdivisions within this network. Subnets allow you to organize and separate your cloud resources based on **access and security requirements**. Subnets can be classified into public or private, each serving different purposes.

### Public Subnets

Public subnets are designed for resources that need to be accessible directly from the Internet. This is achieved by associating the subnet with an **Internet Gateway (IGW)**, a VPC component that provides a route for inbound and outbound traffic between the Internet and resources within the subnet. To be accessible from the Internet, a resource in a public subnet must have a **public IP address** or an **Elastic IP address**. Public subnets are ideal for front-end web servers, public APIs, or services that require direct interaction with users or external systems.

- **Elastic IP Address**: An Elastic IP Address is a static, public IPv4 address that can be easily reassigned to different instances. Unlike a standard public IP address, which can change if an instance is stopped or restarted, an Elastic IP Address remains consistent, ensuring a stable point of access.

### Private Subnets

Private subnets are designed for resources that should **not be directly accessible** from the Internet. Resources within private subnets can communicate with each other and with resources in public subnets, but they lack a direct route to the Internet in their route tables. Instead, they access the Internet via a **NAT Gateway** in a public subnet, which allows outbound traffic for tasks like software updates while blocking inbound traffic from the Internet.

Private subnets are typically used for back-end servers, databases, and other high-security application layers. Using private subnets enhances security by isolating sensitive and critical workloads from public-facing services, optimizing network performance by localizing traffic, and simplifying management through clear access control policies.

### Key Components

#### Internet Gateway (IGW)

An Internet Gateway is a VPC component that enables communication between instances in a public subnet and the Internet. It provides a route for inbound and outbound traffic to flow between your VPC and the outside world.

#### Router

Routers in the VPC handle traffic within and outside the VPC based on routing rules defined in route tables. They ensure that traffic is correctly directed between subnets, the Internet, and other networks.

#### Route Table

Route tables contain rules (routes) that determine where network traffic is directed. In a VPC, you can have multiple route tables:

- **Public Subnets**: Route tables that include a route to the Internet Gateway (`0.0.0.0/0`) to facilitate direct Internet access.
- **Private Subnets**: Route tables that use a NAT Gateway for Internet-bound traffic, allowing outbound connections without exposing the resources directly to the Internet.

#### NAT Gateway

A NAT (Network Address Translation) Gateway allows instances in private subnets to initiate outbound traffic to the Internet (e.g., for updates) while preventing inbound traffic from the Internet. This ensures that private instances can communicate externally without being directly exposed.

### Security

#### Security Groups

Security Groups act as virtual firewalls for instances, controlling inbound and outbound traffic at the instance level. They define rules specifying the protocols, IP addresses, and port numbers that are allowed or restricted. Security Groups are **stateful**, meaning if traffic is allowed in, the response is automatically allowed out. Importantly, Security Groups can only have "allow" rules; there are no explicit "deny" rules. They provide a granular, stateful control mechanism for managing access to individual instances.

#### Network Access Control Lists (NACLs)

NACLs serve as an additional security layer at the subnet level, providing a stateless checkpoint for regulating inbound and outbound traffic. Unlike Security Groups, NACLs are **stateless**, meaning that both incoming and outgoing traffic must be explicitly allowed through separate rules. NACLs allow you to define both "allow" and "deny" rules, which can block specific IP addresses or IP ranges across the entire subnet, offering broad protection against unauthorized access.

### Benefits of Using VPC and Subnets

- **Enhanced Security**: By separating public-facing services from sensitive workloads, you strengthen the security of your cloud environment.
- **Optimized Performance**: Localizing traffic within private subnets minimizes latency and maximizes throughput.
- **Simplified Management**: Clear roles and policies simplify access control, traffic monitoring, and compliance with data governance requirements.


# 3 - IAM

IAM allows you to securely control access to AWS resources under specific conditions. With IAM, you can create and manage users, groups, and policies to define who can access specific resources and under what conditions.

### Key Features

- **User Management**: Create individual user accounts with tailored permissions.
- **Group Management**: Organize users into groups to apply permissions at scale.
- **Condition-Based Access**: Define access conditions, specifying when and how users can access resources.
- **Access Control**: Manage who can access specific resources and under what conditions, ensuring a secure environment.

### Least Privilege Principle

IAM supports the security best practice known as the **Least Privilege Principle**. This principle ensures that each user, group, or application has only the permissions necessary to perform their tasks—nothing more. By adhering to this principle, you minimize security risks by reducing the potential for unauthorized access.

### Multi-Factor Authentication (MFA)

IAM also supports **Multi-Factor Authentication (MFA)**, providing an additional layer of security for accessing AWS resources. By requiring users to provide a second form of authentication (e.g., a one-time code sent to a mobile device), MFA significantly reduces the risk of unauthorized access even if credentials are compromised.

### IAM Roles and Application Access

IAM allows applications to securely access other AWS resources using **IAM roles**. These roles grant the necessary permissions without the need to store AWS credentials within the application. This practice not only enhances security by avoiding hardcoded credentials but also ensures that applications have only the permissions they need to interact with AWS services.

### Integration and Federation

IAM can integrate with existing identity systems, such as Microsoft Active Directory (AD), allowing organizations to use their existing infrastructure for access control. It also supports **Identity Federation**, enabling users to authenticate using existing identities from external systems (e.g., corporate directories or Single Sign-On (SSO) solutions) without creating separate IAM accounts.

### Key Terms

- **Users**: Individuals or services that can be granted access to AWS resources.
- **Groups**: Collections of users to which you can apply permissions collectively.
- **Roles**: Sets of permissions that allow users or services to perform actions in AWS without using direct credentials.
- **Permissions**: Define what actions users or services can perform on AWS resources.
- **Policies**: JSON documents that define permissions and specify which resources users or roles can access and how they can interact with them.
- **Identity Federation**: Enables users to access AWS resources using external identities (e.g., corporate directory services), avoiding the need for a separate IAM user account for each user.

# 4 - Design a VPC

![AWS_VPC_Architecture.png](/portfolio/blog/week5/AWS_VPC_Architecture.png)

## Requirements

1. **VPC Design**: Create a VPC with a specified CIDR block.
2. **Subnet Design**:
    - Two public subnets (one in each AZ).
    - Four private subnets (two in each AZ) for the application and databases.
3. **Internet Connectivity**:
    - Internet Gateway for public subnets.
    - NAT Gateway in public subnets for private subnet Internet access.
4. **Route Tables**:
    - Configure route tables for proper routing between public and private subnets.
5. **Security**:
    - Restrict database access in the private subnet to only application servers.
6. **Documentation**:
    - Provide an architecture diagram and explain the design choices.

## Architecture Design

### Network

I selected a large CIDR block for the VPC: `10.0.0.0/16`. This provides a substantial number of IP addresses (65,534 usable addresses) to accommodate current and potential future needs. Although the theoretical maximum is 65,536 addresses, AWS reserves the first four and the last IP addresses in each subnet, as documented [here](https://docs.aws.amazon.com/vpc/latest/userguide/subnet-sizing.html):

- **10.0.0.0**: Network address.
- **10.0.0.1**: Reserved by AWS for the VPC router.
- **10.0.0.2**: Reserved by AWS for the DNS server.
- **10.0.0.3**: Reserved by AWS for future use.
- **10.0.0.255**: Broadcast address.

Given the architecture requirements, we need six subnets, which I have allocated as follows:

|Name|Subnet|Mask|Number of Addresses|
|---|---|---|---|
|az1-public-subnet|10.0.1.0|/24|251|
|az1-application-subnet|10.0.2.0|/24|251|
|az1-database-subnet|10.0.3.0|/24|251|
|az2-public-subnet|10.0.4.0|/24|251|
|az2-application-subnet|10.0.5.0|/24|251|
|az2-database-subnet|10.0.6.0|/24|251|

Each `/24` subnet provides 251 usable IP addresses (256 total minus the 5 reserved by AWS). This design uses a large range to facilitate scalability and operational simplicity, though in practice, smaller subnets would suffice for many use cases.

### Components

- **Region**: The architecture is deployed in a single AWS Region: `eu-west-3` (Paris).
- **VPC**: A single VPC containing all resources across two Availability Zones (AZs).
- **Availability Zones**: The resources are distributed across 2 AZs to ensure high availability and fault tolerance.
- **Public Subnets**: 2 subnets, one in each AZ, with Internet access for the NAT Gateways.
- **Private Subnets**: 4 subnets (2 per AZ) isolated from direct Internet access for application servers and databases.
- **Internet Gateway (IGW)**: A single Internet Gateway attached to the VPC to provide Internet connectivity to the public subnets.

### Route Tables

The routing setup is straightforward:

**Public Subnets**: The public subnets require a route to the Internet Gateway to allow inbound and outbound Internet traffic.

| Destination | Target |
| ----------- | ------ |
| 0.0.0.0/0   | IGW    |
| 10.0.0.0/16 | Local  |

**App Subnets :** To allow instances in private subnets to access the Internet for updates, we use a NAT Gateway. The other entry allow to communciate with all the resources presents within the network.

| Destination | Target |
| ----------- | ------ |
| 0.0.0.0/0   | NAT    |
| 10.0.0.0/16 | Local  |

**DB Subnets :** DB don't need direct access to Internet. Only our application can access our database.
The `0.0.0.0/0` route is a catch-all route, directing traffic to the specified target when no more specific route is found.

| Destination | Target |
| ----------- | ------ |
| 10.0.0.0/16 | Local  |

### High Availability

Our architecture is designed for resilience and high availability by distributing resources across two Availability Zones (AZs). If one AZ experiences a failure, the other AZ can continue to handle traffic seamlessly, ensuring uninterrupted service. While the architecture could be extended to span multiple regions for even greater fault tolerance, this might be excessive for a basic application of this scope.

### Security

Security is enforced through the following measures:

- **Private Subnets**: Application servers and databases reside in private subnets, preventing direct Internet access. Any Internet-bound traffic must go through the NAT Gateway, providing control and monitoring over outgoing communications.
- **Security Groups**:
    - **Application Security Group**: Controls inbound and outbound traffic for the application instances.
    - **Database Security Group**: Configured to only allow inbound traffic from the application security group, ensuring that the database can only be accessed by the application servers. This provides a more granular level of security compared to Network Access Control Lists (NACLs).
- **NAT Gateway**: Used to facilitate outbound Internet access for instances in the private subnets without exposing them directly to the Internet.

By combining private subnets, NAT Gateways, and tightly controlled security groups, we maintain strict control over network traffic, thereby enhancing the security posture of the application and database.

## Conclusion

This architecture leverages AWS best practices to ensure a scalable, highly available, and secure environment for the web application. The design not only meets the current requirements but also provides flexibility for future growth.

# 5 - Setting Up Bastion host

### What is a Bastion Host?

A **bastion host**, also known as a jump server, is a **secure server** that acts as a gateway between an external network (e.g., the Internet) and a private network. It provides secure access to instances within a private subnet. Administrators typically connect to the bastion host via SSH (for Linux instances) or RDP (for Windows instances). Once connected, they can then access resources in the private subnets through the bastion host.

**Security**: The bastion host is placed in a public subnet and secured with strict security group rules. Only specific IP addresses (e.g., those of network administrators) are allowed to connect to it, ensuring that unauthorized access is blocked.

**Purpose**: The primary purpose of a bastion host is to securely manage and administer instances in private subnets without exposing those instances directly to the Internet.

### Key Differences Between Bastion Host and NAT Gateway

- **Bastion Host**: Provides a secure entry point for administrators to access private instances for management and administrative tasks.
- **NAT Gateway**: Allows instances in private subnets to initiate outbound traffic to the Internet (e.g., for downloading updates) while blocking inbound traffic from the Internet.

In this setup, we replaced the NAT Gateway with a bastion host to reduce costs, as the NAT Gateway can be quite expensive. The bastion host will be an EC2 instance, and we will connect to it via SSH from our local machines.

### Practical Experiment

As a practical experiment, I used my VPC architecture of the precedent part and replace it with a Bastion Host in order to test things and have a better view of how it works. NAT Gateway are pretty expensive so I wanted to avoid that. You can see in yellow the workflow of the experiment.

![AWS_VPC_ARCHITECTURE_Bastion.png](/portfolio/blog/week5/AWS_VPC_ARCHITECTURE_Bastion.png)

The practical steps include:

1. **Connect to the Bastion Host**: First, we connect to the bastion host using SSH from our local machine.
2. **Access EC2 Instances in the Private Subnet**: From the bastion host, we then connect to an EC2 instance located in the app subnet.
3. **Ping an Instance in Another AZ**: From this instance, we ping another instance located in a different AZ to ensure connectivity within the private subnets.

### Security Measures Implemented

- We set an inbound rule in the bastion host's security group to allow SSH access only from our specific IP address.
- To test the security configurations:
    - We removed the route to the Internet Gateway (IGW) from the route table of the public subnet. As a result, we could no longer connect to our instances via SSH, proving the effectiveness of the bastion host as the only access point.
    - We also deleted a security group rule in the app subnet of the second AZ that allowed access from the first app subnet. This prevented access between the subnets, confirming that inter-subnet traffic is strictly controlled by security group rules.

### Learning Outcome

Through this hands-on experiment, I gained a deeper practical understanding of VPC security and access control. It's crucial to keep security groups up to date, as the default configurations often allow traffic from any IP address, posing a significant security risk. Properly configuring security groups is essential to protect the network and its resources.