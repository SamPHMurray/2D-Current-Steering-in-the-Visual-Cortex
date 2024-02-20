# 2D-Current-Steering-in-the-Visual-Cortex
A model of the visual cortex which represents the changes in firing rates of neurons due to current steering.

The code represents a model of a 2 dimensional space of the V1 primary visual cortex. It utilises brian2 simualtor to simulate neurons. Specifically the goal of the model was to represent the effects of a process called current steering, on the changes in firing rates in the visual cortex. However the code can be used to model the effects of any electrical stimulation paradamigms in general.

The model was used to try and mimic current steering data from the following article...
Meikle, S.J., Hagan, M.A., Price, N.S.C. and Wong, Y.T. (2022). Intracortical current steering shifts the location of evoked neural activity. Journal of Neural Engineering, 19(3), p.035003. doi:https://doi.org/10.1088/1741-2552/ac77bf.
The processing of the data is not in this repository.

For starters this model contains 2 sub-models. They are extremely similar however one focuses on current steering in within a layer of the visual cortex (horizontal model) and one focuses on current steering between layers on the V1 visual cortex (vertical model).

Each model contains 5 files.
Spatial file: Contains 2 objects, a tile and a grid, these objects are where neurons, electrodes, and other valuable simulation paradigms can be established through their functions.
Create / set up file: This contains a couple of functions. These functions are used to simplify the process of setting up the simulation, they allow users to easily change neuron densities, neuron connections, the size of the 2D space they want to work with, the location of electrodes etc.
Main file: This main file uses the functions from create/set up to run a specific simulation with paramters that worked well to match the data I specifcally was dealing with, users can simply change values of variables in this file to easily simulate their own functions. This file ultimately produces a text file of the neural firing rates at different locations in the 2D space, as well as a contour plot of an image which visually represents this.

The next two files are just example files, they show how I processed the data so I could extrapolate meaning from it.
Process file: The process file takes the text files from multiple simulations and processes is it into a single text file, in this text file, only firing rates in between the electrodes are present (and not the firing rates in the whole grid).
data analysis file: In the data analysis file, the proccessed data was taken and so was the raw experimental data (which was also in a text file of the same format). It then plots them in ways which they can be compared easily.
Of these five files the only needed one is the spatial file, the other two were just for simplification of setting up the model and for readability of the set up and the results.
