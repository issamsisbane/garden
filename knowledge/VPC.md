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