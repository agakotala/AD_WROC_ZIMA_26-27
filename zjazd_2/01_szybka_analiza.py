# Importujemy bibliotekę pandas i nadajemy jej skróconą nazwę `pd`.
# Biblioteka pandas służy do pracy z danymi tabelarycznymi,
# na przykład do wczytywania plików CSV i analizowania ich zawartości.
import pandas as pd

# Wczytujemy dane z pliku `wynagrodzenia.csv` do zmiennej `df`.
# `df` to DataFrame, czyli tabela danych składająca się z wierszy i kolumn.
df = pd.read_csv("wynagrodzenia.csv")

# Wyświetlamy napis informujący, że zaraz pokażemy pierwsze 5 wierszy tabeli.
print("Pierwsze 5 wierszy:")

# Metoda `head()` zwraca pierwsze 5 wierszy DataFrame.
# Dzięki temu możemy szybko zobaczyć, jak wyglądają dane po wczytaniu.
print(df.head())

# Wyświetlamy pustą linię (`\n`), aby wynik był bardziej czytelny,
# a następnie napis informujący o kolejnej części analizy.
print("\nOstatnie 5 wierszy:")

# Metoda `tail()` zwraca ostatnie 5 wierszy tabeli.
# To pozwala sprawdzić, jak wyglądają dane na końcu pliku.
print(df.tail())

# Wyświetlamy nagłówek dla informacji o strukturze danych.
print("\nInformacje o danych:")

# Metoda `info()` pokazuje podstawowe informacje o zbiorze danych:
# nazwy kolumn, liczbę niepustych wartości, typy danych i zużycie pamięci.
# Uwaga: `info()` samo wypisuje wynik, więc po `print(df.info())`
# na końcu może pojawić się jeszcze `None`.
print(df.info())

# Wyświetlamy nagłówek dla sekcji dotyczącej brakujących danych.
print("\nBrakujące dane w każdej kolumnie:")

# `isnull()` sprawdza, które wartości są puste,
# a `sum()` zlicza liczbę braków w każdej kolumnie.
print(df.isnull().sum())

# Wyświetlamy nagłówek dla statystyk opisowych wszystkich kolumn liczbowych.
print("\nStatystki dla wszystkich kolumn liczbowych")

# `describe()` oblicza podstawowe statystyki dla kolumn liczbowych,
# takie jak liczba wartości, średnia, odchylenie standardowe,
# minimum, kwartyle i maksimum.
print(df.describe())

# Wyświetlamy nagłówek dla statystyk tylko wybranych dwóch kolumn.
print("\nStatystyki tylko dla kolumn wiek i dochód:")

# Wybieramy z tabeli tylko kolumny `wiek` i `dochód`,
# a następnie obliczamy dla nich statystyki opisowe.
print(df[["wiek", "dochód"]].describe())

# Tworzymy nowy DataFrame zawierający tylko dwie kolumny:
# `wiek` oraz `dochód`.
wiek_i_dochod = df[["wiek", "dochód"]]

# Filtrujemy dane i zapisujemy tylko te osoby,
# których wiek jest większy niż 30 lat.
powyzej_30 = df[df["wiek"] > 30]  # filtrujemy dane i zapisujemy tylko te osoby powyżej 30 lat

# Tworzymy kolejny filtr:
# wybieramy tylko osoby mające więcej niż 30 lat
# oraz tylko te, których płeć to "K", czyli kobieta.
# Operator `&` oznacza, że oba warunki muszą być spełnione jednocześnie.
powyzej_30_kobiety = df[(df["wiek"] > 30) & (df["płeć"] == "K")]  # wybieramy tylko kobiety powyżej 30, dwa warunki do spełnienia jednocześnie

# Wyświetlamy nagłówek dla danych zawierających tylko kolumny wiek i dochód.
print("\nTylko kolumny wiek i dochód:")

# Pokazujemy pierwsze 5 wierszy nowego DataFrame z wybranymi kolumnami.
print(wiek_i_dochod.head())

# Wyświetlamy nagłówek dla osób powyżej 30 lat.
print("\nOsoby powyżej 30 lat:")

# Pokazujemy pierwsze 5 rekordów osób, które mają więcej niż 30 lat.
print(powyzej_30.head())

# Wyświetlamy nagłówek dla kobiet powyżej 30 lat.
print("\nKobiety powyżej 30 lat:")

# Pokazujemy pierwsze 5 rekordów kobiet starszych niż 30 lat.
print(powyzej_30_kobiety.head())

# Grupujemy dane według kolumny `płeć`,
# następnie liczymy średni dochód w każdej grupie
# i zaokrąglamy wynik do 2 miejsc po przecinku.
sredni_dochod_plec = df.groupby("płeć")["dochód"].mean().round(2)  # grupujemy dane wg płci, liczymy średni dochód i zaokrąglamy wynik do 2 miejsc po przecinku

# Wyświetlamy nagłówek dla średniego dochodu według płci.
print("\nŚredni dochód według płci:")

# Wyświetlamy obliczony średni dochód dla każdej płci.
print(sredni_dochod_plec)

# Grupujemy dane według płci i tworzymy zestaw agregatów,
# czyli kilku statystyk liczonych jednocześnie dla różnych kolumn.
agregaty = df.groupby("płeć").agg({
    # Dla kolumny `dochód` liczymy:
    # średnią (`mean`), medianę (`median`) oraz odchylenie standardowe (`std`).
    "dochód": ["mean", "median", "std"],  # dla kolumny dochód liczymy średnią, medianę i odchylenie standardowe

    # Dla kolumny `wiek` liczymy:
    # najmniejszą wartość (`min`), największą wartość (`max`)
    # oraz liczbę obserwacji (`count`).
    "wiek": ["min", "max", "count"]  # dla kolumny wiek liczymy najmniejszą wartość, największą wartość i liczbę obserwacji
}).round(2)

# Wyświetlamy nagłówek dla sekcji z agregatami.
print("\nAgregaty według płci:")

# Pokazujemy tabelę agregatów policzonych dla każdej płci.
print(agregaty)

# Definiujemy własną funkcję `przydziel_wiek`,
# która na podstawie liczby lat przypisze osobę do grupy wiekowej.
def przydziel_wiek(wiek):
    # Jeśli wiek jest mniejszy niż 30,
    # funkcja zwraca napis "młody".
    if wiek < 30:
        return "młody"

    # Jeśli wiek nie był mniejszy niż 30,
    # ale jest mniejszy niż 60,
    # funkcja zwraca napis "dorosły".
    elif wiek < 60:
        return "dorosły"

    # Jeśli żaden z powyższych warunków nie został spełniony,
    # oznacza to, że wiek wynosi 60 lub więcej,
    # więc zwracamy napis "senior".
    else:
        return "senior"

# Tworzymy nową kolumnę `wiek_grupa`.
# Do każdej wartości z kolumny `wiek` stosujemy funkcję `przydziel_wiek`,
# dzięki czemu każda osoba zostaje przypisana do odpowiedniej grupy wiekowej.
df["wiek_grupa"] = df["wiek"].apply(przydziel_wiek)

# Wyświetlamy nagłówek dla nowej kolumny z grupą wiekową.
print("\nKolumna wiek grupa:")

# Pokazujemy pierwsze 10 wierszy z kolumnami `wiek` i `wiek_grupa`,
# aby sprawdzić, czy przypisanie grup przebiegło poprawnie.
print(df[["wiek", "wiek_grupa"]].head(10))

# Grupujemy dane według kolumny `wiek_grupa`,
# następnie dla każdej grupy wiekowej liczymy średni dochód
# i zaokrąglamy wynik do 2 miejsc po przecinku.
sredni_dochod_wg_grupy = df.groupby("wiek_grupa", observed=False)["dochód"].mean().round(2)

# Wyświetlamy nagłówek dla średniego dochodu według grupy wiekowej.
print("\nŚredni dochód według grupy wiekowej:")

# Pokazujemy średni dochód obliczony dla każdej grupy wiekowej.
print(sredni_dochod_wg_grupy)

# Wyświetlamy nagłówek dla liczby osób według stanu cywilnego.
print("\nLiczba osób według stanu cywilnego:")

# `value_counts()` zlicza, ile razy każda wartość występuje w kolumnie `stan_cywilny`.
# Dzięki temu widzimy liczbę osób w poszczególnych kategoriach stanu cywilnego.
print(df["stan_cywilny"].value_counts())

# Wyświetlamy nagłówek dla zestawienia osób z najwyższymi zarobkami.
print("\nTop 10 osób z najwyższym wynagrodzeniem:")

# Sortujemy dane malejąco według kolumny `dochód`,
# czyli od najwyższego dochodu do najniższego,
# a następnie wybieramy pierwsze 10 rekordów.
print(df.sort_values("dochód", ascending=False).head(10))

# Wyświetlamy nagłówek końcowego podsumowania analizy.
print("\nPODSUMOWANIE:")

# `len(df)` zwraca liczbę wszystkich wierszy,
# czyli całkowitą liczbę rekordów w tabeli.
print(f"Liczba rekordów: {len(df)}")

# Obliczamy średni wiek z kolumny `wiek`
# i wyświetlamy wynik zaokrąglony do 2 miejsc po przecinku.
print(f"Średni wiek: {df['wiek'].mean():.2f}")

# Obliczamy średni dochód z kolumny `dochód`
# i wyświetlamy wynik zaokrąglony do 2 miejsc po przecinku.
print(f"Średni dochód: {df['dochód'].mean():.2f}")

# Obliczamy medianę dochodu,
# czyli wartość środkową po uporządkowaniu danych,
# i wyświetlamy ją z dokładnością do 2 miejsc po przecinku.
print(f"Mediana dochodu: {df['dochód'].median():.2f}")