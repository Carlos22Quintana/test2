## 6.1.5. Pass/fail criteria

from common.io.writeToa import readToa
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from config import globalConfig
from config.l1bConfig import l1bConfig

# Check for all bands that the differences with respect to the output TOA (l1b_toa_) are <0.01% for at
# least 3-sigma of the points.
bands = ['VNIR-0','VNIR-1','VNIR-2','VNIR-3']
my_toa_path = r"C:\EODP\EODP_TER\EODP-TS-L1C\outputcarlos"
luss_toa_path = r"C:\EODP\EODP_TER\EODP-TS-L1C\output"
l1b_toa = 'l1c_toa_'

#Check for all bands that the differences with respect to the output TOA are <0.01% for 3-sigma of the points.

for band in bands:

    # 1. Read LUSS
    luss_toa = readToa(luss_toa_path, l1b_toa + band + '.nc')

    # 2. Read your outputs
    my_toa = readToa(my_toa_path, l1b_toa + band + '.nc')

    # 3. Compare
    result = np.sort(my_toa) - np.sort(luss_toa)
    porcentaje = result / my_toa * 100
    df = pd.DataFrame(porcentaje)
    porcentaje_df = df.fillna(0) # The division per zero gives some annoying NaN values
    boolean_comparison = np.array(porcentaje_df < 0.01)

    # Calculate the total number of values in each matrix
    total_values = boolean_comparison.size
    trues_matrix = np.full(boolean_comparison.shape, True)
    # Calculate the number of matching values (True values in the same positions)
    matching_values = np.sum(boolean_comparison == trues_matrix)
    # Calculate the threshold for 99.7% (3sigma) matching values
    threshold = 0.997 * total_values
    # Apply threshold to the matching values
    is_3sigma = matching_values >= threshold

    if is_3sigma == True:
        print("Yes, the differences with respect to the output TOA (", l1b_toa + band,
            ") are <0.01% for at least 3-sigma of the points.")
    else:
        print("No!, the differences with respect to the output TOA (", l1b_toa + band,
            ") are not all <0.01% for at least 3-sigma of the points.")


    #Plot for all bands the L1C grid points and plot the georeferenced TOA (with Panoply). Verify that the grid points are equispaced, see Figure 6-3

    # I plot it inside l1c.py because I dont know how to take inside the toa the lon and latitude separetly

    a = 2