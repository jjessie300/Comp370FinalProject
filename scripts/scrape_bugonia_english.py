import requests
import json
import time
from langdetect import detect, LangDetectException

query = "Bugonia"
limit = 100
posts = []
after = None

headers = {"User-Agent": "Mozilla/5.0"}

while len(posts) < limit:
    url = f"https://www.reddit.com/search.json?q={query}&sort=new&limit=100"
    if after:
        url += f"&after={after}"

    print("Fetching:", url)
    r = requests.get(url, headers=headers)
    data = r.json()

    children = data.get("data", {}).get("children", [])
    if not children:
        break

    for child in children:
        if len(posts) >= limit:
            break

        p = child["data"]
        title = p.get("title", "")

        # -----------------------
        # LANGUAGE DETECTION HERE
        # -----------------------
        try:
            lang = detect(title) if title.strip() else "unknown"
        except LangDetectException:
            lang = "unknown"

        if lang != "en":
            continue  # skip non-English posts

        # -----------------------
        # SAVE ONLY DESIRED FIELDS
        # -----------------------
        posts.append({
            "id": p.get("id"),
            "title": p.get("title"),
            "selftext": p.get("selftext"),
            "subreddit": p.get("subreddit"),
            "url": "https://www.reddit.com" + p.get("permalink", ""),
            "created_utc": p.get("created_utc"),
            "num_comments": p.get("num_comments"),
            "ups": p.get("ups"),
            "downs": p.get("downs"),
            "search_query": query
        })

    after = data.get("data", {}).get("after", None)
    if not after:
        break

    time.sleep(1)

print("Collected", len(posts), "English posts.")

with open("bugonia_posts.json", "w", encoding="utf-8") as f:
    json.dump(posts, f, indent=2, ensure_ascii=False)

print("Saved to bugonia_posts.json")
