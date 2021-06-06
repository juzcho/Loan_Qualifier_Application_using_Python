# -*- coding: utf-8 -*-
"""Helper functions to load and save CSV data.

This contains a helper function for loading and saving CSV files.

"""
import csv


def load_csv(csvpath):
    """Reads the CSV file from path provided.

    Args:
        csvpath (Path): The csv file path.

    Returns:
        A list of lists that contains the rows of data from the CSV file.

    """
    # This will open the csv file and allow the user to read it.
    with open(csvpath, "r") as csvfile: 
        data = []    # Creates and initialize a new list.
        csvreader = csv.reader(csvfile, delimiter=",")

        # Skip the CSV Header
        next(csvreader)

        # Read the CSV data
        for row in csvreader:
            data.append(row)
    return data

# This save_csv function lets the user open the csv
# given the location of the csv, and write a new csv data.
def save_csv(csvpath, data, header=None): 
    """Saves the CSV file from path provided.

    Args:
        csvpath (Path): The CSV file path.
        data (list of lists): A list of the rows of data for the CSV file.
        header (list): An optional header for the CSV.
    """
    
    # This will open an existing file and then it will overwrite with new data, 
    # otherwise it'll create a new file and add new data, if file doesn't exist.

    with open(csvpath, "w", newline="") as csvfile: 
        # This will define that a comma is considered a separator 
        # for new data in a row.
        csvwriter = csv.writer(csvfile, delimiter=',') 
        if header: # If a header is provided
            csvwriter.writerow(header)  # Writes a header as the first row in the csv.
        csvwriter.writerows(data) # Writes each item in data in each row in csv.
    