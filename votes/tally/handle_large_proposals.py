import requests
import json
import time
import datetime
import pandas as pd

CHAIN_ID = 'eip155:1'
VOTE_LIMIT = 3000

TALLY_API_KEY = json.load(open('tally_api_key.json'))['key']
url = "https://api.tally.xyz/query"

headers = {
  'Api-Key': TALLY_API_KEY,
  'Content-Type': 'application/json'
}

import os
if not os.path.exists(CHAIN_ID):
    os.makedirs(CHAIN_ID)

def make_proposal_query(chain_id: str, proposal_id: str, votes_limit: int, votes_offset: int) -> str:
    query = """query ProposalsWithVotes {
        proposals(chainId: "%s", proposalIds: ["%s"]) {
            id
            votes(pagination: { limit: %d, offset: %d }) {
                id
                voter {
                    id
                }
                support
                reason
                weight
                proposal {
                    id
                    governor {
                        id
                    }
                }
                block {
                    timestamp
                }
            }
        }
    }"""
    return query % (chain_id, proposal_id, votes_limit, votes_offset)


def get_large_proposal(proposal_id: str):
    votes_offset = 0
    reached_limit = False
    all_votes = []
    large_proposal_vote_limit = 1200
    print('get large prop', CHAIN_ID, proposal_id, datetime.datetime.now())
    while not reached_limit:
        query = make_proposal_query(CHAIN_ID, proposal_id, large_proposal_vote_limit, votes_offset)
        status_code = 999
        while status_code != 200:
            response = requests.request("POST", url, headers=headers, data=json.dumps({'query': query}))
            status_code = response.status_code
            if status_code != 200:
                print('    error', CHAIN_ID, 'proposal:', proposal_id, ' votes:', votes_offset, '-', large_proposal_vote_limit+votes_offset, response.status_code, datetime.datetime.now())
                # wait
                time.sleep(5)
        data = response.json()
        proposal = data['data']['proposals'][-1]
        votes_count = len(proposal['votes'])
        all_votes += proposal['votes']
        print('    votes_count', votes_count, 'large_proposal_vote_limit', large_proposal_vote_limit)

        if votes_count < large_proposal_vote_limit:
            print('    reached votes limit', CHAIN_ID, 'proposal:', proposal_id, ' votes:', votes_offset, '-', large_proposal_vote_limit+votes_offset, response.status_code, datetime.datetime.now())
            reached_limit = True
        else:
            votes_offset += large_proposal_vote_limit
            print('    done', CHAIN_ID, 'proposal:', proposal_id, ' votes:', votes_offset, '-', large_proposal_vote_limit+votes_offset, response.status_code, datetime.datetime.now())
            # print total no of votes so far
            print('    total votes so far', len(all_votes))
    proposal['votes'] = all_votes
    # print total no of votes
    print('    total votes', len(all_votes))
    return proposal


# get prop ids from csv
# read in over_3000_votes_proposals.csv
df = pd.read_csv('over_3000_votes_proposals.csv')
# where chain is CHAIN_ID
df = df[df['chain'] == CHAIN_ID]
# get prop ids
proposal_ids_with_over_3000_votes = df['id'].tolist()

for proposal_id in proposal_ids_with_over_3000_votes:
    if os.path.exists(CHAIN_ID + '/' + proposal_id + '.json'):
        print('SKIPPING', CHAIN_ID, proposal_id, 'file exists')
        continue
    print('RUNNING', CHAIN_ID, proposal_id)
    proposal = get_large_proposal(proposal_id)
    with open(CHAIN_ID + '/' + proposal_id + '.json', 'w') as outfile:
        json.dump(proposal, outfile)
