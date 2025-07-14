[Ansible Vault | DevSecOps](https://blog.stephane-robert.info/docs/infra-as-code/gestion-de-configuration/ansible/vault/)

[Best Practices — Ansible Documentation](https://docs.ansible.com/ansible/2.9/user_guide/playbooks_best_practices.html#best-practices-for-variables-and-vaults)

Un vault ansible permet de créer des fichiers encryptés contenant des secrets qui peuvent être commit et push dans des repos de code sans risque d'être exposés directement.

Pour utiliser ansible vault c'est très simple. 

## Variable Structure

- Variables are stored in files located in the `vars` folder.
- Sensitive variables are annotated with `# SECRET_IN_VAULT` in the `vars` files for easy reference.
- The actual values of these sensitive variables are stored in encrypted files within the `vault` folder.
- If both vars and vault files exist, they must be referenced in the playbook in the following order to allow the vault secret value to override the value from the vars file:
    1. vars
    2. vault

### Example

For the file `./vars/postgres.yml`, any secret variables annotated with `# SECRET_IN_VAULT` will have their encrypted counterparts stored in `./vault/postgres.yml`. In the file `./playbook/postgres.yml` we would have :

```yaml
    vars_files:
    - ./vars/postgres.yml
    - ./vault/postgres.yml
```

## Vault Password Management

You need a password to interact with the vault files. There are two ways to provide the vault password:

1. **Manual Entry**: Use the `--ask-vault-pass` option, and you will be prompted to enter the password manually each time you access the vault.
    
    Example:
    
    ```shell
    ansible-playbook -i hosts my_playbook.yaml --ask-vault-pass
    ```
    
2. **Password File**: Store the password in a file (e.g., `vault_password.txt`) and reference it using the `--vault-password-file` option.
    
    Example:
    
    ```shell
    ansible-playbook -i hosts my_playbook.yaml --vault-password-file vault_password.txt
    ```
    

> **Note**: Ensure that the password file is not tracked in version control by adding it to `.gitignore`.

## Common Vault Operations

### View Variables in a Vault File

To view the contents of an encrypted vault file:

```shell
ansible-vault view ./vault/file.yml
```

### Edit Variables in a Vault File

To edit the contents of an encrypted vault file:

```shell
ansible-vault edit ./vault/file.yml
```

### Encrypt an Existing File

To encrypt a file and store it in the vault:

```shell
ansible-vault encrypt ./vault/file.yml
```