# 1 - Install tomcat

```
sudo yum install tomcat
```

# 2 - Update the conf to port 6200

```
vi /etc/tomcat/server.xml
```

In Connector we change port from 8080 to 6200

# 3 - Copy ROOT.war into the machines

back to the bastion host : 
``` bash
ssh /tmp/ROOT.war tomy@stapp01:/tmp
```

back to the machine : 
``` bash
cp /tmp/ROOT.war /usr/share/tomcat/webapps/
```

Naming the file `ROOT.war` allow it to be served at the root path. localhost/ and no `localhost/nameofthefile`
# 4 - Restart tomcat

```
sudo systemctl restart tomcat
```

# 5 - Test

```
curl http://stapp01:6200
```