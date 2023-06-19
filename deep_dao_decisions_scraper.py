import requests
import json
import os
import pandas as pd

# Use this to pick up a partially-completed scraping
RECOVERY_DIR_NAME = None
MIN_DELAY = 1
MAX_DELAY = 10
COUNT = 2    # deep dao currently has ~2300 DAOs

def get_all_organizations_basic_info() -> pd.DataFrame:
    """
    Gets the basic info of all DAOs
    :return: a dataframe with the basic info of all DAOs
    """
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
        'limit': '3000',
        'offset': '0',
        'orderBy': 'totalNumProposals',
        'order': 'DESC',
    }

    response = requests.get('https://deepdao-server.deepdao.io/dashboard/ksdf3ksa-937slj3', params=params, headers=headers)

    data = json.loads(response.content)
    return pd.DataFrame(data['daosSummary'])


def get_decision_platforms(organization_id) -> pd.DataFrame:
    """
    Gets the decision platforms of a DAO
    :param organization_id: the id of the DAO
    :return: a dataframe with the decision platforms
    """
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


if __name__ == '__main__':
    folder_name = RECOVERY_DIR_NAME if RECOVERY_DIR_NAME else make_current_timestamp_folder()
    df = get_all_organizations_basic_info()[:COUNT]
    df.to_csv(f'./{folder_name}/organizations.csv')

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
        if os.path.exists(f'./{folder_name}/{oid}.csv'):
            print(f'Already exists {oid}.csv')
            continue
        else:
            decision_platforms = get_decision_platforms(oid)
            decision_platforms.to_csv(f'./{folder_name}/{oid}.csv')

        # random sleep
        import time
        import random
        delay = random.randint(MIN_DELAY, MAX_DELAY)
        print(f'Finished {i+1} of {len(df)}')
        print(f'Sleeping {delay} seconds')
        time.sleep(delay)
