import sys
import matplotlib as mpl
mpl.use('Agg')
import pylab as plt
import numpy as np
from cosmocalc import cosmocalc

data = np.genfromtxt(sys.argv[1], delimiter=',', skip_header=1)

Hubble_h = 0.73

# # Cone.
# oangle =  60.0 * 60.0
# Min_redshift = 0.0
# Max_redshift = 0.15
# volume = (cosmocalc(Max_redshift, H0=Hubble_h*100.0)['VCM_Gpc3'] - cosmocalc(Min_redshift, H0=Hubble_h*100.0)['VCM_Gpc3']) * (1000.0**3.0) * (oangle/41252.96)

# Box.
# BoxSize = 62.5
BoxSize = 500.0
volume = (BoxSize/Hubble_h)**3.0

# set up figure
plt.figure()
ax = plt.subplot(111)

mi = -30.0
ma = -15.0
binwidth = 0.25
NB = (ma - mi) / binwidth

(counts, binedges) = np.histogram(data-1.85, range=(mi, ma), bins=NB)  # convert K-band AB to Vega

# Set the x-axis values to be the centre of the bins
xaxeshisto = binedges[:-1] + 0.5 * binwidth

# Cole et al. 2001 K band 2dFGRS LF
Cole_Phi = np.array([3.1315561E-03, 8.2625253E-03, 0.0000000E+00, 4.6483092E-03, 5.7576019E-03, 9.1649834E-03, 1.1232893E-02,
                     1.0536440E-02, 8.5763102E-03, 8.8181989E-03, 6.9448259E-03, 6.0896124E-03, 9.2596142E-03, 6.9631678E-03,
                     7.2867479E-03, 6.9923755E-03, 5.9844730E-03, 5.9305103E-03, 5.3865365E-03, 5.8525647E-03, 5.2373926E-03,
                     4.9635037E-03, 4.1801766E-03, 2.7171015E-03, 1.8800517E-03, 1.2136410E-03, 6.5419916E-04, 3.4594961E-04,
                     1.4771589E-04, 5.5521199E-05, 2.1283222E-05, 9.4211919E-06, 1.0871951E-06, 2.7923562E-07])
Cole_PhiErr = np.array([3.6377162E-03, 6.6833422E-03, 1.0000000E-10, 4.0996978E-03, 4.3155681E-03, 5.6722397E-03, 6.4211683E-03,
                        5.7120644E-03, 4.6346937E-03, 3.8633577E-03, 2.4383855E-03, 1.6279118E-03, 1.6941463E-03, 1.1781409E-03,
                        9.7785855E-04, 7.9027453E-04, 6.0649612E-04, 5.1598746E-04, 4.2267537E-04, 3.7395130E-04, 2.8177485E-04,
                        2.1805518E-04, 1.6829016E-04, 1.1366483E-04, 8.1871600E-05, 5.7472309E-05, 3.6554517E-05, 2.3141622E-05,
                        1.2801432E-05, 6.5092854E-06, 3.3540452E-06, 1.9559407E-06, 5.6035748E-07, 2.8150106E-07])
Cole_Mag = np.array([-18.00000, -18.25000, -18.50000, -18.75000, -19.00000, -19.25000, -19.50000, -19.75000, -20.00000,
                     -20.25000, -20.50000, -20.75000, -21.00000, -21.25000, -21.50000, -21.75000, -22.00000, -22.25000,
                     -22.50000, -22.75000, -23.00000, -23.25000, -23.50000, -23.75000, -24.00000, -24.25000, -24.50000,
                     -24.75000, -25.00000, -25.25000, -25.50000, -25.75000, -26.00000, -26.25000])

# Huang et al. 2003 K band Hawaii+AAO LF
Huang_Phi = np.array([0.0347093, 0.0252148, 0.0437980, 0.0250516, 0.00939655, 0.0193473, 0.0162743, 0.0142267, 0.0174460,
                      0.0100971, 0.0136507, 0.00994688, 0.00655286, 0.00528234, 0.00310017, 0.00157789, 0.000721131,
                      0.000272634, 8.33409e-05, 2.12150e-05, 3.97432e-06, 5.07697e-06, 5.42939e-07])
Huang_PhiErr = np.array([ 0.0249755, 0.0181685, 0.0161526, 0.0105895, 0.00479689, 0.00525068, 0.00428192, 0.00308970, 0.00248676,
                          0.00166458, 0.00166691, 0.00106289, 0.000704721, 0.000527429, 0.000340814, 0.000170548, 8.25681e-05,
                          3.81529e-05, 1.50279e-05, 6.16614e-06, 2.34362e-06, 1.98971e-06, 5.54946e-07])
Huang_Mag = np.array([-19.8000, -20.1000, -20.4000, -20.7000, -21.0000, -21.3000, -21.6000, -21.9000, -22.2000, -22.5000,
                      -22.8000, -23.1000, -23.4000, -23.7000, -24.0000, -24.3000, -24.6000, -24.9000, -25.2000,
                      -25.5000, -25.8000, -26.1000, -26.4000])

# Finally plot the observational data
plt.errorbar(Cole_Mag+5.0*np.log10(Hubble_h), Cole_Phi*Hubble_h*Hubble_h*Hubble_h, yerr=Cole_PhiErr*Hubble_h*Hubble_h*Hubble_h, color='m', lw=1.0, marker='o', ls='none', label='Cole et al. 2001')
plt.errorbar(Huang_Mag+5.0*np.log10(Hubble_h), Huang_Phi*Hubble_h*Hubble_h*Hubble_h, yerr=Huang_PhiErr*Hubble_h*Hubble_h*Hubble_h, color='g', lw=1.0, marker='o', ls='none', label='Huang et al. 2003')

# Overplot the model histograms
plt.plot(xaxeshisto, counts    / volume / binwidth, 'k-', label='Model - All')

plt.yscale('log', nonposy='clip')
plt.axis([-19.5, -27.5, 4.0e-7, 4.0e-2])

# Set the x-axis minor ticks
ax.xaxis.set_minor_locator(plt.MultipleLocator(0.1))

plt.ylabel(r'$\phi\ (\mathrm{Mpc}^{-3}\ \mathrm{mag}^{-1})$')  # Set the y...
plt.xlabel(r'$M_\mathrm{K}$')  # and the x-axis labels

leg = plt.legend(loc='lower left', numpoints=1, labelspacing=0.1)
leg.draw_frame(False)  # Don't want a box frame
for t in leg.get_texts():  # Reduce the size of the text
    t.set_fontsize('medium')

outputFile = 'luminosity_k.png'
plt.savefig(outputFile)  # Save the figure
