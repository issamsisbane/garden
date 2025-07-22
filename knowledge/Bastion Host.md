[[Teleport]]
[[Wallix]]

A **bastion host** (also known as a jump server) is a **secure server** that acts as a gateway between the external network (e.g., the Internet) and a private network.

It is used to provide secure access to instances within a private subnet. Typically, administrators connect to the bastion host via SSH (for Linux instances) or RDP (for Windows instances), and then from the bastion host, they can access the resources within the private subnets.

**Security**: The bastion host is placed in a public subnet and is secured with strict security group rules, allowing only specific IP addresses to connect to it (e.g., the IP address of the network administrator).

**Purpose**: It is used to securely manage and administer instances in private subnets without exposing those instances directly to the Internet.
### Key Differences with NAT GATEWAY

**Bastion Host**: Provides secure access to private instances for administrative tasks.
**NAT Gateway**: Allows private instances to access the Internet for outbound traffic only (e.g., downloading updates).