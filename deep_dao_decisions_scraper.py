import requests
import json
import pandas as pd

def get_all_dao_basic_info():
    headers = {
        'authority': 'deepdao-server.deepdao.io',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'es-ES,es;q=0.9',
        'cache-control': 'no-cache',
        'origin': 'https://deepdao.io',
        'pragma': 'no-cache',
        'referer': 'https://deepdao.io/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
        'x-api-key': 'YN9xJRmtxn88knalayQab3QQwKf5EjpJ85rov27s',
    }

    params = {
        'limit': '2500',
        'offset': '0',
        'orderBy': 'totalNumProposals',
        'order': 'DESC',
    }

    response = requests.get('https://deepdao-server.deepdao.io/dashboard/ksdf3ksa-937slj3', params=params, headers=headers)

    data = json.loads(response.content)
    return pd.DataFrame(data['daosSummary'])


def get_decisions(organization_id):
    headers = {
        'authority': 'deepdao-server.deepdao.io',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'origin': 'https://deepdao.io',
        'pragma': 'no-cache',
        'referer': 'https://deepdao.io/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
        'x-api-key': 'YN9xJRmtxn88knalayQab3QQwKf5EjpJ85rov27s',
    }
    response = requests.get(
        f'https://deepdao-server.deepdao.io/organization/ksdf3ksa-937slj3/{organization_id}/dao',
        headers=headers,
    )
    data = json.loads(response.content)
    return pd.DataFrame(data['data'])


def make_current_timestamp_folder() -> str:
    """
    Creates a folder with the current timestamp as name
    :return: the name of the folder
    """
    import datetime
    import os
    now = datetime.datetime.now()
    epoch = datetime.datetime.utcfromtimestamp(0)
    timestamp = int((now - epoch).total_seconds() * 1000.0)
    os.mkdir(f'./{timestamp}')
    return str(timestamp)

MAX_DELAY = 5
COUNT = 7

folder_name = make_current_timestamp_folder()
df = get_all_dao_basic_info()[:COUNT]
df.to_csv(f'./{folder_name}/daos.csv')

"""
organizationId          object
uniqueKey               object
daoName                 object
title                   object
logo                    object
totalNumMembers        float64
totalNumProposals      float64
totalNumVotes          float64
activeMembers            int64
totalValueUSD          float64
change24hPercentage    float64
mainTreasuryAddress     object
mainTreasuryTitle       object
mainTreasuryAum        float64
chainLogo               object
createdAt               object
categories              object
aum                     object
dtype: object
"""

for i in range(len(df)):
    oid = df.iloc[i].organizationId
    decisions = get_decisions(oid)
    decisions.to_csv(f'./{folder_name}/{oid}.csv')

    # random sleep
    import time
    import random
    delay = random.randint(1, MAX_DELAY)
    print(f'Finished {i} of {len(df)}')
    print(f'Sleeping {delay} seconds')
    time.sleep(delay)
