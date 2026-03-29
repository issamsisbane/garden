---
title: "Enhancing my Cloud Skills - Week 2 - Git & Cloud Architecture"
description: "Week 2 of enhancing my Cloud Skills."
lang: "en"
pubDate: "Sept 13 2024"
heroImage: "/portfolio/blog/week2/week2.drawio.png"
badge: "Enhancing my Cloud Skills"
tags: ["Cloud", "GIT", "Cloud Engineer Academy", "Architecture"]
---

*The **second module** of the Academy covered **Git** and **Cloud Architecture**. It was a great mix of refreshing concepts I was already familiar with and discovering **new insights** that I hadn’t explored before.*

*I had the opportunity to **review some things** that I already knew, while also deepening my understanding in certain areas. This module focused on using **Git** effectively in cloud environments and highlighted key elements of **cloud architecture**, ensuring scalable, secure, and efficient solutions.*

*As I mentioned earlier, I come from a background in **cloud computing** and **software engineering**, so throughout my learning journey, I will be marking new concepts with the hashtag **#new**. This will help highlight what’s new to me and offer readers a clearer idea of where they might find additional value—whether they’re revisiting familiar concepts or encountering fresh material themselves.*

*Stay tuned as I continue to document my learning process and share practical takeaways from each module !*

---

1 - **Version Control** <br/>
2 - **Cloud Architecture** <br/>
3 - **System Design** <br/>
4 - **AWS Console** <br/>
5 - **Project | Design a Basic Architecture for a Web Application Project** <br/>

---


# Version Control 

Une petite introduction à GIT, à quoi cela sert avec création d'un repo github et utilisation de commande très basique tel que : 

``` bash
git init
```

``` bash
git checkout -b dev
```

C'est très important d'utiliser des versions control car ...

# Cloud Architecture

**Cloud architecture** refers to the structure and components involved in delivering cloud computing services. It includes the **frontend**, **backend**, **cloud infrastructure**, and **networking**, which work together to provide scalable, secure, and reliable solutions for running applications in the cloud.

---

### Key Components of Cloud Architecture:

1. **Frontend**:  
    The user-facing part of the system, which includes the **user interface** (UI) and **client-side logic**. It handles user interactions and sends requests to the backend. Its purpose is to deliver a user-friendly experience.
    
2. **Backend**:  
    The server-side infrastructure that processes user requests and manages data. It consists of **databases** and **servers** that ensure data integrity and handle the business logic.
    
3. **Cloud**:  
    The physical and virtual infrastructure that stores and manages data and applications. It can be **public**, **private**, or **hybrid**, depending on how resources are managed. Cloud platforms like **AWS**, **Azure**, or **Google Cloud** provide scalable services.
    
4. **Network**:  
    Ensures connectivity between the frontend and backend by facilitating **data transfer** and enabling communication between cloud components. A reliable network ensures **low latency**, **high availability**, and **secure connections**.
    

---

### Cloud Architecture Layers:

1. **Applications and Services**:  
    This layer includes the applications and services that users interact with, such as web and mobile apps.
    
2. **Virtualization Layer**:  
    Creates virtual representations of computing resources (e.g., servers, storage) and allows for **dynamic scaling** of resources.
    
3. **Hardware Layer**:  
    The physical infrastructure (servers, storage, networking equipment) that supports the cloud, located in data centers. This is the backbone of cloud services.
    

---

### Best Practices in Cloud Architecture:

1. **Scalability**:  
    The architecture should support **vertical scaling** (adding more resources to a single machine) and **horizontal scaling** (adding more machines to handle the load). This ensures that the system can grow with user demand.
    
2. **Security**:  
    Implementing best practices like **data encryption**, **multi-factor authentication (MFA)**, and **role-based access control (RBAC)** ensures the system is protected against threats and complies with regulations like **GDPR**.
    
3. **Reliability**:  
    Ensuring the system can handle failures and recover quickly by using **redundancy**, **resilience systems**, and **disaster recovery plans**.
    
4. **Performance**:  
    Optimize the system to reduce latency and improve response times through **load balancing** and efficient resource allocation.
    
5. **Cost Efficiency**:  
    Utilize **on-demand resource allocation** and **auto-scaling** to ensure cost-effective cloud infrastructure without compromising on performance or scalability.
    

---

### Roles in Cloud Architecture:

- **Cloud Architects** design the overall cloud solutions, ensuring scalability, security, and efficiency.
- **Cloud Engineers** build, implement, and maintain the architecture, ensuring smooth operation.

Together, they ensure that cloud systems are scalable, reliable, secure, and cost-efficient.

# System Design

**System design** is the process of creating systems that are **scalable**, **reliable**, and **efficient**. It involves carefully considering every layer, from the **infrastructure** and **hardware** to the **software** and **data flow**, to ensure that systems can handle growing demands while maintaining performance and reliability.

**System design** is essential for creating applications and services that can **scale**, remain **available**, and handle **failures** effectively. By following best practices like **load balancing**, ensuring **high availability**, and implementing **scalable architecture**, systems can meet growing demands without compromising performance.

The **cloud architect** is responsible for designing the system, while **cloud engineers** build and implement the architecture to ensure it meets business requirements for **scalability**, **reliability**, **performance**, and **cost-efficiency**.

---

## System Design Process

To build a robust system, a clear design process must be followed. This process includes:

- **Requirements**: Understanding the business and technical requirements, such as performance, user demands, and specific functionalities.
- **Architecture**: Defining the overall structure, including how components interact and how data flows between them.
- **Components**: Identifying the key system components (e.g., servers, databases, APIs).
- **Data**: Managing how data is stored, processed, and retrieved.
- **Interface**: Defining how users interact with the system (e.g., via frontend applications or APIs).
- **Security**: Ensuring that the system is protected from unauthorized access and vulnerabilities.

---

## Backend vs Frontend

In system design, it is essential to distinguish between the **backend** and **frontend**:

- **Frontend**: This is the **user-facing part** of the system, including web pages, mobile apps, and user interfaces. It handles **user interaction** and sends requests to the backend.
- **Backend**: This is the **server-side** part of the system that processes user requests, manages databases, and handles the logic of the application.

Both layers must work seamlessly together to ensure that users get a smooth, efficient experience.

![user_client.png](/portfolio/blog/week2/user_client.png)

---

## Scaling in System Design

**Scaling** refers to the system's ability to **handle increasing loads**. There are two primary types of scaling:

![horizontal_vertical_sclaing.png](/portfolio/blog/week2/horizontal_vertical_sclaing.png)
### Vertical Scaling

**Vertical scaling** involves **increasing the processing power** of a single machine. This is done by upgrading the server's hardware to make it more powerful, such as adding more CPU, RAM, or storage.

- **Advantages**: Simple to implement, no need to change application architecture.
- **Limitations**: There’s a **limit to how much you can scale vertically** (hardware limitations), and it can become very **expensive**.

### Horizontal Scaling

**Horizontal scaling** involves adding **multiple instances of servers** to handle the increasing demand. Instead of upgrading a single server, you add more servers to distribute the workload.

- **Advantages**: **Unlimited growth** potential, better distribution of traffic, and fault tolerance.
- **Limitations**: Requires more complex architecture, such as load balancing and managing multiple servers.

Horizontal scaling is generally more **cost-effective** and **scalable** in the long term.

---

## Load Balancing

A **load balancer** is a critical component in system design, especially for scalable and reliable systems. It **distributes incoming traffic** across multiple backend servers, ensuring that no single server is overwhelmed with too many requests.

### Key Benefits of Load Balancing:

- **Scalability**: Allows the backend to scale by adding more servers as demand grows.
- **Reduced Downtime**: If one server fails, the load balancer redirects traffic to healthy servers.
- **Improved Performance**: Distributes the workload evenly across servers, preventing bottlenecks.
- **SSL Offloading**: Can handle SSL decryption and encryption, reducing the workload on backend servers.
- **Health Checks**: Routinely checks the health of backend servers to ensure they are operational.
- **Session Persistence**: Ensures that users' sessions are maintained across multiple backend servers, improving the user experience.

---

## High Availability

**High availability** is the ability of a system to **remain operational** and **accessible** despite failures. It ensures that the system has **minimal downtime** and is always available for users.

### Components of High Availability:

- **Load Balancer**: Ensures continuous traffic distribution, even during server failures.
- **Redundancy**: Having **multiple instances** of critical components so that if one fails, others take over.
- **Failover Process**: Automatically switches to backup systems in case of failure.
- **Health Checks**: Constant monitoring of system components to ensure they are operational.

High availability improves **business continuity**, builds **trust** with users, and maximizes **uptime**.

---

## Fault Tolerance

**Fault tolerance** is the ability of a system to **continue operating** even if some of its components fail. It involves designing systems that can handle hardware, software, or network failures without causing **interruption** to the service.

### Fault Tolerance Techniques:

- **Standby Clusters**: In case the entire high-availability cluster fails, a **standby cluster** can take over, ensuring that the system continues to operate.
- **Redundancy**: Multiple backups for critical components ensure that there’s always a fallback.
- **Failover**: Similar to high availability, but with more emphasis on continuous operation even during multiple failures.

### Key Differences Between Fault Tolerance and High Availability:

- **Fault tolerance** ensures **continuous operation** with zero downtime, even during failures.
- **High availability** minimizes downtime but may require some recovery time during failures.

Both fault tolerance and high availability are crucial in ensuring **system reliability** and user trust.

# AWS Console

I could use the aws console for the first time to : 

### Create a new IAM user

### Add a policy to the user 

### Create a s3 bucket

### Add a file to the bucket

## Project : Design a Basic Architecture for a Web Application

Finally, There was a projet. You can find it here

![Week2_Architecture_basic.png](/portfolio/blog/week2/Week2_Architecture_basic.png)
### Project Objective:

The goal of this project is to design a cloud infrastructure that supports a web application, ensuring high availability, fault tolerance, and scalability.

### Architecture Overview:

1. **Firewall**:  
    The first component in my architecture is the firewall. It acts as a security layer that filters incoming requests based on predefined rules. Only legitimate traffic is allowed through, protecting the infrastructure from potential attacks.
    
2. **Load Balancer**:  
    Once traffic passes through the firewall, it is directed to the load balancer. The load balancer’s role is to distribute requests across the most efficient available resources, ensuring balanced traffic and optimal performance. I deploy multiple load balancers to handle increased traffic and provide redundancy in case one fails.
    
3. **Geographical Redundancy**:  
    I have designed the architecture to span two geographic regions. This allows for disaster recovery if one region becomes unavailable. Additionally, incoming traffic can be routed to the nearest region based on the user’s location, improving response time.
    
4. **Clusters in Each Region**:
    
    - **High Availability Cluster**: This cluster contains the primary resources needed to run the web application. It handles normal operations and is designed for high performance.
    - **Standby Cluster**: The standby cluster serves as a backup. If the high availability cluster experiences a failure within the same region, the standby cluster takes over, ensuring continuity.
5. **Application Components**:
    
    - **Frontend**: The web application frontend resides in a public subnet, making it accessible to users. It delivers the user interface and handles client-side requests.
    - **Backend**: The backend, consisting of APIs and databases, is hosted in a private subnet to enhance security. By isolating the backend from public access, I reduce the attack surface and protect sensitive data.

### Scaling Strategies for High Availability and Fault Tolerance:

Each component in the architecture is scaled according to its function and needs to ensure performance and resilience:

| Component                         | Scaling Type       | Reason                                                                                                                                                          |
| --------------------------------- | ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Frontend (CDN)**                | Horizontal Scaling | Horizontal scaling makes it easier to add more servers, providing better fault tolerance.                                                                       |
| **Backend (Application Servers)** | Horizontal Scaling | Multiple backend servers ensure that more user requests can be handled simultaneously.                                                                          |
| **Load Balancer**                 | Horizontal Scaling | Multiple load balancers distribute traffic more effectively and provide redundancy.                                                                             |
| **Firewall**                      | Horizontal Scaling | Scaling horizontally ensures that more traffic can be processed and that the system remains secure.                                                             |
| **Database (SQL)**                | Vertical Scaling   | For relational databases, vertical scaling is often used since it's more complex to horizontally scale and maintain data consistency across multiple instances. |

---

### Summary of Design Choices:

- **Horizontal Scaling** is chosen for most components because it provides better fault tolerance, performance, and ease of scaling by adding more servers.
- **Geographical Redundancy** ensures that the system can handle regional failures, automatically routing traffic to the nearest available region.
- **Clusters** are used within each region to provide failover capabilities, ensuring that if one set of resources fails, the standby cluster takes over without affecting users.
- **Vertical Scaling** is applied to the relational database to improve capacity without the complexity of managing multiple database instances.

This architecture is designed to be highly available, scalable, and secure, making it well-suited for supporting a robust web application.