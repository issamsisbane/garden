#!/bin/bash

DIRECTORIES=("content/blog" "content/projects")

for DIR in "${DIRECTORIES[@]}"; do
  if [ ! -d "$DIR" ]; then
    echo "Répertoire non trouvé : $DIR"
    continue
  fi

  find "$DIR" -type f -print0 | while IFS= read -r -d '' FILE; do
    # Vérifier si le chemin contient /fr/ ou /en/
    if [[ "$FILE" == *"/fr/"* ]]; then
      OTHER_FILE="${FILE//\/fr\//\/en\/}"
      if [ ! -f "$OTHER_FILE" ]; then
        echo "$FILE"
      fi
    elif [[ "$FILE" == *"/en/"* ]]; then
      OTHER_FILE="${FILE//\/en\//\/fr\/}"
      if [ ! -f "$OTHER_FILE" ]; then
        echo "$FILE"
      fi
    fi
  done
done

