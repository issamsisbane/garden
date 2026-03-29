Script to generate an outline to add to mardown file.

```
#!/bin/bash

# Vérifier si des fichiers ont été passés en argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 fichier1.md [fichier2.md ...]"
    exit 1
fi

# Fonction pour générer le sommaire d'un fichier
generate_toc() {
    local file=$1
    local filename=$(basename "$file" .md)

    echo "## Sommaire pour $filename"
    echo ""

    # Lire le fichier ligne par ligne
    while IFS= read -r line; do
        # Vérifier si la ligne est un titre de niveau 1, 2 ou 3
        if [[ $line =~ ^\#\#\#\ (.*) ]]; then
            echo "  - [${BASH_REMATCH[1]}](#${filename// /-}-${BASH_REMATCH[1]// /-})"
        elif [[ $line =~ ^\#\#\ (.*) ]]; then
            echo "  - [${BASH_REMATCH[1]}](#${filename// /-}-${BASH_REMATCH[1]// /-})"
        elif [[ $line =~ ^\#\ (.*) ]]; then
            echo "- [${BASH_REMATCH[1]}](#${filename// /-}-${BASH_REMATCH[1]// /-})"
        fi
    done < "$file"

    echo ""
}

# Parcourir tous les fichiers passés en argument
for file in "$@"; do
    if [ -f "$file" ]; then
        generate_toc "$file"
    else
        echo "Le fichier $file n'existe pas."
    fi
done
```