from google import genai
import json
import os
import re

def generate_trailer_script(user_prompt: str, api_key: str) -> dict:
    client = genai.Client(api_key=api_key)

    formatted_prompt = f"""
    You are a professional movie trailer scriptwriter.

    Given the story idea: "{user_prompt}"

    Write a 30-second trailer script in exactly 6 lines — 3 scenes and 3 voiceovers.
    Each scene is followed by a dramatic voiceover. Keep it emotional, suspenseful, and cinematic.

    Use this format (no extra text):

    Scene: ...
    Voiceover: ...
    Scene: ...
    Voiceover: ...
    Scene: ...
    Voiceover: ...

    At the end, suggest a short movie title (maximum 4 words) like:
    Title: ...
    """

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=formatted_prompt
    )

    lines = [line.strip() for line in response.text.strip().splitlines() if line.strip()]
    
    script = []
    title = ""
    current_scene = None

    for line in lines:
        if line.startswith("Scene:"):
            current_scene = line[len("Scene:"):].strip()
        elif line.startswith("Voiceover:") and current_scene is not None:
            voiceover = line[len("Voiceover:"):].strip()
            script.append({"scene": current_scene, "voiceover": voiceover})
            current_scene = None
        elif line.startswith("Title:"):
            title = line[len("Title:"):].strip()

    result = {"title": title, "script": script}

    # ✅ Save to JSON file
    safe_title = re.sub(r'[^a-zA-Z0-9_]', '_', title.strip().lower())
    os.makedirs("trailers", exist_ok=True)
    filename = os.path.join("trailers", f"trailer_{safe_title}.json")

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n Trailer saved to: {filename}")
    return result

# 🧪 Test
result = generate_trailer_script(
    "Create a movie trailer about a joker",
    api_key="AIzaSyAp0raYPs7aImjgX1nM-MaHjtTcnef3QCM"
)

print("\n Title:", result["title"])
print("\n Script:")
for i, pair in enumerate(result["script"], 1):
    print(f"\nLine {i}:")
    print("Scene:", pair["scene"])
    print("Voiceover:", pair["voiceover"])
