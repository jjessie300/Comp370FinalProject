import json

# Load the original Reddit JSON file
with open("ahouseofdynamiteformatted.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# The posts are inside: data["data"]["children"]
posts = data["data"]["children"]

cleaned_posts = []

for post in posts:
    p = post["data"]

    cleaned_posts.append({
        "id": p.get("id"),
        "title": p.get("title"),
        "selftext": p.get("selftext"),
        "subreddit": p.get("subreddit"),
        "url": p.get("url"),
        "created_utc": p.get("created_utc"), 
        "num_comments": p.get("num_comments"), 
        "ups": p.get("ups"), 
        "downs": p.get("downs"), 
        "search_query": "a house of dynamite"
    })

# Save to new JSON file
with open("ahouseofdynamiteclean.json", "w", encoding="utf-8") as out:
    json.dump(cleaned_posts, out, indent=4, ensure_ascii=False)

print("Done! Extracted fields saved to cleaned.json")
