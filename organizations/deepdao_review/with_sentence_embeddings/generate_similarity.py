import pyarrow.parquet as pq
import pyarrow as pa
import tqdm
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
import logging

# Define chunk size (number of rows to read and modify at a time)
CHUNK_SIZE = 8_000  # Adjust this according to your needs

# The number of rows to be stores in each parquet file
# FILE_ROW_COUNT = CHUNK_SIZE * 4
FILE_ROW_COUNT = CHUNK_SIZE * 12

def main():
    parquet_file = pq.ParquetFile('pairs_with_empty_similarity.parquet')

    # mkdir pairs_with_similarity if not exists
    if not os.path.exists('pairs_with_similarity'):
        os.mkdir('pairs_with_similarity')

    # make completed_files_list.txt if not exists
    if not os.path.exists('./pairs_with_similarity/completed_files_list.txt'):
        open('./pairs_with_similarity/completed_files_list.txt', 'w').close()

    total_rows = parquet_file.metadata.num_rows
    logging.info(f"total_rows: {total_rows}")

    output_writer = None

    # read string_to_embedding.pickle
    with open('string_to_embedding.pickle', 'rb') as handle:
        string_to_embedding = pickle.load(handle)
    logging.info("loaded string_to_embedding.pickle")

    # log number of files based on FILE_ROW_COUNT
    logging.info("number of files: " + str(int(total_rows / FILE_ROW_COUNT)))

    file_count = 0
    rows_since_last_file = FILE_ROW_COUNT * 2 # start big so we can create a new file on the first iteration

    def get_output_file_name():
        return f'./pairs_with_similarity/out_{file_count}.parquet'

    try:
        logging.info("starting iteration over chunks")
        for batch in tqdm.tqdm(parquet_file.iter_batches(CHUNK_SIZE), total=int(total_rows / CHUNK_SIZE)):
            # check if the file exists in completed_files_list.txt
            if get_output_file_name() in open('./pairs_with_similarity/completed_files_list.txt').read():
                logging.info("file " + str(file_count) + " already completed, skipping...")
                file_count += 1 # bump
                rows_since_last_file = 0 # reset
                continue

            # logging.info("rows so far: " + str(rows_since_last_file) + " file count: " + str(file_count))
            df = batch.to_pandas()
            df['similarity'] = df.apply(lambda row: cosine_similarity([string_to_embedding[row['census_name'].lower()]], [string_to_embedding[row['deepdao_name'].lower()]])[0][0], axis=1)

            modified_chunk_table = pa.Table.from_pandas(df)

            # Append the modified chunk_table to the output Parquet file
            # check if we need to create a new file
            if rows_since_last_file >= FILE_ROW_COUNT:
                # write to completed_files_list.txt
                with open('./pairs_with_similarity/completed_files_list.txt', 'a') as f:
                    f.write(get_output_file_name() + '\n')
                # create a new file
                file_count += 1 # bump
                rows_since_last_file = 0 # reset
                output_writer = pq.ParquetWriter(
                    get_output_file_name(),
                    modified_chunk_table.schema,
                )
                logging.info(f"created new file: out_{file_count}.parquet")

            if output_writer is None:
                logging.info("output_writer is None, picking up at " + str(file_count))
                # this case happens when we pick up after some files are already completed
                output_writer = pq.ParquetWriter(
                    get_output_file_name(),
                    modified_chunk_table.schema,
                )
                # we don't bump or reset here because we're not advancing to a new file
                # we also don't write to completed_files_list.txt because we're not done with this file yet
                logging.info(f"created new file: out_{file_count}.parquet")
            output_writer.write_table(modified_chunk_table)


            rows_since_last_file += len(df)
            
    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt, closing output_writer")
        output_writer.close()
        
    output_writer.close()
    logging.info("done iterating over chunks")


if __name__ == '__main__':
    main()
