The apache app (httpd) should be accessible from the jump host when using : 
``` bash
curl http://stapp01:8087
```

We have this error : 
![[Pasted image 20250913163233.png]]

By sshing to the machine and doing a curl on localhost we have a response with sendmail in it.

By doing : 
``` bash
telnet localhost 8087
```

we see that the port is used.

By using : 

``` bash
sudo netstat -tulnp | grep ':8087'
```

We see that the port is used by sendmail.

``` bash
sudo systemctl status httpd
```

We see that httpd is stopped caused by an error because the port was already in use.

So we need to stop it change the port and relaunch httpd.

# 1 - Change sendmail config

Stop sendmail : 
```
sudo systemctl stop sendmail
```

Change the port form `8087` to `25` in `/etc/mail/sendmail.mc`

Relanch sendmail : 
```
sudo systemctl restart sendmail
```

# 2 - Restart httpd

``` bash
sudo systemctl restart httpd
```

We verify it run  :
``` bash
sudo systemctl status httpd
```

![[Pasted image 20250913163056.png]]

# 3 - Test again

From the jumphost : 
![[Pasted image 20250913163442.png]]

We still have the same issue.

# 4 - Debug

It doesn't seem to be firewall error : 
```
sudo iptables -L -n
```

![[Pasted image 20250913163954.png]]

But in the httpd config file we had : 
```
Listen 8087
```

By default it only listens to `127.0.0.1`.
So we have to change it to : 
``` 
Listen 0.0.0.0:8087
```

restart apache service : 
``` bash
sudo systemctl restart apache
```

not working again, but by adding this : 
```
sudo iptables -I INPUT -p tcp --dport 8087 -j ACCEPT
```

It works. This doesn't makes sense because we have already this rule :
![[Pasted image 20250913165444.png]]
allowing all the traffic


> [!IMPORTANT] Title
> WE needed another rule because : 
> "- Autorise tout trafic **entrant** qui fait partie d’une **connexion déjà établie** ou **connexe**."
