Un workflow c'est un group de jobs.

On peut chainer les workflows avec des dépendances comme cela : 

``` yaml
on:
  workflow_run:
    workflows: ["Lint"]
    branches:
      - dev
    types:
        - completed
```

https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#onworkflow_runbranchesbranches-ignore

## Limitations 

On ne peut pas avoir plus de trois workflow à la suite.

Par contre il faut que le workflow lint existe sur la branch par défaut (main) sinon ça ne trigger pas.
