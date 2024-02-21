# This file takes in the classes from spatial, and utilises them to show
# the effects of current steering within layers
 
# The purpose of this is to use it model current steering in between layers
# However this specific main file, checks for accuracy for model within a single
# layer (this being the infagranular layer)

# Created by Sam Murray and assisted by Proffessor Yan Wong
# Created on the 08/01/2024


from createGridHoz import setup_grid, mass_sim
import time
st = time.time()

# Grid dimensions
g_width = 24
g_height = 6
dim = 25 * 10**(-6)

# Grid resistivities
res_vals = [(5,g_height)]

# Grid layers
layers = [2,2,2]

# Grid neurons 
neurons = [10,10,10]

# Grid connectivities
all_conections = []

c11 = (1, 1, 0.2, 0.3)
c12 = (1, 2, 0.2, 0.2)
c13 = (1, 3, 0.2, 0.5)
all_conections.extend([c11,c12,c13])

c21 = (2, 1, 0.2, 0.1)
c22 = (2, 2, 0.2, 0.2)
c23 = (2, 3, 0.2, 0.5)
all_conections.extend([c21,c22,c23])

c31 = (3, 1, 0.2, 0.1)
c32 = (3, 2, 0.2, 0.2)
c33 = (3, 3, 0.2, 0.75)
all_conections.extend([c31,c32,c33])

# Seting up grid based on parameters
my_grid = setup_grid(g_width, g_height, dim, res_vals, layers, neurons, all_conections)

# Print 
et = time.time() - st
print(f"CONNECTIONS DONE at {et}")

# List of simulations 
total_CS = []

# Horizontal sims
h300_1 = [[150*10**(-6), 87.5*10**(-6), 10*10**(-6)],[450*10**(-6), 87.5*10**(-6), 0*10**(-6)]]
h300_2 = [[150*10**(-6), 87.5*10**(-6), 7.5*10**(-6)],[450*10**(-6), 87.5*10**(-6), 2.5*10**(-6)]]
h300_3 = [[150*10**(-6), 87.5*10**(-6), 5*10**(-6)],[450*10**(-6), 87.5*10**(-6), 5*10**(-6)]]
h300_4 = [[150*10**(-6), 87.5*10**(-6), 2.5*10**(-6)],[450*10**(-6), 87.5*10**(-6), 7.5*10**(-6)]]
h300_5 = [[150*10**(-6), 87.5*10**(-6), 0*10**(-6)],[450*10**(-6), 87.5*10**(-6), 10*10**(-6)]]

h400_1 = [[100*10**(-6), 87.5*10**(-6), 10*10**(-6)],[500*10**(-6), 87.5*10**(-6), 0*10**(-6)]]
h400_2 = [[100*10**(-6), 87.5*10**(-6), 7.5*10**(-6)],[500*10**(-6), 87.5*10**(-6), 2.5*10**(-6)]]
h400_3 = [[100*10**(-6), 87.5*10**(-6), 5*10**(-6)],[500*10**(-6), 87.5*10**(-6), 5*10**(-6)]]
h400_4 = [[100*10**(-6), 87.5*10**(-6), 2.5*10**(-6)],[500*10**(-6), 87.5*10**(-6), 7.5*10**(-6)]]
h400_5 = [[100*10**(-6), 87.5*10**(-6), 0*10**(-6)],[500*10**(-6), 87.5*10**(-6), 10*10**(-6)]]

h500_1 = [[50*10**(-6), 87.5*10**(-6), 10*10**(-6)],[550*10**(-6), 87.5*10**(-6), 0*10**(-6)]]
h500_2 = [[50*10**(-6), 87.5*10**(-6), 7.5*10**(-6)],[550*10**(-6), 87.5*10**(-6), 2.5*10**(-6)]]
h500_3 = [[50*10**(-6), 87.5*10**(-6), 5*10**(-6)],[550*10**(-6), 87.5*10**(-6), 5*10**(-6)]]
h500_4 = [[50*10**(-6), 87.5*10**(-6), 2.5*10**(-6)],[550*10**(-6), 87.5*10**(-6), 7.5*10**(-6)]]
h500_5 = [[50*10**(-6), 87.5*10**(-6), 0*10**(-6)],[550*10**(-6), 87.5*10**(-6), 10*10**(-6)]]

total_CS.extend([h300_1,h300_2,h300_3,h300_4,h300_5,h400_1,h400_2,h400_3,h400_4,h400_5,h500_1,h500_2,h500_3,h500_4,h500_5])

# simulation
sim_time = 100 #ms
plot_names = []

# Generating plot names
for i in range(len(total_CS)):
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
    elif i < 10:
        dist = '400'
    else:
        dist = '500'

    plot_names.append(f"FR {dist} {split} - 3 ps Norm BL - 1100,300,3300 - 30700")
        
mass_sim(my_grid,total_CS,sim_time, plot_names)

