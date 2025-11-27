import requests
import json
import re

def clean_filename(filename):
    """Sanitize the movie name to create a valid filename."""
    # Remove invalid characters and replace spaces with underscores
    return re.sub(r'[\\/*?:"<>|]', "", filename).replace(" ", "_").lower()

def fetch_posts_for_movie(movie, target_count=150):
    print(f"Fetching posts for: {movie}")
    posts_collected = []
    after = None
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    while len(posts_collected) < target_count:
        try:
            url = f"https://www.reddit.com/search.json"
            params = {
                'q': movie,
                'sort': 'relevance',
                'limit': 100,
                't': 'all',
                'type': 'link' # search for posts (links), not subreddits or users
            }
            if after:
                params['after'] = after

            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            # same as data['data']['children']  but more secure
            children = data.get('data', {}).get('children', [])
            
            if not children:
                print("No more results found.")
                break
            
            for child in children:
                post = child['data']
                post_data = {
                    'create_date': post.get('created_utc'),
                    'id': post.get('id'),
                    'subreddit': post.get('subreddit'),
                    'link': f"https://www.reddit.com{post.get('permalink')}",
                    'self_text': post.get('selftext'),
                    'title': post.get('title'),
                    'search_query': movie
                }
                
                posts_collected.append(post_data)
                if len(posts_collected) >= target_count:
                    break
            
            # when a request has the param after, it will start searching from the posts specified by after
            # same as " after = data['data']['after'] " but more secure
            after = data.get('data', {}).get('after')
            if not after:
                break
            
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    
    print(f"Collected {len(posts_collected)} posts for {movie}")
    
    filename = f"{clean_filename(movie)}_posts.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(posts_collected, f, indent=4)
    
    print(f"Successfully saved posts to {filename}")

def main():
    movies = ["predator: badlands", "roofman"]
    for movie in movies:
        fetch_posts_for_movie(movie)

if __name__ == "__main__":
    main()
