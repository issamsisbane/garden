
## Setup

Setup your account in the console

https://k21academy.com/amazon-web-services/aws-solutions-architect/aws-cli/

go to IAM => My Security Credentials => Create access key => choose for CLI

then in the aws console in you terminal : 

``` bash
aws configure
```

## S3 Bucket

Commands to interact with S3 buckets

### List S3 Bucket

``` bash
aws s3 ls 
```

### Create S3 Bucket

``` bash
aws s3 mb s3://[name-of-the-bucket]
```

### Add a File to Bucket

```
aws s3 cp [name-of-the-file] s3://[name-of-the-bucket]
```

### List bucket content

```
aws s3 ls s3://[name-of-the-bucket]
```


## IAM

Command to interact with IAM

### Create a new IAM User

```
aws iam create-user --user-name [name-of-the-user]
```

### List IAM Users

```
aws iam list-users
```

### Attach policy to a user

```
aws iam attach-user-policy --user-name [name-of-the-user] --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
```

### Verify policy attachement

```
aws iam list-attached-user-policies --user-name [name-of-the-user]
```

### Generate access keys

Enable programmatic access for the user by using the `AccessKeyId` and the `SecretAccessKey`

```
aws iam create-access-key --user-name [name-of-the-user]
```