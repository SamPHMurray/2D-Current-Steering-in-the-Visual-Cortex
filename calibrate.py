import sys
sys.path.insert(0, '/home/sampii/.local/lib/python3.11/site-packages') # important to ensure python3.11 finds the correct packages

import numpy as np
import os
import sys
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseEvent
from machinevisiontoolbox import Image, CentralCamera

# Load the points from the text file
points_path = '/home/sampii/param/calibration_points.txt'
if not os.path.exists(points_path):
    print(f"Points file '{points_path}' not found.")
    sys.exit(1)

p = np.loadtxt(points_path, delimiter=',').T

cm = 0.01  # centimetre to metre conversion factor

P_calib = np.array([
    [ 0,  -12.2, 12.2],
    [ 0,   -6.2, 12.2],
    [ 0,  -12.2,  6.2],
    [ 0,   -6.2,  6.2],
    [ 6.2,  0,   12.2],
    [12.2,  0,   12.2],
    [ 6.2,  0,    6.2],
    [12.2,  0,    6.2]
]).T * cm  # calibration rig specs

# Compute the camera matrix
C, _ = CentralCamera.points2C(P_calib, p)
camera = CentralCamera.decomposeC(C)

print("\nCamera info:\n", camera)

# Save the intrinsic parameters 
data_dir = os.path.join(os.getcwd(), "param")
os.makedirs(data_dir, exist_ok=True)  # Create the directory if it doesn't exist
print("\nIntrinsic parameters:\n", camera.K)
file_name_intrinsic = os.path.join(data_dir, "intrinsic.txt")
np.savetxt(file_name_intrinsic, camera.K, delimiter=',')
print(f"Intrinsic parameters saved to {file_name_intrinsic}")

# extrinsic parameters
print("\nExtrinsic parameters:\n", repr(camera.pose))
