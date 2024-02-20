# A file used to process data into a simpler more concise form
# so that meaning can be found easier and that data can be 
# plotted easier

# Made by Sam Murray with Professor Yan Wong 
# Created on the 19/01/24

import os
import csv

def process_file(file_path, edge_num1, edge_num2):
    """
    This function takes in a file path and selects a specific column of the data to
    isolate, and also removes irrelavant data either side of the 'electrodes' from the simulation

    Arguments:
        - file_path: Is a string that represents the file path of the data to be processed
        - edge_num1: Is an integer indicating what row from the top edge the electrodes were present in
        - edge_num2: Is an integer indicating what row from the bottom edge the electrodes were present in

    Returns: A list of floats representing the isolated numbers
    """
    with open(file_path, 'r') as file:

        temp_data = []

        # Turning the file into a list of lists
        for line in file:
            values = list(map(float, line.strip().split(',')))
            temp_data.append(values)
       
       # Extracting second column
            relevant_data = [row[1] for row in temp_data[edge_num1:edge_num2]]
        
        return relevant_data


cwd = os.getcwd()
folder_name = 'Vertical model data\\Model V18 data\\Full model V18 data'
folder_path = os.path.join(cwd, folder_name)
output_file_path = 'V18 analysis data.txt'

collated_data = []

# Iterate through files
for i in range(3):

    if i == 0:
        lays = 'ii'
        edge1 = 7
    elif i == 1:
        lays = 'gi'
        edge1 = 5
    elif i == 2:
        lays = 'si'
        edge1 = 2

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
            edge2 = edge1 + 5
        elif i < 10:
            dist = '400'
            edge2 = edge1 + 7
        else:
            dist = '500'
            edge2 = edge1 + 9

        filename = f"FR {dist} {split} - V18 {lays}.txt"
        file_path = os.path.join(folder_path, filename)
        data = process_file(file_path, edge1, edge2)
        collated_data.append(data)


# Write the collated data to a new file
with open(output_file_path,'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(collated_data)

