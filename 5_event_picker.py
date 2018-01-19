import pickle
from datetime import datetime

# A list of tuples in the form of (minute, flair)
# so we can find out what the team was talking about
# at a given time.
extraction = [
    # ("00:03:", "Alabama"),
    ("00:11:", "Georgia"),
]

for _ in range(1, 6):
    with open("thread_{}_full_comments.p".format(_), "rb") as f:
        comments = pickle.load(f)

    # Tuple unpack the extraction list
    for minute, flair in extraction:
        for comment in comments:
            # We decrease the timestamp by 28800 seconds (8 hours)
            dt = datetime.fromtimestamp(comment["created"] - 28800)
            if minute in str(dt) and flair in (comment["flair"] or ""):
                try:
                    print(_, dt, comment["flair"].split(" / ")[0], comment["comment"])
                except Exception as e:
                    pass