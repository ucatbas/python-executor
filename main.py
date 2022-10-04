from os import path
import sys, getopt

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

def is_file_path_valid(_path: str):
    if path.exists(_path):
        _, extension = path.splitext(_path)
        if extension == '.parquet':
            return True
        else:
            print ("Path provided is not valid -- File is not in parquet type!")
            sys.exit()
    else:
        print ("Path provided is not valid -- File does not exist!")
        sys.exit()

def output_path(_path: str):
    name, extension = path.splitext(_path)
    return name + '_updated' + extension
    
def write_parquet_file(file_path, df):
    parquet_schema = pa.Table.from_pandas(df=df).schema
    parquet_writer = pq.ParquetWriter(
        file_path, parquet_schema, compression='snappy')
    table = pa.Table.from_pandas(df, schema=parquet_schema)
    parquet_writer.write_table(table)

def main(argv):
    __script = None
    __path = None
    
    try:
        opts, args = getopt.getopt(argv,"s:p:",["script=","path="])
    except getopt.GetoptError:
        print('client.containers.run("test:latest", ["--script", "<script>", "--path", ".../parquet_path"])')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('client.containers.run("test:latest", ["--script", "<script>", "--path", ".../parquet_path"])')
            sys.exit()
        elif opt in ("-s", "--script"):
            __script = arg
        elif opt in ("-p", "--path"):
            __path = arg

    try:        
        if(is_file_path_valid(__path)):
            df = pd.read_parquet(__path, engine='pyarrow')
            exec(__script)
            write_parquet_file(output_path(__path), df)
    except:
        Exception("Execution Failed!!!")

if __name__ == "__main__":
    main(sys.argv[1:])
