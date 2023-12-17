import csv
import zstandard as zstd
import os
import json
import logging
from datetime import datetime

# Set up logging
log = logging.getLogger("bot")
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())

# Function to read and decode compressed file chunks
def read_and_decode(reader, chunk_size, max_window_size, previous_chunk=None, bytes_read=0):
    chunk = reader.read(chunk_size)
    bytes_read += chunk_size
    if previous_chunk is not None:
        chunk = previous_chunk + chunk
    try:
        return chunk.decode()
    except UnicodeDecodeError:
        if bytes_read > max_window_size:
            raise UnicodeError(f"Unable to decode frame after reading {bytes_read:,} bytes")
        log.info(f"Decoding error at {bytes_read:,} bytes, reading another block")
        return read_and_decode(reader, chunk_size, max_window_size, chunk, bytes_read)

# Function to iterate over lines in a compressed file
def read_lines_zst(file_name):
    with open(file_name, 'rb') as file_handle:
        buffer = ''
        reader = zstd.ZstdDecompressor(max_window_size=2**31).stream_reader(file_handle)
        while True:
            chunk = read_and_decode(reader, 2**27, (2**29) * 2)
            if not chunk:
                break
            lines = (buffer + chunk).split("\n")
            for line in lines[:-1]:
                yield line
            buffer = lines[-1]
        reader.close()

# Main execution block
if __name__ == "__main__":
    #Select the file you want to process
    file_path = 'RS_2019-04.zst'
    #Select the output file name
    output_file_path = 'RS_politics_extracted.csv'
    
    # CSV headers
    csv_headers = [
        "id",
        "created_utc",
        "author",
        "title",
        "num_comments",
        "subreddit",
        "subreddit_id",
        "score",
        
        
    ]

    file_size = os.stat(file_path).st_size
    file_lines = 0
    bad_lines = 0
    #Select the subreddit you want to extract
    value = "politics"

    with open(output_file_path, 'w', encoding='utf-8', newline='') as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(csv_headers)

        for line in read_lines_zst(file_path):
            try:
                obj = json.loads(line)
                if obj.get('subreddit') == value:
                    csv_values = [obj.get(header, "") for header in csv_headers]
                    csv_writer.writerow(csv_values)
            except json.JSONDecodeError as err:
                bad_lines += 1
                continue
            file_lines += 1
            if file_lines % 100000 == 0:
                log.info(f"Processed {file_lines:,} lines; Bad lines: {bad_lines:,}")

    log.info(f"Finished processing. Total lines: {file_lines:,}; Bad lines: {bad_lines:,}")
