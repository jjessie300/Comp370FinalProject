import json

INPUT_FILE = "wickedforgoodraw.json"
OUTPUT_FILE = "wickedforgoodformatted.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("✔ Pretty JSON saved to", OUTPUT_FILE)
