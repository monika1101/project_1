import numpy as np
import argparse

class Transformacje:
    def __init__(self, model: str = "WGS84"):
        """
        

        Parameters
        ----------
        model : str, optional
            DESCRIPTION. The default is "WGS84".

        Raises
        ------
        NotImplementedError
            DESCRIPTION.

        Returns
        -------
        None.

        """
        if model == "WGS84":
            self.a = 6378137.0 
            self.b = 6356752.31424518
            self.e2 = ((self.a)**2 - (self.b)**2)/(self.a)**2
        elif model == "GRS80":
            self.a = 6378137.0
            self.b = 6356752.3141
            self.e2 = 0.00669438002290
        elif model == "Krasowskiego":
            self.a = 6378245.0
            self.b = 6356583.800
            self.e2 = 0.00669342162296
        else:
            raise NotImplementedError(f"{model} model not implemented") 
        
    def Np(f, self):
        """
        

        Parameters
        ----------
        f : TYPE
            DESCRIPTION.
        self : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        
        N = self.a / np.sqrt(1 - self.e2 * np.sin(f)**2)
        return(N)
    
    def XYZ2flh(self, X, Y, Z):
        """
        

        Parameters
        ----------
        X, Y, Z : FLOAT
            Współrzęndne w układzie ortokartezjanskim
        
        Returns
        -------
        f
            długosć geodezyjna
        l
            szerokosć geodezyjna
        h: FLOAT
            wysokosć elipsoidalna [m]

        """
        
        p = np.sqrt(X**2 + Y**2)
        f = np.arctan(Z / (p * (1 - self.e2)))
        while True:
            N = Np(self, f)
            h = (p / np.cos(f)) - N
            fs = f
            f = np.arctan(Z / (p * (1 - ((self.e2 * N )/ (N + h)))))
            if np.abs(fs - f) < (0.000001/206265):
                break
        l = np.arctan2(Y, X)
        return(f, l, h)
    
    def flh2XYZ(f, l, h, self):
        """
        

        Parameters
        ----------
        f : TYPE
            DESCRIPTION.
        l : TYPE
            DESCRIPTION.
        h : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        N = Np(f, self)
        X = (N + h) * np.cos(f) * np.cos(l)
        Y = (N + h) * np.cos(f) * np.sin(l)
        Z = (N * (1 - self.e2) + h) * np.sin(f)
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
    
    def fl2PL2000(f, l, l0, self, m0=0.999923):
        """
        

        Parameters
        ----------
        f : TYPE
            DESCRIPTION.
        l : TYPE
            DESCRIPTION.
        l0 : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        b2 = (self.a**2)* (1 - self.e2)
        e22 = (self.a**2 - self.b2)/self.b2
        delta = l - l0
        t = np.tan(f)
        ni2 = e22 * (np.cos(f))**2
        N = Np(f, self)
        s = sigma(f, self)
        xgk = s + (delta**2/2) * N * np.sin(f)*np.cos(f)*(1 + (delta**2/12)*np.cos(f)**2*(5 - t**2 + 9*ni2 + 4*ni2**2)+ ((delta**4)/360)*np.cos(f)**4*(61 - 58*t**2 + t**4 + 270*ni2 - 330*ni2*t**2))
        ygk = delta*N*np.cos(f)*(1+(delta**2/6)*np.cos(f)**2*(1 - t**2 + ni2) + (delta**4/120)*np.cos(f)**4*(5 - 18*t**2 + t**4 + 14*ni2 - 58*ni2*t**2))
        ns = float(str(xgk)[0])
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
    
    def fl2PL1992(f, l, l0, self, m0=0.9993):
        """
        

        Parameters
        ----------
        f : TYPE
            DESCRIPTION.
        l : TYPE
            DESCRIPTION.
        l0 : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        
        b2 = (self.a**2)* (1 - self.e2)
        e22 = (self.a**2 - self.b2)/self.b2
        delta = l - l0
        t = np.tan(f)
        ni2 = e22 * (np.cos(f))**2
        N = Np(f, self)
        s = sigma(f, self)
        xgk = s + (delta**2/2) * N * np.sin(f)*np.cos(f)*(1 + (delta**2/12)*np.cos(f)**2*(5 - t**2 + 9*ni2 + 4*ni2**2)+ ((delta**4)/360)*np.cos(f)**4*(61 - 58*t**2 + t**4 + 270*ni2 - 330*ni2*t**2))
        ygk = delta*N*np.cos(f)*(1+(delta**2/6)*np.cos(f)**2*(1 - t**2 + ni2) + (delta**4/120)*np.cos(f)**4*(5 - 18*t**2 + t**4 + 14*ni2 - 58*ni2*t**2))
        ns = radians(19)
        x92 = xgk * m0 - 5300000
        u92 = ygk * m0 + 500000
        return(x92, y92)

if __name__ == '__main__':
    wspolrzendne = Transformacje(model = 'WGS84')
    X = 3664940.500
    Y = 1409153.590
    Z = 5009571.170
    phi, lam, h = wspolrzendne.XYZ2flh(X, Y, Z)
    print(phi, lam, h)
    
    