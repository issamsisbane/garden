Before this I had to create an ssh key and copy the public key to the backup server in order to have passwordless scp. See [[Kodecloud - 100 Days of DevOps - 07 - SSH passwordless]].

``` bash
#!/bin/bash

# Create the archived in backup
tar -cvf /backup/xfusioncorp_media.zip /var/www/html/media

# SCP to Nautilaus backup server
scp /backup/xfusioncorp_media.zip clint@stbkp01:/backup/
```

I have to use the zip package and not tar...

``` bash
sudo yum install zip
```

``` bash
#!/bin/bash

# Create the archived in backup
zip -r /backup/xfusioncorp_ecommerce.zip /var/www/html/ecommerce

# SCP to Nautilaus backup server
scp /backup/xfusioncorp_ecommerce.zip clint@stbkp01:/backup/
```

