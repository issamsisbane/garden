---
title: "Fixing SSH Error with Git & Github"
description: "How to fix SSH Error using git to push to github."
lang: "en"
pubDate: "feb 10 2024"
heroImage: "/portfolio/blog/git_ssh_error/git_ssh_error.jpg"
badge: "GIT"
tags: ["Git", "Github"]
---

# SSH Error on Github

Recently, I had to work in a new working environment, particularly with a different network configuration.

While trying to push the latest changes added to one of my projects to my GitHub, an error occurred:

![SSH Error](/portfolio/blog/git_ssh_error/git_ssh_error_0.png)

This was the first time I encountered this error, and after some research online, I concluded that the SSH port (22) was blocked in this network configuration, preventing me from communicating with GitHub via SSH.

One solution is to change the network connection, for example, by using the hotspot feature of your phone.

Another solution is to switch back to HTTPS instead of using SSH.

### 1 - Retrieve the HTTPS link from GitHub:

![HTTPS Link](/portfolio/blog/git_ssh_error/git_ssh_error_1.png)

### 2 - Modify the origin of our Git repository:

![Modify Origin](/portfolio/blog/git_ssh_error/git_ssh_error_2.png)

### 3 - Connect to GitHub

![Connect to GitHub](/portfolio/blog/git_ssh_error/git_ssh_error_3.png)

Simply log in with GitHub, and now you can push without any issues!
