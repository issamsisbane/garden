# Docker Hardening

## Docker Service

We can see docker logs if we use it as a cni :

```bash
dockerd --debug
```

When the docker daemon start, it listens to a unix socket `/var/run/docker.sock`.

It is a unix socket for communication between process on the same host.

The docker daemon is only accessible within the same host. The docker cli interact with the docker daemon via the socket.

We can make the docker daemon accessible using the following flag : 

```bash
dockerd --host=tcp://192.168.1.10:2375
```

`2375` is the default port for docker **unencrypted traffic**.

To access it we need to specify an env var in the client : 

```bash
export DOCKER_HOST="tcp://192.168.1.10:2375"
```

Its tcp so the traffic is not encrypted. Opening this port is a security risk.

We can enable TLS using the following flags :

```bash
dockerd --host=tcp://192.168.1.10:2376 \
		--tls=true \
		--tlscert=/var/docker/server.pem \
		--tlskey=/var/docker/serverkey.pem
```

The port is now `2376` which means **encrypted traffic**.

We can specify this in a config file at `/etc/docker/daemon.json`:

```json
{
	"debug": true,
	"hosts": ["tcp://192.168.1.10:2376"],
	"tls": true, // Enable TLS
	"tlscert": "/var/docker/server.pem",
	"tlskey": "/var/docker/serverkey.pem",
	"tlsverify": true, // Enable client certificate-based authentication
	"tlscacert": "/var/docker/caserver.pem"
}
```

On the client :

```bash
## Only for TLS
export DOCKER_TLS=true
export DOCKER_HOST="tcp://192.168.1.10:2376"

## Client Certificate-based authent
export DOCKER_TLS_VERIF=true
```

```bash
docker --tlscert=<> --tlskey=<> --tlscacert=<>
```

We can also add the certs and key in the `$HOME/.docker` directory.

## Securing Docker Server

Anyone with access to the docker demon can : 
- delete existing containers with data
- create new containers
- gain root access to the host system by running a privileged container.

By default, we can talk to the docker daemon only from the same host via unix socket.

So the first line of defense is securing the host :
- Disable password-based authentication
- Enable SSH key-based authentication
- Determine users who need access to the server

If we enable access from outside we must enable tls and ensure the accessibility is only from trusted host and not public facing. We also need to enabled certificate based client authentication.