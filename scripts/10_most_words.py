import csv
import math
import re
from collections import Counter, defaultdict

# === Adjust this if your path is different ===
CSV_PATH = r"C:\Users\roman\Downloads\all_movie_posts.csv"

# Very simple tokenizer: lowercase + keep only alphabetic words
WORD_PATTERN = re.compile(r"[a-zA-Z']+")

# Optional: basic stopword list so words like "the", "and" don't dominate
STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "if", "in", "on", "at", "to", "of",
    "for", "with", "this", "that", "is", "it", "as", "be", "by", "from",
    "are", "was", "were", "so", "we", "you", "i", "they", "he", "she", "them",
    "their", "our", "my", "your", "me", "us", "about", "would", "what", "because", "just", "did"
}


def tokenize(text):
    text = text.lower()
    tokens = WORD_PATTERN.findall(text)
    # remove stopwords
    return [t for t in tokens if t not in STOPWORDS]


def main():
    docs = []                        # list of (topic, term_frequency_counter)
    df_counts = Counter()            # document frequency per term
    topic_doc_counts = Counter()     # number of docs per topic

    # --- 1. Read CSV and build TF + DF ---
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            title = row.get("title") or ""
            selftext = row.get("selftext") or ""
            topic = row.get("topic") or "UNKNOWN"

            text = f"{title} {selftext}"
            tokens = tokenize(text)

            if not tokens:
                continue  # skip empty docs

            topic_doc_counts[topic] += 1
            tf = Counter(tokens)
            docs.append((topic, tf))

            # update document frequency (count each term once per doc)
            unique_terms = set(tf.keys())
            for term in unique_terms:
                df_counts[term] += 1

    N = len(docs)
    if N == 0:
        print("No documents found after preprocessing.")
        return

    # --- 2. Compute IDF for each term ---
    # idf(term) = log(N / (1 + df(term)))  (1 added to avoid division by zero)
    idf = {term: math.log(N / (1 + df)) for term, df in df_counts.items()}

    # --- 3. Accumulate TF-IDF scores per topic ---
    topic_term_scores = defaultdict(lambda: defaultdict(float))

    for topic, tf_counter in docs:
        doc_len = sum(tf_counter.values())
        if doc_len == 0:
            continue

        for term, freq in tf_counter.items():
            tf = freq / doc_len
            tfidf = tf * idf[term]
            topic_term_scores[topic][term] += tfidf

    # --- 4. Compute average TF-IDF per term per topic and print top 10 ---
    TOP_N = 10

    for topic, term_scores in topic_term_scores.items():
        n_docs = topic_doc_counts[topic]
        # average over all docs of that topic
        avg_scores = [
            (term, total_score / n_docs)
            for term, total_score in term_scores.items()
        ]

        # sort by score, descending
        avg_scores.sort(key=lambda x: x[1], reverse=True)
        top_terms = avg_scores[:TOP_N]

        print(f"\n=== Top {TOP_N} terms for topic: {topic} ===")
        for term, score in top_terms:
            print(f"{term:20s}  {score:.4f}")


if __name__ == "__main__":
    main()
