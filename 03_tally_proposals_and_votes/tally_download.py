# here we can get the proposals and votes at the same time
# we have to paginate, otherwise the request is too big and it breaks

import requests
import pandas as pd
import datetime
import os

now = datetime.datetime.now()
now = int(now.timestamp())

# OUTPUT_PATH = f'tally_scraping_{now}'
OUTPUT_PATH = 'tally_scraping_1687958657'
BATCH_SIZE = 6

# make if not exists
if not os.path.exists(OUTPUT_PATH):
    os.mkdir(OUTPUT_PATH)

headers = {
    'api-key': 'a0a4cd00bb6953720c9c201c010cdd36a563e65c97e926a36a8acdfcd1d1eeb7',
}

query = '''
    query GovernanceProposals($sort: ProposalSort, $chainId: ChainID!, $pagination: Pagination, $governanceIds: [AccountID!], $proposerIds: [AccountID!], $voters: [Address!], $votersPagination: Pagination, $includeVotes: Boolean!) {
    proposals(
        sort: $sort
        chainId: $chainId
        pagination: $pagination
        governanceIds: $governanceIds
        proposerIds: $proposerIds
      ) {
        id
        block {
            timestamp
        }
        votes(voters: $voters, pagination: $votersPagination) @include(if: $includeVotes) {
            id
            voter {
                address
            }
            block {
                timestamp
            }
            weight
            support
        }
        governance {
            # TODO: use slug instead of id
            id
        }
    }
}
'''


def get_proposals_with_votes(limit, offset):
    json_data = {
        'query': query,
        'variables': {
            'pagination': {
                'limit': limit,
                'offset': offset,
            },
            'sort': {
                'field': 'START_BLOCK',
                'order': 'DESC',
            },
            'chainId': 'eip155:1',
            # 'chainId': 'eip155:10',
            'governanceIds': [
                "eip155:1:0x637deEED4e4deb1D222650bD4B64192abf002c00", # rari, on eip155:1
                'eip155:1:0x8a994C6F55Be1fD2B4d0dc3B8f8F7D4E3a2dA8F1', # ampleforth, on eip155:1
                "eip155:1:0xDbD27635A534A3d3169Ef0498beB56Fb9c937489", # gitcoin, on eip155:1
                "eip155:1:0x3D5Fc645320be0A085A32885F078F7121e5E5375", # idle, on eip155:1
                "eip155:1:0x95129751769f99CC39824a0793eF4933DD8Bb74B", # indexed, on eip155:1
                "eip155:1:0xB3a87172F555ae2a2AB79Be60B336D2F7D0187f0", # pooltogether, on eip155:1
                "eip155:1:0x690e775361AD66D1c4A25d89da9fCd639F5198eD", # radicle, on eip155:1
            ],
            'votersPagination': {}, # none
            'includeVotes': True,
        },
    }

    response = requests.post('https://api.tally.xyz/query', headers=headers, json=json_data)

    df = pd.DataFrame(response.json()['data']['proposals'])
    print('  before date filtering', df.shape)

    # ======= keep only proposals for our time period =======

    if df.shape[0] == 0:
        print('done, no results left')
        quit(99)

    # map block.timestamp to proposalCreatedAt column
    df['proposalCreatedAt'] = df['block'].apply(lambda x: x['timestamp'])
    # remove block column
    df.drop(columns=['block'], inplace=True)
    df.head()

    # make createdAt column datetime parse format
    df['proposalCreatedAt'] = pd.to_datetime(df['proposalCreatedAt'], format="%Y-%m-%dT%H:%M:%SZ")

    YEAR_AGO_EPOCH = 1656021600  # 2022-06-24 00:00:00
    NOW_EPOCH =      1687557600  # 2023-06-24 00:00:00
    # make these into datetimes
    YEAR_AGO_EPOCH = pd.to_datetime(YEAR_AGO_EPOCH, unit='s')
    NOW_EPOCH = pd.to_datetime(NOW_EPOCH, unit='s')

    # filter df by createdAt column
    df = df[(df['proposalCreatedAt'] > YEAR_AGO_EPOCH) & (df['proposalCreatedAt'] < NOW_EPOCH)]
    # drop proposalCreatedAt column
    df.drop(columns=['proposalCreatedAt'], inplace=True)

    print('  after date filtering', df.shape)

    if df.shape[0] == 0:
        print('  no results after filtering, exiting method')
        return None


    # ======= expand votes =======
    df = df.explode('votes')
    print('  after exploding votes', df.shape)

    df.rename(columns={'id': 'proposalId'}, inplace=True)
    # make organizationId column from governance.id
    df['organizationId'] = df['governance'].apply(lambda x: x['id'])
    # drop governance
    df.drop('governance', axis=1, inplace=True)

    # expand votes
    df = pd.concat([df.drop(['votes'], axis=1), df['votes'].apply(pd.Series)], axis=1)

    # add voter
    df['voter'] = df['voter'].apply(lambda x: x['address'] if not pd.isnull(x) else None)
    # add createdAt from votes.block.timestamp
    df['createdAt'] = df['block'].apply(lambda x: x['timestamp'] if not pd.isnull(x) else None)
    # make timestamp
    df['createdAt'] = pd.to_datetime(df['createdAt'], format="%Y-%m-%dT%H:%M:%SZ")
    # drop block
    df.drop('block', axis=1, inplace=True)
    # drop mysterious column 0 if it exists
    if 0 in df.columns:
        df.drop(0, axis=1, inplace=True)

    print('  final shape', df.shape)

    # ======= save to csv =======
    print(f'getting {i} to {i+BATCH_SIZE}')
    df.to_csv(f'{OUTPUT_PATH}/proposals_with_votes_{offset}_{offset+limit}.csv', index=False)

# run endlessly in batches
print('using output path', OUTPUT_PATH)
for i in range(0, 9999999999, BATCH_SIZE):
    # # if file already exists, skip
    filepath = f'{OUTPUT_PATH}/proposals_with_votes_{i}_{i+BATCH_SIZE}.csv'
    print(f'getting {i} to {i+BATCH_SIZE}')
    if os.path.exists(filepath):
        print(f'  {i} to {i+BATCH_SIZE} already exists, skipping')
        continue
    get_proposals_with_votes(BATCH_SIZE, i)
