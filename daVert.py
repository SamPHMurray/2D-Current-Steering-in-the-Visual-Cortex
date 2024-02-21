# Analysing data from the vertical model 
# This file exits specifically to extract the data from the experimental and
# model data files, and the compare them by plotting them against each other
# Various functions are also plottefd which compare precentage changes in data
# and plot the difference in data
 
# This file is not well documented 

# Created by Sam Murray on the 18/01/2024

import matplotlib.pyplot as plt
import numpy as np
import os
import csv

def get_fr_data(file_path, split, if_ed=0):
    # Defining data
    file_data = []

    # Load data from ED files
    with open(file_path, 'r') as file:
        
        # Iterate through each line
        for line in file:
            numbers = [float(num) for num in line.strip().split(split)]
            if if_ed:
                numbers = numbers[1:-1]
            file_data.append(numbers)
    
    # Returning data
    return(file_data)

def get_percentage_change_data(file_path, split, if_ed=0):
    
    # Creating file data
    file_data = []

    # Reading file
    with open(file_path, 'r') as file:
        
        # Iterate through each line
        for line in file:
            numbers = [float(num) for num in line.strip().split(split)]
            if if_ed:
                numbers = numbers[1:-1]
            file_data.append(numbers)
    
    # Getting percentage changes
    percetage_data = []
    for k in range(3):
        for i in range(3):
            for j in range(4):
                base_index = 5 * i + 15 * k
                comparative_index =  5*i + 15*k + j + 1
                
                temp_data = []
                for idx in range(len(file_data[base_index])):
                    if file_data[base_index][idx] == 0:
                        temp_data.append(0)
                    else:
                        temp_data.append(100*file_data[comparative_index][idx]/file_data[base_index][idx])
                
                percetage_data.append(temp_data)
        
    return(percetage_data)
    
def plot_comparison(ed_data, md_data, title, yax):
    
    # Create 15 subplots
    for i in range(len(ed_data)):
        # Define x-axis values
        ed_x_values = np.arange(50, 50 * (len(ed_data[i]) + 1), 50)
        md_x_values = np.arange(50, 50 * (len(md_data[i]) + 1), 50)
        plt.plot(ed_x_values, ed_data[i], label='Experimental data', color='blue')
        plt.plot(md_x_values, md_data[i], label='Modeled data', color='orange')
        plt.title(f'{title[i]}')
        plt.xlabel('Seperation distance')
        plt.ylabel(yax)
        plt.legend()

        # Saving file
        direc = os.getcwd()
        plt.savefig(direc + f'/{title[i]}')

        # Clearing
        plt.clf()

def plot_differences(ed_data, md_data, title, yax):
    
    # Create 15 subplots
    for i in range(len(ed_data)):
        # Define x-axis values
        ed_x_values = np.arange(50, 50 * (len(ed_data[i]) + 1), 50)
        dif_y_vals = [a - b for a,b in zip(ed_data[i], md_data[i])]
        plt.plot(ed_x_values, dif_y_vals, label='Experimental data', color='red')
        plt.title(f'{title[i]}')
        plt.xlabel('Seperation distance')
        plt.ylabel(yax)
        plt.legend()

        # Saving file
        direc = os.getcwd()
        plt.savefig(direc + f'/{title[i]}')

        # Clearing
        plt.clf()

def calculate_differences(ed_data, md_data, file_name):
    
    # Creating variables to store difference data
    model_differences_per_electrode = 0
    difference_list = []

    # Looping through each row of data
    ust = 0
    ost = 0
    for row in range(len(ed_data)):
        
        row_difference = 0
        rec_sites = len(ed_data[row])
        
        for num in range(rec_sites):
            ed_val = ed_data[row][num]
            md_val = md_data[row][num]
            row_difference += abs(ed_val - md_val)
            if ed_val > md_val:
                ust += abs(ed_val - md_val)
            else:
                ost += abs(ed_val - md_val)
        difference_list.append([row_difference/rec_sites])
        model_differences_per_electrode += row_difference/rec_sites
    
    # Making total model differences, per electrode
    model_differences_per_electrode = model_differences_per_electrode / len(ed_data)

    # Saving data to file
    cwd = os.getcwd()
    file_path = os.path.join(cwd,file_name)
    with open(file_path,'w', newline='') as file:
        file.write("Number of firing rate differences between model and experiment per recording site\n")
        writer = csv.writer(file)
        writer.writerows(difference_list)
        file.write("\n\n")
        file.write(f"Total differences for the model per recording site is: {model_differences_per_electrode}")
        file.write(f"\n\nUndershot: {ust}\n\nOvershot: {ost}")

def calc_det_differences(ed_data, md_data, file_name):
    
    # Creating a list of the differences
    dif_list = [0]*15

    # Looping through data
    for layer in range(3):

        # Finding row of first recording electrode in each layer
        if layer == 0:
            start = 6
        elif layer == 1:
            start = 3
        elif layer == 2:
            start = 0

        for row in range(15):

            # Calculating recording sites
            rec_sites = len(ed_data[row])

            # Looping through values
            for num in range(rec_sites):
                # print(layer*15 + row)
                ed_val = ed_data[layer*15 + row][num]
                md_val = md_data[layer*15 + row][num]
                dif_val = ed_val - md_val
                dif_list[start + num] += dif_val



    # Saving data to file
    cwd = os.getcwd()
    file_path = os.path.join(cwd,file_name)
    with open(file_path,'w', newline='') as file:
        file.write("Number of firing rate differences between model and experiment per recording site\n")
        # writer = csv.writer(file)
        for i in range(15):
            file.write(f"Site {i + 1} differences: {dif_list[i]}\n")
 

        
# Specify the file paths for ED and MD
cwd = os.getcwd()
folder_name = 'Vertical model data\\Model V18 data'
folder_path = os.path.join(cwd, folder_name)
ed_file_path = os.path.join(folder_path,'throughDataF.txt')
md_file_path = os.path.join(folder_path,'V18 analysis data.txt')

# Get firing rate comparisons
ed_fr_data = get_fr_data(ed_file_path,', ', 1)
md_fr_data = get_fr_data(md_file_path,',')

# Get percentage comparisons
ed_per_data = get_percentage_change_data(ed_file_path,', ', 1)
md_per_data = get_percentage_change_data(md_file_path,',')

# Titles
titles = []
titles_per = []
for i in range(3):
    if i == 0:
        lay = 'ii'
    if i == 1:
        lay = 'gi'
    if i == 2:
        lay = 'si'

    titles.extend([f'sep {lay} 300 100-0',f'sep {lay} 300 75-25',f'sep {lay} 300 50-50',f'sep {lay} 300 25-75',f'sep {lay} 300 0-100'])
    titles.extend([f'sep {lay} 400 100-0',f'sep {lay} 400 75-25',f'sep {lay} 400 50-50',f'sep {lay} 400 25-75',f'sep {lay} 400 0-100'])
    titles.extend([f'sep {lay} 500 100-0',f'sep {lay} 500 75-25',f'sep {lay} 500 50-50',f'sep {lay} 500 25-75',f'sep {lay} 500 0-100'])

    titles_per.extend([f'dif sep {lay} 300 100-0',f'dif sep {lay} 300 75-25',f'dif sep {lay} 300 50-50',f'dif sep {lay} 300 25-75',f'dif sep {lay} 300 0-100'])
    titles_per.extend([f'dif sep {lay} 400 100-0',f'dif sep {lay} 400 75-25',f'dif sep {lay} 400 50-50',f'dif sep {lay} 400 25-75',f'dif sep {lay} 400 0-100'])
    titles_per.extend([f'dif sep {lay} 500 100-0',f'dif sep {lay} 500 75-25',f'dif sep {lay} 500 50-50',f'dif sep {lay} 500 25-75',f'dif sep {lay} 500 0-100'])

# Call the function to plot the comparison
# plot_comparison(ed_fr_data, md_fr_data, titles, "Firing rate")
# plot_differences(ed_fr_data, md_fr_data, titles_per, "Firing rate differences")
# plot_comparison(ed_per_data, md_per_data, titles_per, "Percentage change from 100-0 split")
calculate_differences(ed_fr_data,md_fr_data,"V18 FR accuracy.txt")
calc_det_differences(ed_fr_data, md_fr_data, "V18 recording site differences.txt")
