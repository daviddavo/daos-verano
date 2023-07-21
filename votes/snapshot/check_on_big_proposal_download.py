# glob get files in large_proposal_votes_2023_07_21
import glob
all_files = glob.glob("large_proposal_votes_2023_07_21/*/*.json")

# break all strings on / to make 2d list
all_files = [x.split("/") for x in all_files]
import pandas as pd
df = pd.DataFrame(all_files, columns = ["folder", "proposal_id", "chunk_id"])

# group by proposal_id and count chunk_id
files_per_proposal = df.groupby("proposal_id").chunk_id.count()
files_per_proposal = files_per_proposal.to_frame()
# reset index to make proposal_id a column
files_per_proposal = files_per_proposal.reset_index()
# rename chunk_id to file_count
files_per_proposal = files_per_proposal.rename(columns={"chunk_id": "file_count"})

# for each chunk, check if finished.txt is in the folder, if it is read its value into a new column called remainder
import os
import json
def get_remainder(row):
    if os.path.isfile('large_proposal_votes_2023_07_21/' + row.proposal_id + "/finished.txt"):
        # get the number of votes in the last file
        file_names = glob.glob(f'large_proposal_votes_2023_07_21/{row.proposal_id}/votes_*.json')
        last_file = max([int(x.split('_')[-1].split('.')[0]) for x in file_names])
        with open(f'large_proposal_votes_2023_07_21/{row.proposal_id}/votes_{last_file}.json', 'r') as f:
            votes = json.load(f)
        return len(votes)
    else:
        return None

files_per_proposal["remainder"] = files_per_proposal.apply(get_remainder, axis=1)


import pickle
large_proposals_and_votes = pickle.load(open('large_proposals_and_votes.pkl', 'rb'))

# make large_proposals_and_votes a dataframe
large_proposals_and_votes = pd.DataFrame(large_proposals_and_votes, columns=["proposal_id", "vote"])


# %%
files_per_proposal = files_per_proposal.merge(large_proposals_and_votes, on="proposal_id", how="inner", validate="one_to_one")
# %%
# make a column called downloaded_votes that is the file_count * 1000 + remainder if remainder is not None
def get_downloaded_votes(row):
    if pd.isnull(row.remainder):
        return row.file_count * 1000
    else:
        return row.file_count * 1000 + row.remainder

files_per_proposal["downloaded_votes"] = files_per_proposal.apply(get_downloaded_votes, axis=1)

# %%
# rename vote to total_votes
files_per_proposal = files_per_proposal.rename(columns={"vote": "total_votes"})
# make col called percent_downloaded
files_per_proposal["percent_downloaded"] = files_per_proposal.downloaded_votes / files_per_proposal.total_votes

# %%
# check on the big one
print(files_per_proposal.sort_values("total_votes", ascending=False).iloc[0])
