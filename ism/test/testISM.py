#4.1.5. Pass/fail criteria
import pandas as pd

from common.io.writeToa import readToa
from common.io.readMat import readMat
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from config import globalConfig
from config.l1bConfig import l1bConfig

#Check for all bands that the differences with respect to the output TOA (ism_toa_isrf) are <0.01% for at least 3-sigma of the points.

bands = ['VNIR-0','VNIR-1','VNIR-2','VNIR-3']
my_toa_path = r"C:\EODP\EODP_TER\EODP-TS-ISM\outputcarlos"
luss_toa_path = r"C:\EODP\EODP_TER\EODP-TS-ISM\output"

ism_toa_isrf = 'ism_toa_isrf_'
ism_toa_optical = 'ism_toa_optical_'
Hdiff = 'Hdiff_'
Hdefoc = 'Hdefoc_'
Hwfe = 'Hwfe_'
Hdet = 'Hdet_'
Hsmear = 'Hsmear_'
Hmotion = 'Hmotion_'
Hsys = 'Hsys_'

for band in bands:

    # 1. Read LUSS
    luss_toa = readToa(luss_toa_path, ism_toa_isrf + band + '.nc')

    # 2. Read your outputs
    my_toa = readToa(my_toa_path, ism_toa_isrf + band + '.nc')

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
        print("Yes, the differences with respect to the output TOA (", ism_toa_isrf + band,
            ") are <0.01% for at least 3-sigma of the points.")
    else:
        print("No!, the differences with respect to the output TOA (", ism_toa_isrf + band,
            ") are not all <0.01% for at least 3-sigma of the points.")

    # Check for all bands that the differences with respect to the output TOA (ism_toa_optical) are <0.01%
    # for at least 3-sigma of the points.

    # 1. Read LUSS
    luss_toa = readToa(luss_toa_path, ism_toa_optical + band + '.nc')

    # 2. Read your outputs
    my_toa = readToa(my_toa_path, ism_toa_optical + band + '.nc')

    # 3. Compare
    result = my_toa - luss_toa
    porcentaje = result / my_toa * 100
    df = pd.DataFrame(porcentaje)
    porcentaje_df = df.fillna(0)  # The division per zero gives some annoying NaN values
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
        print("Yes, the differences with respect to the output TOA (", ism_toa_optical + band,
                  ") are <0.01% for at least 3-sigma of the points.")
    else:
        print("No!, the differences with respect to the output TOA (", ism_toa_optical + band,
                  ") are not all <0.01% for at least 3-sigma of the points.")

    # What is the radiance to irradiance conversion factor for each band. What are the units of the TOA at this stage.

    # Plot for all bands the System MTF across and along track (for the central pixels). Report the MTF at
    # the Nyquist frequency. Explain whether this is a decent or mediocre value and why

    # Read your outputs
    my_Hdiff = readMat(luss_toa_path, Hdiff + band + '.nc')
    #fnAct: 1D normalised frequencies 2D ACT (f/(1/w))

    nlines_ALT = my_toa.shape[0]
    ALT_central_line = int(nlines_ALT / 2)
    #nlines_ACT = my_toa.shape[1]
    #ALC_central_line = int(nlines_ALT / 2)

    plt.plot(my_Hdiff[ALT_central_line])
    plt.xlabel('ACT pixel [-]')
    plt.ylabel('TOA [mW/m2/sr]')
    plt.title("Effect of equalization for " + band)
    plt.show()
    A=2

    #plt.plot(my_toa[ALT_central_line])
    #plt.plot(isrf_toa[ALT_central_line])
    #plt.xlabel('ACT pixel [-]')
    #plt.ylabel('TOA [mW/m2/sr]')
    #plt.title("Effect of equalization for " + band)
    #plt.legend(['TOA LB1 with eq', 'TOA after the ISRF'])
    #plt.savefig("l1b_plot_eq" + band + ".png")  # Save and show tiene que ser este orden porque si no peta
    #plt.show()  # Si no le pongo el show tambien peta



