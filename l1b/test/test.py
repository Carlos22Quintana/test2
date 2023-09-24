## 5.1.5. Pass/fail criteria

from common.io.writeToa import readToa
import numpy as np
import matplotlib.pyplot as plt
from config import globalConfig
from config.l1bConfig import l1bConfig

# Check for all bands that the differences with respect to the output TOA (l1b_toa_) are <0.01% for at
# least 3-sigma of the points.
bands = ['VNIR-0','VNIR-1','VNIR-2','VNIR-3']
my_toa_path = r"C:\EODP\EODP_TER\EODP-TS-L1B\outputcarlos"
luss_toa_path = r"C:\EODP\EODP_TER\EODP-TS-L1B\output"
isrf_toa_path = r"C:\EODP\EODP_TER\EODP-TS-ISM\output"
l1b_toa = 'l1b_toa_'
l1b_toa_eq = 'l1b_toa_eq_'
ism_toa_isrf = 'ism_toa_isrf_'

for band in bands:

    # 1. Read LUSS
    luss_toa = readToa(luss_toa_path, l1b_toa + band + '.nc')

    # 2. Read your outputs
    my_toa = readToa(my_toa_path, l1b_toa + band + '.nc')
    my_toa_eq = readToa(my_toa_path, l1b_toa_eq + band + '.nc')

    # 3. Compare
    result = my_toa - luss_toa
    porcentaje = result/my_toa*100
    boolean_comparison = porcentaje < 0.01
    # np.unique(result/my_toa*100 < 0.01) #demasiado inentendible
    if boolean_comparison.size == np.count_nonzero(boolean_comparison):
        print("Yes, the differences with respect to the output TOA (", l1b_toa + band,") are <0.01% for at least 3-sigma of the points.")
    else:
        print("No!, the differences with respect to the output TOA (", l1b_toa + band,") are not all <0.01% for at least 3-sigma of the points.")


    #For the central ALT position, plot the restored signal (l1b_toa), and the TOA after the ISRF
    #(ism_toa_isrf). Explain the differences.

    # For restored I understand ours equalizated toa
    nlines_ALT = my_toa.shape[0]
    ALT_central_line = int(nlines_ALT/2)
    isrf_toa = readToa(isrf_toa_path, ism_toa_isrf + band + '.nc')

    # Ploting with Condition if we are equalizing or not

    if l1bConfig().do_equalization == True:
        plt.plot(my_toa_eq[ALT_central_line])
        plt.plot(isrf_toa[ALT_central_line])
        plt.xlabel('ACT pixel [-]')
        plt.ylabel('TOA [mW/m2/sr]')
        plt.title("Effect of equalization for " + band)
        plt.legend(['TOA LB1 with eq', 'TOA after the ISRF'])
        plt.savefig("l1b_plot_eq"+band+".png") #Save and show tiene que ser este orden porque si no peta
        plt.show() # Si no le pongo el show tambien peta
    else:
        plt.plot(my_toa[ALT_central_line])
        plt.plot(isrf_toa[ALT_central_line])
        plt.xlabel('ACT pixel [-]')
        plt.ylabel('TOA [mW/m2/sr]')
        plt.title("Effect of equalization for " + band)
        plt.legend(['TOA LB1 without eq', 'TOA after the ISRF'])
        plt.savefig("l1b_plot_no_eq" + band + ".png")
        plt.show()


