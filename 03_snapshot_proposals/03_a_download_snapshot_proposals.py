import pandas as pd
import datetime
import time
import requests
import json
import pandas as pd
import os
import random


FILE_NAME = '../02_combine_deepdao_aragon_and_messari/messari_deepdao_aragon_organizations.csv'
LIMIT = 30

# Use this to pick up a partially-completed scraping
# RECOVERY_DIR_NAME = None
RECOVERY_DIR_NAME = '1687790956'
RECOVERY_MODE = RECOVERY_DIR_NAME is not None

# ==================

df = pd.read_csv(FILE_NAME)
# get pages with platform title is Snapshot
df = df[df['platformType'] == 'Snapshot']

# epoch from a year ago
now = datetime.datetime.now()
year_ago = now - datetime.timedelta(days=365)
YEAR_AGO_EPOCH = int(time.mktime(year_ago.timetuple()))

def generate_query(space, first, skip):
    base = """
        query Proposals {
         proposals(where: {space: "%s", created_gte: %s}, first: %s, skip: %s, orderDirection: desc, orderBy: "created") {
            id
            ipfs
            author
            created
            network
            symbol
            type
            strategies {
              network
              params
            }
            validation {
              params
            }
            plugins
            title
            # body
            discussion
            choices
            start
            end
            quorum
            privacy
            snapshot
            state
            link
            app
            scores
            scores_by_strategy
            scores_state
            scores_total
            scores_updated
            votes
            flagged
          }
        }
    """
    return base % (space, YEAR_AGO_EPOCH, first, skip)


def get_all_proposals(snapshotId):
    URL = "https://hub.snapshot.org/graphql"

    all_proposals = []

    has_next_page = True
    skip = 0
    while has_next_page:
        query = generate_query(snapshotId, 1000, skip)
        r = requests.post(URL, json={'query': query})
        data = json.loads(r.text)

        proposals = data['data']['proposals']
        all_proposals += proposals

        if len(proposals) < 1000:
            has_next_page = False
        skip += 1000

    all_proposals_df = pd.DataFrame(all_proposals)

    # add snapshotId to the df
    all_proposals_df['snapshotId'] = snapshotId
    return all_proposals_df

NOW_EPOCH = int(time.mktime(now.timetuple()))

folder_name = RECOVERY_DIR_NAME if RECOVERY_MODE else str(NOW_EPOCH)

if not os.path.exists(folder_name):
    os.makedirs(folder_name)

print(f'Folder name: {folder_name}')
print(f'Recovery mode? {RECOVERY_MODE}')
for i, row in enumerate(df[:LIMIT].itertuples(), 1):
    sid = row.platformId  # this is the key to query the api

    if os.path.exists(f'./{folder_name}/{sid}.csv'):
        print(f'Already exists {sid}.csv')
        continue

    print('getting row', i, sid)
    proposals = get_all_proposals(sid)
    proposals.to_csv(f'{folder_name}/{sid}.csv', index=False)
    
    # add random wait
    wait_time = random.randint(1, 10)
    print(f'waiting {wait_time} seconds')
    time.sleep(wait_time)
