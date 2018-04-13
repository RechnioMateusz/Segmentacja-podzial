# **Segmentacja - Metoda podziału**
__ __ __ __ __
__ __ __ __ __
### **Funkcjonalność**
__ __ __ __ __
Program służy do przeprowadzania segmentacji obrazów cyfrowych za pomocą metody podziału.
Program wykonuje następujące kroki:
* Import obrazu w postaci macierzy pikseli
* Rekurencyjne dzielenie macierzy na podmacierze w zależności od współczynników i tworzenie na ich podstawie drzewa czwórkowego
* Aktualizacja wartości pikseli w odpowiednich podmacierzach
* Eksport zaktualizowanego obrazu do pliku .jpg

### **Instalacja i uruchamianie (_windows_)**
__ __ __ __ __
Program jest napisany w języku [_Python ver. 3.6.5_](https://www.python.org/ftp/python/3.6.5/python-3.6.5.exe) z wykorzystaniem klasy _Image_ z biblioteki [_Pillow_](https://pillow.readthedocs.io/en/5.1.x/). Z tego powodu należy zainstalować w.w. bibliotekę za pomocą komendy:
- `pip install pillow`

[_W razie problemów z instalacją biblioteki Pillow_](https://pillow.readthedocs.io/en/5.1.x/installation.html)

Aby uruchomić program należy w konsoli przejść do folderu w którym zapisane są pliki źródłowe i użyć komendy:
- `python Segmentaion.py`

### **Instrukcja użytkowania**
__ __ __ __ __
Po uruchomieniu programu należy podać ścieżkę do pliku czyli obrazu cyfrowego. Ważne jest, aby obraz nie był monochromatyczny (przykładowo .jpg .png itd.).

![loading](https://github.com/RechnioMateusz/Segmentacja-podzial/blob/master/READMEimages/loading.jpg)

Po załadowaniu obrazu można wybrać:

![menu](https://github.com/RechnioMateusz/Segmentacja-podzial/blob/master/READMEimages/menu.jpg)

* Po wybraniu "_1_" program rozpocznie proces segmentacji
* Po wybraniu "_2_" można zmienić współczynnik "_alpha_"
* Po wybraniu "_3_" można zmienić wymiary najmniejszej możliwej podmacierzy
* Po wybraniu "_4_" można zmienić poziom drzewa od którego rozpocznie się sprawdzanie spójności podmacierzy
* Po wybraniu "_8_" można zaimportować nowy obraz
* Po wybraniu "_9_" można przeładować obraz
* Po wybraniu "_0_" program zakończy działanie

### **Zasada działania i współczynniki**
__ __ __ __ __
Zasady określające logikę:
* O (_obszar_) = zbiór punktów obrazu R pozostających w relacji spójności
* R = R1 + R2 + ... + Rn (partycje)
* P = predykat logiczny (suma logiczna warunków)
* Każdy Ri<=>O powinien spełniać predykat logiczny P
* Dla żadnej pary przyległych Ri i Rj (gdy Ri<=>O ^ Rj<=>O) nie może być spełniony predykat logiczny P

Jeżeli dla dowolnego Ri nie jest spełniony predykat P to Ri jest dzielone na cztery podmacierze, które stają się dziećmi Ri.
Następnie dla każdego dziecka jest sprawdzany predykat P itd...
Jeżeli dla dowolnego Ri spełniony jest predykat P to Ri staje się obszarem O i przestaje być dalej dzielony.



Współczynniki definiujące predykat logiczny P:
* _alpha_ - określa akceptowalny przedział odchylenia wartości piksela od średniego koloru partycji Ri (ustala spójność podmacierzy)
* najmniejsza możliwa podmacierz - wysokość i szerokość najmniejszej dopuszczalnej podmacierzy
* początkowa wysokość drzewa - wysokość drzewa od której rozpoczyna się sprawdzanie spójności podmacierzy, przed nią następuje tylko podział

### **Licencja**
__ __ __ __ __
>**_MIT License_**
>
>_Copyright (c) 2018 Mateusz Rechnio_
>
>_Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:_
>
>_The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software._
>
>_THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE._

### **Przeiwdywane zmiany i rozwój**
Przewiduje się rozbudowanie użytej metody segmentacji o dodanie metody łączenia.
Pewnym jest poprawienie kodu, szczególnie w pliku [_TreeConfiguration.py_](https://github.com/RechnioMateusz/Segmentacja-podzial/blob/master/TreeConfiguration.py)