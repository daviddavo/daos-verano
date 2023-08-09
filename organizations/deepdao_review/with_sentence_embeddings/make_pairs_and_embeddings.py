# read in ../../parquest_version6/deployments.parquet
from sentence_transformers import SentenceTransformer
import itertools
import json
import pandas as pd
import pickle
import pyarrow.parquet as pq
import requests
import logging

INPUT_FILENAME = '../../../parquet_versions/parquets_version7/deployments.parquet'

def main(input_filename: str = INPUT_FILENAME):
    df = pq.read_table(input_filename).to_pandas()

    # remove where name is null
    df = df[df['name'].notnull()]

    # keep only id and name columns
    df = df[['id', 'name']]

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
            'limit': '99999',
            'offset': '0',
            'orderBy': 'totalNumProposals',
            'order': 'DESC',
        }

        logging.info("making request to deepdao-server.deepdao.io")
        response = requests.get('https://deepdao-server.deepdao.io/dashboard/ksdf3ksa-937slj3', params=params, headers=headers)
        logging.info(f"response.status_code: {response.status_code}")

        data = json.loads(response.content)
        return pd.DataFrame(data['daosSummary'])

    deepdao = get_all_organizations_basic_info()
    deepdao = deepdao[['title', 'organizationId']]
    deepdao = deepdao.rename(
        columns={'title': 'deepdao_name', 'organizationId': 'deepdao_organization_id'}
    )

    logging.info("making pairs_df")
    pairs_df = pd.DataFrame(
        list(itertools.product(df.id, deepdao.deepdao_organization_id)),
        columns=['census_id','deepdao_organization_id']
    )

    logging.info("making deepdao_id_to_name")
    # make dict of id -> title from deepdao df
    deepdao_id_to_name = dict(zip(deepdao['deepdao_organization_id'], deepdao['deepdao_name']))

    # make dict of census id -> title from df
    census_id_to_name = dict(zip(df['id'], df['name']))

    # use the dicts to add a census_name and an internal_name colummn to the df
    pairs_df['deepdao_name'] = pairs_df['deepdao_organization_id'].map(deepdao_id_to_name)
    pairs_df['census_name'] = pairs_df['census_id'].map(census_id_to_name)
    pairs_df

    all_strings_to_embed = list(census_id_to_name.values()) + list(deepdao_id_to_name.values())
    all_strings_to_embed = [s.lower() for s in all_strings_to_embed]
    all_strings_to_embed = list(set(all_strings_to_embed))

    logging.info("making embeddings")
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    embeddings = model.encode(all_strings_to_embed, show_progress_bar=True)

    # make a dict of the form {string: [embedding], ...}
    # from all_strings_to_embed and embeddings
    string_to_embedding = {}
    for i in range(len(all_strings_to_embed)):
        string_to_embedding[all_strings_to_embed[i]] = embeddings[i]

    logging.info("saving embeddings to pickle")
    # save string_to_embedding as pickle file
    with open('string_to_embedding.pickle', 'wb') as handle:
        pickle.dump(string_to_embedding, handle)

    logging.info("saving pairs to parquet")
    pairs_df.to_parquet('pairs_df.parquet')

    logging.info("done")

if __name__ == '__main__':
    main()
