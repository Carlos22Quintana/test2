from common.io.writeToa import readToa
import numpy as np
from config import globalConfig

# Compare outputs
bands = ['VNIR-0','VNIR-1','VNIR-2','VNIR-3']
my_toa_path = r"C:\EODP\EODP_TER\EODP-TS-L1B\outputcarlos"
luss_toa_path = r"C:\EODP\EODP_TER\EODP-TS-L1B\output"
l1b_toa = 'l1b_toa_'
for band in bands:

    # 1. Read LUSS
    my_toa = readToa(my_toa_path, l1b_toa + band + '.nc')
    print(my_toa[0])

    luss_toa = readToa(luss_toa_path, l1b_toa + band + '.nc')
    result = my_toa-luss_toa

    # 2. Read your outputs

    # 3. Compare
    porcentaje = result/my_toa*100
    boolean_comparison = porcentaje < 0.01
    # np.unique(result/my_toa*100 < 0.01) #demasiado inentendible
    if boolean_comparison.size == np.count_nonzero(boolean_comparison):
        print("Yes, the differences with respect to the output TOA (l1b_toa_) are <0.01% for at least 3-sigma of the points.")
    a = 2
