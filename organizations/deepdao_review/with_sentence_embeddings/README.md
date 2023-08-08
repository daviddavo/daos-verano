Here we expand on the analysis of the top 100 deepdao organizations.

We generate a `deepdao_org` x `our_data_deployment` pair for every deepdao org
and each of our deployments. This is about 66M rows.

We then generate word embeddings for every name present in this list and 
calculate the similarity for each pair.

## Data pipeline

1. `generate_pairs_and_embeddings.ipynb`
2. `add_row_ids.ipynb`
3. `add_empty_similarity_column.ipynb`
4. `generate_similarity.ipynb` (this is the same as `to_run_on_server.py`)
