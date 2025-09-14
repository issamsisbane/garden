
### 1. Setup Terraform for AWS : 

`main.ts`
``` hcl
provider "aws" {
  region = "eu-west-3"
}
```

### 2. Init the Terraform configuration

``` sh
terraform init
```

### 3. Plan to view the changes to the infrastructure

``` terraform
terraform plan
```

### 4. Apply the changes to the infrastructure

``` terraform
terraform apply
```

In my opinion, we get nicer outputs from Terraform than CloudFormation : 

![[terraform_plan_apply_1_screenshot.png]]

---