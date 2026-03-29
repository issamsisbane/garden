```bash
#!/bin/bash

APP_PORT=6300
LB_HOST="stlb01"

# Use full paths
DNF=/usr/bin/dnf
IPTABLES=/usr/sbin/iptables
SERVICE=/usr/sbin/service
SYSTEMCTL=/usr/bin/systemctl
GETENT=/usr/bin/getent
AWK=/usr/bin/awk

# Install iptables
$DNF install -y iptables iptables-services

# Enable and start iptables
$SYSTEMCTL enable iptables
$SYSTEMCTL start iptables

# Flush rules
$IPTABLES -F

# Get LB IP
LB_IP=$($GETENT hosts $LB_HOST | $AWK '{print $1}')
if [ -z "$LB_IP" ]; then
  echo "Error: Cannot resolve LB host IP"
  exit 1
fi

# Allow LB host
$IPTABLES -A INPUT -p tcp -s $LB_IP --dport $APP_PORT -j ACCEPT

# Drop all other traffic
$IPTABLES -A INPUT -p tcp --dport $APP_PORT -j DROP

# Save rules
$SERVICE iptables save

echo "Iptables setup completed."
```
