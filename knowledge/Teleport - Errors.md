# Investigation EOF Error

* Test de création d'un vm rocky linux en local pour installer teleport avec self signed cert => OK
* Test de création d'une nouvelle vm Rocky Linux + test reinstallation de teleport de zéro avec self signed cert => Teleport OK mais toujours le même problème
* Test avec une IP Publique => Toujours le même problème
* Test avec une IP Publique + security group qui allow tout => Toujours le même problème
* Test avec le pc perso via Powershell => FONCTIONNE
* Suppression de la vm et test avec la machine TELEPORT1 de base =>  nouvelle erreur : 
``` err
ERROR REPORT:
Original Error: trace.aggregate connection error: desc = "transport: authentication handshake failed: read tcp 172.23.240.49:48504->142.44.48.2:443: read: connection reset by peer&#34;
Stack Trace:
github.com/gravitational/teleport/lib/client/api.go:4074 github.com/gravitational/teleport/lib/client.(*TeleportClient).ConnectToRootCluster
github.com/gravitational/teleport/tool/tsh/common/tsh.go:1956 github.com/gravitational/teleport/tool/tsh/common.onLogin
github.com/gravitational/teleport/tool/tsh/common/tsh.go:1433 github.com/gravitational/teleport/tool/tsh/common.Run
github.com/gravitational/teleport/tool/tsh/common/tsh.go:608 github.com/gravitational/teleport/tool/tsh/common.Main
github.com/gravitational/teleport/tool/tsh/main.go:26 main.main
        runtime/proc.go:271 runtime.main
        runtime/asm_amd64.s:1695 runtime.goexit
User Message: connection error: desc = "transport: authentication handshake failed: read tcp 172.23.240.49:48504->142.44.48.2:443: read: connection reset by peer&#34;
```

Investigation dans les log stormshield :
![[Pasted image 20241031141458.png]]

Ajout de la règle protocole applicatif : 
![[Pasted image 20241031141526.png]]

Cela fonctionne. 