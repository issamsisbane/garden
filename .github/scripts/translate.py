import os
import re
import sys
from google import genai
from google.genai import types

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("The environment variable GOOGLE_API_KEY is not set.")


MODEL_NAME = "gemini-2.0-flash-lite"
MAX_INPUT_TOKENS = 4000
TEMPERATURE = 0.3

PROMPT_CONTEXT = """
You are a professional translator and copywriter, specialized in translating markdown content.
"""
PROMPT_TASK_TO_ENGLISH = """
Your task is to translate the provided markdown text into **fluent and natural French**.
"""
PROMPT_TASK_TO_FRENCH = """
Your task is to translate the provided markdown text into **fluent and natural English**.
"""
PROMPT_INSTRUCTION = """
- You may lightly rephrase for clarity and style, but do **not omit or summarize** any content.
- All **titles, subtitles, and headings** should be translated as well.
- **Preserve all markdown formatting**, including:
    - Links
    - Images
    - Code blocks
    - File references
    - Lists and indentation
- If the input structure is inconsistent, **normalize it**, ensuring titles appear on a single line.
- Your output must be in **markdown format only**, with no extra explanations or comments.
- You will change the frontmatter properties of the notes to match the language of the translation but only the following properties : title, description and lang. DO NOT change the others properties. DO NOT change the pubDate proerty.
Only return the translated markdown content.
"""

def detect_language_from_path(path):
    # Simple détection en fonction du chemin fr/ ou en/
    if "/fr/" in path:
        return "fr"
    elif "/en/" in path:
        return "en"
    else:
        raise ValueError("Unable to detect langage from path")

def get_output_path(input_path, src_lang):
    if src_lang == "fr":
        return input_path.replace("/fr/", "/en/")
    else:
        return input_path.replace("/en/", "/fr/")

def translate_file(input_file):
    client = genai.Client()
    src_lang = detect_language_from_path(input_file)
    target_lang = "fr" if src_lang == "en" else "en"
    output_file = get_output_path(input_file, src_lang)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    system_instruction = PROMPT_CONTEXT + (PROMPT_TASK_TO_FRENCH if target_lang == "en" else PROMPT_TASK_TO_ENGLISH) + PROMPT_INSTRUCTION
    print(f"Translation of {input_file} ({src_lang}) to {target_lang}...")
    print(f"System Instruction {system_instruction}")

    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = re.split(r'(?=^#{1,6} )', content, flags=re.MULTILINE)
    blocks = [b.strip() for b in blocks if b.strip()]

    chunks = []
    current_chunk = ""
    for block in blocks:
        tentative = current_chunk + "\n\n" + block if current_chunk else block
        token_result = client.models.count_tokens(model=MODEL_NAME, contents=[tentative])
        total_tokens = token_result.total_tokens
        if total_tokens <= MAX_INPUT_TOKENS:
            current_chunk = tentative
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = block
    if current_chunk:
        chunks.append(current_chunk.strip())

    translated_chunks = []
    for idx, chunk in enumerate(chunks):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=[chunk],
                config=types.GenerateContentConfig(
                    temperature=TEMPERATURE,
                    system_instruction=system_instruction
                ),
            )
            translated_chunks.append(response.text)
        except Exception as e:
            translated_chunks.append(f"<!-- Error: {e} -->\n\n{chunk}")
    
    print(f"Translated {len(translated_chunks)} chunks from {input_file} to {target_lang}.")
    print(translated_chunks[0])
    print(translated_chunks[-1])

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n\n".join(translated_chunks))

    print(f"Translation of {input_file} to {target_lang} saved in {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: translate.py <input_file>")
        sys.exit(1)
    translate_file(sys.argv[1])