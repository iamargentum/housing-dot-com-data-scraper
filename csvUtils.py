import csv
import os

def appendDictsToCSV(data, filename):
    """
    Appends a list of dictionaries to a CSV file.
    Creates the file with headers if it does not exist.

    :param data: List[Dict] - list of dictionaries with identical keys
    :param filename: str - path to CSV file
    """
    if not data:
        raise ValueError("Input data list is empty.")

    file_exists = os.path.isfile(filename)
    fieldnames = data[0].keys()

    # Open file in append mode
    with open(filename, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        # Write header only if file didn't exist
        if not file_exists:
            writer.writeheader()

        # Write all rows
        for row in data:
            writer.writerow(row)

def saveInfoToCSV(propertyInfos: list[dict], csvFileName: str) -> None:
    """
    This method accepts the list of properties in one response
    and appends it to the configured CSV file.
    If the file does not exist and it doesn't have columns, it
    takes care of creating the file and adding columns.
    """
    if len(propertyInfos) == 0: return
    
    appendDictsToCSV(propertyInfos, csvFileName)