import numpy as np

class Transformacje:
    
    def Np(f, a, e2):
        """
        

        Parameters
        ----------
        f : TYPE
            DESCRIPTION.
        a : TYPE
            DESCRIPTION.
        e2 : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        
        N = a / np.sqrt(1 - e2 * np.sin(f)**2)
        return(N)
    def XYZ2flh(X, Y, Z, a, e2):
        """
        

        Parameters
        ----------
        X : TYPE
            DESCRIPTION.
        Y : TYPE
            DESCRIPTION.
        Z : TYPE
            DESCRIPTION.
        a : TYPE
            DESCRIPTION.
        e2 : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        p = np.sqrt(X**2 + Y**2)
        f = np.arctan(Z / (p * (1 - e2)))
        while True:
            N = Np(f, a, e2)
            h = (p / np.cos(f)) - N
            fs = f
            f = np.arctan(Z / (p * (1 - ((e2 * N )/ (N + h)))))
            if np.abs(fs - f) < (0.000001/206265):
                break
        l = np.arctan2(Y, X)
        return(f, l, h)
    def flh2XYZ(f, l, h, a, e2):
        """
        

        Parameters
        ----------
        f : TYPE
            DESCRIPTION.
        l : TYPE
            DESCRIPTION.
        h : TYPE
            DESCRIPTION.
        a : TYPE
            DESCRIPTION.
        e2 : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        N = Np(f, a, e2)
        X = (N + h) * np.cos(f) * np.cos(l)
        Y = (N + h) * np.cos(f) * np.sin(l)
        Z = (N * (1 - e2) + h) * np.sin(f)
        return(X, Y, Z)
    def xyz2neu(dX, fa, la):
        """
        

        Parameters
        ----------
        dX : TYPE
            DESCRIPTION.
        fa : TYPE
            DESCRIPTION.
        la : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        R = np.array([[-np.sin(fa) * np.cos(la), -np.sin(la), np.cos(fa) * np.cos(la) ],
                                   [-np.sin(fa) * np.sin(la), np.cos(la), np.cos(fa) * np.sin(la)],
                                   [np.cos(fa), 0, np.sin(fa)]])
        return(R.T @ dX)
    def fl2PL2000(f, l, l0, ns, a, e2, m0=0.999923):
        """
        

        Parameters
        ----------
        f : TYPE
            DESCRIPTION.
        l : TYPE
            DESCRIPTION.
        l0 : TYPE
            DESCRIPTION.
        ns : TYPE
            DESCRIPTION.
        a : TYPE
            DESCRIPTION.
        e2 : TYPE
            DESCRIPTION.
        m0 : TYPE, optional
            DESCRIPTION. The default is 0.999923.

        Returns
        -------
        None.

        """
        b2 = (a**2)* (1 - e2)
        e22 = (a**2 - b2)/b2
        delta = l - l0
        t = np.tan(f)
        ni2 = e22 * (np.cos(f))**2
        N = Np(f, a, e2)
        s = sigma(f, a, e2)
        xgk = s + (delta**2/2) * N * np.sin(f)*np.cos(f)*(1 + (delta**2/12)*np.cos(f)**2*(5 - t**2 + 9*ni2 + 4*ni2**2)+ ((delta**4)/360)*np.cos(f)**4*(61 - 58*t**2 + t**4 + 270*ni2 - 330*ni2*t**2))
        ygk = delta*N*np.cos(f)*(1+(delta**2/6)*np.cos(f)**2*(1 - t**2 + ni2) + (delta**4/120)*np.cos(f)**4*(5 - 18*t**2 + t**4 + 14*ni2 - 58*ni2*t**2))
        if ns == 5:
            l0 = radians(15)
        elif ns == 6:
            l0 = radians(18)
        elif ns == 7:
            l0 = radians(21)
        elif ns == 8:
            l0 = radians(24)
        x2000 = xgk * m0
        y2000 = ygk * m0 + ns * 1000000 + 500000
        return(x2000, y2000)
    def fl2PL1992(f, l, l0, a, e2, m0=0.9993):
        """
        

        Parameters
        ----------
        f : TYPE
            DESCRIPTION.
        l : TYPE
            DESCRIPTION.
        l0 : TYPE
            DESCRIPTION.
        a : TYPE
            DESCRIPTION.
        e2 : TYPE
            DESCRIPTION.
        m0 : TYPE, optional
            DESCRIPTION. The default is 0.9993.

        Returns
        -------
        None.

        """
        
        b2 = (a**2)* (1 - e2)
        e22 = (a**2 - b2)/b2
        delta = l - l0
        t = np.tan(f)
        ni2 = e22 * (np.cos(f))**2
        N = Np(f, a, e2)
        s = sigma(f, a, e2)
        xgk = s + (delta**2/2) * N * np.sin(f)*np.cos(f)*(1 + (delta**2/12)*np.cos(f)**2*(5 - t**2 + 9*ni2 + 4*ni2**2)+ ((delta**4)/360)*np.cos(f)**4*(61 - 58*t**2 + t**4 + 270*ni2 - 330*ni2*t**2))
        ygk = delta*N*np.cos(f)*(1+(delta**2/6)*np.cos(f)**2*(1 - t**2 + ni2) + (delta**4/120)*np.cos(f)**4*(5 - 18*t**2 + t**4 + 14*ni2 - 58*ni2*t**2))
        ns = radians(19)
        x92 = xgk * m0 - 5300000
        u92 = ygk * m0 + 500000
        return(x92, y92)

    
    