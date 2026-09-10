---
creation date: 2026-03-19-22:34:06
modification date: 2026-03-19-22:34:06
imageNameKey: GIT_-_Rewrite_history
---
I had push some commits on my homelab repo from my work pc. So it was another gitlab user. 

And I had 2 contributors on my repo. I don't like this. 

So i find this utils that allow to change the author of commit.

Gitlab and Github use the email and name from git config to identify an user.

1. Install the tool

```bash
pip install git-filter-repo
```

2. Change the authors of commit
```bash
git filter-repo --commit-callback '
  if commit.author_name == b"user":
    commit.author_name = b"user"
    commit.author_email = b"email"
    commit.committer_name = b"user"
    commit.committer_email = b"email"
' --force
```

3. Add back the remote (deleted for safety by the utils)
4. Force Push to github

Now I have the same user for all my commits.