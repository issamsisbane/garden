I have two accounts in github using the same laptop. 
I couldn't add the my ssh key to the other account. So I had to create a new one, add it to the account.

Then to specify the key to use in `~/.ssh/config`

```bash
Host github.com
	IdentityFile ~/.ssh/github_rsa
``` 

```
```
I have two accounts in github using the same laptop. 
I couldn't add the my ssh key to the other account. So I had to create a new one, add it to the account.

Then to specify the key to use in `~/.ssh/config`

```bash
Host github.com
	IdentityFile ~/.ssh/github_rsa
```
