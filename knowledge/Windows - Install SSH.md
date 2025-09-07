# Avec Internet

## Powershell Commands

``` powershell
# Verifier l'installation de OpenSSH-Server
Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH*'

# Installation de OpenSSh-Server
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0

# Demarrer le service OpenSSH
Start-Service sshd

# Configurer le démarrage automatique de SSH
Set-Service -Name sshd -StartupType 'Automatic'

# Ajouter SSH au parefeu Windows
New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
```

## Connexion Virtualbox

En mode NAT, configurer la redirection de ports.

Ajouter une nouvelle règle pour rediriger le port 2222 (ou un autre port que tu choisis) de l'hôte vers le port 22 de l'invité :

- **Protocole** : TCP
- **Port hôte** : 2222
- **Adresse IP invité** : (Adresse IP de la VM trouvée avec `ipconfig` dans la VM)
- **Port invité** : 22

## Test de la connexion SSH

``` sh
ssh username@127.0.0.1
```

## Création d'un compte Administrateur

1 / Ajout de l'utilisateur

``` sh
net user [username] [password] /add
```

2 / Ajout au group administrateurs

```
net localgroup Administrators nouvel_utilisateur /add
```

3 / Désactiver l'expiration du mot de passe

```
wmic UserAccount where Name='myuser' set PasswordExpires=False
```

# Sans Internet

On veut installer SSH Server dans la machine Windows Server 2019 mais les machines en PREPROD n'ont pas accès à Internet et même en activant via Stormshield cela ne fonctionnait pas. Il faut donc trouver une alternative. Cette alternative est d'utiliser RDP et le partage de fichier avec l'hôte.

[How to install OpenSSH server on Windows Server 2019 in offline environment | The Commonplace book by IT-Infrastructure Engineer (it-infra-ya.com)](https://it-infra-ya.com/en/ws19-sshserver_en/)

### 1 - Téléchargement de openSSH via GITHUB

Pour windows server 2019, on prends la version 7.7.0 (que des versions beta apparement).
[Release v7.7.2.0p1-Beta · PowerShell/Win32-OpenSSH (github.com)](https://github.com/PowerShell/Win32-OpenSSH/releases/tag/v7.7.2.0p1-Beta)

* On décompresse l'archive dans un dossier.

### 2 - Copier le dossier dans la VM

* On se connecte à la VM via RDP (En configurant le partage de notre dossier).
* On copie notre dossier dans `C:\ProgramFiles`.
* On lance installsshd.ps1 via une fenêtre powershell en Administrateur.

```
# Si tout est bon on devrait avoir ce résultat.
sshd and ssh-agent services successfully installed
```

* On ajoute notre dossier au path pour l'accès au commande.
``` powershell
$env:Path = 'C:\ProgramFiles\OpenSSH-Win64'
```

* On configure ssh.
``` powershell
# Demarrer le service OpenSSH
Start-Service sshd

# Configurer le démarrage automatique de SSH
Set-Service -Name sshd -StartupType 'Automatic'

# Ajouter SSH au parefeu Windows
New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
```

* On met Powershell en tant que shell par défaut lors de toutes connexion ssh.
``` powershell
New-ItemProperty -Path "HKLM:\SOFTWARE\OpenSSH" -Name DefaultShell -Value "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" -PropertyType String -Force
```

[Administrer des serveurs Windows avec Ansible | DevSecOps (stephane-robert.info)](https://blog.stephane-robert.info/post/ansible-windows-openssh-admin/)

[Administrer des serveurs Windows avec Ansible | DevSecOps (stephane-robert.info)](https://blog.stephane-robert.info/post/ansible-windows-openssh-admin/)