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


![[AWS_VPC_ARCHITECTURE_Bastion.png]]
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