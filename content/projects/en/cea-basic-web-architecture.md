---
title: "Design a Basic Web Application Architecture"
description: "This project aims to create a basic architecture for a Web Application."
lang: "en"
pubDate: "Sept 09 2024"
heroImage: "/portfolio/projects/cea-basic-web-architecture/cea-basic-web-architecture-cover.webp"
badge: "PERSONAL"
tags: ["Cloud", "Architecture", "Cloud Engineer Academy"]
---

## Project Objective

The goal of this project is to design a cloud infrastructure that supports a web application, ensuring high availability, fault tolerance, and scalability.

## Architecture Overview

![Week2_Architecture_basic.png](/portfolio/projects/cea-basic-web-architecture/Week2_Architecture_basic.png)

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

## Scaling Strategies for High Availability and Fault Tolerance

Each component in the architecture is scaled according to its function and needs to ensure performance and resilience:



| Component                         | Scaling Type       | Reason                                                                                                                                                          |
| --------------------------------- | ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Frontend (CDN)**                | Horizontal Scaling | Horizontal scaling makes it easier to add more servers, providing better fault tolerance.                                                                       |
| **Backend (Application Servers)** | Horizontal Scaling | Multiple backend servers ensure that more user requests can be handled simultaneously.                                                                          |
| **Load Balancer**                 | Horizontal Scaling | Multiple load balancers distribute traffic more effectively and provide redundancy.                                                                             |
| **Firewall**                      | Horizontal Scaling | Scaling horizontally ensures that more traffic can be processed and that the system remains secure.                                                             |
| **Database (SQL)**                | Vertical Scaling   | For relational databases, vertical scaling is often used since it's more complex to horizontally scale and maintain data consistency across multiple instances. |

---

## Summary of Design Choices

- **Horizontal Scaling** is chosen for most components because it provides better fault tolerance, performance, and ease of scaling by adding more servers.
- **Geographical Redundancy** ensures that the system can handle regional failures, automatically routing traffic to the nearest available region.
- **Clusters** are used within each region to provide failover capabilities, ensuring that if one set of resources fails, the standby cluster takes over without affecting users.
- **Vertical Scaling** is applied to the relational database to improve capacity without the complexity of managing multiple database instances.

This architecture is designed to be highly available, scalable, and secure, making it well-suited for supporting a robust web application.