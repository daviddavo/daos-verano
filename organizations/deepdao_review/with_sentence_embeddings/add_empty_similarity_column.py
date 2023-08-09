import pyarrow.parquet as pq
import pyarrow as pa
import tqdm
import logging


def main():
    # Define chunk size (number of rows to read and modify at a time)
    CHUNK_SIZE = 64_000  # Adjust this according to your needs

    parquet_file = pq.ParquetFile('pairs_df_with_rows.parquet')

    total_rows = parquet_file.metadata.num_rows
    logging.info(f"total_rows: {total_rows}")

    output_writer = None

    for batch in tqdm.tqdm(parquet_file.iter_batches(CHUNK_SIZE), total=int(total_rows / CHUNK_SIZE)):
        # add similarity double column to batch without making into pandas
        similarity_column = pa.array([-1.0] * len(batch))

        batch_with_results = pa.RecordBatch.from_arrays(
            batch.columns + [similarity_column],  # add new column to batch
            schema=batch.schema.append(pa.field("similarity", 'double'))
        )

        # Append the modified chunk_table to the output Parquet file
        if not output_writer:
            # Create or open the output Parquet file
            output_writer = pq.ParquetWriter(
                'pairs_with_empty_similarity.parquet',
                batch_with_results.schema,
            )
        output_writer.write_table(
            pa.Table.from_batches([batch_with_results])
        )
        
    # Close the output Parquet writer
    output_writer.close()
    logging.info("done iterating over chunks")
