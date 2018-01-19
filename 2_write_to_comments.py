import pickle
from datetime import datetime

with open("comments.txt", "a") as fd:
    # Iterate 1 - 5 for our thread comments
    for _ in range(1, 6):
        # Read in each of the pickle files
        # created previously
        with open("thread_{}_full_comments.p".format(_), "rb") as f:
            comments = pickle.load(f)

        # Sort them by date created descending
        comments = sorted(comments, key=lambda x: x["created"])

        # Write out the comment data to comments.txt
        # Each comment on its own line
        for comment in comments:
            try:
                fd.write("{}\n".format(comment["comment"].replace("\n", "")))
            except Exception as e:
                pass