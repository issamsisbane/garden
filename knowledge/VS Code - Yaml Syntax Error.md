
There can be error with CloudFormation Yaml syntax. To fix this we have to had this in user settings.

`ctrl` + `shift` + `p` => user settings

and had this lines : 
``` json
"yaml.customTags": [
        "!Base64 scalar",
        "!Cidr scalar",
        "!And sequence",
        "!Equals sequence",
        "!If sequence",
        "!Not sequence",
        "!Or sequence",
        "!Condition scalar",
        "!FindInMap sequence",
        "!GetAtt sequence",
        "!GetAZs scalar",
        "!ImportValue scalar",
        "!Join sequence",
        "!Select sequence",
        "!Split sequence",
        "!Sub scalar",
        "!Transform mapping",
        "!Ref scalar",
    ]
```