import re
import os 

def extract_image_paths(markdown_content):
    # Utilise une expression régulière pour trouver les chemins d'images dans le markdown
    return re.findall(r'!\[[^\]]*\]\((?P<filename>.*?)(?=\"|\))(?P<optionalpart>\".*\")?\)', markdown_content)

with open(os.path.join("./content/blog/test.md"), 'r') as file:
    markdown_content = file.read()
    print(extract_image_paths(markdown_content))