[[Kodecloud - 100 Days of DevOps - 01 - Create a user with non interactive shell]]
[[Kodecloud - 100 Days of DevOps - 02 - Create an user with an expiration date]]
[[Kodecloud - 100 Days of DevOps - 03 - Disable ssh root login]]
[[Kodecloud - 100 Days of DevOps - 04 - File Exec permission]]
[[Kodecloud - 100 Days of DevOps - 05 - Install SELinux]]
[[Kodecloud - 100 Days of DevOps - 06 - Cron]]
[[Kodecloud - 100 Days of DevOps - 07 - SSH passwordless]]
[[Kodecloud - 100 Days of DevOps - 08 - MariaDB Troubleshooting]]
[[Kodecloud - 100 Days of DevOps - 09 - Backup Script]]
[[Kodecloud - 100 Days of DevOps - 10 - Install tomcat server]]
[[Kodecloud - 100 Days of DevOps - 11 - Linux Network Services]]

This is the board with the informations to connect to each machines. It is public and are just VMs within the challenges environment so no problem sharing it.

| **Server Name** | **IP**        | **Hostname**                      | **User** | **Password** | **Purpose**                    |
| --------------- | ------------- | --------------------------------- | -------- | ------------ | ------------------------------ |
| stapp01         | 172.16.238.10 | stapp01.stratos.xfusioncorp.com   | tony     | Ir0nM@n      | Nautilus App 1                 |
| stapp02         | 172.16.238.11 | stapp02.stratos.xfusioncorp.com   | steve    | Am3ric@      | Nautilus App 2                 |
| stapp03         | 172.16.238.12 | stapp03.stratos.xfusioncorp.com   | banner   | BigGr33n     | Nautilus App 3                 |
| stlb01          | 172.16.238.14 | stlb01.stratos.xfusioncorp.com    | loki     | Mischi3f     | Nautilus HTTP LBR              |
| stdb01          | 172.16.239.10 | stdb01.stratos.xfusioncorp.com    | peter    | Sp!dy        | Nautilus DB Server             |
| ststor01        | 172.16.238.15 | ststor01.stratos.xfusioncorp.com  | natasha  | Bl@kW        | Nautilus Storage Server        |
| stbkp01         | 172.16.238.16 | stbkp01.stratos.xfusioncorp.com   | clint    | H@wk3y3      | Nautilus Backup Server         |
| stmail01        | 172.16.238.17 | stmail01.stratos.xfusioncorp.com  | groot    | Gr00T123     | Nautilus Mail Server           |
| jump_host       | Dynamic       | jump_host.stratos.xfusioncorp.com | thor     | mjolnir123   | Jump Server to Access Stork DC |
| jenkins         | 172.16.238.19 | jenkins.stratos.xfusioncorp.com   | jenkins  | j@rv!s       | Jenkins Server for CI/CD       |