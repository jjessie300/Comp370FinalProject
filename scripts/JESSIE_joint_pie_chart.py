import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

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

legend_order = [
    "Announcements/News/Release Info",
    "Cast Performance/Acting/Actor Discussion",
    "Memes/Jokes/Humor/Satire",
    "Plot/Story/Interpretation/Analysis",
    "Promotion/Advertising",
    "Reviews/Reactions/Feelings"
]

# Clean dataframe
df = df[df["topic"].notna()]
df = df[df["topic"].str.strip() != ""]
df = df[df["topic"].isin(valid_topics)]

movies = df["movie"].unique()

# Create figure
fig = plt.figure(figsize=(18, 12))

# Define axes positions (left, bottom, width, height)
# Top row: 3 pies evenly spaced
# Bottom row: 2 pies centered under top row
positions = [
    (0.05, 0.55, 0.25, 0.4),  # top-left
    (0.35, 0.55, 0.25, 0.4),  # top-middle
    (0.65, 0.55, 0.25, 0.4),  # top-right
    (0.2, 0.05, 0.25, 0.4),   # bottom-left (centered under top row)
    (0.5, 0.05, 0.25, 0.4)    # bottom-right (bottom row)
]

for i, movie_name in enumerate(movies):
    ax = fig.add_axes(positions[i])

    topic_counts = df[df["movie"] == movie_name]["topic"].value_counts()
    topic_counts = topic_counts.reindex(legend_order).fillna(0)

    colors = [topic_colors[topic] for topic in topic_counts.index]

    wedges, texts, autotexts = ax.pie(
        topic_counts,
        labels=None,
        autopct="%1.1f%%",
        startangle=90,
        pctdistance=0.85,
        colors=colors
    )

    ax.set_title(f"{movie_name}'s Topic Distribution")

# Create legend patches
legend_patches = [Patch(facecolor=topic_colors[topic], label=topic) for topic in legend_order]

# Place legend to the right of bottom row
fig.legend(
    handles=legend_patches,
    title="Topics",
    loc='center left',
    bbox_to_anchor=(0.77, 0.25)
)

plt.show()
