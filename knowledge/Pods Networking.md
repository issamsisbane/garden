Each pod gets its own IP address.

By default, pods can connect to all pods on all nodes. It's possible to limit that though [[Network Policy]].

Containers in pods can communicate with each others through localhost (like a big vm just need to use the port).

This communication is possible thanks to [[Container Network Interface Plugin]]