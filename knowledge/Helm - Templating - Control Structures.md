[Helm | Flow Control](https://helm.sh/docs/chart_template_guide/control_structures/)

Les variables déclarés dans les ifs sont scopé à ce if et pas accessible à l'extérieur. 

Il faut utiliser un dict pour recuperer la valeur : 

Ne marche pas :
```
{{- $userPasswords := dict }}
{{- range $db := $cluster.databases -}}
{{- $host := printf "%s-rw" $db.name }}
{{- $ownerName := $db.owner.name }}
{{- if not (hasKey $userPasswords $ownerName) }}
  {{- $password := randAlphaNum 32 }}
  {{- $_ := set $userPasswords $ownerName $password }}
{{- else }}
  {{- $password := get $userPasswords $ownerName}}
{{- end }}
```

Fonctionne : 
```
{{- $userPasswords := dict }}
{{- range $db := $cluster.databases -}}
{{- $host := printf "%s-rw" $db.name }}
{{- $ownerName := $db.owner.name }}
{{- if not (hasKey $userPasswords $ownerName) }}
  {{- $password := randAlphaNum 32 }}
  {{- $_ := set $userPasswords $ownerName $password }}
{{- end }}
{{- $password := get $userPasswords $ownerName}}
```