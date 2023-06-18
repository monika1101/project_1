import numpy as np
import sys
import argparse
from math import *

class Transformacje:
    def __init__(self, model: str):
        """
        Wybieramy jedną z podanych elipsoid: GRS80, WGS84, Krasowskiego.
        Następnie funkcja wykorzystuje ją do kolejnych obliczeń współrzędnych.

        Parameters
        ----------
                a - Dłuższa półoś elipsoidy. Wartość w metrach.
                b - Krótsza półoś elipsoidy. Wartość w metrach.
                e2 - Pierwszy mimośród w potędze 2. Wartość jest liczbą, nie ma jednostki.
        model : STR
            Wybrana elipsoida. Wartość możliwa: "GRS80", "WGS84", "Krasowskiego".
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
    
    def XYZ2flh(self, X, Y, Z):
        """
        Funkcja oblicza Algorytm Hirvonena. Jest to tranformacja współrzędnych ortokartezjańskich (X,Y,Z)
        na współrzędne geodezyjne: szerokość geodezyjną i długość geodezyjną oraz wysokość elipsoidalną (φ,λ,h)
        W wyniku procesu iteracyjnego danych, można otrzymać współrzędne z dokładnością ok. 1 cm.

        Parameters
        ----------
        X, Y, Z : FLOAT
                  Współrzędne w układzie  ortokartezjańskim. Wartość należy podać w metrach.
                  
        Returns
        -------
        Kolejność wyników: szerokość geod.(φ), długość geod.(λ), wysokość elips.(h)
        Jednostki wyników:    radiany             radiany             metry

        """
        p = np.sqrt(X**2 + Y**2)
        f = np.arctan(Z / (p * (1 - self.e2)))
        while True:
            N = self.a / np.sqrt(1 - self.e2 * np.sin(f)**2)
            h = (p / np.cos(f)) - N
            fs = f
            f = np.arctan(Z / (p * (1 - ((self.e2 * N )/ (N + h)))))
            if np.abs(fs - f) < (0.000001/206265):
                break
        l = np.arctan2(Y, X)
        return(f, l, h)
    
    def flh2XYZ(self, f, l, h):
        """
        Funkcja odwrotna do Algorytmu Hirvonena. Trasformacja polega na przejsciu z
        współrzędnych geodezyjnych: szerokosci  i długosci geodezyjnej oraz wysokosci elipsoidalnej (φ,λ,h)
        na współrzędne ortokartezjańskie (X,Y,Z).

        Parameters
        ----------
        f : FLOAT
            Szerokość geodezyjna(φ). Wartość należy podać w radianach.
        l : FLOAT
            Długość geodezyjna(λ). Wartość należy podać w radianach.
        h : FLOAT
            Wysokość elipsoidalna(h). Wartość należy podać w metrach.
        

        Returns
        -------
        Kolejność wyników: współrzędna X, współrzędna Y, współrzędna Z
        Jednostki wyników:    metry          metry           metry

        """
        N = self.a / np.sqrt(1 - self.e2 * np.sin(f)**2)
        X = (N + h) * np.cos(f) * np.cos(l)
        Y = (N + h) * np.cos(f) * np.sin(l)
        Z = (N * (1 - self.e2) + h) * np.sin(f)
        return(X, Y, Z)
    
    def xyz2neu(self, X, Y, Z, fa, la):
        """
        Funkcja przelicza przyrosty pomiędzy dwoma punktami z współrzędnych ortokartezjańskich (ΔXYZ)
        na przyrosty we współrzędnych topocenrycznych (Δneu).

        Parameters
        ----------
        X, Y, Z : FLOAT
            Współrzędne środka układu w układzie ortokartezjańskim. Wartość należy podać w metrach.
        fa : FLOAT
            Szerokość geodezyjna(φ). Wartość należy podać w radianach.
        la : FLOAT
            Długość geodezyjna(λ). Wartość należy podać w radianach.

        Returns
        -------
        Współrzędne topocentryczne (neu) . 
        Jednostka: metry.

        """
        R = np.array([[-np.sin(fa) * np.cos(la), -np.sin(la), np.cos(fa) * np.cos(la) ],
                                   [-np.sin(fa) * np.sin(la), np.cos(la), np.cos(fa) * np.sin(la)],
                                   [np.cos(fa), 0, np.sin(fa)]])
        NEU = np.dot(R, np.array([X,Y,Z]))
        n = NEU[0]
        e = NEU[1]
        u = NEU[2]
        return(n,e,u)
    
    def fl2PL2000(self, f, l, m0=0.999923):
        """
        Funkcja przelicza współrzędne geodezyjne: szerokość geodezyjną
        i długość geodezyjną oraz wysokość elipsoidalną (φ,λ,h) na współrzędne płaskie
        w układzie PL-2000 (X,Y). Układ PL-2000 jest układem płaskim, prostokątnym opartym 
        na odwzorowaniu Gaussa-Krugera. Wyróżnia się w nim 4 strefy o nr 5, 6, 7, 8, którym kolejno
        odpowiadają południki miejscowe: 15°E, 18°E, 21°E, 24°E.

        Parameters
        ----------
        f : FLOAT
            Szerokość geodezyjna(φ). Wartość należy podać w radianach.
        l : FLOAT
            Długość geodezyjna(λ). Wartość należy podać w radianach.
        

        Returns
        -------
        Kolejność wyników: współrzędna X (PL-2000), współrzędna Y (PL-2000)
        Jednostki wyników:         metry                    metry

        """
        L = l * 180/pi
        if 13.5 <= L <=  16.5:
            l0 = radians(15)
            ns = 5
        elif 15.5 < L <=  19.5:
            ns = 6
            l0 = radians(18)
        elif 19.5 < L <=  22.5:
            ns = 7
            l0 = radians(21)
        elif 22.5 < L <=  25.5:
            ns = 8
            l0 = radians(24)
        else:
            print('Wartość współrzędnej nie mieści się w zakresie')
            return(0.0,0.0)
        b2 = (self.a**2)* (1 - self.e2)
        e22 = (self.a**2 - b2)/b2
        delta = l - l0
        t = np.tan(f)
        ni2 = e22 * (np.cos(f))**2
        N = self.a / np.sqrt(1 - self.e2 * np.sin(f)**2)
        A0 = 1 - (self.e2/4) - ((3*(self.e2)**2)/64) - ((5*(self.e2)**3)/256)
        A2 = (3/8) * (self.e2 + (self.e2**2/4) + ((15*(self.e2)**3)/128))
        A4 = (15/256) * ((self.e2)**2 + ((3*(self.e2)**3)/4))
        A6 = (35*self.e2**3)/3072
        s = self.a * (A0*f - A2*np.sin(2*f) + A4*np.sin(4*f) - A6*np.sin(6*f))
        xgk = s + (delta**2/2) * N * np.sin(f)*np.cos(f)*(1 + (delta**2/12)*np.cos(f)**2*(5 - t**2 + 9*ni2 + 4*ni2**2)+ ((delta**4)/360)*np.cos(f)**4*(61 - 58*t**2 + t**4 + 270*ni2 - 330*ni2*t**2))
        ygk = delta*N*np.cos(f)*(1+(delta**2/6)*np.cos(f)**2*(1 - t**2 + ni2) + (delta**4/120)*np.cos(f)**4*(5 - 18*t**2 + t**4 + 14*ni2 - 58*ni2*t**2))
        x2000 = xgk * m0
        y2000 = ygk * m0 + ns * 1000000 + 500000
        return(x2000, y2000)
    
    def fl2PL1992(self, f, l, m0=0.9993):
        """
        Funkcja przelicza współrzędne geodezyjne: szerokość geodezyjną
        i długość geodezyjną oraz wysokość elipsoidalną (φ,λ,h) na współrzędne płaskie
        w układzie PL-1992 (X,Y). Układ PL-1992 jest układem płaskim, prostokątnym opartym 
        na odwzorowaniu Gaussa-Krugera, gdzie początkiem układu jest południk miejscowy 19°E.

        Parameters
        ----------
        f : FLOAT
            Szerokość geodezyjna(φ). Wartość należy podać w radianach.
        l : FLOAT
            Długość geodezyjna(λ). Wartość należy podać w radianach.

        Returns
        -------
        Kolejność wyników: współrzędna X (PL-1992), współrzędna Y (PL-1992)
        Jednostki wyników:         metry                    metry

        """
        
        l0 = radians(19)
        b2 = (self.a**2)* (1 - self.e2)
        e22 = (self.a**2 - b2)/b2
        delta = l - l0
        t = np.tan(f)
        ni2 = e22 * (np.cos(f))**2
        N = self.a / np.sqrt(1 - self.e2 * np.sin(f)**2)
        A0 = 1 - (self.e2/4) - ((3*(self.e2)**2)/64) - ((5*(self.e2)**3)/256)
        A2 = (3/8) * (self.e2 + (self.e2**2/4) + ((15*(self.e2)**3)/128))
        A4 = (15/256) * ((self.e2)**2 + ((3*(self.e2)**3)/4))
        A6 = (35*self.e2**3)/3072
        s = self.a * (A0*f - A2*np.sin(2*f) + A4*np.sin(4*f) - A6*np.sin(6*f))
        xgk = s + (delta**2/2) * N * np.sin(f)*np.cos(f)*(1 + (delta**2/12)*np.cos(f)**2*(5 - t**2 + 9*ni2 + 4*ni2**2)+ ((delta**4)/360)*np.cos(f)**4*(61 - 58*t**2 + t**4 + 270*ni2 - 330*ni2*t**2))
        ygk = delta*N*np.cos(f)*(1+(delta**2/6)*np.cos(f)**2*(1 - t**2 + ni2) + (delta**4/120)*np.cos(f)**4*(5 - 18*t**2 + t**4 + 14*ni2 - 58*ni2*t**2))
        ns = radians(19)
        x92 = xgk * m0 - 5300000
        y92 = ygk * m0 + 500000
        return(x92, y92)
    
    def rad2deg(f):
        """
        Funkcja zamienia wartość z miary radianowej na miarę stopniową.

        Parameters
        ----------
        f : FLOAT
            Wartość do przeliczenia. Wartość należy podać w radianach.
        Returns
        -------
        Wartość w stopniach --> h, min, s.

        """
        f = f * 180/pi
        d = int(f)
        m = int((f - d) * 60)
        s = (f - d - m/60) * 3600
        st = f'\n {d:3d}°{m:2d}’{s:7.5}”'
        return(st)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('plik', help="Plik z danymi")
    parser.add_argument('wyniki', help="Plik wyjsciowy")
    
    print('Wpisz cyfrę przypisaną do wybranej elipsoidy:')
    print("1. WGS84")
    print("2. GRS80")
    print("3. Krasowskiego")    
    while True :
        try :
            option = int(input())
            if (option < 1 or option > 3) :
                raise ValueError
            else:
                break
        except ValueError :
            print("Wybrana wartość nie istnieje.")

    model = ""
    if option == 1:
        model = "WGS84"
        print("Model: ", model)
    elif option ==2:
        model = "GRS80"
        print("Model: ", model)
    elif option ==3:
        model = "Krasowskiego"
        print("Model:", model)
    else:
        print("Nieprawidłowa wartość. Wybierz spośród 1-3.")
    print('Wpisz cyfrę odpowiedzialną za model transformacji:')
    print('1. XYZ na φ,λ,h')
    print('2. φ,λ,h na XYZ')
    print('3. XYZ na neu')
    print('4. φ,λ,h na PL-2000')
    print('5. φ,λ,h na PL-1992')
    
    while True :
        try :
            input_int = [int(x) for x in input().split()]

            if not input_int :
                raise ValueError

            for x in input_int :
                if x < 1 or x > 5 :
                    raise ValueError
            break
        except ValueError:
            print("Wybrana metoda nie istnieje. Wybierz spośród 1-5.")
            
    methods = []

    for method in input_int :
        if method == 1:
            methods.append("XYZ2flh")
        if method == 2:
            methods.append("flh2XYZ")
        if method == 3:
            methods.append("xyz2neu")
        if method == 4:
            methods.append("fl2PL2000")
        if method == 5:
            methods.append("fl2PL1992")
        
        
    args = parser.parse_args()    
    wspolrzedne = Transformacje(model)
    
    try :
        f = open(args.plik, 'r')
    except IOError :
        print("Wybrany plik nie istnieje.")
        sys.exit(IOError)
    dane_wiersze = f.readlines()
    f.close()
    wsp = []

    try :
        for wiersz in dane_wiersze:
            wiersz = [float(el) for el in wiersz.split(',')]
            wsp.append(wiersz)

    except ValueError:
        print("Plik zawiera błędne dane.")

    # print(f'wczytane współrzędne: \n {wsp}')
    plik = open(args.wyniki, 'w')
    temp = []
    try :
        for wiersz in wsp:
            if 'XYZ2flh' in methods:
                temp = (wspolrzedne.XYZ2flh(wiersz[0], wiersz[1], wiersz[2]))
                plik.write(f'  {temp[0]:.5f}  {temp[1]:.5f}  {temp[2]:.5f}  ')
            if 'flh2XYZ' in methods:
                temp = (wspolrzedne.flh2XYZ(wiersz[0], wiersz[1], wiersz[2]))
                plik.write(f'  {temp[0]:.5f}  {temp[1]:.5f}  {temp[2]:.5f}  ')
            if 'fl2PL2000' in methods:
                temp = (wspolrzedne.fl2PL2000(wiersz[0], wiersz[1]))
                plik.write(f'  {temp[0]:.3f}  {temp[1]:.3f}  ')
            if 'fl2PL1992' in methods:
                temp = (wspolrzedne.fl2PL1992(wiersz[0], wiersz[1]))
                plik.write(f'  {temp[0]:.3f}  {temp[1]:.3f}  ')
            if 'xyz2neu' in methods:
                temp = (wspolrzedne.xyz2neu(wiersz[0], wiersz[1],wiersz[2],wiersz[3],wiersz[4]))
                plik.write(f'  {temp[0]:.5f}  {temp[1]:.5f}  {temp[2]:.5f}  ')
            plik.write('\n')
        print(f'wczytane współrzędne: \n {wsp}')
    except IndexError:
        print("Za mało zmiennych w wierszu. Podaj właciwą liczbe zmmienych dla wybranej transformacji")
    plik.close()
    
