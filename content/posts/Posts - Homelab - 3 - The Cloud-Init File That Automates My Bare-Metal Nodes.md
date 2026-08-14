𝐓𝐡𝐞 𝐂𝐥𝐨𝐮𝐝-𝐈𝐧𝐢𝐭 𝐅𝐢𝐥𝐞 𝐓𝐡𝐚𝐭 𝐀𝐮𝐭𝐨𝐦𝐚𝐭𝐞𝐬 𝐌𝐲 𝐁𝐚𝐫𝐞-𝐌𝐞𝐭𝐚𝐥 𝐍𝐨𝐝𝐞𝐬  
  
I have three nodes composing my homelab Kubernetes cluster. Different hardware, different WiFi chips, different BIOS versions. I wanted to provision all three without ever plugging in a keyboard.  
  
One file made that possible.  
  
𝗪𝗵𝗮𝘁 𝗖𝗹𝗼𝘂𝗱-𝗜𝗻𝗶𝘁 𝗔𝗰𝘁𝘂𝗮𝗹𝗹𝘆 𝗗𝗼𝗲𝘀  
  
Ubuntu Server 24.04 ships with a built-in installer called autoinstall. It reads a file called user-data at boot and installs the OS completely hands-off. No clicks, no prompts.  
  
My user-data file handles everything in a single pass:  
  
- Creates the kuadm user with a hashed password  
- Injects my SSH public key and disables password login entirely  
- Installs wpasupplicant so WiFi works after reboot  
- Writes the Netplan WiFi config directly to disk  
- Sets locale to fr_FR.UTF-8 and keyboard to US International  
- Grants passwordless sudo via a late-command, so Ansible can run without prompts  
  
𝗪𝗵𝘆 𝗢𝗻𝗲 𝗙𝗶𝗹𝗲 𝗙𝗼𝗿 𝗔𝗹𝗹 𝗧𝗵𝗿𝗲𝗲 𝗡𝗼𝗱𝗲𝘀  
  
The only thing that changes between nodes is the hostname. Everything else such as the user, the key, the packages, the WiFi config stays identical.  
  
This is the point. The file is the truth. If all three nodes were installed from the same file, they are identical by construction. No "I think I configured this the same way." No drift.  
  
It also means a rebuild is just: boot from USB, wait 10 minutes, done. No documentation to consult, no manual steps to remember.  
  
𝗛𝗼𝘄 𝗜𝘁 𝗚𝗲𝘁𝘀 𝗧𝗼 𝗧𝗵𝗲 𝗡𝗼𝗱𝗲𝘀  
  
I use Ventoy, a tool that lets you copy ISO files to a USB stick without reflashing. I placed the user-data file at the root of the USB drive alongside the Ubuntu ISO. The installer picks it up automatically at boot.  
  
One USB stick, one config file, three identical nodes.  
  
---  
  
Read the full article here: [https://lnkd.in/dp7gAD8a](https://lnkd.in/dp7gAD8a)  
  
Homelab - 3 / 3

(cloudinit-node-provisioning.png)