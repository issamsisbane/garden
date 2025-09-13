Install cronie : 
```
sudo yum install cronie
```

Add a cron for the root user : 
```
`*/5 * * * * echo hello > /tmp/cron_text`
```