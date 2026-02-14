mariadb service could'nt launch correctly.

``` bash
sudo systemctl status mariadb
sudo journalctl -u mariadb -f
```

I restart the service, there was an error of permission on /var/log/mysql
Indeed the owner was root, so I change the ownership of the folder to mysql : 

``` bash
sudo chown -R mysql:mysql mysql
```

And relaunch the service : 
``` bash
sudo systemctl restart mariadb
```