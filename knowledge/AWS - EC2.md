It's an AWS Resource that provides scalable Computing Capacity within the AWS environment.
It allows us to launch virtual servers known as instances. It's a physical machine hosts and AWS Datacenters. 

It provides compute for a lot of different needs which include : 
- CPU Power Intensive
- Memory intensive
- General Purpose
- Mahchine learning

It provides :
- Scalability
- Cost-efficiency : choose only what you need
- Flexibility : choice between different instance type

instance types :
different instance types optimized for different workloads.
- General purpose : Web Servers, Dev environment, small to medium database.
- Compute Optimized:  Batch Processing, High-performance Computing and Scientific Modeling.
- Memory optimised : High-performance Databases, In memory Databases, Big Data Analytics
- Storage optimized : Distributed File Systems, Data Warehousing, Log Processing
- Accelerated Computing : Machine Learning, Scientific Simulation or 3d rendering

Many differents kind for each types :
Example for general purpose : 
* t2.micro
* t3.large
* m5.xlarge


| Prefix                | Number  |
| --------------------- | ------- |
| t - Burstable         | large   |
| m - General Purpose   | xlarge  |
| c - Compute Optimized | 2xlarge |

Choosing the right instance depends on :
- Workload Requirements
- Performance Needs
- Budget Constraints

We need to considers the following factors : 
* CPU
* Memory
* Storage
* Network Bandwidth
* Hardware Needs

EC2 offers Three main pricing models :

### On-demand instances
Pay by the second for the instance you launch
No Long-term Commitments
No Upfront Payments

Ideal for Short-term, Spiky, or Unpredictable Workloads

### Reserved Instances
Low price
Commitment Of 1 or 3 years

ideal for steady-state / predictable workloads

### Spot Instances
Bid On Unused EC2 Capacity with prices fluctuating between supply & demand
Cost savings but might be interrupted if the spot price exceeds your bid.

**Spot Instances** in AWS are EC2 instances that use AWS's unused compute capacity, offered at a significantly reduced price compared to standard On-Demand instances. Here are the key points:

1. **Reduced Cost**: Spot Instances can offer up to 90% savings compared to On-Demand instances, making them ideal for cost-sensitive, flexible workloads.
    
2. **Available Capacity**: They use AWS's excess capacity, but their availability can vary. If AWS needs this capacity back (e.g., for On-Demand or Reserved instances), your Spot Instances may be interrupted.
    
3. **Interruption**: Spot Instances can be interrupted by AWS with a 2-minute notice when the capacity is needed elsewhere. They're best suited for workloads that can handle interruptions, like batch processing, data analysis, and CI/CD tasks.
    
4. **Use Cases**: Ideal for batch jobs, data analysis, video rendering, and test and development environments where interruptions are acceptable.
    
5. **Purchase Options**:
    
    - **Spot Fleet**: Manages a group of Spot Instances to maintain a specified capacity based on availability and pricing.
    - **Spot Blocks**: Run Spot Instances for a continuous period of 1 to 6 hours without interruption.
    - **Single Spot Instance**: Launch a single Spot Instance by specifying the desired number.
6. **Configuration**: Configurable via the AWS console, CLI, or APIs, with options to handle interruptions, such as stopping or terminating the instances.
    

In summary, AWS Spot Instances offer a cost-effective way to run flexible, interruption-tolerant workloads by utilizing AWS's excess compute capacity.

AWS Also proposes differents Processor Options such as : 
Intel Processors, AMD Processors, NVIDIA GPUs or AWS Graviton (custom-build [[ARM]] Processor)

We can use a combination of On-Demand and reserved instances to optimize costs.
It's important to watch the resources utilzation over the time in order to scale out or in. 
We can use monitoring tools such as Amazon CloudWatch to watch CPU, Memory and Network Usage. It will helps to identify Bottlenecks and select the most approprtiate ec2 instance.

[[EC2 Storage]]
