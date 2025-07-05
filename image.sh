#!/bin/bash

blogpath="./content"

# Browse blog and projects directories and find all images in md files


# Get images path
# find $blogpath -type f \( -name "*.md" -o -name "*.markdown" \) | while read -r file; do
#         echo "Processing file: $file"
#         grep -oP '!\[\[.*?\]\]' "$file"
#     done

# WORKING VERSION
find $blogpath -type f \( -name "*.md" -o -name "*.markdown" \) | while read -r file; do
    grep -oP '!\[\[[^\]]+\]\]' "$file" | while read -r match; do
        image=$(echo "$match" | sed -E 's/!\[\[|\]\]//g')
        if [[ ! -f "./assets/$image" ]]; then
            pwd
            echo "Image not found: $image in ./assets/$image"
        else
            echo "Image found: $image in ./assets/$image"
            # cp "./assets/$image" "./content/$image"
        fi
    done
done

# new_prefix="new_path/"

# find "$blogpath" -type f \( -name "*.md" -o -name "*.markdown" \) | while read -r file; do
#     # Utiliser sed pour remplacer le chemin dans le fichier
#     sed -i -E "s|!\[\[(.*?)\]\]|![]($new_prefix\1)|g" "$file"
# done

# Classic md
# find $blogpath -type f \( -name "*.md" -o -name "*.markdown" \) | while read -r file; do
#     grep -oP '!\[.*?\]\(\K.*?(?=\"|\))' "$file" | while read -r image; do
#         if [[ ! -f "$image" ]]; then
#             echo "Image not found: $image in $file"
#         fi
#     done
# done



# Replace image paths to - Only in files copied portfolio


