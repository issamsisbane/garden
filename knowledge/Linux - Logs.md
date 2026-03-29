To have the wrapping but without less (handled by the terminal) :

```
journalctl -u etcd --no-pager
```

To keep less and the wrapping :

```
journalctl -u etcd | less
```

We can also pipe in vim : 

```
journalctl -u etcd | vim -
```