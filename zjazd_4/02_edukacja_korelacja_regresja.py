import pandas as pd  # Importujemy bibliotekę pandas jako pd; służy do pracy z danymi tabelarycznymi, np. plikami CSV i DataFrame.
import numpy as np  # Importujemy bibliotekę numpy jako np; służy m.in. do obliczeń numerycznych i tworzenia tablic/liczb.
import matplotlib.pyplot as plt  # Importujemy moduł pyplot z matplotlib; będzie używany do tworzenia wykresów.
from scipy.stats import ttest_ind  # Importujemy funkcję testu t-Studenta dla dwóch niezależnych grup.
from scipy.stats import pearsonr  # Importujemy funkcję obliczającą korelację Pearsona i jej istotność statystyczną.
from sklearn.linear_model import LinearRegression  # Importujemy model regresji liniowej z biblioteki scikit-learn.
from sklearn.model_selection import train_test_split  # Importujemy funkcję do dzielenia danych na zbiór treningowy i testowy.
from sklearn.metrics import r2_score  # Importujemy metrykę R2, która ocenia dopasowanie modelu regresji.
from sklearn.metrics import mean_absolute_error  # Importujemy metrykę MAE, czyli średni błąd bezwzględny predykcji.
from sklearn.metrics import mean_squared_error  # Importujemy metrykę MSE, czyli średni błąd kwadratowy predykcji.

pd.set_option('display.max_columns', 100)  # Ustawiamy maksymalną liczbę kolumn wyświetlanych przez pandas na 100.
pd.set_option("display.float_format", lambda x: f"{x:.3f}")  # Ustawiamy wyświetlanie liczb zmiennoprzecinkowych do 3 miejsc po przecinku.

print("=== START ANALIZY: EDUKACJA, KORELACJA, REGRESJA ===")  # Wyświetlamy nagłówek informujący o rozpoczęciu analizy danych.
print("Wczytywanie danych...")  # Wyświetlamy komunikat informujący, że program zaczyna pobierać dane.

url_openintro = "https://www.openintro.org/data/csv/gpa_study_hours.csv"  # Zapisujemy główny adres URL do pliku CSV z danymi.

url_zapasowy = "https://vincentarelbundock.github.io/Rdatasets/csv/openintro/gpa_study_hours.csv"  # Zapisujemy zapasowy adres URL, gdyby główne źródło nie działało.

try:  # Rozpoczynamy blok try, czyli próbujemy wykonać kod, który może spowodować błąd.
    df = pd.read_csv(  # Wczytujemy dane CSV do ramki danych DataFrame o nazwie df.
        url_openintro,  # Podajemy główny adres URL, z którego mają zostać pobrane dane.
        storage_options={  # Przekazujemy dodatkowe ustawienia żądania HTTP potrzebne przy pobieraniu danych z internetu.
            "User-Agent": "Mozilla/5.0",  # Ustawiamy User-Agent, aby serwer traktował zapytanie jak pochodzące z przeglądarki.
            "Accept": "text/csv,*/*"  # Informujemy serwer, że akceptujemy plik CSV lub inny typ odpowiedzi.
        }  # Kończymy słownik z dodatkowymi opcjami pobierania danych.
    )  # Kończymy wywołanie funkcji pd.read_csv.
    print("Dane pobrane z OpenIntro.")  # Jeśli dane udało się pobrać, wyświetlamy komunikat potwierdzający.

except Exception as e:  # Jeśli wystąpi jakikolwiek błąd w bloku try, przechwytujemy go jako zmienną e.

    print("Nie udało się pobrać danych z OpenIntro.")  # Informujemy, że pobranie danych z głównego źródła się nie udało.
    print("Używam źródła zapasowego")  # Informujemy, że program spróbuje pobrać dane z zapasowego adresu.
    print("Błąd:", type(e).__name__)  # Wyświetlamy nazwę typu błędu, który wystąpił podczas pobierania danych.

    df = pd.read_csv(url_zapasowy)  # Wczytujemy dane z zapasowego źródła i zapisujemy je w DataFrame df.

print("Usuwanie technicznej kolumny indeksowej, jeśli istnieje")  # Informujemy, że program sprawdzi i usunie zbędną kolumnę techniczną.
df = df.drop(columns=["rownames"], errors="ignore")  # Usuwamy kolumnę rownames, jeśli istnieje; errors="ignore" zapobiega błędowi, gdy jej nie ma.
print("Pierwsze 5 wierszy danych:")  # Wyświetlamy informację, że za chwilę pokażemy pierwsze 5 wierszy.
print(df.head())  # Wyświetlamy pierwsze 5 wierszy danych, aby szybko sprawdzić ich strukturę.

print("PODSTAWOWE INFO O ZBIORZE")  # Wyświetlamy nagłówek sekcji z podstawowymi informacjami o danych.
print("Liczba wierszy i kolumn:", df.shape)  # Wyświetlamy rozmiar zbioru danych jako liczbę wierszy i kolumn.

print("Informacja o typach danych:")  # Wyświetlamy komunikat zapowiadający informacje o typach danych.
print(df.info())  # Wyświetlamy typy kolumn, liczbę wartości niepustych oraz informacje o pamięci; sama funkcja dodatkowo zwraca None.

print("Podstawowe statystki opisowe:")  # Wyświetlamy nagłówek sekcji ze statystykami opisowymi.
print(df.describe())  # Wyświetlamy podstawowe statystyki dla kolumn liczbowych, np. średnią, minimum, maksimum i kwartyle.

print("Liczba braków danych w kolumnach:")  # Wyświetlamy komunikat zapowiadający sprawdzenie brakujących wartości.
print(df.isna().sum())  # Sprawdzamy, ile braków danych znajduje się w każdej kolumnie.

print("Nazwy kolumn w zbiorze:")  # Wyświetlamy komunikat zapowiadający listę nazw kolumn.
print(df.columns)  # Wyświetlamy nazwy wszystkich kolumn znajdujących się w DataFrame.

print("Podgląd kolumn GPA i liczby godzin nauki:")  # Informujemy, że wyświetlimy tylko dwie wybrane kolumny.
print(df[["gpa", "study_hours"]].head())  # Wyświetlamy pierwsze 5 wierszy kolumn gpa i study_hours.

print("Statystyki opisowe dla wybranych kolumn GPA i liczby godzin nauki:")  # Wyświetlamy nagłówek statystyk dla dwóch najważniejszych zmiennych.
print(df[["gpa", "study_hours"]].agg(["count", "mean", "median", "std", "min", "max"]))  # Obliczamy liczbę obserwacji, średnią, medianę, odchylenie standardowe, minimum i maksimum.

print("Tworzenie histogramu liczby godzin nauki...")  # Informujemy, że program tworzy histogram liczby godzin nauki.
plt.hist(df["study_hours"].dropna(), bins=15)  # Tworzymy histogram dla kolumny study_hours, usuwając braki danych i dzieląc dane na 15 przedziałów.
plt.xlabel("Liczba godzin nauki")  # Dodajemy opis osi X, która pokazuje liczbę godzin nauki.
plt.ylabel("Liczba studentów")  # Dodajemy opis osi Y, która pokazuje liczbę studentów w danym przedziale.
plt.title("Rozkład liczby godzin nauki")  # Dodajemy tytuł wykresu.
plt.show()  # Wyświetlamy gotowy histogram.

print("Tworzenie histogramu GPA...")  # Informujemy, że program tworzy histogram ocen GPA.
plt.hist(df["gpa"].dropna(), bins=15)  # Tworzymy histogram dla kolumny gpa, pomijając brakujące wartości.
plt.xlabel("GPA")  # Dodajemy opis osi X, która pokazuje wartości GPA.
plt.ylabel("Liczba studentów")  # Dodajemy opis osi Y, która pokazuje liczbę studentów.
plt.title("Rozkład GPA")  # Dodajemy tytuł wykresu przedstawiającego rozkład GPA.
plt.show()  # Wyświetlamy histogram GPA.

print("Tworzenie wykresu punktowego: godziny nauki a GPA...")  # Informujemy, że program tworzy wykres punktowy zależności między zmiennymi.
plt.scatter(df["study_hours"], df["gpa"])  # Tworzymy wykres punktowy, gdzie X to godziny nauki, a Y to GPA.
plt.xlabel("Liczba godzin nauki")  # Dodajemy opis osi X.
plt.ylabel("GPA")  # Dodajemy opis osi Y.
plt.title("Zależność między liczbą godzin nauki a GPA")  # Dodajemy tytuł wykresu punktowego.
plt.show()  # Wyświetlamy wykres punktowy.

print("Macierz korelacji dla liczby godzin nauki i GPA:")  # Informujemy, że zostanie obliczona macierz korelacji.

print(df[["study_hours", "gpa"]].corr())  # Obliczamy i wyświetlamy korelację między study_hours i gpa.
print("Obliczanie korelacji Pearsona...")  # Informujemy, że zostanie obliczony współczynnik korelacji Pearsona.

corr, p_value = pearsonr(df["study_hours"], df["gpa"])  # Obliczamy korelację Pearsona oraz p-value dla zależności między godzinami nauki a GPA.

print("Korelacja Pearsona:", corr)  # Wyświetlamy wartość współczynnika korelacji Pearsona.
print("p_value:", p_value)  # Wyświetlamy p-value, które informuje o istotności statystycznej korelacji.

print("Obliczanie mediany liczby godzin nauki....")  # Informujemy, że zostanie obliczona mediana godzin nauki.

mediana_godzin = df["study_hours"].median()  # Obliczamy medianę liczby godzin nauki i zapisujemy ją w zmiennej mediana_godzin.
print("Mediana liczby godzin nauki:", mediana_godzin)  # Wyświetlamy obliczoną medianę liczby godzin nauki.

print("Tworzenie grup studentów według liczby godzin nauki....")  # Informujemy, że studenci zostaną podzieleni na dwie grupy.
df["grupa_nauki"] = np.where(  # Tworzymy nową kolumnę grupa_nauki na podstawie warunku logicznego.
    df["study_hours"] >= mediana_godzin,  # Sprawdzamy, czy liczba godzin nauki jest większa lub równa medianie.
    "duzo",  # Jeśli warunek jest spełniony, student trafia do grupy "duzo".
    "malo"  # Jeśli warunek nie jest spełniony, student trafia do grupy "malo".
)  # Kończymy wywołanie np.where.

print("Dane po dodaniu kolumny grupa_nauki:")  # Informujemy, że pokażemy dane po dodaniu nowej kolumny.

print(df.head())  # Wyświetlamy pierwsze 5 wierszy danych z nową kolumną grupa_nauki.

print("Liczebność grup nauki:")  # Wyświetlamy nagłówek sekcji z liczebnością grup.
print(df["grupa_nauki"].value_counts())  # Liczymy, ilu studentów znajduje się w grupie "duzo" i "malo".
print("Statystyki GPA w grupach nauki:")  # Wyświetlamy nagłówek statystyk GPA w grupach.
print(df.groupby("grupa_nauki")["gpa"].agg(["count", "mean", "median", "std"]))  # Grupujemy dane według grupy nauki i obliczamy statystyki GPA.

print("Przygotowanie danych do porównania GPA między grupami...")  # Informujemy, że przygotowujemy dane do testu porównującego grupy.
gpa_malo = df.loc[df["grupa_nauki"] == "malo", "gpa"]  # Wybieramy wartości GPA tylko dla studentów z grupy "malo".
gpa_duzo = df.loc[df["grupa_nauki"] == "duzo", "gpa"]  # Wybieramy wartości GPA tylko dla studentów z grupy "duzo".

print("Liczba osób w grupie 'mało nauki':", len(gpa_malo))  # Wyświetlamy liczbę studentów w grupie "malo".
print("Liczba osób w grupie 'dużo nauki':", len(gpa_duzo))  # Wyświetlamy liczbę studentów w grupie "duzo".

print("Tworzenie wykresu pudełkowego GPA w grupach...")  # Informujemy, że program tworzy wykres pudełkowy dla GPA w dwóch grupach.

plt.boxplot(  # Rozpoczynamy tworzenie wykresu pudełkowego.
    [gpa_malo, gpa_duzo],  # Przekazujemy dwie grupy danych: GPA studentów uczących się mało i dużo.
    tick_labels=["Mało nauki", "Dużo nauki"]  # Ustawiamy etykiety dla dwóch pudełek na wykresie.
)  # Kończymy wywołanie funkcji boxplot.

plt.ylabel("GPA")  # Dodajemy opis osi Y, która pokazuje wartości GPA.
plt.title("GPA w grupach według liczby godzin nauki")  # Dodajemy tytuł wykresu pudełkowego.
plt.show()  # Wyświetlamy wykres pudełkowy.

print("Wykonanie testu t-Studenta dla GPA w dwóch grupach...")  # Informujemy, że zostanie wykonany test t-Studenta.

stat, p_value = ttest_ind(gpa_malo, gpa_duzo, equal_var=False)  # Wykonujemy test t-Studenta dla dwóch niezależnych grup, zakładając nierówne wariancje.
print("Statystyka t:", stat)  # Wyświetlamy wartość statystyki t.
print("p_value:", p_value)  # Wyświetlamy p-value testu t-Studenta.
alpha = 0.05  # Ustalamy poziom istotności statystycznej na 0.05, czyli 5%.

print("Interpretacja testu t-Studenta:")  # Wyświetlamy nagłówek interpretacji testu t-Studenta.

if p_value < alpha:  # Sprawdzamy, czy p-value jest mniejsze od przyjętego poziomu istotności.
    print("Odrzucamy H0. Średni GPA różni się istotnie statystycznie.")  # Jeśli p-value < 0.05, uznajemy różnicę średnich za istotną statystycznie.
else:  # Wykonujemy tę część, jeśli p-value jest większe lub równe 0.05.
    print("Brak podstaw do odrzucenia H0. Nie wykazano istotnej różnicy średnich.")  # Informujemy, że nie ma podstaw do stwierdzenia istotnej różnicy średnich.

print("===REGRESJA LINIOWA NA CAŁYM ZBIORZE===")  # Wyświetlamy nagłówek sekcji dotyczącej regresji liniowej.
print("Przygotowanie zmiennej objaśniającej X i zmiennej objaśnianej y...")  # Informujemy, że przygotowujemy dane wejściowe do modelu.

X = df[["study_hours"]]  # Tworzymy zmienną X jako DataFrame z jedną kolumną study_hours, czyli zmienną objaśniającą.
y = df["gpa"]  # Tworzymy zmienną y jako serię z kolumną gpa, czyli zmienną objaśnianą/przewidywaną.

print("Tworzenie i trenowanie modelu regresji liniowej...")  # Informujemy, że model regresji liniowej zostanie utworzony i dopasowany do danych.

model = LinearRegression()  # Tworzymy pusty model regresji liniowej.
model.fit(X, y)  # Trenujemy model na całym zbiorze danych, ucząc go zależności między godzinami nauki a GPA.

print("Współczynnik:", model.coef_[0])  # Wyświetlamy współczynnik kierunkowy regresji, czyli zmianę GPA przy wzroście liczby godzin nauki o 1.
print("Wyraz wolny:", model.intercept_)  # Wyświetlamy wyraz wolny, czyli przewidywane GPA przy zerowej liczbie godzin nauki.

print("Tworzenie linii regresji do wykresu...")  # Informujemy, że przygotowujemy dane potrzebne do narysowania linii regresji.

x_range = np.linspace(df["study_hours"].min(), df["study_hours"].max(), 100)  # Tworzymy 100 równomiernie rozmieszczonych wartości od minimalnej do maksymalnej liczby godzin nauki.

y_pred_line = model.predict(pd.DataFrame({"study_hours": x_range}))  # Obliczamy przewidywane GPA dla wartości z x_range, aby narysować linię regresji.

print("Tworzenie wykresu regresji liniowej...")  # Informujemy, że zostanie utworzony wykres punktowy z linią regresji.

plt.scatter(df["study_hours"], df["gpa"])  # Rysujemy punkty danych: liczba godzin nauki na osi X i GPA na osi Y.
plt.plot(x_range, y_pred_line)  # Rysujemy linię regresji pokazującą przewidywaną zależność między godzinami nauki a GPA.
plt.xlabel("Liczba godzin nauki")  # Dodajemy opis osi X.
plt.ylabel("GPA")  # Dodajemy opis osi Y.
plt.title("Regresja liniowa: GPA ~ liczba godzin nauki")  # Dodajemy tytuł wykresu regresji liniowej.
plt.show()  # Wyświetlamy wykres regresji.

print("Przewidywanie GPA dla nowych wartości liczby godzin nauki")  # Informujemy, że model zostanie użyty do przewidywania GPA dla nowych danych.

nowe_dane = pd.DataFrame({  # Tworzymy nowy DataFrame z przykładowymi wartościami liczby godzin nauki.
    "study_hours": [7, 12, 18, 27]  # Definiujemy cztery nowe wartości godzin nauki, dla których chcemy przewidzieć GPA.
})  # Kończymy tworzenie DataFrame z nowymi danymi.

nowe_dane["przewidywany_gpa"] = model.predict(nowe_dane)  # Dodajemy kolumnę z GPA przewidzianym przez model regresji.

print("Nowe dane z przewidywanym GPA:")  # Informujemy, że za chwilę zostaną pokazane nowe dane wraz z predykcjami.
print(nowe_dane)  # Wyświetlamy tabelę z godzinami nauki i przewidywanym GPA.

print("Podział na zbiór treningowy i testowy")  # Wyświetlamy nagłówek sekcji dotyczącej podziału danych.

X = df[["study_hours"]]  # Ponownie definiujemy zmienną X jako dane wejściowe modelu, czyli liczbę godzin nauki.
y = df["gpa"]  # Ponownie definiujemy zmienną y jako wartość przewidywaną, czyli GPA.

print("Dzielenie danych na zbiór trenigowy i testowy...")  # Informujemy, że dane zostaną podzielone na część treningową i testową.

X_train, X_test, y_train, y_test = train_test_split(  # Dzielimy dane X i y na zbiory treningowe oraz testowe.
    X,  # Przekazujemy zmienną objaśniającą, czyli liczbę godzin nauki.
    y,  # Przekazujemy zmienną objaśnianą, czyli GPA.
    test_size=0.2,  # Ustawiamy, że 20% danych trafi do zbioru testowego.
    random_state=42  # Ustawiamy ziarno losowości, aby podział danych był powtarzalny przy każdym uruchomieniu.
)  # Kończymy wywołanie funkcji train_test_split.

print("Liczba obserwacji w treningu:", len(X_train))  # Wyświetlamy liczbę obserwacji w zbiorze treningowym.
print("Liczba obserwacji w teście:", len(X_test))  # Wyświetlamy liczbę obserwacji w zbiorze testowym.

print("Trenowanie modelu na zbiorze treningowym")  # Informujemy, że model zostanie wytrenowany tylko na danych treningowych.

model = LinearRegression()  # Tworzymy nowy model regresji liniowej, niezależny od wcześniejszego modelu trenowanego na całym zbiorze.
model.fit(X_train, y_train)  # Trenujemy model na zbiorze treningowym.

print("Przewidywanie GPA dla zbioru testowego")  # Informujemy, że model wykona predykcje dla danych testowych.

y_pred = model.predict(X_test)  # Obliczamy przewidywane wartości GPA dla obserwacji ze zbioru testowego.

print("Ocena jakości modelu:")  # Wyświetlamy nagłówek sekcji z oceną jakości modelu.
print("R2:", r2_score(y_test, y_pred))  # Obliczamy i wyświetlamy R2, czyli miarę dopasowania modelu do danych testowych.

print("MAE:", mean_absolute_error(y_test, y_pred))  # Obliczamy i wyświetlamy średni błąd bezwzględny predykcji.
print("MSE:", mean_squared_error(y_test, y_pred))  # Obliczamy i wyświetlamy średni błąd kwadratowy predykcji.

print("Tworzenie tabeli z wynikami rzeczywistymi i przewidywanymi")  # Informujemy, że zostanie utworzona tabela porównująca wyniki rzeczywiste i przewidywane.
wyniki = pd.DataFrame({  # Tworzymy nowy DataFrame z wynikami predykcji.
    "study_hours": X_test["study_hours"],  # Dodajemy kolumnę z liczbą godzin nauki ze zbioru testowego.
    "gpa_rzeczywisty": y_test,  # Dodajemy kolumnę z rzeczywistymi wartościami GPA.
    "gpa_przewidywane": y_pred  # Dodajemy kolumnę z wartościami GPA przewidzianymi przez model.
})  # Kończymy tworzenie tabeli wyników.

wyniki["blad"] = wyniki["gpa_rzeczywisty"] - wyniki["gpa_przewidywane"]  # Dodajemy kolumnę z błędem predykcji, czyli różnicą między wartością rzeczywistą a przewidywaną.

print("pierwsze 10 wyników predykcji:")  # Informujemy, że wyświetlone zostanie pierwsze 10 wierszy tabeli wyników.
print(wyniki.head(10))  # Wyświetlamy pierwsze 10 wyników predykcji wraz z błędami.