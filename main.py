"""
This is the entrypoint to the program. 'python main.py' will be executed and the 
expected csv file should exist in ../data/destination/ after the execution is complete.
"""
import os
from pathlib import Path
from csv import writer
from src.some_storage_library import SomeStorageLibrary

BASE_PATH = Path(__file__).parent
TEMP = BASE_PATH / "data" / "temp"
SOURCE = BASE_PATH / "data" / "source"


def get_file_columns() -> list:
    """
    Reads the column names from a source file and returns them as a list.

    Returns:
        list: A list containing the column names.
    """
    file_path: str = SOURCE / "SOURCECOLUMNS.txt"
    # I am assuming a fixed number of columns for this challenge, 
    # like it comes from a static source system e.g. SAP
    columns = [None] * 11 

    with open(file_path, "r") as file:
        for line in file:
            idx, column = line.strip().split("|")
            columns[int(idx) - 1] = column

    return columns


def process_source_data(source_path: Path, columns: list, output_path: Path):
    """
    Reads the source data, processes it, and writes it to a CSV file.

    Args:
        source_path (Path): Path to the source data file.
        columns (list): List of column names.
        output_path (Path): Path to the output CSV file.
    """
    with open(source_path, "r") as source, open(output_path, "w", newline="") as output:
        csv_writer = writer(output)
        csv_writer.writerow(columns)

        for line in source:
            csv_writer.writerow(line.strip().split("|"))


def write_out_file(output_name: str):
    """
    Processes the source data and writes it to a CSV file, then loads it to the destination using the storage library.
    """
    source_path: str = SOURCE / "SOURCEDATA.txt"
    TEMP.mkdir(parents=True, exist_ok=True)
    temp_file_path = TEMP / f"{output_name}.csv"

    columns: list = get_file_columns()
    process_source_data(source_path, columns, temp_file_path)

    sl = SomeStorageLibrary()
    sl.load_csv(filename=str(temp_file_path))


if __name__ == '__main__':
    """Entrypoint"""
    print('Beginning the ETL process...')
    write_out_file(output_name='output')
