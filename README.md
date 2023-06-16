# project_1

#CZYM ZAJMUJE SIĘ PROGRAM?
+ Program służy do przeliczania współrzędnych. Możliwe są transformacje pomiędzy układami:
    - współrzędnych ortokartezjańskich na współrzędne geodezyjne;
    - współrzędnych geodezyjnych na współrzędne ortokartezjańskie;
    - współrzędnych ortokartezjańskich na współrzędne topocentryczne;
    - współrzędnych geodezyjnych na współrzędne płaskie w odwzorowaniu PL-2000;
    - współrzędnych geodezyjnych na współrzędne płaskie w odwzorowaniu PL-1992.
+ Możliwy jest wybór przeliczania współrzędnych dla elipsoid GRS80, WGS84, Krasowskiego.

#CO JEST POTRZEBNE, ABY PROGRAM ZADZIAŁAŁ?
+ Do poprawnego działania programu potrzebne są: 
     - zainstalowany python w wersji 3.9 (w takiej wersji został napisany program);
     - pobrane biblioteki: numpy, datetime, math, argparse.

+ Program został napisany dla systemu operacyjnego Windows.
+ Aby skorzystać z programu potrzebny jest plik z danymi w formacie txt.

#JAK PRZYGOTOWAĆ PLIK DO WCZYTANIA DANYCH?
  +  Dane w pliku powinny być oddzielone przecinkami, separatorem powinna być kropka oraz zawierać współrzędne ortokartezjańskie w kolejności X,Y,Z w metrach lub współrzędne geodezyjne(φ,λ,h) w radianach. 
  +  W pliku do przeliczania na wspórzędne topocentryczne (N,E,U) należy podać 8 pozycji w wierszu z czego pierwsze 6 to współrzędne xyz 2 punktów do przelicznia w metrach a ostatnie dwa to współrzędne punktu środkowego φ,λ w radianach. Współrzędne powinny być oddzielone przecinkami, separator to kropka oraz powinny znajdować się w wym samym wierszu.
  
#SPRAWDZONY SPOSÓB WCZYTANIA DANYCH.
?
  + Wczytanie danych do programu Spyder (Python 3.9) odbyło się za pomocą zakładki 'Run', podpunktu 'Run configuration per file' -->(można również użyć skrótu Ctrl+F6).
     Następnie należało w ramce 'General settings' wkleić ścieżkę dostępu do pliku i zatwierdzić 'Run'.
     Ta opcja została wybrana, ponieważ wczytanie nazwy ścieżki bądź nazwy pliku do konsoli w Spyderze generowało błąd:  NameError: name 'wsp_kopia' is not defined. 
  
#REZULTATY WCZYTANIA DANYCH.
 + Po wczytaniu danych utworzy się plik wyjściowy o nazwie wyniki.txt, który jest raportem z wynikami. Wyniki są oddzielone dwoma spacjami od siebie.
 + Raport zawiera w zależności od wybranej transformacji następujące dane:
      + współrzędne geodezyjne(φ,λ,h) w radianach jeśli została wybrana fransformacja XYZ2flh
      + współrzędne ortokartezjańskie(X,Y,Z) w metrach jeśli została wybrana fransformacja flh2XYZ
      + współrzędne płaskie w układzie PL-2000(X,Y) w metrach jeśli została wybrana fransformacja fl2PL2000
      + współrzędne płaskie w układzie PL-1992(X,Y)w metrach jeśli została wybrana fransformacja fl2PL1992
      + wspórzędne topocentryczne (N,E,U) w metrach jeśli została wybrana fransformacja xyz2NEU.
 
  
  #POZOSTAŁE WAŻNE INFORMACJE
 -
  
  #ZNANE BŁĘDY
?
  1) Wczytanie nazwy ścieżki bądź nazwy pliku do konsoli w Spyderze generuje błąd:  NameError: name 'wsp_proba' is not defined. 
     Problem ten nie został naprawiony, ale znaleziono obejście problemu ( czyt. SPRAWDZONY SPOSÓB WCZYTANIA DANYCH)
?
  2) Transformacja z użyciem elipsoidy krasowskiego na układ PL-2000 lub 1992 zwraca błędne wyniki więc nie powinna być stosowana.
  