# %%
import pickle
large_proposals_and_votes = pickle.load(open('large_proposals_and_votes.pkl', 'rb'))
large_proposals_and_votes

# %%
# min. no. of query groups
sum([x[1] for x in large_proposals_and_votes]) / 5000

# %%
# 2700 queries just for this one proposal!
2765849 / 1000

# %%
def make_query(proposal_id: str, created_gte: int) -> str:
    """
    * platform
    * platform_deployment_id
    * proposal_id
    * vote_id
    * voter -- the id of the person who made the vote
    * date -- this should be as a pandas date, not as an epoch
    * choice -- this should be a string as this is not always true/false
    * weight -- the vote weight
    """
    base = """
       query {
         votes(where: {proposal: "%s", created_gte: %s}, first: 1000, orderBy: "created", orderDirection: asc) {
            space {
              id
            }
            proposal {
              id
            }
            id
            voter
            created
            vp_by_strategy
            vp
          }
        }
    """
    return base % (proposal_id, created_gte)

# %%
import requests
import backoff
URL = "https://hub.snapshot.org/graphql"

# make custom SnapshotException
class SnapshotException(Exception):

    def __init__(self, message='SnapshotException'):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"SnapshotException: {self.message}"


@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException)
@backoff.on_exception(backoff.expo,
                      SnapshotException)
def query_snapshot(query):
    r = requests.post(URL, json={'query': query})
    data = r.json()
    if data.get('error'):
        raise SnapshotException
    # print(data)
    return data['data']['votes']

# %%
# mkdir large_proposal_votes_2023_07_21 if it doesn't exist
import os
os.makedirs('large_proposal_votes_2023_07_21', exist_ok=True)
# make child dirs for each large_proposals_and_votes item if they don't exist
for proposal_id, _ in large_proposals_and_votes:
    os.makedirs(f'large_proposal_votes_2023_07_21/{proposal_id}', exist_ok=True)

# %%
import json
import glob

JAN_1_2000 = 946684800

def process_large_proposal(proposal_id):
    # look for file in dir that has the largest number in the filename, use this to start
    files = glob.glob(f'large_proposal_votes_2023_07_21/{proposal_id}/votes_*.json')
    # files like votes_<timestamp>.json
    if len(files) == 0:
        next_timestamp = JAN_1_2000
    else:
        next_timestamp = max([int(x.split('_')[-1].split('.')[0]) for x in files])
    
    finished_indicator_filename = f'large_proposal_votes_2023_07_21/{proposal_id}/finished.txt'
    if os.path.exists(finished_indicator_filename):
        print('already finished', proposal_id)
        return 0

    print('starting from', proposal_id, next_timestamp)

    # pagination logic
    has_more = True
    while has_more:
        timestamp = next_timestamp
        filename = f'large_proposal_votes_2023_07_21/{proposal_id}/votes_{timestamp}.json'

        if os.path.exists(filename):
            # this is a restart, so we need to read the last timestamp from the file
            with open(filename, 'r') as f:
                votes = json.load(f)
            timestamp = votes[-1]['created']
        query = make_query(proposal_id, timestamp)
        votes = query_snapshot(query)
        print('got', len(votes), 'votes for', proposal_id, timestamp)
        # save votes to file in the output dir
        with open(filename, 'w') as f:
            json.dump(votes, f)
        if len(votes) == 1000:
            # get the last timestamp and use that as the next_timestamp
            next_timestamp = votes[-1]['created']
        else:
            has_more = False
            # write finished indicator file
            with open(finished_indicator_filename, 'w') as f:
                f.write(len(votes))
    return 0

# %%
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=1) as executor:
    futures = [executor.submit(process_large_proposal, proposal_id) for proposal_id, _ in large_proposals_and_votes]

    # Wait for all threads to complete
    votes_processed_list = [future.result() for future in futures]


