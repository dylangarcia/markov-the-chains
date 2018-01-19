import praw
import pickle
from pprint import pprint
from config import CLIENT_ID, CLIENT_SECRET, USER_AGENT

# https://praw.readthedocs.io/en/latest/
reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent=USER_AGENT)

thread_ids = ["7p36ds", "7p3r99", "7p48fo", "7p4jhr", "7p4twp"]

for i, thread_id in enumerate(thread_ids, start=1):
    submission = reddit.submission(id=thread_id)

    # https://praw.readthedocs.io/en/latest/tutorials/comments.html#the-replace-more-method
    submission.comments.replace_more(limit=None)
    comments = []
    for comment in submission.comments.list():
        # Create a dictionary to be able to pickle them later
        data = {
            "created": comment.created,
            "flair": comment.author_flair_text,
            "score": comment.score,
            "comment": comment.body
        }
        comments.append(data)

    # Write all of the thread's comments to a
    # pickle so you don't have to network request them later
    with open("thread_{}_full_comments.p".format(i), "wb") as f:
        pickle.dump(comments, f)


