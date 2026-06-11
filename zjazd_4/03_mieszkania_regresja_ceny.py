import pandas as pd  # Importujemy bibliotekę pandas jako pd; służy do pracy z danymi tabelarycznymi, np. DataFrame i plikami CSV.
import numpy as np  # Importujemy bibliotekę numpy jako np; służy do obliczeń numerycznych, np. tworzenia zakresów liczbowych.
import matplotlib.pyplot as plt  # Importujemy moduł pyplot z matplotlib; będzie używany do tworzenia wykresów.
from scipy.stats import pearsonr  # Importujemy funkcję pearsonr, która oblicza korelację Pearsona oraz p-value.
from sklearn.linear_model import LinearRegression  # Importujemy model regresji liniowej z biblioteki scikit-learn.
from sklearn.model_selection import train_test_split  # Importujemy funkcję do dzielenia danych na zbiór treningowy i testowy.
from sklearn.metrics import r2_score  # Importujemy metrykę R2, która ocenia, jak dobrze model wyjaśnia zmienność danych.
from sklearn.metrics import mean_absolute_error  # Importujemy metrykę MAE, czyli średni błąd bezwzględny predykcji.
from sklearn.metrics import mean_squared_error  # Importujemy metrykę MSE, czyli średni błąd kwadratowy predykcji.


pd.set_option('display.max_columns', 150)  # Ustawiamy maksymalną liczbę wyświetlanych kolumn w pandas na 150.
pd.set_option("display.float_format", lambda x: f"{x:.3f}")  # Ustawiamy format wyświetlania liczb zmiennoprzecinkowych do 3 miejsc po przecinku.

print("=== START ANALIZY: REGRESJA CEN NIERUCHOMOŚCI ===")  # Wyświetlamy nagłówek informujący o rozpoczęciu analizy cen nieruchomości.
print("Wczytywanie danych...")  # Wyświetlamy komunikat informujący, że program zaczyna wczytywać dane.

url_openintro = "https://www.openintro.org/data/csv/ames.csv"  # Zapisujemy główny adres URL do pliku CSV ze zbiorem danych Ames.

url_zapasowy = "https://vincentarelbundock.github.io/Rdatasets/csv/openintro/ames.csv"  # Zapisujemy zapasowy adres URL, gdyby główne źródło nie działało.

try:  # Rozpoczynamy blok try, czyli próbujemy wykonać kod, który może zakończyć się błędem.
    df = pd.read_csv(  # Wczytujemy dane CSV do obiektu DataFrame o nazwie df.
        url_openintro,  # Podajemy główny adres URL, z którego mają zostać pobrane dane.
        storage_options={  # Przekazujemy dodatkowe opcje pobierania danych z internetu.
            "User-Agent": "Mozzilla/5.0",  # Ustawiamy User-Agent; tutaj jest literówka „Mozzilla”, poprawnie powinno być „Mozilla”, ale kod może nadal działać.
            "Accept": "text/csv,*/*"  # Informujemy serwer, że akceptujemy plik CSV albo dowolny inny typ odpowiedzi.
        }  # Kończymy słownik z opcjami pobierania danych.
    )  # Kończymy wywołanie funkcji pd.read_csv.
    print("Dane pobrane z OpenIntro.")  # Jeśli pobieranie z głównego źródła się udało, wyświetlamy komunikat potwierdzający.

except Exception as e:  # Jeśli w bloku try wystąpi błąd, przechwytujemy go jako zmienną e.
    print("Nie udało się pobrać danych z OpenIntro.")  # Informujemy, że nie udało się pobrać danych z głównego źródła.
    print("Używam źródła zapasowego")  # Informujemy, że program skorzysta ze źródła zapasowego.
    print("Błąd:", type(e).__name__, e)  # Wyświetlamy nazwę błędu oraz jego treść, aby łatwiej było zdiagnozować problem.
    df = pd.read_csv(url_zapasowy)  # Wczytujemy dane z zapasowego adresu URL do DataFrame df.

print("Dane zostały wczytane")  # Wyświetlamy komunikat potwierdzający, że dane są już dostępne w programie.

print("Pierwsze 5 wierszy danych:")  # Informujemy, że za chwilę zostanie pokazanych pierwszych 5 wierszy danych.
print(df.head(5))  # Wyświetlamy pierwsze 5 wierszy DataFrame, aby sprawdzić strukturę i przykładowe wartości.

print("=== PODSTAWOWE INFORMACJE O ZBIORZE ===")  # Wyświetlamy nagłówek sekcji z podstawowymi informacjami o zbiorze danych.

print("Liczba wierszy i kolumn:", df.shape)  # Wyświetlamy liczbę wierszy i kolumn w zbiorze danych.
print("Informacje o typach danych:")  # Wyświetlamy komunikat zapowiadający informacje o typach danych.
print(df.info())  # Wyświetlamy typy kolumn, liczbę wartości niepustych oraz zużycie pamięci.
print("Lista dostępnych kolumn:")  # Informujemy, że zostanie pokazana lista wszystkich kolumn w zbiorze.
print(df.columns.tolist())  # Wyświetlamy nazwy kolumn jako zwykłą listę Pythona.


print("=== WYBÓR POTRZEBNYCH KOLUMNY ===")  # Wyświetlamy nagłówek sekcji dotyczącej wyboru kolumn potrzebnych do analizy.

def wybierz_pierwsza_istniejaca(lista_kandydatow, kolumny):  # Definiujemy funkcję, która wybierze pierwszą istniejącą kolumnę z listy możliwych nazw.
    for kandydat in lista_kandydatow:  # Przechodzimy po każdej potencjalnej nazwie kolumny z listy kandydatów.
        if kandydat in kolumny:  # Sprawdzamy, czy dana nazwa kolumny występuje w zbiorze danych.
            return kandydat  # Jeśli kolumna istnieje, zwracamy jej nazwę i kończymy działanie funkcji.
    return None  # Jeśli żadna z nazw nie została znaleziona, zwracamy None.

kandydaci = {  # Tworzymy słownik, który zawiera docelowe nazwy zmiennych i możliwe nazwy tych kolumn w danych.
    "cena": ["price", "SalePrice"],  # Dla ceny nieruchomości sprawdzamy możliwe nazwy kolumn: price lub SalePrice.
    "metraz": ["area", "Gr.Liv.Area", "GrLivArea"],  # Dla metrażu sprawdzamy kilka możliwych nazw kolumn.
    "liczba_sypialni": ["Bedroom.AbvGr", "Bedroom.AbvGrd", "Bedrooms.Above.Grade"],  # Dla liczby sypialni sprawdzamy możliwe nazwy kolumn.
    "liczba_pokoi": ["TotRms.AbvGrd", "TotRms.AbvGr", "Total.Rooms.Above.Grade"],  # Dla liczby pokoi sprawdzamy możliwe nazwy kolumn.
    "rok_budowy": ["Year.Built", "YearBuilt"],  # Dla roku budowy sprawdzamy możliwe nazwy kolumn.
    "jakosc_ogolna": ["Overall.Qual", "OverallQual", "Overall.Quality"]  # Dla jakości ogólnej nieruchomości sprawdzamy możliwe nazwy kolumn.
}  # Kończymy tworzenie słownika kandydatów.

wybrane = {  # Tworzymy słownik, który połączy nowe nazwy zmiennych z faktycznie znalezionymi kolumnami w danych.
    nowe_nazwy: wybierz_pierwsza_istniejaca(stare_nazwy, df.columns)  # Dla każdej zmiennej wybieramy pierwszą istniejącą nazwę kolumny.
    for nowe_nazwy, stare_nazwy in kandydaci.items()  # Przechodzimy po parach: nowa nazwa zmiennej oraz lista możliwych starych nazw.
}  # Kończymy tworzenie słownika wybrane.

print("Wybrane kolumny")  # Wyświetlamy komunikat informujący, że zostaną pokazane wybrane kolumny.
print(wybrane)  # Wyświetlamy słownik pokazujący, jakie kolumny zostały dopasowane do nazw używanych w analizie.

brakujace_kolumny = [nowe_nazwy for nowe_nazwy, stare_nazwy in wybrane.items() if stare_nazwy is None]  # Tworzymy listę kolumn, których nie udało się znaleźć w zbiorze danych.
if brakujace_kolumny:  # Sprawdzamy, czy lista brakujących kolumn nie jest pusta.
    print("Brakujące kolumny:", brakujace_kolumny)  # Jeśli czegoś brakuje, wyświetlamy listę brakujących kolumn.
    print("Sprawdź dostępne kolumny w df.columns.tolist()")  # Podpowiadamy, aby sprawdzić pełną listę kolumn w danych.
else:  # Jeśli lista brakujących kolumn jest pusta, wykonujemy tę część kodu.
    print("Wszystkie potrzebne kolumny znalezione")  # Informujemy, że wszystkie potrzebne kolumny zostały znalezione.

print("Tworzenie roboczego zbioru danych z wybranych kolumn:")  # Informujemy, że tworzony jest mniejszy zbiór danych tylko z potrzebnych kolumn.
kolumny_zrodlowe = list(wybrane.values())  # Tworzymy listę faktycznych nazw kolumn znalezionych w oryginalnym DataFrame.

mapowanie = {stare_nazwy: nowe_nazwy for nowe_nazwy, stare_nazwy in wybrane.items()}  # Tworzymy słownik mapujący stare nazwy kolumn na nowe, prostsze nazwy.

dane = df[kolumny_zrodlowe].rename(columns=mapowanie).copy()  # Wybieramy potrzebne kolumny, zmieniamy ich nazwy i tworzymy kopię roboczego zbioru danych.

dane["metraz_m2"] = dane["metraz"] * 0.092903  # Tworzymy nową kolumnę metraz_m2, przeliczając powierzchnię ze stóp kwadratowych na metry kwadratowe.

print("Pierwsze 5 wierszy roboczego zbioru danych:")  # Informujemy, że zostanie pokazany podgląd roboczego zbioru danych.
print(dane.head(5))  # Wyświetlamy pierwsze 5 wierszy roboczego DataFrame dane.

print("Liczba braków danych w wybranych kolumnach:")  # Wyświetlamy nagłówek dotyczący brakujących wartości.
print(dane.isna().sum())  # Liczymy i wyświetlamy liczbę braków danych w każdej kolumnie roboczego zbioru.

print("Podstawowe statystyki opisowe:")  # Wyświetlamy nagłówek sekcji ze statystykami opisowymi.
print(dane.describe())  # Wyświetlamy podstawowe statystyki dla kolumn liczbowych, np. średnią, minimum, maksimum i kwartyle.

print("Statystyki opisowe dla ceny i metrażu:")  # Informujemy, że pokażemy statystyki dla ceny i powierzchni.
print(dane[["cena", "metraz", "metraz_m2"]].agg(["count", "mean", "std", "min", "max"]))  # Obliczamy liczność, średnią, odchylenie standardowe, minimum i maksimum dla ceny oraz metrażu.


print("Tworzenie histogramu cen nieruchomości....")  # Informujemy, że tworzony jest histogram cen nieruchomości.
plt.hist(dane["cena"], bins=30)  # Tworzymy histogram cen, dzieląc dane na 30 przedziałów.
plt.xlabel("Cena")  # Dodajemy podpis osi X informujący, że przedstawia ona cenę.
plt.ylabel("Liczba nieruchomości")  # Dodajemy podpis osi Y informujący, ile nieruchomości znajduje się w danym przedziale ceny.
plt.title("Rozkład cen nieruchomości")  # Dodajemy tytuł histogramu cen.
plt.show()  # Wyświetlamy histogram cen.


print("Tworzenie histogramu metrażu:")  # Informujemy, że tworzony jest histogram metrażu.
plt.hist(dane["metraz_m2"], bins=30)  # Tworzymy histogram powierzchni w metrach kwadratowych, dzieląc dane na 30 przedziałów.
plt.xlabel("Metraż w m2")  # Dodajemy podpis osi X informujący, że przedstawia metraż w metrach kwadratowych.
plt.ylabel("Liczba nieruchomości")  # Dodajemy podpis osi Y informujący, ile nieruchomości znajduje się w danym przedziale metrażu.
plt.title("Rozkład metrażu w m2")  # Dodajemy tytuł histogramu metrażu.
plt.show()  # Wyświetlamy histogram metrażu.

print("Tworzenie wykresu punktowego: cena, a metraż w m2")  # Informujemy, że powstanie wykres punktowy zależności ceny od metrażu.
plt.scatter(dane["metraz_m2"], dane["cena"])  # Tworzymy wykres punktowy, gdzie oś X to metraż, a oś Y to cena.
plt.xlabel("Metraż w m2")  # Dodajemy podpis osi X.
plt.ylabel("Cena")  # Dodajemy podpis osi Y.
plt.title("Zależność ceny od metrażu")  # Dodajemy tytuł wykresu punktowego.
plt.show()  # Wyświetlamy wykres punktowy.

print("Analiza korelacji")  # Wyświetlamy nagłówek sekcji dotyczącej analizy korelacji.

print("Macierz korelacji:")  # Informujemy, że zostanie wyświetlona macierz korelacji.
macierz_korelacji = dane.corr(numeric_only=True)  # Obliczamy korelacje między wszystkimi kolumnami liczbowymi w roboczym zbiorze danych.
print(macierz_korelacji)  # Wyświetlamy obliczoną macierz korelacji.

print("Korelacje zmiennych z ceną:")  # Informujemy, że zostaną pokazane korelacje poszczególnych zmiennych z ceną.
print(macierz_korelacji["cena"].sort_values(ascending=False))  # Wyświetlamy korelacje z ceną, posortowane od największej do najmniejszej.

print("Obliczanie korelacji Pearsona między ceną a metrażem")  # Informujemy, że zostanie obliczona korelacja Pearsona dla ceny i metrażu.

corr, p_value = pearsonr(dane["cena"], dane["metraz_m2"])  # Obliczamy współczynnik korelacji Pearsona oraz p-value między ceną a metrażem.
print("Korelacja cena-metraż:", corr)  # Wyświetlamy wartość korelacji między ceną a metrażem.

print("p_value:", p_value)  # Wyświetlamy wartość p-value, która pozwala ocenić istotność statystyczną korelacji.

print("Prosty model regresji liniowej: cena ~ metraż")  # Wyświetlamy nagłówek sekcji dotyczącej prostego modelu regresji liniowej.

print("Przygotowanie zmiennej X i y")  # Informujemy, że przygotowywane są zmienne do modelu regresji.

X = dane[["metraz_m2"]]  # Tworzymy zmienną X jako DataFrame z jedną kolumną: metraż w metrach kwadratowych.

y = dane[["cena"]]  # Tworzymy zmienną y jako DataFrame z kolumną cena, czyli wartością przewidywaną.
print("Trenowanie prostego modelu regresji liniowej na całym zbiorze")  # Informujemy, że model będzie trenowany na całym zbiorze danych.

model_prosty = LinearRegression()  # Tworzymy obiekt prostego modelu regresji liniowej.
model_prosty.fit(X, y)  # Dopasowujemy model do danych, aby nauczył się zależności między metrażem a ceną.

print("Współczynnik", model_prosty.coef_[0])  # Wyświetlamy współczynnik regresji, czyli wpływ metrażu na przewidywaną cenę.

print("Wyraz wolny", model_prosty.intercept_)  # Wyświetlamy wyraz wolny modelu, czyli przewidywaną cenę przy metrażu równym zero.

print("Tworzenie linii regresji...")  # Informujemy, że przygotowywane są wartości potrzebne do narysowania linii regresji.

x_range = np.linspace(dane["metraz_m2"].min(), dane["metraz_m2"].max(), 100)  # Tworzymy 100 równomiernie rozmieszczonych wartości metrażu od minimum do maksimum.

x_df = pd.DataFrame({"metraz_m2": x_range})  # Tworzymy DataFrame z wartościami metrażu, aby można było przekazać je do modelu.

y_pred_line = model_prosty.predict(x_df)  # Obliczamy przewidywane ceny dla kolejnych wartości metrażu, aby narysować linię regresji.

print("Tworzenie wykresu regresji liniowej")  # Informujemy, że powstanie wykres punktowy z linią regresji.

plt.scatter(dane["metraz_m2"], dane["cena"])  # Rysujemy punkty danych: metraż na osi X i cena na osi Y.
plt.plot(x_range, y_pred_line)  # Rysujemy linię regresji pokazującą przewidywaną cenę dla różnych wartości metrażu.
plt.xlabel("Metraż w m2")  # Dodajemy podpis osi X.
plt.ylabel("Cena")  # Dodajemy podpis osi Y.
plt.title("Regresja liniowa: cena ~ metraż")  # Dodajemy tytuł wykresu regresji liniowej.
plt.show()  # Wyświetlamy wykres regresji.

print("Ocena prostego modelu na zbiorze testowym")  # Wyświetlamy nagłówek sekcji oceny prostego modelu.

X = dane[["metraz_m2"]]  # Ponownie ustawiamy zmienną X jako metraż w metrach kwadratowych.
y = dane[["cena"]]  # Ponownie ustawiamy zmienną y jako cenę nieruchomości.
print("Dzielenie danych na zbiór treningowy i testowy")  # Informujemy, że dane zostaną podzielone na treningowe i testowe.

X_train, X_test, y_train, y_test = train_test_split(  # Dzielimy dane na zbiory treningowe i testowe.
    X, y,  # Przekazujemy zmienne X i y, które mają zostać podzielone.
    test_size=0.2,  # Ustawiamy, że 20% danych zostanie przeznaczone na zbiór testowy.
    random_state=7  # Ustawiamy ziarno losowości, aby podział był taki sam przy każdym uruchomieniu programu.
)  # Kończymy wywołanie funkcji train_test_split.

print("Liczba obserwacji treningowych:", len(X_train))  # Wyświetlamy liczbę obserwacji w zbiorze treningowym.
print("Liczba obserwacji testowych:", len(X_test))  # Wyświetlamy liczbę obserwacji w zbiorze testowym.

print("Trenowanie prostego modelu na zbiorze treningowym")  # Informujemy, że prosty model zostanie wytrenowany tylko na danych treningowych.

model_prosty = LinearRegression()  # Tworzymy nowy model regresji liniowej dla prostego modelu.
model_prosty.fit(X_train, y_train)  # Trenujemy prosty model na zbiorze treningowym.

print("Przewidywanie cen dla zbioru testowego")  # Informujemy, że model przewidzi ceny dla danych testowych.

pred_prosty = model_prosty.predict(X_test)  # Obliczamy przewidywane ceny dla obserwacji ze zbioru testowego.
print("Wyniki prostego modelu:")  # Wyświetlamy nagłówek wyników prostego modelu.

print("R2:", r2_score(y_test, pred_prosty))  # Obliczamy i wyświetlamy R2 prostego modelu na danych testowych.
print("MAE:", mean_absolute_error(y_test, pred_prosty))  # Obliczamy i wyświetlamy średni błąd bezwzględny prostego modelu.
print("MSE:", mean_squared_error(y_test, pred_prosty))  # Obliczamy i wyświetlamy średni błąd kwadratowy prostego modelu.

print("=== MODEL WIELORAKI ===")  # Wyświetlamy nagłówek sekcji dotyczącej modelu regresji wielorakiej.

cechy = ["metraz_m2", "liczba_sypialni", "liczba_pokoi", "rok_budowy", "jakosc_ogolna"]  # Tworzymy listę cech używanych jako zmienne objaśniające w modelu wielorakim.

print("Cechy użyte w modelu wielorakim:", cechy)  # Wyświetlamy listę cech użytych w modelu wielorakim.

X = dane[cechy]  # Tworzymy zmienną X zawierającą kilka cech nieruchomości.
y = dane["cena"]  # Tworzymy zmienną y jako cenę nieruchomości, czyli zmienną przewidywaną.


print("Dzielenie danych na zbiór treningowy i testowy dla modelu wielorakiego")  # Informujemy, że dane dla modelu wielorakiego będą podzielone na treningowe i testowe.

X_train, X_test, y_train, y_test = train_test_split(  # Dzielimy dane modelu wielorakiego na zbiór treningowy i testowy.
    X, y,  # Przekazujemy cechy oraz zmienną przewidywaną.
    test_size=0.2,  # Ustawiamy, że 20% obserwacji trafi do zbioru testowego.
    random_state=7  # Ustawiamy stałe ziarno losowości, aby wynik podziału był powtarzalny.
)  # Kończymy wywołanie train_test_split.

print("Liczba obserwacji treningowych:", len(X_train))  # Wyświetlamy liczbę obserwacji treningowych.
print("Liczba obserwacji testowych:", len(X_test))  # Wyświetlamy liczbę obserwacji testowych.

print("Trenowanie modelu wielorakiego")  # Informujemy, że rozpoczyna się trenowanie modelu wielorakiego.
model_wieloraki = LinearRegression()  # Tworzymy model regresji liniowej, który będzie korzystał z wielu zmiennych.
model_wieloraki.fit(X_train, y_train)  # Trenujemy model wieloraki na danych treningowych.

print("Przewidywanie cen dla zbioru testowego")  # Informujemy, że model wieloraki będzie przewidywał ceny dla danych testowych.

pred_wieloraki = model_wieloraki.predict(X_test)  # Obliczamy przewidywane ceny dla zbioru testowego.
print("Współczynniki modelu wielorakiego:")  # Wyświetlamy nagłówek sekcji ze współczynnikami modelu.

wspolczynniki = pd.DataFrame({  # Tworzymy DataFrame pokazujący współczynniki regresji dla poszczególnych zmiennych.
    "zmienna": cechy,  # Pierwsza kolumna zawiera nazwy zmiennych użytych w modelu.
    "wspolczynnik": model_wieloraki.coef_  # Druga kolumna zawiera współczynniki przypisane tym zmiennym przez model.
}).sort_values("wspolczynnik", ascending=False)  # Sortujemy współczynniki malejąco, od największych do najmniejszych.


print(wspolczynniki)  # Wyświetlamy tabelę współczynników modelu wielorakiego.

print("Ocena modelu wielorakiego")  # Wyświetlamy nagłówek sekcji oceniającej model wieloraki.
print("Wyraz wolny:", model_wieloraki.intercept_)  # Wyświetlamy wyraz wolny modelu wielorakiego.
print("R2:", r2_score(y_test, pred_wieloraki))  # Obliczamy i wyświetlamy R2 modelu wielorakiego na zbiorze testowym.
print("MAE:", mean_absolute_error(y_test, pred_wieloraki))  # Obliczamy i wyświetlamy średni błąd bezwzględny modelu wielorakiego.
print("MSE:", mean_squared_error(y_test, pred_wieloraki))  # Obliczamy i wyświetlamy średni błąd kwadratowy modelu wielorakiego.

print("Porównanie modelu prostego i wielorakiego")  # Informujemy, że zostanie utworzona tabela porównująca oba modele.

porownanie_modeli = pd.DataFrame({  # Tworzymy DataFrame z porównaniem jakości modelu prostego i wielorakiego.
    "model": ["Model prosty: metraż", "Model wieloraki"],  # Tworzymy kolumnę z nazwami porównywanych modeli.
    "R2": [r2_score(y_test, model_prosty.predict(X_test[["metraz_m2"]])),  # Obliczamy R2 modelu prostego na kolumnie metrażu z aktualnego zbioru testowego.
           r2_score(y_test, pred_wieloraki)],  # Obliczamy R2 modelu wielorakiego na tym samym zbiorze testowym.
    "MAE": [mean_absolute_error(y_test, model_prosty.predict(X_test[["metraz_m2"]])),  # Obliczamy MAE modelu prostego na podstawie metrażu.
            mean_absolute_error(y_test, pred_wieloraki)]  # Obliczamy MAE modelu wielorakiego.
})  # Kończymy tworzenie tabeli porównującej modele.

print(porownanie_modeli)  # Wyświetlamy tabelę porównania modeli.

print("=== Predykcja dla nowej nieruchomości ===")  # Wyświetlamy nagłówek sekcji dotyczącej predykcji dla nowej nieruchomości.
nowa_nieruchomosc = pd.DataFrame({  # Tworzymy DataFrame z parametrami jednej nowej nieruchomości.
    "metraz_m2": [190],  # Podajemy metraż nowej nieruchomości w metrach kwadratowych.
    "liczba_sypialni": [5],  # Podajemy liczbę sypialni w nowej nieruchomości.
    "liczba_pokoi": [8],  # Podajemy całkowitą liczbę pokoi w nowej nieruchomości.
    "rok_budowy": [2010],  # Podajemy rok budowy nowej nieruchomości.
    "jakosc_ogolna": [7],  # Podajemy ocenę jakości ogólnej nowej nieruchomości.
})  # Kończymy tworzenie DataFrame z nową nieruchomością.

print("Dane nowej nieruchomości:")  # Informujemy, że zostaną pokazane dane nowej nieruchomości.
print(nowa_nieruchomosc)  # Wyświetlamy dane nowej nieruchomości.

przewidywana_cena = model_wieloraki.predict(nowa_nieruchomosc)  # Używamy modelu wielorakiego do przewidzenia ceny nowej nieruchomości.

print("Przewidywana cena:", przewidywana_cena[0])  # Wyświetlamy przewidywaną cenę; [0] pobiera pierwszą i jedyną wartość z wyniku predykcji.

print("PORÓWNANIE CEN RZECZYWISTYCH I PRZEWIDZIANYCH")  # Wyświetlamy nagłówek sekcji porównującej ceny rzeczywiste i przewidywane.

porownanie = pd.DataFrame({  # Tworzymy DataFrame z cenami rzeczywistymi i przewidywanymi.
    "cena_rzeczywista": y_test,  # Dodajemy kolumnę z rzeczywistymi cenami ze zbioru testowego.
    "cena_przewidziana": pred_wieloraki,  # Dodajemy kolumnę z cenami przewidzianymi przez model wieloraki.
})  # Kończymy tworzenie tabeli porównawczej.

porownanie["blad"] = porownanie["cena_rzeczywista"] - porownanie["cena_przewidziana"]  # Tworzymy kolumnę błędu, czyli różnicę między ceną rzeczywistą a przewidzianą.

print("Pierwsze 10 wyników porównania:")  # Informujemy, że zostanie pokazanych pierwszych 10 wyników porównania.
print(porownanie.head(10))  # Wyświetlamy pierwsze 10 wierszy tabeli porównującej ceny rzeczywiste i przewidywane.

print("Tworzenie wykres: ceny rzeczywiste vs ceny przewidywane...")  # Informujemy, że zostanie utworzony wykres porównujący ceny rzeczywiste i przewidywane.
plt.scatter(porownanie["cena_rzeczywista"],  # Tworzymy wykres punktowy; na osi X znajdą się ceny rzeczywiste.
            porownanie["cena_przewidziana"])  # Na osi Y znajdą się ceny przewidziane przez model.
plt.xlabel("cena rzeczywista")  # Dodajemy podpis osi X.
plt.ylabel("cena przewidziana")  # Dodajemy podpis osi Y.
plt.title("Ceny rzeczywista v cena przewidziana")  # Dodajemy tytuł wykresu porównującego wartości rzeczywiste i przewidywane.

plt.show()  # Wyświetlamy wykres.