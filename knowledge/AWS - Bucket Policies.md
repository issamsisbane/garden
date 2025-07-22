## Bucket Access Control Lists Vs Bucket Policies

1 ) Access Control Lists (ACLs) are legacy (but not deprecated), 2) bucket/IAM policies are recommended by AWS, and 3) ACLs give control over buckets AND objects, policies are only at the bucket level.

Decide which to use by considering the following: (As noted [below](https://stackoverflow.com/a/47818804/2121526) by John Hanley, more than one type could apply and the **most** restrictive/least privilege permission will apply.)

Use S3 bucket policies if you want to:

- Control access in S3 environment
- Know _who_ can access a bucket
- Stay under 20kb policy size max

Use IAM policies if you want to:

- Control access in IAM environment, for potentially more than just buckets
- Manage very large numbers of buckets
- Know what a _user_ can do in _AWS_
- Stay under 2-10kb policy size max, depending if user/group/role

Use ACLs if you want to:

- Control access to buckets _and objects_
- Exceed 20kb policy size max
- Continue using ACLs and you're happy with them

### When to Use an Object ACL

- when **objects** are not owned by **bucket owner**
- permissions vary by object

### When to Use a Bucket ACL

- to grant write permission to the Amazon S3 Log Delivery group to write access log objects to your bucket

### When to Use a Bucket Policy

- to manage cross-account permissions for all Amazon S3 permissions (ACLs can only do read, write, read ACL, write ACL, and "full control" - all of the previous permissions)

### When to Use a User Policy

- if you want to manage permissions individually by attaching policies to users (or user groups) rather than at the bucket level using a Bucket Policy

Acl are used to give a more granular control in order to allow and/or  deny  very specific objects etc. 