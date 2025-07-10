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