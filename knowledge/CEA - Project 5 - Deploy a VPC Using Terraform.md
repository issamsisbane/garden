---
state: published
tags: ["Cloud Academy"]
---
We already deploy a VPC architecture using clickOps & CloudFormation. You can find the link [here](https://medium.com/@issam.sisbane/design-a-vpc-for-a-basic-web-application-6dbc61abb888) Now we want to deploy it again using Terraform.

## 1. Define the remote state

We have to create an S3 bucket and a DynamoDB table. Then create a state.tf file : 

``` hcl
terraform {                                        # top level block to define terraform behaviour in our backend configuration
  backend "s3" {                                   # backend block to define the s3 backend
    bucket         = "terraform-state-bucket-is"   # bucket name to store the state file
    key            = "global/s3/terraform.tfstate" # path where to store the state file within the bucket
    region         = "eu-west-3"
    dynamodb_table = "terraform-locks" # dynamodb table name to lock the state file, to prevent concurrent modifications
  }
}

```

We want to execute `terraform init` to setup our remote state. Before we need to create our s3 bucket and our DynamoDB Table.

```
terraform init
```

To verify I tried : 

```
terraform plan
```

I run through this error : 

![[terraform_s3_error.png]]

It was because I name the partition key as `tf` but we need to name it `LockID`. I had to recreate a new table and change the state.tf file with the name of the new table. 

Now it's working : 

![[terraform_migrate_state_s3.png]]

## 2. Writing the configuration

I created the configuration in main.tf : 

```hcl
provider "aws" {
  region = "eu-west-3"
}

# VPC
resource "aws_vpc" "main" {
  cidr_block = "192.168.0.0/16"

  tags = {
    Name = "main-tf-vpc"
  }
}

# Subnet 1
resource "aws_subnet" "subnet1" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "192.168.1.0/24"
  availability_zone = "eu-west-3a"
  tags = {
    Name = "main-tf-vpc-subnet1"
  }
}

# Subnet 1
resource "aws_subnet" "subnet2" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "192.168.2.0/24"
  availability_zone = "eu-west-3b"
  tags = {
    Name = "main-tf-vpc-subnet2"
  }
}


# Internet Gateway
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "main-tf-vpc-igw"
  }
}

# Route Table
resource "aws_route_table" "rt" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id

  }
  tags = {
    Name = "main-tf-vpc-rt"
  }
}

# Route Table Association Subnet 1
resource "aws_route_table_association" "rta1" {
  subnet_id      = aws_subnet.subnet1.id
  route_table_id = aws_route_table.rt.id
}

# Route Table Association Subnet 2
resource "aws_route_table_association" "rta2" {
  subnet_id      = aws_subnet.subnet2.id
  route_table_id = aws_route_table.rt.id
}

```

## 3. Plan

We run : 

```
terraform plan
```

We can review everything that will be deployed : 

![[terraform_apply_screenshot.png]]

## 4. Apply 

We can then validate to let terraform create the resources : 

```
terraform apply
```

![[terraform_apply_screenshot_2.png]]
We can go to the AWS Portal to verify everything was created.

## 5. Clean

Finally we can delete the resources : 

```
terraform destroy
```

![[terraform_destroy.png]]

Finally, We could conclude that terraform has a less verbose syntax making it zasier than CLoudFormation. Moreover we have lot more informations in the CLI and we could directly see if everything is ok that is a lot better and more visual.