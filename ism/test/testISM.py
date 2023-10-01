#4.1.5. Pass/fail criteria
from common.io.writeToa import readToa
import numpy as np
import matplotlib.pyplot as plt
from config import globalConfig
from config.l1bConfig import l1bConfig

#Check for all bands that the differences with respect to the output TOA (ism_toa_isrf) are <0.01% for at least 3-sigma of the points.

bands = ['VNIR-0','VNIR-1','VNIR-2','VNIR-3']
my_toa_path = r"C:\EODP\EODP_TER\EODP-TS-ISM\outputcarlos"
luss_toa_path = r"C:\EODP\EODP_TER\EODP-TS-ISM\output"

ism_toa_isrf = 'ism_toa_isrf_'

for band in bands:

    # 1. Read LUSS
    luss_toa = readToa(luss_toa_path, ism_toa_isrf + band + '.nc')

    # 2. Read your outputs
    my_toa = readToa(my_toa_path, ism_toa_isrf + band + '.nc')