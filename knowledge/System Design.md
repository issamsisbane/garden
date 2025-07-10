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

![[user_client.png]]

---

## Scaling in System Design

**Scaling** refers to the system's ability to **handle increasing loads**. There are two primary types of scaling:

![[horizontal_vertical_sclaing.png]]
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

---

The basic architecture project : [[CEA - Project 1 - Design a Basic Architecture for a Web Application Project]]

**Blog about System Design :** 
https://www.linkedin.com/feed/update/urn:li:activity:7163502201875742720/?updateEntityUrn=urn%3Ali%3Afs_updateV2%3A%28urn%3Ali%3Aactivity%3A7163502201875742720%2CFEED_DETAIL%2CEMPTY%2CDEFAULT%2Cfalse%29

**How I would learn System Design (If I could start over) :**
https://www.linkedin.com/feed/update/urn:li:activity:7167746424078626816/?updateEntityUrn=urn%3Ali%3Afs_updateV2%3A(urn%3Ali%3Aactivity%3A7167746424078626816%2CFEED_DETAIL%2CEMPTY%2CDEFAULT%2Cfalse)