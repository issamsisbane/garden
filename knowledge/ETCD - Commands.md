ETCDCTL is the CLI tool used to interact with ETCD.  
  
ETCDCTL can interact with ETCD Server using 2 API versions - Version 2 and Version 3.  By default its set to use Version 2. Each version has different sets of commands.  

For example ETCDCTL version 2 supports the following commands:

1. etcdctl backup
2. etcdctl cluster-health
3. etcdctl mk
4. etcdctl mkdir
5. etcdctl set

  

Whereas the commands are different in version 3

1. etcdctl snapshot save 
2. etcdctl endpoint health
3. etcdctl get
4. etcdctl put

  
To set the right version of API set the environment variable ETCDCTL_API command

`export ETCDCTL_API=3`

  

When API version is not set, it is assumed to be set to version 2. And version 3 commands listed above don't work. When API version is set to version 3, version 2 commands listed above don't work.