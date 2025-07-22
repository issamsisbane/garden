**AWS Regions** are a global network of clusters of data centers located in specific geographic areas. Each region is designed to be **completely independent** of others, providing resilience and fault isolation. This means if one region experiences an issue, it does not affect the others. Regions are identified using specific naming conventions, such as `eu-west-2` for the London region. This independence ensures that applications and services can remain available even in the event of a regional failure.
![[AWS_Regions.png]]



**AWS Availability Zones (AZs)** are isolated locations within an AWS region, each consisting of one or more discrete data centers with their own redundant power, networking, and connectivity. By being **physically separate** (typically up to 100 km apart), AZs provide enhanced fault tolerance and stability. They allow you to run services across multiple zones, ensuring that if one data center encounters an issue, the other zones can continue to operate without interruption, thereby maintaining high availability for your applications.

**Local Zones** are smaller, more localized extensions of AWS regions that bring compute, storage, and other AWS services closer to end-users. They are designed for **latency-sensitive applications** that require ultra-low latency by reducing the physical distance between the user and the cloud services. This is particularly useful for use cases like gaming, media streaming, and real-time simulations, where every millisecond counts.

![[AWS_Local_zones.png]]

**Edge Locations** are part of AWS's global Content Delivery Network (CDN), Amazon CloudFront. They **cache data** closer to end-users, ensuring even lower latency and faster delivery of content. By positioning data at the "last mile" between AWS and the client, edge locations significantly enhance the user experience by reducing the time it takes to load content, regardless of the user's geographic location.

### Service Availability Across Regions

Not all AWS services are available in every region. Services are launched in regions based on factors like demand, regulatory requirements, and infrastructure capabilities. However, some services, such as **IAM (Identity and Access Management)** and **S3 (Simple Storage Service)**, are considered **global services** and are accessible from any region.

### Reliability and Performance

AWS's vast and highly reliable global infrastructure ensures that your applications can be **highly available and performant** from anywhere in the world. By leveraging regions, availability zones, local zones, and edge locations, AWS enables you to build robust, low-latency applications that can withstand failures and deliver consistent performance to users globally.