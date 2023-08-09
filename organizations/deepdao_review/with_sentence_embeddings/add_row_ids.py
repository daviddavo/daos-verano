import pyarrow.parquet as pq
import pyarrow as pa
import tqdm
import os
import logging


# Specify the Parquet file paths
INPUT_PARQUET_FILE_PATH = 'pairs_df.parquet'
OUTPUT_PARQUET_FILE_PATH = 'pairs_df_with_rows.parquet'

# Define chunk size (number of rows to read and modify at a time)
CHUNK_SIZE = 64_000  # Adjust this according to your needs


def main():
    # Open the input Parquet file
    logging.info("opening input Parquet file")
    input_parquet_file = pq.ParquetFile(INPUT_PARQUET_FILE_PATH)

    # Get the total number of rows
    total_rows = input_parquet_file.metadata.num_rows
    logging.info(f"total_rows: {total_rows}")

    # delete pairs_df_with_rows.parquet if it already exists
    if os.path.exists(OUTPUT_PARQUET_FILE_PATH):
        os.remove(OUTPUT_PARQUET_FILE_PATH)


    parquet_file = pq.ParquetFile(INPUT_PARQUET_FILE_PATH)

    output_writer = None

    logging.info("iterating over chunks")
    for batch in tqdm.tqdm(parquet_file.iter_batches(CHUNK_SIZE), total=int(total_rows / CHUNK_SIZE)):
        batch_df = batch.to_pandas()
        batch_df['row_id'] = batch_df['census_id'] + '_' + batch_df['deepdao_organization_id']

        modified_chunk_table = pa.Table.from_pandas(batch_df)

        # Append the modified chunk_table to the output Parquet file
        if not output_writer:
            # Create or open the output Parquet file
            output_writer = pq.ParquetWriter(
                OUTPUT_PARQUET_FILE_PATH,
                modified_chunk_table.schema,
            )
        output_writer.write_table(modified_chunk_table)

    # Close the output Parquet writer
    output_writer.close()
    logging.info("done iterating over chunks")

    # Open the output Parquet file
    output_parquet_file = pq.ParquetFile(OUTPUT_PARQUET_FILE_PATH)

    # Get the total number of rows
    logging.info(f"output_parquet_file.metadata.num_rows: {output_parquet_file.metadata.num_rows}")
