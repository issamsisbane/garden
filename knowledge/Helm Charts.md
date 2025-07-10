Helm charts are kubernetes manifests template with variables in it. That woulds be overloaded with the values.yaml file.

If we dont overload a variables form the values.yaml file it will just use the default values from the default values.yaml.

To create the values.yaml file, we can do : 
```
helm show values repository/name | vim
```