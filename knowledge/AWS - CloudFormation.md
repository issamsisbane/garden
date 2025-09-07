
# Commands

#### Create a stack : 
``` bash
aws cloudformation create-stack --stack-name [name-of-the-stack] --template-body file://[name-of-the-file]
```
*The stack create the resources.* 

#### Update a stack : 
``` bash
aws cloudformation update-stack --stack-name [name-of-the-stack] --template-body file://[name-of-the-file]
```

#### Verify Stack Status :
Get the status of the stack :
``` bash
aws cloudformation describes-stacks --stack-name [name-of-the-stack]
```
*We can go to AWS Portal -> CloudFormation and find a report for our stack and deployments.*

#### Delete a stack :
```
aws cloudformation delete-stack --stack-name [name-of-the-stack]
```
*Deleting a stack, delete all the resources associated.*

# Resources

## Network
#### VPC

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Description: "CloudFormation template to create a VPC"

Resources:
  MyVPC:
    Type: "AWS::EC2::VPC"
    Properties:
      CidrBlock: "172.16.0.0/16" # IP range for the VPC
      EnableDnsSupport: "true" # Allow how resources in the vpc to commnicate with the amazon dns servers
      EnableDnsHostnames: "true" # Allow how resources in the vpc to receive dns hostnames
      Tags:
        - Key: Name
          Value: MyVPC
```

### Subnets

#### Public Subnet

``` yaml
# Public Subnet in Availability Zone 1
  PublicSubnet1A:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref MyVPC # Reference to the VPC created above
      CidrBlock: 172.16.1.0/24 # IP range for the subnet
      AvailabilityZone: !Select [0, !GetAZs ] # Get the first availability zone in the region
      MapPublicIpOnLaunch: true # Enable auto-assign public IP addresses to instances in the subnet
      Tags:
        - Key: Name
```
#### Private Subnet

``` yaml 
  # Application Private Subnet in Availability Zone 1
  AppPrivateSubnet1A:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref MyVPC
      CidrBlock: 172.16.2.0/24
      AvailabilityZone: !Select [0, !GetAZs ]
      Tags:
        - Key: Name
          Value: AppPrivateSubnet1A
```

### Gateway

#### Internet Gateway

``` yaml
# Internet Gateway
  InternetGateway:
    Type: AWS::EC2::InternetGateway
    Properties:
      Tags:
        - Key: Name
          Value: MyVPC-IGW

```

#### Attach gateway
``` yaml
  # Attach Internet Gateway to VPC
  AttachGateway:
    Type: AWS::EC2::VPCGatewayAttachment
    Properties:
      VpcId: !Ref MyVPC
      InternetGatewayId: !Ref InternetGateway
```

### Route Table

#### Public Route Table

``` yaml
  # Route Table
  PublicRouteTable:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref MyVPC
      Tags:
        - Key: Name
          Value: PublicRouteTable
```

#### Public Route

``` yaml
  # Public Route
  PublicRoute:
    Type: AWS::EC2::Route
    DependsOn: AttachGateway
    Properties:
      RouteTableId: !Ref PublicRouteTable
      DestinationCidrBlock: 0.0.0.0/0
      GatewayId: !Ref InternetGateway
```

#### Subnet Route Table Association

``` yaml
 # Public subnet association with route table
  PublicSubnet1ARouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref PublicSubnet1A
      RouteTableId: !Ref PublicRouteTable
```

## EC2 

#### EC2 Instance

``` yaml
  # Bastion Host EC2
  BastionHost:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: t2.micro # Instance type of our EC2 instance
      ImageId: ami-0cb0b94275d5b4aec # Amazon machine image ID
      SubnetId: !Ref PublicSubnet1A
      SecurityGroupIds:
        - !Ref BastionSG
      Tags:
        - Key: Name
          Value: BastionHost
```

#### Security Groups

``` yaml
# Bastion Security Group
  BastionSG:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Enable SSH access
      VpcId: !Ref MyVPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: "22"
          ToPort: "22"
          CidrIp: 89.84.22.189/32 # Your IP address
```


# Definition

**AWS CloudFormation** is Amazon Web Services' **native Infrastructure as Code (IaC)** solution. It allows you to define, provision, and manage AWS resources using code, providing a declarative way to set up infrastructure. By defining resources in a **CloudFormation template**, you can automate the process of infrastructure deployment in an AWS environment without manually configuring each service through the AWS Console or CLI.

In essence, CloudFormation acts as a **detailed blueprint** for your infrastructure, with the entire architecture defined in a single file using **JSON** or **YAML**.

## Key Concepts

###  Templates

A **template** is the file that contains the **configuration** for the AWS resources you want to create. The template specifies what resources are needed, how they should be configured, and the relationships between them. Templates are written in **JSON** or **YAML**, and they serve as the basis for creating and managing resources in AWS.

- **Template Structure**: Each template contains several sections, including:
    - **Resources**: The core of the template, specifying the AWS resources to be created (e.g., EC2 instances, S3 buckets, VPCs).
    - **Outputs** (optional): Return values from the stack, such as resource IDs or URLs.
    - **Parameters** (optional): Allow input values to customize the template at runtime.

### Stacks

A **stack** is a collection of AWS resources defined by a CloudFormation template. Stacks allow you to **group resources together** and manage them as a single unit. You can create, update, and delete entire stacks at once, which simplifies the process of managing multiple resources.

Instead of managing individual AWS services (like EC2, S3, and RDS) separately, you can define them all in one stack and create, update, or delete them in one action.

Deleting a stack will automatically delete all resources associated with it, making resource management much easier and ensuring nothing is left behind.

### ChangeSets

**ChangeSets** allow you to preview the impact of changes made to your infrastructure **before** they are applied. This feature is useful when updating stacks, as it provides an opportunity to review potential changes and avoid unintended consequences, such as resource deletion or configuration mismatches.

Before updating an existing stack to add a new EC2 instance, ChangeSets allow you to see how the update will affect the current infrastructure.

---

## How Does AWS CloudFormation Work?

Using AWS CloudFormation involves defining your infrastructure using code (templates), and then deploying that infrastructure as stacks. The workflow generally follows these steps:

It's possible to find the properties and the name of types by using the AWS CloudFormation [Documentation](https://docs.aws.amazon.com/cloudformation/). This is an example for [Subnets](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet.html).

### **Step 1 - Create a Template**

The first step in using CloudFormation is to define your infrastructure in a template. Below is an example of a simple CloudFormation template written in **YAML** to create an S3 bucket:

``` yaml
# CloudFormationTemplateVersion
# Description

AWSTemplateFormatVersion: "2010-09-09" # Supported version of the template
Description: "CloudFormation template to create an S3 bucket" # What this template does
Resources: # Resources to be created
  S3Bucket: # Logical name of the resource must be unique within the template
    Type: "AWS::S3::Bucket"
    Properties:
      BucketName: "my-issam-s3-bucket-yaml" # globaly lowercase unique name across AWS S3 buckets

```


### **Step 2 - Create a Stack**

Once the template is ready, you can deploy the infrastructure by creating a **stack**. This stack will provision all the resources specified in the template. You can create a stack using the AWS CLI:

``` bash
aws cloudformation create-stack --stack-name [name-of-the-stack] --template-body file://[name-of-the-file]
```

This command will take the template and create the resources defined in the CloudFormation stack.

### **Step 3 - Update the Stack**

When you need to change your infrastructure, you can modify the template and update the stack:

``` bash
aws cloudformation update-stack --stack-name [name-of-the-stack] --template-body file://[name-of-the-file]
```

This updates the resources in the stack to reflect the changes in the template.

### **Step 4 - Verify Stack Status**

After creating or updating a stack, you can check its status using the following command:

``` bash
aws cloudformation describes-stacks --stack-name [name-of-the-stack]
```

This will display the current status of the stack, such as **CREATE_COMPLETE** or **UPDATE_IN_PROGRESS**.

### **Step 5 - Delete the Stack**

To delete all resources associated with a stack, you can use the following command:

```
aws cloudformation delete-stack --stack-name [name-of-the-stack]
```


# Projects
## Project - Deploy a VPC

### Deployment

The objective of this project was to redeploy an entire **VPC architecture** using AWS CloudFormation. The goal was to create a **Bastion Host** to securely access an EC2 instance in a private subnet and ping another EC2 instance in a different **private subnet** located in a different **Availability Zone (AZ)**. This setup was previously done using **ClickOps** (manual setup via the AWS Console), but now, the goal is to automate it using **CloudFormation** for more efficiency and reproducibility ([ClickOps Version](https://medium.com/@issam.sisbane/enhancing-my-cloud-skills-week-5-aws-networking-7a93a503d6d5)). 

![[AWS_VPC_ARCHITECTURE_Bastion.png]]

You can find the complete CloudFormation template code [here](https://github.com/IssamSisbane/cea-cloudformation/blob/main/vpc.yaml).

For instance, this is how to deploy a VPC : 

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Description: "CloudFormation template to create a VPC"

Resources:
  MyVPC:
    Type: "AWS::EC2::VPC"
    Properties:
      CidrBlock: "172.16.0.0/16" # IP range for the VPC
      EnableDnsSupport: "true" # Allow how resources in the vpc to commnicate with the amazon dns servers
      EnableDnsHostnames: "true" # Allow how resources in the vpc to receive dns hostnames
      Tags:
        - Key: Name
          Value: MyVPC
```


This is how to deploy an ec2 instance : 

```yaml
  # Bastion Host EC2
  BastionHost:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: t2.micro # Instance type of our EC2 instance
      ImageId: ami-0cb0b94275d5b4aec # Amazon machine image ID, a template that contains the software configuration (OS). A blue print for our EC2 instance. An image that provides the software that is required to set up and boot an Amazon EC2 instanc
      KeyName: bastion # Key pair name to connect to the instance
      SubnetId: !Ref PublicSubnet1A
      SecurityGroupIds:
        - !Ref BastionSG
      Tags:
        - Key: Name
          Value: BastionHost
```

We need to get the keyname which reference a [[AWS - Key pair]] we previously created and download. It's needed to ssh to our ec2 instances.

You can find the appropriate AMI ID for your instance by navigating to the EC2 dashboard and selecting the relevant Amazon Machine Image : 
![[AMI_image_id.png]]

### Testing the setup

Once the VPC and Bastion Host are deployed, the next step is to test whether the architecture functions as expected by accessing the private instances through the Bastion Host.

1. **Accessing the Bastion Host via SSH**
``` bash
ssh -i bastion.pem ec2-user@[public-ip-address-of-the-ec2-instance]
```

2. **Copy our Key Pair to use ssh**
``` sh
scp -i bastion.pem bastion.pem ec2-user@15.237.184.39:~/private.pem # must be launch from our pc terminal and not ec2
```

3. **Updating File Permissions**
If we can't use the private.pem file in a linux envrionment we need to update permissions : 
``` bash
chmod 400 private.pem
```

This is what we get : 

![[bastion_project_terminal_screen.png]]
