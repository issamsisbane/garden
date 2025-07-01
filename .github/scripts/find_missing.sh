#!/bin/bash

DIRECTORIES=("content/blog" "content/projects")

for DIR in "${DIRECTORIES[@]}"; do
  if [ ! -d "$DIR" ]; then
    echo "Répertoire non trouvé : $DIR"
    continue
  fi

  find "$DIR" -type f \( -name "*.fr.md" -o -name "*.en.md" \) -print0 | while IFS= read -r -d '' FILE; do
    if [[ "$FILE" == *.fr.md ]]; then
      OTHER_FILE="${FILE/.fr.md/.en.md}"
      if [ ! -f "$OTHER_FILE" ]; then
        echo "$FILE"
      fi
    elif [[ "$FILE" == *.en.md ]]; then
      OTHER_FILE="${FILE/.en.md/.fr.md}"
      if [ ! -f "$OTHER_FILE" ]; then
        echo "$FILE"
      fi
    fi
  done
done
