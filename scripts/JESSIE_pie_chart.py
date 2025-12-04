import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("all_movie_posts_with_name.csv")

valid_topics = [
    "Reviews/Reactions/Feelings",
    "Memes/Jokes/Humor/Satire",
    "Promotion/Advertising",
    "Plot/Story/Interpretation/Analysis",
    "Cast Performance/Acting/Actor Discussion",
    "Announcements/News/Release Info"
]

topic_colors = {
    "Reviews/Reactions/Feelings": "#1f77b4",         
    "Memes/Jokes/Humor/Satire": "#8c564b",          
    "Promotion/Advertising": "#2ca02c",             
    "Plot/Story/Interpretation/Analysis": "#d62728",
    "Cast Performance/Acting/Actor Discussion": "#9467bd",
    "Announcements/News/Release Info": "#ff7f0e"    
}

# Order for legend to be consistent with bar chart
legend_order = [
    "Announcements/News/Release Info",
    "Cast Performance/Acting/Actor Discussion",
    "Memes/Jokes/Humor/Satire",
    "Plot/Story/Interpretation/Analysis",
    "Promotion/Advertising",
    "Reviews/Reactions/Feelings"
]

df = df[df["topic"].notna()]           
df = df[df["topic"].str.strip() != ""] 
df = df[df["topic"].isin(valid_topics)] 

movies = df["movie"].unique()

for movie_name in movies:
    # Count topics and reindex to match desired legend order
    topic_counts = df[df["movie"] == movie_name]["topic"].value_counts()
    topic_counts = topic_counts.reindex(legend_order).fillna(0)  # missing topics become 0
    
    colors = [topic_colors[topic] for topic in topic_counts.index]

    plt.figure(figsize=(9, 7))

    wedges, texts, autotexts = plt.pie(
        topic_counts,
        labels=None,              
        autopct="%1.1f%%",
        startangle=90, 
        pctdistance=0.85,
        labeldistance=1.05,
        colors=colors             
    )

    plt.legend(
        wedges,
        topic_counts.index,
        title="Topics",
        loc="center left",
        bbox_to_anchor=(1, 0.5)
    )

    plt.title(f"{movie_name}'s Topic Distribution")
    plt.tight_layout()
    plt.show()
