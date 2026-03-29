
The Workflow must be defined in a GitHub repo inside `.github/workflows/main.yaml`

``` yaml
name: My GitHub Actions Workflow
on: [push]

jobs:
  testing_github:
    runs-on: ubuntu-latest
    steps:
      - name: Hello
        run: echo "Hello, world!"
      - name: Display repo name
        run: echo "This repo is $GITHUB_REPOSITORY"
```

![[GitHub_actions_test_workflow.png]]

This is a very simple workflow, running some echo command in the runner cli.