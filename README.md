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
     - pobrane biblioteki: numpy, math, sys, argparse.

+ Program został napisany dla systemu operacyjnego Windows.
+ Aby skorzystać z programu potrzebny jest plik z danymi w formacie txt.

#JAK PRZYGOTOWAĆ PLIK DO WCZYTANIA DANYCH?
  + Dane w pliku powinny być oddzielone przecinkami, separatorem powinna być kropka oraz zawierać współrzędne ortokartezjańskie w kolejności X,Y,Z w metrach lub współrzędne geodezyjne(φ,λ) w radianach oraz wysokość (h) i metrach. 
  + W pliku do przeliczania na wspórzędne topocentryczne (N,E,U) należy podać 5 pozycji w wierszu z czego pierwsze 3 to współrzędne ortokartezjńskie środka układu w metrach a ostatnie dwa to współrzędne punktu przeliczanego (φ,λ) w radianach.
  + Pliki do przelicznia między współrzędnymi ortokartezjańskimi a układami PL-1992 lub PL-2000 powinny zawierać 2 wartości przeliczanych współrzędnych geodezyjnych w wierszu.
  + Plik do przeliczania między współrzędnymi ortokartezjańskimi a układem współrzędnych geodezyjnych powinien zawierać 3 wartości przeliczanych współrzędnych ortokartezjańskich w wierszu.
  + Plik do przeliczania między współrzędnymi geodezyjnymi a układem współrzędnych ortokartezjańskich powinien zawierać 3 wartości przeliczanych współrzędnych geodezyjnych w wierszu.

#SPRAWDZONY SPOSÓB WCZYTANIA DANYCH.
  1) Należy otworzyć Wiersz polecenia oraz otworzyć ścieżkę do dostępu do programu za pomocą funkcji: cd ścieżka_folderu
  2) Następnie aby wykonać transformację należy wpisać: python nazwa_skryptu.txt nazwa_pliku_z_danymi.txt nazwa_pliku_wynikowego.txt
  3) Przykładowe wywołanie: python Skrypt_1.py wsp_kopia.txt Wyniki.txt
  4) Pojawi się wybór pomiędzy dostępnymi elipsoidami odniesienia, należy wpisać do wiersza poleceń numer jej odpowiadający,
  5) Następnie pojawi się wybór pomiędzy dostępnymi transformacjami, należy wpisać wybraną cyfę odpowiadającą transformacji,
  6) W folderze zawierającym program pojawi się plik wynikowy o wybranej przez użytkownika nazwie.
  
#REZULTATY WCZYTANIA DANYCH.
  + Po wczytaniu danych utworzy się plik wyjściowy o nazwie wybranej przez użytkownia z rozszerzeniem txt , który jest raportem z wynikami. Wyniki są oddzielone dwoma spacjami od siebie.
  + Raport zawiera w zależności od wybranej transformacji następujące dane:
      - współrzędne geodezyjne(φ,λ,h) w radianach jeśli została wybrana transformacja XYZ na φ,λ,h,
      - współrzędne ortokartezjańskie(X,Y,Z) w metrach jeśli została wybrana transformacja φ,λ,h na XYZ,
      - współrzędne płaskie w układzie PL-2000(X,Y) w metrach jeśli została wybrana transformacja φ,λ,h na PL-2000,
      - współrzędne płaskie w układzie PL-1992(X,Y)w metrach jeśli została wybrana transformacja φ,λ,h na PL-1992,
      - wspórzędne topocentryczne (n, e, u) w metrach jeśli została wybrana transformacja XYZ na neu.

  #ZNANE BŁĘDY
  1) Transformacja z użyciem elipsoidy krasowskiego na układ PL-2000 lub 1992 zwraca błędne wyniki więc nie powinna być stosowana.
  
