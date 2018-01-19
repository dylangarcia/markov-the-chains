import pickle
from collections import Counter
from datetime import datetime

flairs = Counter()
for _ in range(1, 6):
    with open("./comments/thread_{}_full_comments.p".format(_), "rb") as f:
        comments = pickle.load(f)

    comments = sorted(comments, key=lambda x: x["created"])

    for comment in comments:
        # Comments can have multiple flairs, so split
        # the 'flair' by ' / ' (the default separator)
        for flair in (comment["flair"] or " / ").split(" / "):
            flairs[flair] += 1

# Get the top 10 most common flairs and the frequencies
for flair, frequency in flairs.most_common(10):
    print(flair, frequency)