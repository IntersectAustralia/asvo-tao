import sys, re, math
from calc_kcor import calc_kcor
from calc_z2d import z2d

h = 0.73  # Little h used in the SED module
n = 10    # number of lines to output

required_fields = {'z':     'redshift_cosmological', 
                   'd':     'distance', 
                   'b_abs': 'johnson/johnson_b.dati_absolute', 
                   'b_app': 'johnson/johnson_b.dati_apparent',
                   'r_app': 'johnson/rfilter.dati_apparent'}

csv_delimiter = ', '

if len(sys.argv) < 2:
    print
    print "usage:"
    print "      python test-dm.py <input catalogue>"
    print
    print "      note: input catalogue must be in CSV format and must contain:"
    for field in required_fields:
        print "            %s" % required_fields[field]
    print
    sys.exit()

inputfile = sys.argv[1]
data = open(inputfile, "r")
header = data.readline()
headers = header.split(csv_delimiter)

ids = {}
for field in required_fields:
    if required_fields[field] in headers:
        ids[field] = headers.index(required_fields[field])

if len(ids) != len(required_fields):
   print "can't find all required fields in the catalogue."
   sys.exit()

print "   z(TAO)          d(TAO)           d(z)            d(DM)      diff %"
for i in range(0,n):
    line = data.readline()
    values = line.split(csv_delimiter)
    z      = float(values[ids['z']])
    d      = float(values[ids['d']])
    b_abs  = float(values[ids['b_abs']])
    b_app  = float(values[ids['b_app']])
    r_app  = float(values[ids['r_app']])

    d_z    = z2d(z, 1)  # [Mpc/h]
    color  = b_app - r_app
    k_corr = calc_kcor('B', z, 'B - Rc', color)
    dm     = b_app - b_abs - k_corr # distance modulus
    d_lum  = math.pow(10, 0.2*dm + 1)/1e6  # luminosity distance [Mpc]
    d_m    = h*d_lum/(1+z)  # co-moving distance [Mpc/h]
    diff   = 100*d_m/d - 100; # %
    print "%e\t%e\t%e\t%e\t%.2f" % (z, d, d_z, d_m, diff)
