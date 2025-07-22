Cloudflare tunnels provides a secure way to connect resources to Cloudflare without a publicly routable IP address. 

We would install a small daemon in our infrastructure that will create an **outbound only connection** to Cloudflare's global Network.

We would authenticate to the tunnel using a token for cloudlfared to be able to use the tunnel.

![[Pasted image 20250202140328.png]]

https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/
