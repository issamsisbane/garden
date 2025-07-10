---
title: "Deploy a Next-Js Application using Terraform"
description: "This project aims to deploy a Next-Js application using Terraform, S3 & AWS CloudFront."
lang: "en"
pubDate: "Sept 27 2024"
heroImage: "/portfolio/projects/cea-nextjs-terraform/cloudfront-terraform.drawio.png"
badge: "PERSONAL"
tags: ["Cloud", "AWS", "NextJs", "Terraform", "Cloud Engineer Academy"]
selected: true
---

*This project gave me the opportunity to deploy a static website using object storage and a CDN for the first time, providing valuable hands-on experience. It was particularly engaging to work on a project that closely simulated real-world scenarios. This project was part of the Cloud Engineer Academy courses, further deepening my understanding of cloud technologies.*

---

1 — **Requirements** </br>
2 — **S3 & CloudFront** </br>
3 — **Deployment** </br>
4 — **Conclusion** </br>

---

## 1 - Requirements

### Scenario Overview

**Client:** James Smith, a freelance web designer

**Project:** Portfolio Website Deployment

**Project Description:**  James Smith, a freelance web designer, wants to showcase his work and attract potential clients through an online portfolio. He has designed a modern, responsive single-page website using the Next.js framework. James requires this website to be hosted on a robust, scalable, and cost-effective platform. Additionally, the website needs to be highly available and deliver fast loading times for a global audience.

**My Role:** As a team of cloud engineers, The task is to deploy James's Next.js portfolio website on AWS using Infrastructure as Code (IaC) principles with Terraform. This project will give me hands-on experience with Terraform, S3, and CloudFront, mimicking a real-world deployment scenario.

---

### Problem Statement

James needs his portfolio website to be:

1. **Highly Available:** The website should be accessible to users worldwide with minimal downtime.
2. **Scalable:** As his portfolio gains traction, the hosting solution should handle increased traffic without performance degradation.
3. **Cost-Effective:** Hosting costs should be optimized, avoiding unnecessary expenses.
4. **Fast Loading:** The website should load quickly for visitors, providing a seamless user experience.

Given these requirements, deploying the website using AWS services such as S3 for static hosting and CloudFront for content delivery is an ideal solution. Using Terraform will allow you to automate and manage the infrastructure efficiently.

---

### Project Outcome

By the end of this project, we should have:

1. **Deployed a Next.js Website:** Successfully deployed the Next.js portfolio site on AWS.
2. **Implemented Infrastructure as Code:** Used Terraform to automate the creation of AWS resources.
3. **Configured Global Content Delivery:** Set up AWS CloudFront to deliver the website content globally with low latency.
4. **Ensured Security and Performance:** Applied best practices for security and performance, ensuring a fast and secure website for James's portfolio.
5. **Deploy everything to github:** Create a github repo and host all your project files and code there.

**Here is the Architecture design:**

**![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/site/2148043546/products/d6c6af7-3646-036-7b37-136cd2828ff_Screenshot_2024-05-30_at_10.10.53.png)

We would only use the template example from nextJS to simplify but we could use any static website.
## 2 - S3 & Cloudfront

Using **Amazon CloudFront** with **Amazon S3** allows you to set up a **Content Delivery Network (CDN)** that improves the **performance**, **security**, and **scalability** of your website or application. By delivering content from servers located closer to the user, CloudFront can significantly reduce latency and improve the speed at which data is delivered. I never used a CDN before, I read the documentation about how it works wit S3. It's pretty simple. 

![](/portfolio/projects/cea-nextjs-terraform/cloudform_oai_s3.png)

The diagram above outlines the relationship between the S3 bucket, CloudFront, and OAI. Here's how the components fit together:

1. **CloudFront Distribution**:
    
    - Acts as the **public-facing endpoint** that users interact with.
    - The distribution is configured to use your **S3 bucket** as the **origin** for serving static content (like `index.html` or other files).
2. **S3 Bucket**:
    
    - The **bucket** stores the content (e.g., static web pages, images, videos).
    - It should be **private** to ensure that no one can directly access the bucket from the internet.
3. **Origin Access Identity (OAI)**:
    
    - The OAI is associated with the CloudFront distribution and is the **identity** used to access the private S3 bucket.
    - This ensures that only CloudFront can access your S3 bucket, providing secure access control.
4. **Bucket Policy**:
    
    - You need to configure an **S3 bucket policy** to explicitly allow CloudFront (via the OAI) to access the content in your S3 bucket.
    - This restricts public access to the bucket and allows only requests coming from the CloudFront distribution.

## 3. Deployement

You can find all the project [here](https://github.com/IssamSisbane/terraform-portfolio-project/tree/main/terraform).

### Step 1 : Public Access

For this project, I first allow public access by anyone from anywhere.

``` hcl
provider "aws" {
  region = "eu-west-3"
}

# Create a new S3 bucket
resource "aws_s3_bucket" "portfolio_is_bucket" {
  bucket = "portfolio-nextjs-is"

  tags = {
    Name = "portfolio-nextjs-is"
  }
}

# Enable bucket ownership controls to enforce bucket owner permissions
resource "aws_s3_bucket_ownership_controls" "portfolio_is_ownership_controls" {
  depends_on = [
    aws_s3_bucket.portfolio_is_bucket
  ]

  bucket = aws_s3_bucket.portfolio_is_bucket.id

  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

# Disable public access block to allow public access to the bucket
resource "aws_s3_bucket_public_access_block" "portfolio_is_public_access_block" {
  depends_on = [
    aws_s3_bucket.portfolio_is_bucket
  ]

  bucket = aws_s3_bucket.portfolio_is_bucket.id

  # Set everything to false to allow public access to the bucket
  block_public_acls       = false # Block public ACLs 
  block_public_policy     = false # Block public bucket policies
  ignore_public_acls      = false # Ignore public ACLs
  restrict_public_buckets = false # Block public and cross-account access to buckets
}

resource "aws_s3_bucket_policy" "portfolio-bucket_policy" {
   depends_on = [
     aws_s3_bucket.portfolio-bucket,
     aws_s3_bucket_public_access_block.my_bucket_public_access_block
   ]
   bucket = aws_s3_bucket.portfolio-bucket.id
   policy = jsonencode({
     Version = "2012-10-17",
     Statement = [
       {
         Sid       = "PublicReadGetObject",
         Effect    = "Allow",
         Principal = "*",
         Action    = "s3:GetObject",
         Resource  = "${aws_s3_bucket.portfolio-bucket.arn}/*",
       },
     ],
   })

# Enable the bucket to host a static website
resource "aws_s3_bucket_website_configuration" "portfolio_is_website" {
  depends_on = [
    aws_s3_bucket.portfolio_is_bucket
  ]

  bucket = aws_s3_bucket.portfolio_is_bucket.id

  index_document {
    suffix = "index.html"
  }
  error_document {
    key = "index.html"
  }
}


# Create an origin access identity to allow CloudFront to reach the bucket
resource "aws_cloudfront_origin_access_identity" "portfolio_is_origin_access_identity" {
  comment = "Allow CloudFront to reach the bucket"
}

# Create a CloudFront distribution to serve the static website
resource "aws_cloudfront_distribution" "portfolio_is_cloudfront" {

  # Describes the origin of the files that you want CloudFront to distribute  
  origin {
    domain_name = aws_s3_bucket.portfolio_is_bucket.bucket_regional_domain_name
    origin_id   = aws_s3_bucket.portfolio_is_bucket.id # unique identifier for the origin

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.portfolio_is_origin_access_identity.cloudfront_access_identity_path
    }
  }

  enabled             = true         # enable cloud front distribution directly after creation
  is_ipv6_enabled     = true         # enable IPv6 support
  default_root_object = "index.html" # default root object to serve when a request is made to the root domain


  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"] # HTTP methods that CloudFront processes and forwards to the origin
    cached_methods   = ["GET", "HEAD"]            # HTTP methods for which CloudFront caches responses
    target_origin_id = aws_s3_bucket.portfolio_is_bucket.id

    # Forward the query string to the origin that is associated with this cache behavior
    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
    viewer_protocol_policy = "redirect-to-https" # HTTP and HTTPS requests are automatically redirected to HTTPS
    min_ttl                = 0                   # minimum amount of time that you want objects to stay in a CloudFront cache
    default_ttl            = 3600                # default amount of time (in seconds) that you want objects to stay in CloudFront caches
    max_ttl                = 86400               # maximum amount of time (in seconds) that you want objects to stay in CloudFront caches
  }

  # Allow cloudfront to use default certificate for ssl
  viewer_certificate {
    cloudfront_default_certificate = true
  }

  # Define restrictions on the geographic distribution of your content
  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  tags = {
    Name = "portfolio-cloudfront-nextjs-is"
  }

}
```

### Step 2 : Allowing access from CloudFront only

We have our cloudfront distribution configure with our S3 bucket as origin. We only want people to access our index.html file in our bucket only from CloudFront. So we use an OAI. The OAI allow S3 to indentify our cloudfront distribution. We need to create a bucket policy to allow access to the bucket. What we did earlier wasn't really best practice because our bucket is accessible from anywhere by anybody.

Then I restrict the access. To access the bucket files we need to pass by our CloudFront CDN.

``` hcl
provider "aws" {
  region = "eu-west-3"
}

# Create a new S3 bucket
resource "aws_s3_bucket" "portfolio_is_bucket" {
  bucket = "portfolio-nextjs-is"

  tags = {
    Name = "portfolio-nextjs-is"
  }
}

# Enable bucket ownership controls to enforce bucket owner permissions
resource "aws_s3_bucket_ownership_controls" "portfolio_is_ownership_controls" {
  depends_on = [
    aws_s3_bucket.portfolio_is_bucket
  ]

  bucket = aws_s3_bucket.portfolio_is_bucket.id

  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

# Disable public access block to allow public access to the bucket
resource "aws_s3_bucket_public_access_block" "portfolio_is_public_access_block" {
  depends_on = [
    aws_s3_bucket.portfolio_is_bucket
  ]

  bucket = aws_s3_bucket.portfolio_is_bucket.id

  # Set everything to false to allow public access to the bucket
  block_public_acls       = true # Block public ACLs 
  block_public_policy     = true # Block public bucket policies
  ignore_public_acls      = true # Ignore public ACLs
  restrict_public_buckets = true # Block public and cross-account access to buckets
}

################################
# ACLs are used to have more fine-grained control over objects in the bucket | Not needed for now
# # Set the bucket Access Control List to public-read allowing public read access to the bucket
# resource "aws_s3_bucket_acl" "bucket_acl" {
#   depends_on = [
#     aws_s3_bucket_ownership_controls.bucket_ownership_controls,
#     aws_s3_bucket_public_access_block.my_bucket_public_access_block
#   ]

#   bucket = aws_s3_bucket.portfolio-bucket.id
#   acl    = "public-read"
# }
################################

# Create a bucket policy to allow read access only from CloudFront
resource "aws_s3_bucket_policy" "portfolio_is_bucket_policy" {
  depends_on = [
    aws_s3_bucket.portfolio_is_bucket,
    aws_s3_bucket_public_access_block.my_bucket_public_access_block,
    aws_cloudfront_origin_access_identity.origin_access_identity
  ]
  bucket = aws_s3_bucket.portfolio_is_bucket.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid    = "PublicReadGetObject",
        Effect = "Allow",
        Principal = {
          AWS = "${aws_cloudfront_origin_access_identity.origin_access_identity.iam_arn}" # The ARN of the CloudFront origin access identity
        },
        Action   = "s3:GetObject",
        Resource = "${aws_s3_bucket.portfolio_is_bucket.arn}/*",
      },
    ],
  })
}

################################
# Allow public read access to the bucket from any IP address | We do not want that
# resource "aws_s3_bucket_policy" "portfolio-bucket_policy" {
#   depends_on = [
#     aws_s3_bucket.portfolio-bucket,
#     aws_s3_bucket_public_access_block.my_bucket_public_access_block
#   ]
#   bucket = aws_s3_bucket.portfolio-bucket.id
#   policy = jsonencode({
#     Version = "2012-10-17",
#     Statement = [
#       {
#         Sid       = "PublicReadGetObject",
#         Effect    = "Allow",
#         Principal = "*",
#         Action    = "s3:GetObject",
#         Resource  = "${aws_s3_bucket.portfolio-bucket.arn}/*",
#       },
#     ],
#   })
# }
################################

# Enable the bucket to host a static website
resource "aws_s3_bucket_website_configuration" "portfolio_is_website" {
  depends_on = [
    aws_s3_bucket.portfolio_is_bucket
  ]

  bucket = aws_s3_bucket.portfolio_is_bucket.id

  index_document {
    suffix = "index.html"
  }
  error_document {
    key = "index.html"
  }
}


# Create an origin access identity to allow CloudFront to reach the bucket
resource "aws_cloudfront_origin_access_identity" "portfolio_is_origin_access_identity" {
  comment = "Allow CloudFront to reach the bucket"
}

# Create a CloudFront distribution to serve the static website
resource "aws_cloudfront_distribution" "portfolio_is_cloudfront" {

  # Describes the origin of the files that you want CloudFront to distribute  
  origin {
    domain_name = aws_s3_bucket.portfolio_is_bucket.bucket_regional_domain_name
    origin_id   = aws_s3_bucket.portfolio_is_bucket.id # unique identifier for the origin

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.portfolio_is_origin_access_identity.cloudfront_access_identity_path
    }
  }

  enabled             = true         # enable cloud front distribution directly after creation
  is_ipv6_enabled     = true         # enable IPv6 support
  default_root_object = "index.html" # default root object to serve when a request is made to the root domain


  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"] # HTTP methods that CloudFront processes and forwards to the origin
    cached_methods   = ["GET", "HEAD"]            # HTTP methods for which CloudFront caches responses
    target_origin_id = aws_s3_bucket.portfolio_is_bucket.id

    # Forward the query string to the origin that is associated with this cache behavior
    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
    viewer_protocol_policy = "redirect-to-https" # HTTP and HTTPS requests are automatically redirected to HTTPS
    min_ttl                = 0                   # minimum amount of time that you want objects to stay in a CloudFront cache
    default_ttl            = 3600                # default amount of time (in seconds) that you want objects to stay in CloudFront caches
    max_ttl                = 86400               # maximum amount of time (in seconds) that you want objects to stay in CloudFront caches
  }

  # Allow cloudfront to use default certificate for ssl
  viewer_certificate {
    cloudfront_default_certificate = true
  }

  # Define restrictions on the geographic distribution of your content
  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  tags = {
    Name = "portfolio-cloudfront-nextjs-is"
  }

}
```

### Step 3 : Build & Site Upload
We need to apply the configuration using Terraform. CloudFront can take some time to be created. Then we just to need to build our next-js application using : 

```sh
npm run build
```

We need to copy all the content in the `out` folder created to our bucket.

Finally, We can confirm that only cloudfront can access s3 files.

![](/portfolio/projects/cea-nextjs-terraform/nextjs_cloudfront_browser_screenshot.png)

## Conclusion | Best practices

Write name between quotes, use underscore instead of dash and do not include resource type in the resource name :

```hcl
resource "aws_s3_bucket" "portfolio" {}
```

if we use terraform destroy we have to delete all objects within our bucket before.
