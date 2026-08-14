GitHub Container Registry

To view image of a github repository, we need to go to the package section. There is no ghcr dedicated website as docker hub.

On est obligé de parcourir à la main les pages parcontre, car l'UI GitHub ne permet pas de recherhce des images.

Parcontre on peut le faire via cli et skopeo : 

```bash
skopeo list-tags docker://ghcr.io/cloudnative-pg/postgresql | jq '.Tags[]' | grep "17.9"
```