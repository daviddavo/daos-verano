import tqdm
import pyarrow.parquet as pq
import glob
import os
import logging

OUTPUT_FILE_NAME = './pairs_with_similarity_merged.parquet'

def main(output_file_name=OUTPUT_FILE_NAME):
    # pull all the parquets from pairs_with_similarity with glob
    files = glob.glob('./pairs_with_similarity/*.parquet')
    logging.info(f"found {len(files)} files")

    if __name__ == '__main__':
        # prompt to delete the output file if it exists
        if os.path.exists(output_file_name):
            print(f"WARNING: {output_file_name} already exists, delete it? (y/n)")
            if input() == 'y':
                os.remove(output_file_name)
            else:
                print("aborting")
                exit(1)
    else:
        if os.path.exists(output_file_name):
            logging.warn(f"{output_file_name} already exists, deleting it")
            os.remove(output_file_name)

    output_writer = None

    # write to a new parquet
    logging.info("writing to " + output_file_name)
    for file in tqdm.tqdm(files):
        # read file
        parquet_file = pq.ParquetFile(file)

        arrow_schema = parquet_file.schema.to_arrow_schema()
        if output_writer is None:
            output_writer = pq.ParquetWriter(
                output_file_name,
                arrow_schema,
            )
        output_writer.write_table(parquet_file.read())
    output_writer.close()
    logging.info("done writing to " + output_file_name)

    # check the number of rows
    parquet_file = pq.ParquetFile(output_file_name)
    logging.info('number of rows: ' + str(parquet_file.metadata.num_rows))
