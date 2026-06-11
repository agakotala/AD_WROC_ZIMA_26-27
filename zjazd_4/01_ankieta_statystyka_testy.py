import pandas as pd  # Importujemy bibliotekę pandas i nadajemy jej skrót pd; służy ona do pracy z danymi tabelarycznymi, np. plikami CSV i ramkami danych.
import matplotlib.pyplot as plt  # Importujemy moduł pyplot z biblioteki matplotlib; będzie używany do tworzenia wykresów.
from scipy.stats import chi2_contingency  # Importujemy funkcję do wykonania testu chi-kwadrat niezależności dla tabel krzyżowych.
from scipy.stats import ttest_ind  # Importujemy funkcję do wykonania testu t-Studenta dla dwóch niezależnych grup.

pd.set_option("display.max_columns", 120)  # Ustawiamy maksymalną liczbę kolumn wyświetlanych przez pandas na 120, aby łatwiej oglądać większe tabele.
pd.set_option("display.float_format", lambda x: f"{x:.3f}")  # Ustawiamy format wyświetlania liczb zmiennoprzecinkowych na 3 miejsca po przecinku.

print("=== START ANALIZY DANYCH ANKIETOWYCH ===")  # Wyświetlamy komunikat informujący o rozpoczęciu analizy danych ankietowych.
print("\nWczytanie danych...")  # Wyświetlamy komunikat informujący, że rozpoczyna się wczytywanie danych; \n dodaje pustą linię przed tekstem.

url = "https://vincentarelbundock.github.io/Rdatasets/csv/MASS/survey.csv"  # Zapisujemy adres internetowy pliku CSV z danymi ankietowymi w zmiennej url.
df = pd.read_csv(url)  # Wczytujemy dane z pliku CSV znajdującego się pod podanym adresem i zapisujemy je jako DataFrame o nazwie df.

print("Dane zostały wczytane")  # Wyświetlamy komunikat potwierdzający, że dane zostały poprawnie wczytane.
print("Pierwsze 5 wierszy danych:")  # Wyświetlamy informację, że za chwilę zostanie pokazanych pierwszych 5 wierszy danych.
print(df.head(5))  # Wyświetlamy pierwsze 5 wierszy ramki danych, aby szybko sprawdzić strukturę i przykładowe wartości.

kolumny_do_usuniecia = [c for c in ["rownames", "Unnamed: 0"] if c in df.columns]  # Tworzymy listę technicznych kolumn do usunięcia, ale tylko tych, które faktycznie istnieją w danych.

if kolumny_do_usuniecia:  # Sprawdzamy, czy lista kolumn do usunięcia nie jest pusta.
    print("Usuniete kolumny:", kolumny_do_usuniecia)  # Jeśli znaleziono takie kolumny, wyświetlamy ich nazwy.

else:  # Wykonujemy tę część kodu, jeśli lista kolumn do usunięcia jest pusta.
    print("Nie znaleziono technicznych kolumn do usunięcia")  # Informujemy, że w danych nie znaleziono kolumn technicznych wymagających usunięcia.

df = df.drop(columns=kolumny_do_usuniecia)  # Usuwamy z ramki danych wskazane kolumny techniczne; jeśli lista jest pusta, dane pozostają bez zmian.
print("\nDane po ewentualnym usunięciu kolumn:")  # Wyświetlamy komunikat informujący, że pokażemy dane po usunięciu zbędnych kolumn.
print(df.head(5))  # Ponownie wyświetlamy pierwsze 5 wierszy, aby sprawdzić, jak wyglądają dane po oczyszczeniu.


print("\n=== Podstawowe informacje o zbiorze ===")  # Wyświetlamy nagłówek sekcji z podstawowymi informacjami o zbiorze danych.
print("Liczba wierszy i kolumn:", df.shape)  # Wyświetlamy rozmiar danych; df.shape zwraca liczbę wierszy i kolumn.

print("\nInformacje o typach danych i brakach:")  # Wyświetlamy komunikat informujący, że za chwilę pojawią się informacje o typach danych i brakach.
print(df.info())  # Wyświetlamy informacje o kolumnach, typach danych, liczbie wartości niepustych oraz zużyciu pamięci.

print("\nLiczba braków danych w poszczególnych kolumnach:")  # Wyświetlamy nagłówek sekcji dotyczącej brakujących danych.

print(df.isna().sum().sort_values(ascending=False))  # Liczymy braki danych w każdej kolumnie i sortujemy wyniki malejąco, aby kolumny z największą liczbą braków były na górze.

print("\n=== Podstawowe statystyki dla wszystkich kolumn liczbowych: ===")  # Wyświetlamy nagłówek sekcji ze statystykami opisowymi dla kolumn liczbowych.
print(df.describe())  # Wyświetlamy podstawowe statystyki dla kolumn liczbowych, takie jak średnia, odchylenie standardowe, minimum, maksimum i kwartyle.

print("=== STATYSTYKI DLA WYBRANYCH ZMIENNYCH ILOŚCIOWYCH ===")  # Wyświetlamy nagłówek sekcji dotyczącej wybranych zmiennych ilościowych.
kolumny_ilosciowe = ["Wr.Hnd", "NW.Hnd", "Pulse", "Height", "Age"]  # Tworzymy listę nazw kolumn liczbowych, które będą analizowane szczegółowo.

print("Analizowane kolumny ilościowe:", kolumny_ilosciowe)  # Wyświetlamy listę kolumn ilościowych wybranych do analizy.

print(df[kolumny_ilosciowe].agg(["count", "mean", "std", "min", "max", "median"]))  # Dla wybranych kolumn obliczamy liczbę obserwacji, średnią, odchylenie standardowe, minimum, maksimum i medianę.

print("Tworzenie histogramu wieku respondentów...")  # Wyświetlamy komunikat informujący o tworzeniu histogramu wieku.
plt.hist(df["Age"].dropna(), bins=15)  # Tworzymy histogram wieku; dropna usuwa braki danych, a bins=15 oznacza podział danych na 15 przedziałów.
plt.xlabel("Wiek")  # Dodajemy podpis osi X informujący, że przedstawia ona wiek respondentów.
plt.ylabel("Liczba osób")  # Dodajemy podpis osi Y informujący, że przedstawia ona liczbę osób w danym przedziale wieku.
plt.title("Rozkład wieku respondentów")  # Dodajemy tytuł wykresu opisujący, że wykres pokazuje rozkład wieku respondentów.
plt.show()  # Wyświetlamy utworzony histogram na ekranie.

print("Tworzenie histogramu wzrostu respondentów...")  # Wyświetlamy komunikat informujący o tworzeniu histogramu wzrostu.
plt.hist(df["Height"].dropna(), bins=15)  # Tworzymy histogram wzrostu; usuwamy braki danych i dzielimy wartości wzrostu na 15 przedziałów.
plt.xlabel("Wzrost")  # Dodajemy podpis osi X informujący, że przedstawia ona wzrost respondentów.
plt.ylabel("Liczba osób")  # Dodajemy podpis osi Y informujący, ile osób znajduje się w danym przedziale wzrostu.
plt.title("Rozkład wzrostu respondentów")  # Dodajemy tytuł wykresu opisujący rozkład wzrostu respondentów.
plt.show()  # Wyświetlamy histogram wzrostu.

print("Tworzenie wykresu pudełkowego wzrostu...")  # Wyświetlamy komunikat informujący o tworzeniu wykresu pudełkowego dla wzrostu.
plt.boxplot(df["Height"].dropna(), vert=False)  # Tworzymy poziomy wykres pudełkowy wzrostu, po wcześniejszym usunięciu brakujących wartości.
plt.xlabel("Wzrost")  # Dodajemy podpis osi X, ponieważ wykres jest poziomy i wartości wzrostu znajdują się na osi X.
plt.title("Wykres pudełkowy wzrostu")  # Dodajemy tytuł wykresu pudełkowego.
plt.show()  # Wyświetlamy wykres pudełkowy.

print("=== ANALIZA ZMIENNYCH JAKOŚCIOWYCH ===")  # Wyświetlamy nagłówek sekcji dotyczącej zmiennych jakościowych.

kolumny_jakosciowe = ["Sex", "Smoke", "Exer", "W.Hnd", "Fold", "Clap", "M.I"]  # Tworzymy listę kolumn jakościowych, czyli kategorii opisujących respondentów.
print("Analizowane kolumny jakościowe:", kolumny_jakosciowe)  # Wyświetlamy nazwy kolumn jakościowych wybranych do analizy.

for kolumna in kolumny_jakosciowe:  # Rozpoczynamy pętlę, która przejdzie kolejno przez każdą kolumnę jakościową z listy.
    print(f"Rozkład wartości dla kolumny: {kolumna}")  # Wyświetlamy nazwę aktualnie analizowanej kolumny.
    print(df[kolumna].value_counts(dropna=False))  # Liczymy wystąpienia każdej kategorii w danej kolumnie; dropna=False oznacza, że braki danych też zostaną policzone.

print("Procentowy rozkład płci:")  # Wyświetlamy nagłówek informujący, że za chwilę pojawi się procentowy rozkład płci.
print(df["Sex"].value_counts(normalize=True) * 100)  # Obliczamy procentowy udział poszczególnych wartości w kolumnie Sex.

print("Procentowy rozkład palenia:")  # Wyświetlamy nagłówek informujący, że za chwilę pojawi się procentowy rozkład odpowiedzi dotyczących palenia.
print(df["Smoke"].value_counts(normalize=True, dropna=False) * 100)  # Obliczamy procentowy rozkład kategorii w kolumnie Smoke, uwzględniając także braki danych.

print("=== TEST CHI-KWADRAT: PŁEĆ A PALENIE ===")  # Wyświetlamy nagłówek sekcji dotyczącej testu chi-kwadrat.
print("Tabela krzyżowa: płeć a palenie")  # Informujemy, że zostanie utworzona tabela pokazująca zależność między płcią a paleniem.

tabela_sex_smoke = pd.crosstab(df["Sex"], df["Smoke"])  # Tworzymy tabelę krzyżową, w której wiersze oznaczają płeć, a kolumny kategorie palenia.

print(tabela_sex_smoke)  # Wyświetlamy tabelę krzyżową z liczebnościami dla kombinacji płci i palenia.

print("Tabela procentowa w wierszach:")  # Wyświetlamy komunikat informujący, że za chwilę pojawi się tabela procentowa liczona w obrębie każdego wiersza.
print(pd.crosstab(df["Sex"], df["Smoke"], normalize="index") * 100)  # Tworzymy tabelę krzyżową w procentach, gdzie każdy wiersz sumuje się do 100%.

chi2, p_value, dof, expected = chi2_contingency(tabela_sex_smoke)  # Wykonujemy test chi-kwadrat i zapisujemy statystykę testową, p-value, stopnie swobody i liczebności oczekiwane.

print("Wyniki testu chi-kwadrat")  # Wyświetlamy nagłówek wyników testu chi-kwadrat.
print("Statystyka chi2:", chi2)  # Wyświetlamy wartość statystyki chi-kwadrat.
print("p_value:", p_value)  # Wyświetlamy wartość p-value, która służy do oceny istotności statystycznej wyniku.
print("Stopnie swobody:", dof)  # Wyświetlamy liczbę stopni swobody testu chi-kwadrat.

print("Liczebności oczekiwane:")  # Wyświetlamy komunikat informujący, że za chwilę pojawią się liczebności oczekiwane.

expected_df = pd.DataFrame(  # Tworzymy DataFrame z liczebności oczekiwanych, aby były czytelniejsze do wyświetlenia.
    expected,  # Przekazujemy tablicę liczebności oczekiwanych otrzymaną z testu chi-kwadrat.
    index=tabela_sex_smoke.index,  # Ustawiamy indeks taki sam jak w tabeli krzyżowej, czyli kategorie płci.
    columns=tabela_sex_smoke.columns  # Ustawiamy nazwy kolumn takie same jak w tabeli krzyżowej, czyli kategorie palenia.
)  # Kończymy tworzenie ramki danych z liczebnościami oczekiwanymi.

print(expected_df)  # Wyświetlamy tabelę z liczebnościami oczekiwanymi.

alpha = 0.05  # Ustalamy poziom istotności statystycznej na 0.05, czyli 5%.
print("Interpretacja wyniku testu chi-kwadrat:")  # Wyświetlamy nagłówek sekcji z interpretacją testu chi-kwadrat.

if p_value < alpha:  # Sprawdzamy, czy p-value jest mniejsze od przyjętego poziomu istotności.
    print("Odrzucamy H0. Wynik sugeruje zależność między zmiennymi.")  # Jeśli p-value < 0.05, odrzucamy hipotezę zerową o braku zależności.

else:  # Wykonujemy tę część, jeśli p-value jest większe lub równe 0.05.
    print("Brak podstaw do odrzucenia H0. Nie wykazano zależności między zmiennymi.")  # Informujemy, że nie ma podstaw do uznania zależności za istotną statystycznie.

print("=== PORÓWNANIE WZROSTU KOBIET I MĘŻCZYZN ===")  # Wyświetlamy nagłówek sekcji porównującej wzrost kobiet i mężczyzn.

wzrost_kobiety = df.loc[df["Sex"] == "Female", "Height"].dropna()  # Wybieramy wzrost tylko dla kobiet i usuwamy brakujące wartości.
wzrost_mezczyzn = df.loc[df["Sex"] == "Male", "Height"].dropna()  # Wybieramy wzrost tylko dla mężczyzn i usuwamy brakujące wartości.

print("Liczba kobiet:", len(wzrost_kobiety))  # Wyświetlamy liczbę kobiet, dla których dostępna jest informacja o wzroście.
print("Liczba mężczyzn:", len(wzrost_mezczyzn))  # Wyświetlamy liczbę mężczyzn, dla których dostępna jest informacja o wzroście.

print("Średni wzrost kobiet:", wzrost_kobiety.mean())  # Obliczamy i wyświetlamy średni wzrost kobiet.
print("Średni wzrost mężczyzn:", wzrost_mezczyzn.mean())  # Obliczamy i wyświetlamy średni wzrost mężczyzn.

print("Tworzenie wykresu pudełkowego dla wzrostu kobiet i mężczyzn...")  # Wyświetlamy komunikat informujący o tworzeniu wykresu porównującego wzrost kobiet i mężczyzn.

plt.boxplot(  # Rozpoczynamy tworzenie wykresu pudełkowego dla dwóch grup.
    [wzrost_kobiety, wzrost_mezczyzn],  # Przekazujemy dwie serie danych: wzrost kobiet oraz wzrost mężczyzn.
    tick_labels=["Kobiety", "Mężczyźni"]  # Ustawiamy etykiety pod wykresem dla obu porównywanych grup.
)  # Kończymy tworzenie wykresu pudełkowego.

plt.ylabel("Wzrost")  # Dodajemy podpis osi Y informujący, że wartości na wykresie oznaczają wzrost.
plt.title("Porównanie wzrostu kobiet i mężczyzn")  # Dodajemy tytuł wykresu porównującego wzrost kobiet i mężczyzn.
plt.show()  # Wyświetlamy wykres pudełkowy.


print("Wykonanie testu t-Studenta dla wzrostu kobiet i mężczyzn")  # Wyświetlamy komunikat informujący o wykonaniu testu t-Studenta.

stat, p_value = ttest_ind(wzrost_kobiety, wzrost_mezczyzn, equal_var=False)  # Wykonujemy test t-Studenta dla dwóch niezależnych grup, zakładając nierówne wariancje.

print("Statystyka t:", stat)  # Wyświetlamy wartość statystyki t otrzymanej w teście.
print("p_value:", p_value)  # Wyświetlamy wartość p-value dla testu t-Studenta.


print("Interpretacja wyniku testu t-Studenta:")  # Wyświetlamy nagłówek sekcji z interpretacją wyniku testu t-Studenta.

if p_value < alpha:  # Sprawdzamy, czy p-value z testu t-Studenta jest mniejsze od poziomu istotności 0.05.
    print("Odrzucamy H0. Średnie różnią się istotnie statystycznie.")  # Jeśli p-value < 0.05, uznajemy różnicę średnich za istotną statystycznie.

else:  # Wykonujemy tę część, jeśli p-value jest większe lub równe 0.05.
    print("Brak podstaw do odrzucenia H0. Nie wykazano istotnej różnicy średnich.")  # Informujemy, że nie wykazano istotnej statystycznie różnicy średnich.