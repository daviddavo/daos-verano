import logging

# import make_pairs_and_embeddings
# import add_row_ids
# import add_empty_similarity_column
# import generate_similarity
import concatenate_parquets

# set up logging
logging.basicConfig(
    filename='sentence_embeddings.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(filename)s - %(message)s',
    level=logging.INFO
)

logging.info("starting main.py")

DEPLOYMENTS_PARQUET_PATH = 'deployments.parquet'

if __name__ == '__main__':
    # 1. `generate_pairs_and_embeddings`
    # logging.info("calling make_pairs_and_embeddings.main()")
    # make_pairs_and_embeddings.main(DEPLOYMENTS_PARQUET_PATH)

    # 2. `add_row_ids`
    # logging.info("calling add_row_ids.main()")
    # add_row_ids.main()

    # 3. `add_empty_similarity_column`
    # logging.info("calling add_empty_similarity_column.main()")
    # add_empty_similarity_column.main()

    # 4. `generate_similarity` (this is the same as `to_run_on_server.py`)
    # logging.info("calling generate_similarity.main()")
    # generate_similarity.main()

    # 5. `concatenate_parquets`
    logging.info("calling concatenate_parquets.main()")
    concatenate_parquets.main()

    logging.info("done")
