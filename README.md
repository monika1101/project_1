# project_1
Próba README

 Program służy do przeliczania współrzędnych. Możliwe są transformacje pomiędzy układami:
- współrzędnych ortokartezjańskich na współrzędne geodezyjne;
- współczędnych geodezyjnych na współrzędne ortokartezjańskie;
- współrzędnych ortokartezjańskich na współrzędne toposferyczne;
- współrzędnych geodezyjnych na współrzędne płaskie w odwzorowaniu PL-2000;
- współrzędnych geodezyjnych na współrzędne płaskie w odwzorowaniu PL-1992;
Możliwy jest wybór przeliczania współrzędnych dla elipsoid GRS80, WGS84, Krasowskiego.
 Do poprawnego działania programu potrzebne są: 
- trzeba mieć zainstalowanego pythona w wersji 3.9;
-
 Program został napisany dla systemu operacyjnego Windows.
 Aby skorzystać z programu potrzeby jest plik z danymi w formacie txt.
Dane powinny być oddzielone przecinkami oraz zawierać współrzędne ortokartezjańskie w kolejności X,Y,Z.
Aby uruchomić program należy wejśc w zakładkę 'run' a następnie wybrać 'run configuration per file; (można również użyć skrótu Ctrl+F6). Następnie w ramce 'General settings' wkleić ścieżkę dostępu do pliku.
Plik wyjściowy zawiera obliczone współrzędne w kolejności:
współrzędne geodezyjne(φ,λ,h), współrzędne ortokartezjańskie(X,Y,Z),
współrzędne płaskie w układzie PL-2000(X,Y), współrzędne płaskie w układzie PL-1992(X,Y)

