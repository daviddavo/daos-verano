import pyarrow.parquet as pq
import pyarrow as pa
import tqdm
from sklearn.metrics.pairwise import cosine_similarity

# Define chunk size (number of rows to read and modify at a time)
chunk_size = 8_000  # Adjust this according to your needs

parquet_file = pq.ParquetFile('pairs_with_empty_similarity.parquet')

total_rows = parquet_file.metadata.num_rows

print(total_rows)

output_writer = None

rows = []

count = 0

import pickle
# read string_to_embedding.pickle
with open('string_to_embedding.pickle', 'rb') as handle:
    string_to_embedding = pickle.load(handle)

try:
    for batch in tqdm.tqdm(parquet_file.iter_batches(chunk_size), total=int(total_rows / chunk_size)):
        df = batch.to_pandas()
        # if the row's all have -1 similarity, skip
        if df['similarity'].sum() != -1 * len(df):
            # this means at least one has an overriden value
            print('skipping')
            continue
        df['similarity'] = df.apply(lambda row: cosine_similarity([string_to_embedding[row['census_name'].lower()]], [string_to_embedding[row['deepdao_name'].lower()]])[0][0], axis=1)

        modified_chunk_table = pa.Table.from_pandas(df)

        # Append the modified chunk_table to the output Parquet file
        if not output_writer:
            # Create or open the output Parquet file
            output_writer = pq.ParquetWriter(
                'pairs_with_similarity.parquet',
                modified_chunk_table.schema,
            )
        output_writer.write_table(modified_chunk_table)
        
except KeyboardInterrupt:
    output_writer.close()
    
output_writer.close()


