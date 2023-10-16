#4.2.5. Pass/fail criteria
import pandas as pd

from common.io.writeToa import readToa
from common.io.readMat import readMat
from common.io.readArray import readArray
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from config import globalConfig
from config.l1bConfig import l1bConfig

#Check for all bands that the differences with respect to the output TOA (ism_toa_) are <0.01% for at least 3-sigma of the points.

bands = ['VNIR-0','VNIR-1','VNIR-2','VNIR-3']
my_toa_path = r"C:\EODP\EODP_TER\EODP-TS-ISM\outputcarlos"
luss_toa_path = r"C:\EODP\EODP_TER\EODP-TS-ISM\output"

ism_toa_ = 'ism_toa_'

for band in bands:

    # 1. Read LUSS
    luss_toa = readToa(luss_toa_path, ism_toa_ + band + '.nc')

    # 2. Read your outputs
    my_toa = readToa(my_toa_path, ism_toa_ + band + '.nc')

    # 3. Compare
    result = my_toa - luss_toa
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
        print("Yes, the differences with respect to the output TOA (", ism_toa_ + band,
            ") are <0.01% for at least 3-sigma of the points.")
    else:
        print("No!, the differences with respect to the output TOA (", ism_toa_ + band,
            ") are not all <0.01% for at least 3-sigma of the points.")



    # For all bands, check whether there are any saturated pixels. Quantify the percentage of saturated
    # pixels per band.

    # Read final toa
    my_toa = readToa(my_toa_path, ism_toa_ + band + '.nc')

    number_saturated_values = np.sum(my_toa == 4095)
    porcentaje_saturated = number_saturated_values * 100 / my_toa.size
    print("The percentage of saturated values for", ism_toa_ + band,"is", "{:.2f}".format(porcentaje_saturated), "%.")
