
# MAIN FUNCTION TO CALL THE L1B MODULE

from l1b.src.l1b import l1b

# Directory - this is the common directory for the execution of the E2E, all modules
auxdir = r'C:\EODP\auxiliary'
indir = r"C:\EODP\EODP_TER\EODP-TS-E2E\sgm_out_carlos"
outdir = r"C:\EODP\EODP_TER\EODP-TS-E2E\l1b_out_carlos"

# Initialise the ISM
myL1b = l1b(auxdir, indir, outdir)
myL1b.processModule()
