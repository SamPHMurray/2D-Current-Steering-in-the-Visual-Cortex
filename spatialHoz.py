# This file named 'spatialHoz' provides the classes that create the 2D map that
# the current steering model is preformed on, this 2D map there is a grid
# of tiles. The grid is a class and so are the tiles.

# The tile class holds specific features, neurons, and equations relating to 
# a specific point in space

# The grid class organises tiles in a spatial manner, and has many functions
# associated with it that allow the use to implement current sources to the 
# grid, edit tile paramters row-wise, print grid information, establish connections
# between tiles, and simualte the program amongst other things 

# The purpose of this is to use it model current steering in between layers

# Specifically this model has an emphasis on playing with the equation of how
# current spreads in the heterogenous, anisotropic brain, and using data from 
# Yans lab (by Sabrina) to create an equation for how current spreads 

# Created by Sam Murray and assisted by Proffessor Yan Wong
# Created on the 08/01/2024

# Importing necessary modules
import math
import numpy as np
import matplotlib.pyplot as plt
from brian2 import ms, amp, Mohm, mV, Network, SpikeMonitor, NeuronGroup, prefs, Synapses
from os import getcwd

# This instructs Brian2 simulator to use numpy to create graphs
prefs.codegen.target = "numpy"

# Creating class for a tile in a grid
class Tile:
    """
    A Tile represents a single square in a grid of squares.
    
    Each tile is represented by its x and y location in the grid, 
    the x and y refer to tiles locations with respect to other tiles.

    Each tile has an associated resistivity, permitivity, and 
    electric field. They also have a dimensions refering to the 
    length and width of the square, and a centre location referring 
    to the dimensional coordinates of the tiles centre.
    """

    def __init__(self, x: int, y: int, res: int, dim: int) -> None:
        """
		Initiliases a tile using provided location, resistivty, 
        permeability and dimension.
		
		Arguments:
			- x: Numerical x coordinate of card
            - y: Numerical y coordinate of card
            - res: Tiles inherent resistivitty
            - perm: Tiles inherent permeability
            - dim: Tiles length and width
			
		"""
        
        # The tiles x and y numerical coordinates in the grid
        self.x = x
        self.y = y

        # The tiles associated resistivities and permitvities
        self.res = res

        # The tiles calculated electric field (is initially 0) 
        self.E = 0
        self.I = 3*10**(-10)

        # The centre of the tiles dimensional coordinates on the grid
        self.x_cent = x*dim + dim/2
        self.y_cent = y*dim + dim/2

        # Each tile also contains a group of neurons 
        self.tau = 10*ms # The membranes time constant
        self.R = 100*Mohm # Associated membrane resistance 
        self.v_rest = -80*mV # Associated membrane resting potential
        # Equation which governs the neurons
        self.eqs = ''' 
        dv/dt = (v_rest - v + R*I) / tau : volt
        I : amp (constant)
        tau : second
        R : ohm
        v_rest : volt
        ''' 

        # Creating neuron group (this just defines self.neuron as a group), this needs to occur in the initialisse
        # block so that it becomes functional through the create_group function
        self.num_neurons = 1
        self.neuronG = NeuronGroup(self.num_neurons, self.eqs, threshold='v>-50*mV', reset='v = -80*mV', method='exact')

    def create_group(self, num_neurons: int) -> None:
        """
		Establishes a group of neurons that are 'within' or associated with the tile
		
		Arguments:
			- num_neurons: States how many neurons are to be associated with the tile
        """

        # Stating how many neurons are present in the group
        self.num_neurons = num_neurons

        # Creating the group
        self.neuronG = NeuronGroup(self.num_neurons, self.eqs, threshold='v>-50*mV', reset='v = -80*mV', method='exact')
        
        # Parameters of the group
        self.neuronG.tau = self.tau
        self.neuronG.R = self.R
        self.neuronG.v_rest = self.v_rest
        self.neuronG.v = -80*mV
    
    def __str__(self) -> str:
        """
        This function is used to return a string representation of a tile

        Returns string stating tiles numerical coordinates
        """

        return f"Tile {self.x}, {self.y}"


# Creating a class for the overall grid with associated functions
class Grid:
    """
    A Grid is a grid of squares, with each square containing a Tile

    A grid has an associated height (how many tiles high) and width
    (how many tiles wide). It also has an associated tile dimension
    which specifies the dimensions of the tiles it has.

    The grid has an initially empty dictionary of current sources, 
    which specifiy a current sources dimensional location and
    amplitude on the grid.
    """

    def __init__(self, width: int, height: int, tdim: int):
        """
		Initiliases a grid using provided height, width, and
        tile dimension.
		
		Arguments:
			- width: How many tiles wide the grid is
			- height: How many tiles high the grid is
            - tdim: The dimensions of the tiles within the grid
		"""
        
        # Initialising parameters
        self.width = width
        self.height = height
        self.tdim = tdim

        # Intitialising empty current source dictionary
        self.current_sources = {}

        # Initialising a network for simulation
        self.net = Network()
        self.spike_monitors = []

    def create_grid(self) -> list[Tile]:
        """"
        This function is used to actually create the grid of tiles.

        Returns a list of the tiles in the grid.
        """

        grid = []
        for y in range(self.height):
            res = 10 # This is a standard value for white matter
            for x in range(self.width):
                tile = Tile(x, y, res, self.tdim)
                grid.append(tile)
        self.tiles = grid
        return grid

    def get_tile(self, x: int, y:int) -> Tile:
        """
        This function takes in a numerical coordinate and gives
        the tile at that coordinate

        Returns a tile object
        """

        index = y * self.width + x
        return self.tiles[index]
    
    def get_row(self, row: int) -> list[Tile]:
        """
        This function takes in a number and gives a list of the
        tiles at that row

        Returns a list of tile objects
        """
        if 0 <= row < self.height:
            start_index = row * self.width
            end_index = (row + 1) * self.width
            return self.tiles[start_index:end_index]
        else:
            return None
    
    def edit_res(self, res_list: list[tuple[float, int]]) -> None:
        """"
        This function is used to edit the resistivities of the tiles in the grid.

        Arguments:
            - res_list: Is a list of tuples, the tuples indicate the resistivity and then how many rows
                from the top take that resisitivity value, if theres multiple tuples, the next ones
                indicate the resistivity of the next rows

        Returns nothing.
        """
        
        current_row = 0
        for new_res, num_rows in res_list:
            for y in range(num_rows):
                for x in range(self.width):
                    tempTile = self.get_tile(x, current_row)
                    tempTile.res = new_res
                current_row += 1

    def print_grid_res(self) -> None:
        """
        Function prints out all the grid resistivities in an 
        array format
        """

        print("GRID RESISTIVITIES")
        for row in range(self.height):
            for col in range(self.width):
                tile = self.get_tile(col, row)
                print(f"{tile.res} ",end="")
            print("\n",end="")
        print("\n",end="")

    def print_grid_currents(self) -> None:
        """
        Function prints out all the tiles input currents in an 
        array format
        """

        print("GRID CURRENTS")
        for row in range(self.height):
            for col in range(self.width):
                tile = self.get_tile(col, row)
                print(f"{tile.I:.3e} ",end="")
            print("\n",end="")
        print("\n",end="")

    def calculate_distance(self, tile: Tile, point: tuple[float, float]) -> float:
        """
        Function which calculates the distance between a tiles
        centre and a coordinate

        Arguments:
            - tile: A Tile class object
            - point: A tuple of a coordinate

        Returns a float of the distance
        """

        # Calculate distance between tile and point
        return math.sqrt((point[0] - tile.x_cent)**2 + (point[1] - tile.y_cent)**2)

    def points_obtain(self, tile: Tile, point: tuple[float, float], num_points: int) -> list[float]:
        """
        Function which provides a list of evenly spaced
        points between a tile and a coordinate

        Arguments:
            - tile: A Tile clas object
            - point: A tuple of a coordinate
            - num_points: An integer of the number of points
            the user wants (the higher the points the greater
            the accuracy)

        Returns a list of dimensional coordinates as tuples
        """

        points = []
        dx = (point[0] - tile.x_cent) / (num_points - 1)
        dy = (point[1] - tile.y_cent) / (num_points - 1)

        for i in range(num_points):
            current_x = tile.x_cent + i * dx
            current_y = tile.y_cent + i * dy
            points.append((current_x, current_y))
        return points

    def tile_loc(self, x: float, y: float) -> Tile:
        """
        This function takes in a dimensional coordinate and gives
        the tile that coordinate is in

        Arguments: 
            x: Dimensional x coordinate
            y: Dimensional y coordiante

        Returns a Tile object
        """

        x_loc = x//self.tdim
        y_loc = y//self.tdim
        
        for tile in self.tiles:
            if (tile.x == x_loc and tile.y == y_loc):
                return tile
            
    def ave_res(self, tile: Tile, point_coord: tuple[float, float], num_points: int) -> float:
        """
        This function calculates the average resistivity between a tiles 
        center and a dimensional coordinate

        Arguments:
            - tile: A tile object
            - point_coord: A tuple coordinate
            - num_points: The number of points used to calculate
            the average resistivity (an accuracy parameter)

        Returns a float of the average resistivity
        """

        # Calculate the distance between tiles, and the number of segments used to 
        # calculate the average resistance, and then the length of each segment
        dist = self.calculate_distance(tile, point_coord)
        weighted_dist = dist/num_points

        # Generating list of points and initialising total resistance
        points = self.points_obtain(tile, point_coord, num_points)
        total_res = 0

        # Looping through points and adding to total_res
        for point in points:
            temp_tile = self.tile_loc(point[0], point[1])
            total_res += temp_tile.res*weighted_dist
        
        # Calculating and returning average resistance
        return total_res/dist

    def add_CS(self, x: float, y: float, amp: float) -> None:
        """
        This function adds a current source to the grids dictionary

        Arguments:
            - x: The dimensional x coordinate of the source
            - y: The dimensional y coordinate of the source
            - amp: The amplitude of the source

        Returns nothing
        """

        if (x > self.width*self.tdim) or (y > self.height*self.tdim):
            print("Cannot add a current source outside the grid")
            return

        # Ensuring there is not already a current source there
        if (x, y) in self.current_sources:
            print("Cannot add another current source to the same location")
            print("Please delete the current source from ({x, y}) first or try a different location")
            return
        
        # Provided the current source is within the grid, add it to CS dictionary
        self.current_sources[(x, y)] = amp
    
    def remove_CS(self, x: float, y: float) -> None:
        """
        This function removes a current source from the dictionaty

        Arguments: 
            - x: The dimensional x coordinate of the source
            - y: The dimensional y coordinate of the source

        Retruns nothing
        """

        if (x, y) in self.current_sources:
            del self.current_sources[(x,y)]
        else:
            print("No current source to remove at this location")

    def calc_Ifield(self) -> None:
        """
        This function calculate the currents on each tile based on the
        current sources and the resistivities 

        Returns nothing
        """

        # Width parameter
        ap1 = 1100
        ap2 = 300
        ap3 = 3300

        # Looping through every tile to calculate voltage for each
        for tile in self.tiles:
            # Resetting tile currents to baseline
            tile.I = 3.3*10**(-10)

            for coord, amp in self.current_sources.items():
                d = self.calculate_distance(tile, coord) # Calculate distance
                temp_cond = 1 / self.ave_res(tile, coord, 30)
                partial_I = amp * (np.exp(-0.5 * (d * ap1 / temp_cond) ** 2) + 0.7  * np.exp(-0.5 * (d * ap2 / temp_cond) ** 2) - 0.6 * np.exp(-0.5 * (d * ap3 / temp_cond) ** 2)) / 130000

                tile.I += partial_I

    def plot_I_contour(self) -> None:
        """
        This function plots a contour plot of the currents magnitudes

        Returns nothing
        """
        tiles_2d = np.array(self.tiles).reshape((self.height,self.width))
        I_2d = [[obj.I for obj in row] for row in tiles_2d]

        plt.contourf(I_2d, cmap='viridis', levels = 25)
        plt.colorbar(label='Values')  # Add a colorbar
        plt.xlabel('Column Index')
        plt.ylabel('Row Index')
        plt.title('Contour Plot of I field from current sources')
        plt.show()

    def create_neurons_in_row(self, rows: list[int], num_neurons: list[int]) -> None:
        """
        This function adds a certain amount of neurons to every tile in a row.
        This function must be called for neuron related features to become functional.

        Arguments:
            - rows: Is a list containing the rows that neurons are to be added to
            - num_neurons: Is a list of equal length to rows, the index of num_neurons
            value is the row that the specific number of neurons are added to

        Returns nothing
        """
        # Ensures the length of rows and neurons are the same
        if len(rows) != len(num_neurons):
            raise ValueError("The lists 'rows' and 'num_neurons' must have the same size.")

        # Loops through tiles calling the create_group function from tile class
        for row, num_neurons in zip(rows, num_neurons):
            temp_row = self.get_row(row)
            for tile in temp_row:
                tile.create_group(num_neurons)

    def establish_connectivities(self, row1: int, row2: int, weight: float, prob: float) -> None:
        """
        This function establishes neural connectivities (synaptic connections)
        between neurons.

        Arguments:
            - row1: Is the row which delivers synaptic input
            - row2: Is the row which recieves synpatic input from row1
            - weight: Is the effective strength (in mV) of the synaptic input 
            from a neuron from row1 on a neuron from row2 
            - prob: Is the probability that a neuron from row1 will connect with
            a neuron from row2

        Returns nothing
        """

        tiles1 = self.get_row(row1)
        tiles2 = self.get_row(row2)
        for i in range(len(tiles1)):
            spike_boost = 'v_post += {}*mV'.format(weight)
            synapses = Synapses(tiles1[i].neuronG, tiles2[i].neuronG, on_pre=spike_boost)
            synapses.connect(condition='rand() < prob')
            self.net.add(synapses)

    def introduce_currents(self) -> None:
        """
        This function tranfers the natural current in a tile to an input
        current for a neuron group in the tile

        Returns nothing
        """
        for tile in self.tiles:
            tile.neuronG.I = tile.I * amp
            # print(tile.I)
    
    def create_network(self) -> None:
        """
        This function creates a network that can be simulatedd 

        Returns nothing
        """
        # Adding neuron group and spikemonitors to network
        for i, group in enumerate(self.tiles):
            spike_monitor = SpikeMonitor(group.neuronG, record=True)
            spike_monitor.add_attribute('old_spikes')
            spike_monitor.old_spikes = 0
            spike_monitor.add_attribute('sim_spikes')
            self.spike_monitors.append(spike_monitor)
            self.net.add(group.neuronG, spike_monitor)

    def simulate(self, duration) -> tuple[list[float]]: 
        """
        This function simualtes the neurons acting.

        Arguments: 
            duration: Is the time the simulation occurs for (default set to 10ms) 

        Returns a tuple containing two lists. The first a list of the number of 
        recorded spikes for each tile, the second a list of the number of recorded
        spikes per neuron for each tile
        """

        # Running sim
        self.net.run(duration*ms)

        # Displaying data
        spike_data = []
        spike_data_pn = []
        for i, spike_monitor in enumerate(self.spike_monitors):
            spike_monitor.sim_spikes = len(spike_monitor.t) - spike_monitor.old_spikes
            spike_monitor.old_spikes = len(spike_monitor.t)
            spike_data.append(spike_monitor.sim_spikes)
            spike_data_pn.append(spike_monitor.sim_spikes/(self.tiles[i].num_neurons))
        
        spike_array = np.reshape(spike_data, (self.height,self.width))
        spike_array_pn = np.reshape(spike_data_pn, (self.height,self.width))
        firing_rate_ps = spike_array_pn/(duration*0.001)
        
        return (spike_array,spike_array_pn,firing_rate_ps)
    
    def plot_FR_contour(self, fr_data: list[list[int]], plt_name: str) -> None:
        """
        This function plots a contour plot of the firing rate

        Arguments: 
            - fr_data: Is a list of the firing rates recorded in each tile
            - plt_name: Is the title of the plot and its file name

        Returns nothing
        """
        # Clearing any previous plors
        plt.clf()
        # Plotting contour
        plt.contourf(fr_data, levels=25)
        # Invert the y-axis
        plt.gca().invert_yaxis()

        # Plotting CS locations
        for coords, value in self.current_sources.items():
            temp_tile = self.tile_loc(coords[0],coords[1])
            plt.scatter(temp_tile.x, temp_tile.y, color='red', marker='o') 

        # Formatting
        max_val = np.max(fr_data)
        if max_val == 0:
            bounds = np.linspace(0,26,26)
        else:
            bounds = np.linspace(0,max_val,26)
        vals = np.linspace(0,25,25)
        plt.colorbar(label='Firing rate', boundaries=bounds,values=vals)  # Add a colorbar
        plt.xlabel('Column Index')
        plt.ylabel('Row Index')
        plt.title(f'{plt_name}')
        # plt.show()

        # Saving file
        direc = getcwd()
        plt.savefig(direc + f'/{plt_name}')

        # Saving data file
        savedData = np.array(fr_data)
        np.savetxt(f'{plt_name}.txt',savedData,fmt='%.2f',delimiter=', ')


