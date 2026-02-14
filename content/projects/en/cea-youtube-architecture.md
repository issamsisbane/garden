---
title: "Design an Architecture for Youtube"
description: "This project aims to design an architecture for few most used Youtube functionalities."
lang: "en"
pubDate: "Sept 16 2024"
heroImage: "/portfolio/projects/cea-youtube-architecture/youtube.webp"
badge: "PERSONAL"
tags: ["Cloud", "Architecture", "Cloud Engineer Academy"]
---

1 — **Requirements** </br>
2 — **Upload a Video** </br>
3 — **Search and watch Videos** </br>
4 — **Key System Components** </br>
5 — **Considerations** </br>
6 — **Conclusion** </br>

---

## 1 - Requirements

Before designing an architecture, it’s crucial to understand the **features** of the application and define the **architecture requirements**.

The key features are :

- **Upload Videos**
- **Search Videos**
- **View Videos**
- **Filter Adult Content**

The architecture must be :

- **Scalability**: The system must handle millions of users and video uploads simultaneously.
- **Resilience**: The system should be fault-tolerant and available at all times.
- **Cost Efficiency**: Optimized use of resources to balance cost with performance.
- **Security**: The platform must ensure secure data storage and prevent unauthorized access.

---

## 2 - Video Upload


![](/portfolio/projects/cea-youtube-architecture/youtube_upload_video_architecture.gif)

### 1. **Access YouTube**

**Content creators** (YouTubers) can access YouTube via their **browser** using HTTPS for secure communication.

### 2. **Uploading a Video**

#### **Video Data**

The first part of the upload process is transferring the video itself.

- **YouTubers** typically upload videos at high resolutions (e.g., 4K).
- Since video data is **unstructured** and requires **scalability** and **durability**, an **Object Storage** service (like **Amazon S3**) is ideal for storing video files. Object storage is cost-effective because it supports pay-as-you-go pricing, meaning you only pay for the storage you use, which makes it suitable for massive volumes of video data.

#### **Metadata**

Metadata includes details like the video’s title, description, tags, and more. This is **structured data** that requires fast, scalable storage.

- **Relational databases** (such as MySQL) might struggle to handle the sheer volume of concurrent users on YouTube because relational databases scale **vertically**, which can lead to increased costs and performance bottlenecks.
- Instead, using a **Non-relational (NoSQL) database** (like **Cassandra** or **DynamoDB**) is a better option because it can scale **horizontally**, distributing the load across many servers, making it ideal for massive amounts of metadata.

### 3. **Video Processing**

Once the video is uploaded, YouTube processes the video by:

- **Converting it into multiple resolutions** (e.g., 240p, 360p, 720p, 1080p, 4K) to ensure it can be played smoothly across various devices and internet speeds.
- This can be done using **microservices**, **dedicated servers** or **Serverless Functions** to handle the video transcoding, making sure the content is accessible to everyone.

### 4. **Video Analysis**

Simultaneously with processing, **automated content analysis** checks the video for inappropriate content. The system analyzes each video frame by frame to detect anything that violates YouTube’s policies.

- If flagged, the **metadata** is updated to restrict or block access to the video, ensuring compliance with YouTube's content policies.

### 5. **Optimized Storage**

Once the video is processed, the various resolution versions are stored in another **object storage** system, optimized for streaming.

- **Serverless functions** (like **AWS Lambda**) can be used to automate the process of moving videos to the correct storage locations based on events (e.g., after a video is uploaded).

### 6. **Serving Content**

To ensure fast content delivery, YouTube uses a **Content Delivery Network (CDN)**.

- **CDN caching** stores video content closer to the user's geographical location. When a user watches a video, the CDN ensures the video is served from the closest available cache, reducing **load times** and **latency**.
- If the video is not cached locally, it is fetched from the object storage and then cached for future requests in that region.

---

## 3 - Searching and Watching Videos

![](/portfolio/projects/cea-youtube-architecture/youtube_watch_video_architecture.gif)

### 1. **Accessing YouTube**

When a user visits YouTube, they are presented with the homepage.

- The **homepage** consists mostly of **static content**, such as video thumbnails and recommended videos. This static content is stored in **object storage**, allowing faster page loads.

### 2. **Searching for a Video**

When a user searches for a video, the search request is sent to the **CDN**:

- If the **search results** are cached in the CDN, the user will receive the results instantly.
- If not, the **API Gateway** receives the search query and forwards it to a **serverless function** that queries the **metadata database** for relevant video information (e.g., title, description, tags). The results are then displayed on the search results page, which consists mostly of metadata.

The homepage is **static**, but after performing a search, YouTube's **dynamic content** comes into play, showing personalized search results.

### 3. **Watching a Video**

When a user clicks on a video:

- If the video is cached in the **CDN**, it will be served instantly.
- If the video is not cached, the CDN fetches it from the **object storage** and simultaneously caches it for future users in the same region.

This system ensures that **popular content** is always served with minimal latency and optimized bandwidth.

---

## 4 - Key System Components in YouTube Design

### 1. **Object Storage**

- Used to store unstructured video files.
- Provides **scalability**, **durability**, and **cost efficiency** for large volumes of data.

### 2. **Non-relational Databases (NoSQL)**

- Used to store **metadata** for millions of videos, ensuring that the database scales **horizontally** to handle high traffic. We selected a NoSQL database because the metadata are **free form type** of data (meaning we can have different fields depending on the video) and also because it easily scalable compared to relational database.

### 3. **Video Processing and Analysis**

- Responsible for converting videos into multiple formats and performing **content checks** to flag inappropriate content.

### 4. **CDN (Content Delivery Network)**

- Ensures that video content is cached close to users, reducing load times and improving streaming performance.

### 5. **API Gateway**

- Serves as a central hub for routing **search requests** and **dynamic content** queries to the appropriate backend services.

### 6. **Serverless Functions**

- These handle event-based tasks such as moving video files to different storage locations or responding to search queries.

---

## 5 - Considerations

### **1. Scalability**

To handle the massive user base and continuous video uploads, YouTube's architecture must be designed to scale horizontally and vertically across multiple layers:

- **Video Upload and Storage**:
    
    - **Object Storage**: Using a scalable object storage service allows YouTube to store and manage vast amounts of unstructured video data. Object storage automatically scales to accommodate growing data volumes, ensuring seamless storage of videos, thumbnails, and other media assets.
    - **Auto-Scaling for Video Processing**: The video processing layer (e.g., transcoding) uses an auto-scaling group of servers or microservices to handle fluctuating loads. This setup ensures that multiple videos can be processed concurrently, dynamically allocating more resources during peak times and reducing them during off-peak hours.
- **Metadata Storage**:
    
    - **NoSQL Databases**: A horizontally scalable NoSQL database allows the system to manage and search through billions of metadata entries efficiently. NoSQL databases scale out by adding more nodes, ensuring high throughput and low latency even under heavy traffic.
- **Content Delivery**:
    
    - **CDN**: The CDN ensures that video content is cached close to users, reducing the load on the origin servers and handling large numbers of concurrent streaming requests. CDNs dynamically scale their edge locations globally, distributing the load based on user demand patterns.

### **2. Resilience**

Resilience ensures that YouTube remains available and operational even in the face of failures, network issues, or hardware faults:

- **Data Redundancy**:
    
    - **Object Storage**: Services like Amazon S3 provide built-in redundancy by replicating video files across multiple data centers (availability zones), ensuring durability and availability even if one data center experiences issues.
    - **Database Replication**: NoSQL databases support multi-region replication, ensuring metadata is synchronized and available across different data centers. In the event of a regional failure, traffic can be redirected to a replica in another region without service interruption.
- **Fault Tolerance**:
    
    - **Microservices Architecture**: Breaking down functionalities into microservices allows the system to isolate failures. If the video processing service fails, it doesn’t affect the search or video playback services. Each microservice can be independently managed and scaled, providing fault isolation.
    - **Load Balancers**: Load balancers distribute traffic across multiple servers or services. If one server goes down, the load balancer automatically reroutes traffic to healthy instances, ensuring continuous service availability.
- **Graceful Degradation**:
    
    - **Fallback Mechanisms**: If a particular service (e.g., video processing) is temporarily unavailable, the system can degrade gracefully by, for instance, allowing users to upload videos and view existing ones while deferring new video processing tasks.

### **3. Latency**

Latency is critical for YouTube, as users expect videos to load quickly and play smoothly:

- **Video Playback**:
    
    - **CDN Caching**: By caching video content at CDN edge locations closer to the user's geographical location, the time it takes to fetch and start playing a video is minimized. This significantly reduces latency and provides a buffer-free streaming experience.
    - **Adaptive Bitrate Streaming**: Videos are transcoded into multiple resolutions, enabling adaptive bitrate streaming. This technique adjusts the video quality in real-time based on the user’s internet speed, ensuring smooth playback with minimal buffering.
- **Search and Data Access**:
    
    - **In-Memory Caching**: Frequently accessed data, such as popular video metadata, can be cached in-memory (e.g., using Redis or Memcached) to reduce the time it takes to retrieve search results or video details.
    - **Distributed Query Processing**: NoSQL databases are designed for low-latency data access. By distributing queries across multiple nodes, the system can quickly retrieve metadata for search and filtering, even under heavy user loads.
- **API Gateway**:
    
    - **Efficient Routing**: The API Gateway optimizes routing by directing requests to the appropriate service endpoints. It can also implement caching for frequently requested data, reducing the load on backend services and improving response times.

---

## 6 - **Conclusion**

YouTube’s architecture must handle massive traffic, support the storage and retrieval of large volumes of video data, and deliver content quickly to users around the world. By leveraging **object storage** for videos, **NoSQL databases** for metadata, and **CDNs** for content distribution, YouTube ensures **scalability**, **high availability**, and **performance**. Additionally, the use of **serverless functions** and **API Gateways** helps manage dynamic requests efficiently and enables seamless interaction with a complex microservices architecture.