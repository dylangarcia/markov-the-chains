import pickle
from datetime import datetime

# Top 10 most common flairs
common_flairs = ['Georgia Bulldogs', 'Alabama Crimson Tide', 'Ohio State Buckeyes', 'Michigan Wolverines', 'Texas Longhorns', 'Clemson Tigers', 'Team Chaos', 'Penn State Nittany Lions', 'Notre Dame Fighting Irish']

with open("flair_data_all_flairs.csv", "w") as fd:
    fd.write("Time,Flair,Comment\n")
    for _ in range(1, 6):
        with open("./comments/thread_{}_full_comments.p".format(_), "rb") as f:
            comments = pickle.load(f)

        # Sort comments by time, oldest to newest
        comments = sorted(comments, key=lambda x: x["created"])

        for comment in comments:
            for flair in (comment["flair"] or " / ").split(" / "):
                # Remove the flair if it isn't in the top 10
                if flair not in common_flairs:
                    flair = ""
                # Adjust to the correct timezone
                adjusted_time = comment["created"] - 28800
                dt = datetime.fromtimestamp(adjusted_time)

                # Ignore comments from 01/09/2018 0:30:00 onwards
                if dt.day >= 9 and ((dt.hour == 0 and dt.minute > 30) or (dt.hour > 0)):
                    continue
                try:
                    fd.write("{},{},{}\n".format(adjusted_time, flair, comment["comment"].replace("\n", "")))
                except Exception as e:
                    pass