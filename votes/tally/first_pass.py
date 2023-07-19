import requests
import json
import time
import datetime

CHAIN_ID = 'eip155:10'
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

def make_votes_query(chain: str, limit: int, offset: int, votes_limit: int, votes_offset: int) -> str:
    query = """query ProposalsWithVotes {
        proposals(chainId: "%s", pagination: { limit: %d, offset: %d }) {
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
    return query % (chain, limit, offset, votes_limit, votes_offset)


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
        proposal = data['data']['proposals'][0]
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


# # https://www.tally.xyz/gov/arbitrum/proposals
# prop_id = '70545629960586317780628692755032548222173912190231545322320044688071893662480'

# proposal = get_large_proposal(prop_id)
# # make dir for chain if not exists
# # save proposal to file


# with open(CHAIN_ID + '/' + prop_id + '.json', 'w') as outfile:
#     json.dump(proposal, outfile)



props_count_query = """query ProposalsWithVotes {
  proposals(chainId: "%s") {
    id
  }
}""" % CHAIN_ID
response = requests.request("POST", url, headers=headers, data=json.dumps({'query': props_count_query}))
data = response.json()
proposals = data['data']['proposals']

print('NUMBER OF TOTAL PROPOSALS', len(proposals))

PROPOSALS_COUNT = len(proposals)

def get_query_results(limit, offset):
    query = make_votes_query(CHAIN_ID, limit, offset, VOTE_LIMIT, 0)
    status_code = 999
    while status_code != 200:
        response = requests.request("POST", url, headers=headers, data=json.dumps({'query': query}))
        status_code = response.status_code
        if status_code != 200:
            print('    error', CHAIN_ID, offset, '-', limit+offset, response.status_code, datetime.datetime.now())
            # wait
            time.sleep(5)
    data = response.json()
    proposals = data['data']['proposals']
    print('    done', CHAIN_ID, offset, '-', limit+offset, response.status_code, datetime.datetime.now())
    if len(proposals) < limit:
        print('    reached limit', CHAIN_ID, offset, response.status_code, datetime.datetime.now())
    return proposals

# handling eip155:42161
first_pass_proposals = []

print('starting', CHAIN_ID, datetime.datetime.now())

# get proposals in chunks of 30; there are 252 proposals
for offset in range(0, len(proposals), 30):
    result = get_query_results(30, offset)
    first_pass_proposals.append(result)

# save first pass proposals
with open(CHAIN_ID + '/first_pass_proposals.json', 'w') as outfile:
    json.dump(first_pass_proposals, outfile)

import pdb; pdb.set_trace()

# big_proposals = []
# for i, proposals in enumerate(first_pass_proposals):
#     for proposal in proposals:
#         if proposal.get('votes') is not None and len(proposal.get('votes')) == VOTE_LIMIT:
#             print(i, proposal['id'])
#             big_proposals.append(proposal)
#             # remove from first_pass_proposals
#             first_pass_proposals[i] = None

# print(big_proposals)
# import pdb; pdb.set_trace()

# for proposal in big_proposals:
#     proposal_id = proposal['id']
#     # get big proposal


# all_proposals = first_pass_proposals + big_proposals

