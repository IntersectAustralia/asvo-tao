import math

def z2d(z, h=None, wm=None):
    """
    redshift calculator converts redshift into a distance using given little h.
    """
    n = 1000
    dz = z/n
    integral = 0
    c = 299792.458
    H0 = h*100.0
    WM = wm
    WV = 1.0 - WM # - 0.4165/(H0*H0)
    WR = 4.165E-5/(h*h)
    WK = 1-WM-WR-WV
    az = 1.0/(1+1.0*z)
    DTT = 0.0
    DCMR = 0.0
    for i in range(0, n):
        a = az+(1-az)*(i+0.5)/n
        adot = math.sqrt(WK+(WM/a)+(WR/(a*a))+(WV*a*a))
        DTT = DTT + 1.0/adot
        DCMR = DCMR + 1.0/(a*adot)
        
    DTT = (1.-az)*DTT/n
    DCMR = (1.-az)*DCMR/n
    d = (c/H0)*DCMR
    
    return d

if __name__ == "__main__":
    import doctest
    doctest.testmod()