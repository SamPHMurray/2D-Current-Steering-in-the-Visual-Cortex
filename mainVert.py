# This file takes in the classes from spatial.py, and utilises them to show
# the effects of current steering within or between layers depending on user 
# choice

# The purpose of this is to use it model current steering in between layers
# This specific main 
 
# Created by Sam Murray and assisted by Proffessor Yan Wong
# Created on the 22/01/2024


from createGridVert import setup_grid, mass_sim
import time
st = time.time()

# Grid dimensions
g_width = 3
g_height = 18
dim = 50 * 10**(-6)

# Grid resistivities
res_vals = [(5,g_height)]

# Grid layers
layers = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

# Grid neurons 
neurons = [10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10]

# Grid connectivities
all_conections = []
all = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
all2 = [2,3,4,5,6,7,8,9,11,12,13,14,15,16,17]

# All layers
c1 = (all, [3], -0.2, 0.58)
c2 = (all, [4], -0.2, 0.43)
c3 = (all, [5], -0.2, 0.01)
c4 = (all, [6], 0.2, 0.24)
c5 = (all, [7], -0.2, 0.14)
c6 = (all, [8], -0.2, 0.09)
c7 = (all, [9], -0.2, 0.04)
c8 = (all, [10], 0.2, 0.2)
# c9 = (all, [11], 0.2, 0.05)
c10 = (all, [12], 0.2, 0.01)
c11 = (all, [13], -0.2, 0.57)
c12 = (all, [14], -0.2, 0.28)
c13 = (all, [15], -0.2, 0.29)
c14 = (all, [16], -0.2, 0.08)
c15 = (all, [17], -0.2, 0.15)

all_conections.extend([c1,c2,c3,c4,c5,c6,c7,c8,c10,c11,c12,c13,c14,c15])



# Seting up grid based on parameters
my_grid = setup_grid(g_width, g_height, dim, res_vals, layers, neurons, all_conections)

# Print 
et = time.time() - st
print(f"CONNECTIONS DONE at {et}")

# List of simulations 
total_CS = []
plot_names = []

for layer in range(3):
    
    if layer == 0:
        start = 375 * 10**(-6)
        lays = 'ii'
    if layer == 1:
        start = 225 * 10**(-6)
        lays = 'gi'
    if layer == 2:
        start = 75 * 10**(-6)
        lays = 'si'

    for sep in range(3):
        
        if sep == 0:
            finish = start + 300 * 10**(-6)
            dist = '300'
        elif sep == 1:
            finish = start + 400 * 10**(-6)
            dist = '400'
        elif sep == 2:
            finish = start + 500 * 10**(-6)
            dist = '500'

        for split in range(5):

            # Calculating split
            lowC = split * 2.5 * 10**(-6)
            highC = 10 * 10**(-6) - lowC

            temp_cs = [[80*10**(-6), start, highC],[80*10**(-6), finish, lowC]]
            total_CS.append(temp_cs)

            # Calculating split name
            Csplit = f'{100 - 25*split}'

            plot_names.append(f"FR {dist} {Csplit} - V4 {lays}")


# simulation
sim_time = 100 #ms
mass_sim(my_grid,total_CS,sim_time, plot_names)









