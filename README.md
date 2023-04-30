# project_1
-> README
#CZYM ZAJMUJE SIĘ PROGRAM?
-> Program służy do przeliczania współrzędnych. Możliwe są transformacje pomiędzy układami:
    - współrzędnych ortokartezjańskich na współrzędne geodezyjne;
    - współczędnych geodezyjnych na współrzędne ortokartezjańskie;
    - współrzędnych ortokartezjańskich na współrzędne toposferyczne;
    - współrzędnych geodezyjnych na współrzędne płaskie w odwzorowaniu PL-2000;
    - współrzędnych geodezyjnych na współrzędne płaskie w odwzorowaniu PL-1992.
 -> Możliwy jest wybór przeliczania współrzędnych dla elipsoid GRS80, WGS84, Krasowskiego.

#CO JEST POTRZEBNE, ABY PROGRAM ZADZIAŁAŁ?
-> Do poprawnego działania programu potrzebne są: 
 - zainstalowany python w wersji 3.9 (w takiej wersji został napisany program);
 - pobrane biblioteki: numpy, datetime, math, argparse.
-> Program został napisany dla systemu operacyjnego Windows.
-> Aby skorzystać z programu potrzeby jest plik z danymi w formacie txt.

#JAK PRZYGOTOWAĆ PLIK DO WCZYTANIA DANYCH?
  -> Dane w pliku powinny być oddzielone przecinkami oraz zawierać współrzędne ortokartezjańskie w kolejności X,Y,Z. 
     W pliku należy podać co najmniej dwie pozycje (Uzasadnienie poniżej w POZOSTAŁYCH WAŻNYCH INFORMACJACH w pkt. 2).
  
#SPRAWDZONY SPOSÓB WCZYTANIA DANYCH.
  -> Wczytanie danych do programu Spyder (Python 3.9) odbyło się za pomocą zakładki 'Run', podpunktu 'Run configuration per file' -->(można również użyć skrótu Ctrl+F6).
     Następnie należało w ramce 'General settings' wkleić ścieżkę dostępu do pliku i zatwierdzić 'Run'.
     Ta opcja została wybrana, ponieważ wczytanie nazwy ścieżki bądź nazwy pliku do konsoli w Spyderze generowało błąd:  NameError: name 'wsp_kopia' is not defined. 
  
#REZULATATY WCZYTANIA DANYCH.
 -> Po wczytaniu danych utworzy się plik wyjściowy o nazwie Wyniki.txt, który jest raportem z wynikami. Wyniki są oddzielone pięcioma spacjami od siebie.
 -> Raport zawiera następujące dane:
   - tytuł
   - autora
   - datę generacji raportu
   - wyniki obliczeń programu w kolejności:
      + współrzędne geodezyjne(φ,λ,h)
      + współrzędne ortokartezjańskie(X,Y,Z)
      + współrzędne płaskie w układzie PL-2000(X,Y)
      + współrzędne płaskie w układzie PL-1992(X,Y)
      + wspórzędne toposferyczne (N,E,U).
 
  
  #POZOSTAŁE WAŻNE INFORMACJE
  1) Elipsoida WGS84 została ustawiona za automatyczną. Jeżeli użytkownik chce skorzystać z innej elipsoidy musi ją zmienić w kodzie w argumencie  "model". 
     W celu ułatwienia odnalezienia go w skrypcie, został wyróżniony pionowymi odstępani( # # #).
  2) Ze względu na to, że tranformacja ze współrzędnych ortokartezjańskich na współrzędne toposferyczne wymaga podania ΔXYZ do funkcji, ΔXYZ jest obliczona jako różnica pomiędzy kolejnymi podanymi współrzędnymi.
  
  #ZNANE BŁĘDY
  1) Wczytanie nazwy ścieżki bądź nazwy pliku do konsoli w Spyderze generuje błąd:  NameError: name 'wsp_proba' is not defined. 
     Problem ten nie został naprawiony, ale znaleziono obejście problemu ( czyt. SPRAWDZONY SPOSÓB WCZYTANIA DANYCH)
  
  