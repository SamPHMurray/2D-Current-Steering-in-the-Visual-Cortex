# This file is used to process the many text files of raw data gotten from the main file
# and simplifies it to a single text file showing the firing rates in between neurons
 
# Created on the 09/01/2024

import os
import csv


def process_file(file_path: str, edge_num: int) -> list[float]:
    """
    This function takes in a file path and selects a specific row (in this case 3) of the data to
    isolate, and also removes irrelavant data either side of the 'electrodes' from the simulation

    Arguments:
        - file_path: Is a string that represents the file path of the data to be processed
        - edge_num: Is an integer indicating what column from the edges the electrodes were present in

    Returns: A list of floats representing the isolated numbers
    """

    # Opening file
    with open(file_path, 'r') as file:
        lines = file.readlines()

        # stating row
        row = 3
        
        # Assuming each line has 24 numbers and removing the first and last 6 numbers from the 4th line
        data_line = lines[row].strip().split(',')[edge_num:-edge_num]
        
        return [float(num) for num in data_line]


# Getting folder path and the output file path name
cwd = os.getcwd()
folder_name = 'All data\\Different model data\\Model 7 data\\Full model 7 data'
folder_path = os.path.join(cwd, folder_name)
output_file_path = 'M7 Comparable Data.txt'

# Creating a list of the important data
collated_data = []

# Iterate through files based off of how I named them
for i in range(15):
    if (i % 5) == 0:
        split = '100'
    elif (i % 5) == 1:
        split = '75'
    elif (i % 5) == 2:
        split = '50'
    elif (i % 5) == 3:
        split = '25'
    elif (i % 5) == 4:
        split = '0'

    if i < 5:
        dist = '300'
        edge = 6
    elif i < 10:
        dist = '400'
        edge = 4
    else:
        dist = '500'
        edge = 2
    
    # Finding file name/path
    filename = f"FR {dist} {split} - 3 ps Norm BL - 1100,300,3300 - 30700.txt"
    file_path = os.path.join(folder_path, filename)
    data = process_file(file_path, edge)

    # Adding important data to list
    collated_data.append(data)


# Write the collated data to a new file
with open(output_file_path,'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(collated_data)

