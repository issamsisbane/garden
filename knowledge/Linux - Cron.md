Pour vérifier les crons d'un user :

```
# current user
crontab -l

# root
sudo crontab -l
```

Pour editer les crons d'un user : 

```
crontab -e
```

Ces crons sont dans le dossier `/var/spool/cron`

Pour voir les logs de cron on fait : 

``` bash
sudo systemctl status cron
sudo grep CRON /var/log/syslog
```

[Explication expression cron](https://chatgpt.com/c/67f915da-cab0-8008-9f19-b7db316768ba)