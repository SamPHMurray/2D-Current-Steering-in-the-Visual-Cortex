# This file contains functions which make it easier to simulate and plot
# multiple contours of firing rate in the same file 
# It is specifically designed so that I can work backwards to somewhat match Sabrinas
# data

# Created by Sam Murray with Proffessor Yan Wong

# Created on the 15/10/2024

from spatialVert import Grid

def setup_grid(width: int, height: int, dimension: float, res_vals: list[tuple[float,int]], layers: list[int], neurons: list[int], connections: list[tuple[list[int],list[int],float,float]]) -> Grid:
    """
    This function creates a grid with different parameters and properties

    Arguments: 
        - width: How many tiles wide the grid is
        - height: How many tiles high the grid is
        - dimension: The dimension of a tile in the grid (in meters) 
        - res_vals: A list of tuples specifiying the resistivity values of the tiles for specific rows
        - layers: A list of ints that specify the rows present in each layer (each item represents a
        layer and its integer value the number of rows it has)
        - neurons: A list of integers specifying the number of neurons in each tile in a layer
        - connections: A list of tuples, specifying the layers that have a connection and the
        weight and probabiltiy of connection between those layers

    Returns a Grid class object with the properties specified
    """
        
    # Ensuring all inputs are valid
    if sum(layers) != height:
        print("ERROR")
        print("Layer input is invalid, size of specified layers does not match height")
    if len(layers) != len(neurons):
        print("ERROR")
        print("The lenght of neurons per layer list does not much the length of the layer list")
    res_layer_sum = sum(tup[1] for tup in res_vals)
    if res_layer_sum != height:
        print("ERROR")
        print("Resistivity input is invalid, size of specified layers does not match height")
    

    # Creating grid
    my_grid = Grid(width, height, dimension)
    my_grid.create_grid()

    # Editing resistivities
    my_grid.edit_res(res_vals)

    # Creating neurons
    rows = range(height)
    num_neurons = []

    # Looping through each layer to add the specified number of neurons
    for layer in range(len(layers)):
        for row in range(layers[layer]):
            num_neurons.append(neurons[layer])

    my_grid.create_neurons_in_row(rows, num_neurons)

    # Creating list of layers based on rows
    rowed_layers = []
    current_row = 0
    for i in range(len(layers)):
        rowed_layers.append((current_row,current_row + layers[i]))
        current_row += layers[i]

    # Establishing connectivities
    for connection in connections:

        # Creating list for connecting rows
        conectees = []
        conectors = []

        for i in connection[0]:
            temp_layer = rowed_layers[i-1]
            for temp_row in range(temp_layer[0],temp_layer[1]):
                conectees.append(temp_row)
        
        for j in connection[1]:
            temp_layer = rowed_layers[j-1]
            for temp_row in range(temp_layer[0],temp_layer[1]):
                conectors.append(temp_row)

        for row1 in conectees:
            for row2 in conectors:
                my_grid.establish_connectivities(row1, row2, connection[2],connection[3])
                # print(f"Connection established between row {row1} and row {row2}\n")

    # Creating network
    my_grid.create_network()
    
    # Returning grid
    return my_grid

def mass_sim(grid: Grid, current_sources: list[list[list[float]]], sim_time: float, plot_name: str) -> None:
    """
    This function simulates the grid created given different current source scenarios,
    and prints a contour plot of the firing rates

    Arguments: 
        - grid: Is the Grid object to be simulated
        - current_sources: Is a list containing the different simulations which themselves are lists
        which specify the currenst sources in the simulation which themselves are lists of floats which
        specifiy a current sources location and magnitude
        - sim_time: The time (in ms) the simulation is to run for
        - plot_name: A list of strings, as long as the number of simulations, which specifiy the name
        of the plot produced for each simulation

    Returns nothing, and saves the plots in the current directory
    """
    
    # Looping through each simulation
    name_count = 0
    for sim in current_sources:
        # Adding in each current source
        for source in sim:
            grid.add_CS(source[0],source[1],source[2])

        # Calculating current in each tile, and inputting to neurons
        grid.calc_Ifield()
        grid.introduce_currents()

        # Simulating
        data = grid.simulate(sim_time)
        grid.plot_FR_contour(data[2],plot_name[name_count])
        name_count += 1
    
        # Removing each current source
        for source in sim:
            grid.remove_CS(source[0],source[1])

