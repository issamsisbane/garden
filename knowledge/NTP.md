NTP works only on the UDP port.  So trying to telnet to port 123 will not work as telnet works over TCP.

Permet de lister les serveurs qui sont interrogés pour la synchro NTP :
``` sh
chronyc sources
```

Permet de voir l'état de la synchro NTP, si synchronized à false c'est qu'il y a un problème :
``` sh
datetimectl
```