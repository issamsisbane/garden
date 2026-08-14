---
foam_template:
  filepath: "0 - INBOX/Linux - Storage - Extend LV.md"
  description: "New note"
created: "2026-04-07"
---

# Linux - Storage - Extend LV

View the current consumption of storage :

```bash
lsblk
```

To extend an LV - XFS only:

```bash
lvextend -L 100G lv-name    # Extend the size of the volume
xfs_growfs -d path          # Adapt the filesystem to the new capacity
``` 

We need to verify the filesystem type xfs or ext4 and adapt the command accordingly.

https://serverfault.com/questions/1063890/how-to-extend-the-size-of-a-xfs