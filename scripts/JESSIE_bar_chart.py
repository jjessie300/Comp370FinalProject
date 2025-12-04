import pandas as pd
import matplotlib.pyplot as plt

# Load csv
df = pd.read_csv("all_movie_posts_with_name.csv")  

# Our 6 topics 
valid_topics = [
    "Reviews/Reactions/Feelings",
    "Memes/Jokes/Humor/Satire",
    "Promotion/Advertising",
    "Plot/Story/Interpretation/Analysis",
    "Cast Performance/Acting/Actor Discussion",
    "Announcements/News/Release Info"
]

df = df[df["topic"].notna()]                   # remove NaN
df = df[df["topic"].str.strip() != ""]         # remove blank strings
df = df[df["topic"].isin(valid_topics)]        

# Count topics per movie
topic_counts = df.groupby(["movie", "topic"]).size().unstack(fill_value=0)

# Color for each topic
topic_colors = {
    "Reviews/Reactions/Feelings": "#1f77b4",        
    "Memes/Jokes/Humor/Satire": "#8c564b",         
    "Promotion/Advertising": "#2ca02c",              
    "Plot/Story/Interpretation/Analysis": "#d62728",
    "Cast Performance/Acting/Actor Discussion": "#9467bd", 
    "Announcements/News/Release Info": "#ff7f0e"    
}

colors = [topic_colors[topic] for topic in topic_counts.columns]

topic_counts.plot(kind="bar", figsize=(12, 7), color=colors, width=0.6)

plt.title("Topic Coverage by Movie")
plt.xlabel("Movie")
plt.ylabel("Number of Reddit Posts")
plt.xticks(rotation=45, ha="right")

plt.legend(title="Legend", bbox_to_anchor=(1.05, 1), loc="upper left")

plt.tight_layout()
plt.show()
