# Analysing data from the horizontal model 
# This file exits specifically to extract the data from the experimental and
# model data files, and the compare them by plotting them against each other
# Various functions are also plottefd which compare precentage changes in data
# and plot the difference in data

# This file is not well documented 

# Created by Sam Murray on the 16/01/2024

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
    for i in range(3):
        for j in range(4):
            base_index = 5 * i
            comparative_index =  5*i + j + 1
            
            temp_data = []
            for idx in range(len(file_data[base_index])):
                temp_data.append(100*file_data[comparative_index][idx]/file_data[base_index][idx])
            
            percetage_data.append(temp_data)
    
    return(percetage_data)

def plot_comparison(ed_data, md_data, title, yax):
    
    # Create 15 subplots
    for i in range(len(ed_data)):
        # Define x-axis values
        ed_x_values = np.arange(50, 50 * (len(ed_data[i]) + 1), 50)
        md_x_values = np.arange(12.5, 25 * (len(md_data[i]) + 1)-12.5, 25)
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

def calculate_differences(ed_data, md_data, file_name):
    
    # Creating variables to store difference data
    model_differences_per_electrode = 0
    difference_list = []

    # Looping through each row of data
    ust = 0
    ost = 0
    for row in range(len(ed_data)):
        row_difference = 0
        if row < 5:
            rec_sites = 5
        if row < 10:
            rec_sites = 7
        else: 
            rec_sites = 9
        
        for num in range(len(ed_data[row])):
            ed_val = ed_data[row][num]
            md_val = (md_data[row][num*2 + 1] + md_data[row][num*2+2])/2
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


# Specify the file paths for ED and MD
cwd = os.getcwd()
folder_name = 'All data\\Different model data\\Model 7 data'
folder_path = os.path.join(cwd, folder_name)
ed_file_path = os.path.join(folder_path,'acrossDataF.txt')
md_file_path = os.path.join(folder_path,'M7 analysis data.txt')

# Get firing rate comparisons
ed_fr_data = get_fr_data(ed_file_path,', ', 1)
md_fr_data = get_fr_data(md_file_path,',')

# Get percentage comparisons
ed_per_data = get_percentage_change_data(ed_file_path,', ', 1)
md_per_data = get_percentage_change_data(md_file_path,',')

# Titles
titles = ['sep 300 100-0','sep 300 75-25','sep 300 50-50','sep 300 25-75','sep 300 0-100']
titles.extend(['sep 400 100-0','sep 400 75-25','sep 400 50-50','sep 400 25-75','sep 400 0-100'])
titles.extend(['sep 500 100-0','sep 500 75-25','sep 500 50-50','sep 500 25-75','sep 500 0-100'])

titles_per = ['per sep 300 75-25','per sep 300 50-50','per sep 300 25-75','per sep 300 0-100']
titles_per.extend(['per sep 400 75-25','per sep 400 50-50','per sep 400 25-75','per sep 400 0-100'])
titles_per.extend(['per sep 500 75-25','per sep 500 50-50','per sep 500 25-75','per sep 500 0-100'])

# Call the function to plot the comparison
plot_comparison(ed_fr_data, md_fr_data, titles, "Firing rate")
plot_comparison(ed_per_data, md_per_data, titles_per, "Percentage change from 100-0 split")
calculate_differences(ed_fr_data,md_fr_data,"M7 FR accuracy.txt")
