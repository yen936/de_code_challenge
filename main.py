"""
This is the entrypoint to the program. 'python main.py' will be executed and the 
expected csv file should exist in ../data/destination/ after the execution is complete.
"""
import os
from pathlib import Path
from src.some_storage_library import SomeStorageLibrary

base_path = Path(__file__).parent

TEMP = "data/temp/"
SOURCE = "data/source/"

def get_columns() -> str:
    """
    Reads the column names from a source file and returns them as a comma-separated string.

    Returns:
        str: A string containing the column names separated by commas.
    """
    
    file_path = os.path.join(base_path, SOURCE, "SOURCECOLUMNS.txt")

    # init array of fixed size
    columns = [None] * 11

    with open(file_path, "r+") as file:
        for line in file:
            # data cleaning
            line = line.replace("\n", "").split("|")
            # sorting columns based on index
            idx = int(line[0]) - 1
            columns[idx] = line[1]

    return ",".join(columns)

def write_out_file():
    """
    Reads the source data, replaces pipe characters with commas, adds a header, and writes the processed data to a temporary CSV file.

    Finally, loads the CSV file into a storage library.
    """

    cols = get_columns()

    source_path = os.path.join(base_path, SOURCE, "SOURCEDATA.txt")

    with open(source_path, 'r') as f:
        lines = f.readlines()

    lines = [line.replace("|", ",") for line in lines]
    lines.insert(0, cols + "\n")

    sl = SomeStorageLibrary()

    temp_directory = os.path.join(base_path, TEMP)
    if not os.path.exists(temp_directory):
        os.makedirs(temp_directory)

    temp_file_path = temp_directory + "output.csv"
    with open(temp_file_path, "w+") as f:
        f.writelines(lines)

    sl.load_csv(filename=temp_file_path)


if __name__ == '__main__':
    """Entrypoint"""
    print('Beginning the ETL process...')
    write_out_file()
