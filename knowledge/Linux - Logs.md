To have the wrapping but without less (handled by the terminal) :
```bash

journalctl -u etcd --no-pager
```

To keep less and the wrapping :

```bash
journalctl -u etcd | less
```

We can also pipe in vim : 

```bash
journalctl -u etcd | vim -
```
```
