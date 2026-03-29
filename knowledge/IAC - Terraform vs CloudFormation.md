
**AWS CloudFormation** is a native AWS Infrastructure as Code (IaC) service that provides a declarative way to define, provision, and manage resources within the AWS ecosystem. It uses **stacks**, which are collections of resources defined in configuration templates written in **YAML** or **JSON**. CloudFormation is AWS-specific, making it deeply integrated with AWS services but limited in portability outside of AWS.

**Terraform**, on the other hand, is a **cloud-agnostic** IaC tool developed by HashiCorp. It allows you to provision and manage infrastructure across multiple cloud providers and environments, such as AWS, Azure, GCP, and on-premises systems, by using a declarative approach and **HCL (HashiCorp Configuration Language)**.


| Tool           | Portability    | Resources Management | Advantages                     | Disadvantages                                                                 |
| -------------- | -------------- | -------------------- | ------------------------------ | ----------------------------------------------------------------------------- |
| CloudFormation | AWS Native     | Stacks               | Managed                        | AWS Lock in, Lot of code to write                                             |
| Terraform      | Cloud Agnostic | State files          | Cloud Agnostic & Big community | Learning Curve, Complex State Management, Licenses and no longer Open-source. |
In CloudFormation we talk about **properties** and in Terraform we talk about **resource parameters**.
