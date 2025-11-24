import json

INPUT_FILE = "test.json"
OUTPUT_FILE = "testformatted.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("✔ Pretty JSON saved to", OUTPUT_FILE)
