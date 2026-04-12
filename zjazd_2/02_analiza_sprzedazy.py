# Importujemy bibliotekę `pandas` i nadajemy jej skróconą nazwę `pd`.
# Skrót `pd` jest standardowo używany w Pythonie przy pracy z pandas,
# dlatego bardzo często spotyka się właśnie taki zapis.
# Biblioteka pandas służy przede wszystkim do pracy z danymi tabelarycznymi:
# można dzięki niej wczytywać pliki CSV, filtrować dane, grupować je,
# liczyć statystyki i wygodnie analizować duże zestawy informacji.
import pandas as pd

# Importujemy bibliotekę `numpy` i nadajemy jej skrót `np`.
# Numpy jest biblioteką przeznaczoną głównie do obliczeń numerycznych.
# W tym programie wykorzystujemy ją do liczenia statystyk takich jak:
# średnia, mediana, minimum, maksimum oraz współczynnik korelacji.
# Dzięki numpy obliczenia są szybkie i bardzo wygodne.
import numpy as np


# Definiujemy funkcję `analiza_sprzedazy_zaawansowana`.
# Umieszczenie całego kodu w funkcji ma kilka zalet:
# 1. program jest bardziej uporządkowany,
# 2. łatwiej go później uruchomić ponownie,
# 3. można go zaimportować do innego pliku bez automatycznego wykonania.
# Funkcja nie przyjmuje argumentów, bo dane wczytuje bezpośrednio z pliku CSV.
def analiza_sprzedazy_zaawansowana():

    # Rozpoczynamy blok `try`.
    # Blok ten służy do przechwytywania błędów, które mogą pojawić się
    # podczas wykonywania ryzykownego fragmentu kodu.
    # Tutaj takim ryzykownym fragmentem jest odczyt pliku z dysku,
    # ponieważ plik może nie istnieć albo może być uszkodzony.
    try:
        # Wczytujemy dane z pliku `sprzedaz.csv`.
        # Funkcja `pd.read_csv(...)` tworzy na podstawie pliku CSV obiekt DataFrame,
        # czyli tabelę składającą się z wierszy i kolumn.
        #
        # Parametr `encoding="utf-8-sig"` jest bardzo przydatny,
        # gdy plik był zapisany np. w Excelu albo zawiera polskie znaki.
        # Dzięki temu program poprawnie odczyta znaki takie jak ą, ć, ę, ł, ń, ó, ś, ź, ż
        # oraz ewentualny niewidoczny znacznik BOM na początku pliku.
        df = pd.read_csv("sprzedaz.csv", encoding="utf-8-sig")

    # Ten blok wykona się tylko wtedy,
    # gdy Python zgłosi dokładnie błąd `FileNotFoundError`,
    # czyli sytuację, w której plik o podanej nazwie nie istnieje
    # albo nie został znaleziony w bieżącym folderze.
    except FileNotFoundError:
        # Wyświetlamy użytkownikowi czytelny komunikat o problemie.
        # Zamiast technicznego błędu Pythona pokazujemy prostą informację,
        # która jasno mówi, co poszło nie tak.
        print("Błąd: Plik 'sprzedaz.csv' nie został znaleziony!")

        # Kończymy działanie funkcji instrukcją `return`.
        # Dzięki temu program nie próbuje wykonywać dalszej analizy,
        # skoro nie udało się nawet wczytać danych.
        return

    # Ten blok przechwytuje wszystkie inne możliwe wyjątki,
    # które mogłyby wystąpić przy odczycie pliku.
    # Przykładowo mogą to być problemy z kodowaniem, formatem pliku
    # albo uprawnieniami do odczytu.
    except Exception as e:
        # Wyświetlamy bardziej ogólny komunikat z treścią konkretnego błędu.
        # `e` zawiera szczegóły wyjątku zgłoszonego przez Pythona.
        print(f"Błąd podczas czytania pliku: {e}")

        # Kończymy działanie funkcji, bo dalsza analiza bez poprawnie wczytanych danych
        # również nie ma sensu.
        return

    # Czyścimy nazwy kolumn w tabeli.
    # To ważny krok, bo w praktyce pliki CSV często mają "brudne" nagłówki:
    # mogą zawierać spacje, niewidoczne znaki lub dziwne znaki na początku.
    #
    # Po kolei:
    # - `pd.Index(df.columns)` bierze wszystkie nazwy kolumn,
    # - `astype(str)` zamienia je na tekst,
    # - `str.replace("\ufeff", "", regex=False)` usuwa znak BOM,
    # - `str.strip()` usuwa spacje z początku i końca tekstu.
    #
    # Dzięki temu np. kolumna `" produkt "` zamieni się na `"produkt"`,
    # a nazwy kolumn będą łatwiejsze do dalszego użycia.
    df.columns = (
        pd.Index(df.columns)
        .astype(str)
        .str.replace("\ufeff", "", regex=False)
        .str.strip()
    )

    # Tworzymy listę kolumn, które MUSZĄ istnieć,
    # żeby analiza mogła zostać wykonana poprawnie.
    # Bez tych kolumn program nie wiedziałby:
    # - jaki jest identyfikator transakcji,
    # - jaki produkt został sprzedany,
    # - ile sztuk sprzedano,
    # - jaka była cena jednostkowa.
    wymagane = ["transakcja_id", "produkt", "ilość", "cena"]

    # Tworzymy listę brakujących kolumn.
    # Działa to tak:
    # dla każdej kolumny `c` z listy `wymagane`
    # sprawdzamy, czy NIE ma jej w aktualnych kolumnach DataFrame.
    # Jeśli jej nie ma, dodajemy ją do listy `brakujace`.
    brakujace = [c for c in wymagane if c not in df.columns]

    # Sprawdzamy, czy lista brakujących kolumn zawiera jakieś elementy.
    # Jeśli tak, znaczy to, że plik nie ma poprawnej struktury.
    if brakujace:
        # Wyświetlamy użytkownikowi informację,
        # których dokładnie kolumn brakuje.
        print(f"Błąd: Brakuje kolumn w pliku CSV: {brakujace}")

        # Kończymy funkcję, bo bez wymaganych kolumn nie da się analizować danych.
        return

    # Zamieniamy kolumnę `transakcja_id` na wartości liczbowe.
    # `pd.to_numeric(...)` próbuje przekonwertować dane na liczby.
    #
    # Parametr `errors="coerce"` oznacza:
    # jeżeli jakaś wartość nie da się zamienić na liczbę,
    # to zamiast przerwać program błędem, pandas wstawi tam NaN,
    # czyli specjalne oznaczenie brakującej / niepoprawnej wartości.
    df["transakcja_id"] = pd.to_numeric(df["transakcja_id"], errors="coerce")

    # Tak samo konwertujemy kolumnę `ilość`.
    # To ważne, bo później chcemy ją sumować, filtrować i analizować liczbowo.
    df["ilość"] = pd.to_numeric(df["ilość"], errors="coerce")

    # Konwertujemy także kolumnę `cena` na typ liczbowy.
    # Ceny muszą być liczbami, bo będziemy liczyć przychód
    # jako iloczyn ceny i liczby sztuk.
    df["cena"] = pd.to_numeric(df["cena"], errors="coerce")

    # Zamieniamy kolumnę `produkt` na tekst.
    # Nawet jeśli w pliku były liczby lub inne typy danych,
    # po tej operacji wszystko będzie traktowane jako napis.
    # Następnie `str.strip()` usuwa zbędne spacje,
    # np. `" A "` zamieni się na `"A"`.
    df["produkt"] = df["produkt"].astype(str).str.strip()

    # Zapisujemy liczbę wierszy przed czyszczeniem danych.
    # To pozwoli później policzyć, ile rekordów zostało odrzuconych
    # podczas usuwania błędów i walidacji.
    przed = len(df)

    # Usuwamy wszystkie wiersze, w których w co najmniej jednej z podanych kolumn
    # występuje brak danych (NaN).
    #
    # `subset=[...]` oznacza, że sprawdzamy tylko wskazane kolumny,
    # a nie cały DataFrame.
    # Dzięki temu pozostają tylko rekordy kompletne,
    # czyli takie, które mają wszystkie najważniejsze informacje.
    df = df.dropna(subset=["transakcja_id", "produkt", "ilość", "cena"])

    # Po usunięciu pustych i niepoprawnych wartości możemy bezpiecznie zamienić
    # `transakcja_id` na typ całkowity `int`.
    # Identyfikator transakcji powinien być liczbą całkowitą,
    # a nie np. napisem lub liczbą z przecinkiem.
    df["transakcja_id"] = df["transakcja_id"].astype(int)

    # Zamieniamy `ilość` na typ `int`,
    # ponieważ liczba sprzedanych sztuk również powinna być liczbą całkowitą.
    df["ilość"] = df["ilość"].astype(int)

    # Zamieniamy `cena` na typ `float`,
    # ponieważ cena może mieć część dziesiętną, np. 12.50 zł.
    df["cena"] = df["cena"].astype(float)

    # Tworzymy maskę logiczną dla kolumny `produkt`.
    # Maska logiczna to seria wartości True / False mówiąca,
    # które wiersze spełniają określony warunek.
    #
    # Wyrażenie regularne `r"^[A-E]$"` oznacza:
    # - `^` -> początek tekstu,
    # - `[A-E]` -> jedna litera od A do E,
    # - `$` -> koniec tekstu.
    #
    # Innymi słowy: poprawny produkt musi być dokładnie jedną literą
    # z zakresu A, B, C, D lub E.
    #
    # `na=False` oznacza, że brakujące wartości mają być traktowane jako niepoprawne.
    mask_produkt = df["produkt"].str.match(r"^[A-E]$", na=False)

    # Tworzymy drugą maskę logiczną dla kolumny `ilość`.
    # Metoda `between(1, 9, inclusive="both")` sprawdza,
    # czy wartość znajduje się w przedziale od 1 do 9 włącznie.
    #
    # To oznacza, że:
    # - 1 jest poprawne,
    # - 9 jest poprawne,
    # - 0 i 10 są już niepoprawne.
    mask_ilosc = df["ilość"].between(1, 9, inclusive="both")

    # Filtrujemy dane i zostawiamy tylko te wiersze,
    # które spełniają oba warunki jednocześnie:
    # - mają poprawny kod produktu,
    # - mają poprawną ilość.
    #
    # Operator `&` oznacza logiczne "i".
    # `copy()` tworzy niezależną kopię przefiltrowanych danych,
    # co pomaga uniknąć ostrzeżeń pandas przy dalszych modyfikacjach.
    df = df[mask_produkt & mask_ilosc].copy()

    # Zapisujemy liczbę rekordów po czyszczeniu i walidacji.
    po = len(df)

    # Sprawdzamy, czy po odfiltrowaniu zostały jakiekolwiek dane.
    # Jeśli nie został ani jeden poprawny wiersz,
    # analiza nie może zostać wykonana.
    if po == 0:
        # Informujemy użytkownika, że po czyszczeniu nie ma danych do analizy.
        print("Brak danych do analizy!")
        return

    # Jeżeli po czyszczeniu rekordów jest mniej niż przed czyszczeniem,
    # oznacza to, że część danych była błędna i została pominięta.
    if po < przed:
        # Wyświetlamy, ile wierszy usunięto z powodu problemów z danymi.
        print(f"Pominięto {przed - po} wierszy (błędy konwersji/walidacji)")

    # Tworzymy nową kolumnę `przychód`.
    # Przychód z pojedynczego wiersza to:
    # liczba sprzedanych sztuk * cena jednej sztuki.
    #
    # Na przykład:
    # jeśli sprzedano 3 sztuki po 20 zł,
    # to przychód z tej transakcji wynosi 60 zł.
    df["przychód"] = df["ilość"] * df["cena"]

    # Wyświetlamy nagłówek sekcji z podstawowymi statystykami.
    print("=== PODSTAWOWE STATYSTYKI SPRZEDAŻY ===")

    # Liczba transakcji to po prostu liczba wierszy w przefiltrowanym DataFrame.
    liczba_transakcji = len(df)

    # Wyświetlamy obliczoną liczbę transakcji.
    print(f"Liczba transacji: {liczba_transakcji}")

    # Liczymy łączny przychód ze wszystkich transakcji.
    # `sum()` dodaje do siebie wszystkie wartości z kolumny `przychód`.
    laczny_przychod = df["przychód"].sum()

    # Wyświetlamy łączny przychód sformatowany do dwóch miejsc po przecinku.
    print(f"Łączny przychód: {laczny_przychod:.2f} zł")

    # Liczymy średnią wartość transakcji.
    # Najpierw zamieniamy kolumnę `przychód` na tablicę NumPy,
    # a następnie obliczamy średnią funkcją `np.mean(...)`.
    srednia_transakcja = np.mean(df["przychód"].to_numpy())

    # Wyświetlamy średnią wartość jednej transakcji.
    print(f"Średnia wartość transakcji: {srednia_transakcja:.2f} zł")

    # Sumujemy wszystkie sprzedane sztuki w całym zbiorze danych.
    # Wynik zamieniamy na `int`, aby mieć liczbę całkowitą.
    laczna_ilosc = int(df["ilość"].sum())

    # Wyświetlamy łączną liczbę sprzedanych sztuk.
    print(f"Łączna liczba sprzedanych sztuk: {laczna_ilosc}")

    # Rozpoczynamy sekcję analizy produktów.
    print("=== ANALIZA PRODUKTÓW ===")
    print("Ranking produktów według przychodu:")

    # Grupujemy dane według kolumny `produkt`.
    # Oznacza to, że wszystkie transakcje dotyczące tego samego produktu
    # zostaną zebrane razem w jedną grupę.
    #
    # Następnie dla każdej grupy liczymy:
    # - `przychód` -> sumę przychodów,
    # - `ilość` -> sumę sprzedanych sztuk,
    # - `transakcje` -> liczbę transakcji.
    #
    # Na końcu sortujemy wynik malejąco po przychodzie,
    # aby na górze znalazły się najbardziej dochodowe produkty.
    produkty = (
        df.groupby("produkt")
        .agg(
            przychód=("przychód", "sum"),
            ilość=("ilość", "sum"),
            transakcje=("transakcja_id", "count"),
        )
        .sort_values("przychód", ascending=False)
    )

    # Iterujemy po wszystkich wierszach tabeli `produkty`.
    # `iterrows()` zwraca:
    # - indeks wiersza, tutaj nazwany `produkt`,
    # - cały wiersz danych, tutaj nazwany `row`.
    for produkt, row in produkty.iterrows():
        # Dla każdego produktu wyświetlamy:
        # - nazwę produktu,
        # - łączny przychód,
        # - łączną liczbę sprzedanych sztuk,
        # - liczbę transakcji.
        print(
            f"Produkt {produkt}: {row['przychód']:.2f} zł "
            f"({int(row['ilość'])} szt., {int(row['transakcje'])} transakcji)"
        )

    # Rozpoczynamy sekcję efektywności produktów.
    # Tutaj nie patrzymy już na sumy, lecz na średnie wartości.
    print("=== EFEKTYWNOŚĆ PRODUKTÓW ===")

    # Ponownie grupujemy dane według produktu.
    # Tym razem dla każdego produktu liczymy:
    # - średnią ilość w transakcji,
    # - średnią cenę,
    # - średni przychód z jednej transakcji.
    #
    # `sort_index()` sortuje wynik rosnąco według nazwy produktu,
    # czyli np. A, B, C, D, E.
    efektywnosc = (
        df.groupby("produkt")
        .agg(
            srednia_ilosc=("ilość", "mean"),
            srednia_cena=("cena", "mean"),
            sredni_przychod=("przychód", "mean"),
        )
        .sort_index()
    )

    # Przechodzimy po kolejnych produktach w tabeli efektywności.
    for produkt, row in efektywnosc.iterrows():
        # Najpierw wypisujemy nazwę produktu.
        print(f"Produkt {produkt}:")

        # Następnie średnią liczbę sztuk sprzedawanych w pojedynczej transakcji.
        print(f"Średnia ilość/szt.: {row['srednia_ilosc']:.1f}")

        # Wyświetlamy średnią cenę tego produktu.
        print(f"Średnia cena: {row['srednia_cena']:.2f} zł")

        # Wyświetlamy średni przychód uzyskiwany z jednej transakcji tego produktu.
        print(f"Średni przychód: {row['sredni_przychod']:.2f} zł")

    # Rozpoczynamy analizę wielkości transakcji.
    # Chcemy zobaczyć, ile transakcji miało 1 sztukę,
    # ile miało 2 sztuki itd.
    print("=== ANALIZA WIELKOŚCI TRANSAKCJI ===")
    print("Rozkład transakcji według liczby sztuk:")

    # `value_counts()` zlicza wystąpienia każdej wartości w kolumnie `ilość`.
    # Na przykład może policzyć, ile razy wystąpiła ilość 1, 2, 3 itd.
    # `sort_index()` sprawia, że wynik zostanie uporządkowany
    # rosnąco według liczby sztuk.
    rozklad_ilosci = df["ilość"].value_counts().sort_index()

    # Iterujemy po parach:
    # - `ilosc` -> konkretna liczba sztuk,
    # - `liczba` -> liczba transakcji o takiej wielkości.
    for ilosc, liczba in rozklad_ilosci.items():
        # Obliczamy procent wszystkich transakcji,
        # które miały właśnie taką liczbę sztuk.
        procent = (liczba / liczba_transakcji) * 100

        # Wyświetlamy wynik w czytelnej formie tekstowej.
        print(f"{int(ilosc)} sztuk: {int(liczba)} transakcji ({procent:.1f}%)")

    # Rozpoczynamy analizę wartości transakcji.
    print("=== ANALIZA WARTOŚCI TRANSAKCJI ===")

    # Zamieniamy kolumnę `przychód` na tablicę NumPy.
    # Dzięki temu łatwo użyjemy funkcji takich jak `np.min`, `np.max`,
    # `np.mean` i `np.median`.
    wartosci = df["przychód"].to_numpy()

    # Wyświetlamy najmniejszą wartość transakcji.
    print(f"Minimalna wartość: {np.min(wartosci):.2f} zł")

    # Wyświetlamy największą wartość transakcji.
    print(f"Maksymalna wartość: {np.max(wartosci):.2f} zł")

    # Wyświetlamy średnią wartość transakcji.
    print(f"Średnia wartość: {np.mean(wartosci):.2f} zł")

    # Wyświetlamy medianę wartości transakcji.
    # Mediana to wartość środkowa po uporządkowaniu danych.
    print(f"Mediana wartości: {np.median(wartosci):.2f} zł")

    # Rozpoczynamy sekcję z 10 najbardziej wartościowymi transakcjami.
    print("=== TOP 10 NAJBARDZIEJ WARTOŚCIOWYCH TRANSAKCJI ===")

    # Sortujemy wszystkie transakcje malejąco według przychodu,
    # a następnie wybieramy pierwsze 10 rekordów.
    # W ten sposób otrzymujemy ranking najcenniejszych transakcji.
    top10 = df.sort_values("przychód", ascending=False).head(10)

    # Resetujemy indeks, żeby wiersze miały numery 0, 1, 2, ... , 9.
    # Ułatwi to odwoływanie się do nich w pętli.
    top10 = top10.reset_index(drop=True)

    # Przechodzimy po wszystkich rekordach z tabeli `top10`.
    for i in range(len(top10)):
        # Odczytujemy identyfikator transakcji z bieżącego wiersza.
        tid = int(top10.loc[i, "transakcja_id"])

        # Odczytujemy przychód tej transakcji.
        przych = float(top10.loc[i, "przychód"])

        # Odczytujemy kod produktu.
        prod = str(top10.loc[i, "produkt"])

        # Odczytujemy liczbę sprzedanych sztuk.
        il = int(top10.loc[i, "ilość"])

        # Odczytujemy cenę jednostkową produktu.
        cena = float(top10.loc[i, "cena"])

        # Wyświetlamy jeden wpis rankingu.
        # Formatowanie `i+1:2d` oznacza numer pozycji w rankingu,
        # `tid:4d` ustawia szerokość pola dla ID,
        # a `przych:7.2f` ustawia szerokość pola i dwa miejsca po przecinku.
        print(
            f"{i+1:2d}. ID:{tid:4d} | {przych:7.2f} zł | "
            f"Produkt {prod} | {il} szt. x {cena} zł"
        )

    # Rozpoczynamy sekcję częstotliwości sprzedaży.
    print("=== CZĘSTOTLIWOŚĆ SPRZEDAŻY ===")

    # Pobieramy najmniejsze ID transakcji ze zbioru.
    pierwsza = int(df["transakcja_id"].min())

    # Pobieramy największe ID transakcji ze zbioru.
    ostatnia = int(df["transakcja_id"].max())

    # Wyświetlamy zakres identyfikatorów transakcji.
    print(f"Zakres transakcji: ID {pierwsza} - {ostatnia}")

    # `nunique()` liczy liczbę unikalnych produktów,
    # czyli ile różnych kodów produktów występuje w danych.
    liczba_produktow = df["produkt"].nunique()

    # Obliczamy średnią liczbę transakcji przypadającą na jeden produkt.
    # To daje prostą informację o tym,
    # jak często przeciętnie pojawiał się każdy produkt.
    print(f"Średnia liczba transakcji na produkt: {liczba_transakcji / liczba_produktow:.1f}")

    # Rozpoczynamy analizę korelacji.
    # Chcemy sprawdzić, jak zmienia się przychód wraz ze wzrostem ilości
    # dla poszczególnych produktów.
    print("=== ANALIZA KORELACJI ===")

    # Iterujemy po wszystkich unikalnych produktach w kolejności alfabetycznej.
    for produkt in sorted(df["produkt"].unique()):

        # Tworzymy pomocniczy DataFrame `d`,
        # zawierający tylko wiersze dotyczące jednego konkretnego produktu.
        d = df[df["produkt"] == produkt]

        # Jeżeli dla danego produktu jest tylko jeden rekord,
        # to nie ma sensu liczyć korelacji,
        # bo korelacja wymaga co najmniej dwóch obserwacji.
        if len(d) <= 1:
            continue

        # Pobieramy kolumnę `ilość` jako tablicę NumPy.
        ilosci = d["ilość"].to_numpy()

        # Pobieramy kolumnę `przychód` jako tablicę NumPy.
        przychody = d["przychód"].to_numpy()

        # Sprawdzamy, czy wszystkie wartości `ilość` są takie same.
        # Jeśli tak, korelacja nie będzie miała sensu,
        # bo nie ma żadnej zmienności w jednej z badanych cech.
        if np.max(ilosci) == np.min(ilosci):
            continue

        # Wyświetlamy zakres ilości i zakres przychodów
        # dla aktualnie analizowanego produktu.
        print(
            f"Produkt {produkt}: ilość {int(np.min(ilosci))} - {int(np.max(ilosci))} szt., "
            f"przychód {np.min(przychody):.2f} - {np.max(przychody):.2f} zł"
        )

        # Liczymy współczynnik korelacji Pearsona między ilością a przychodem.
        # `np.corrcoef(...)` zwraca macierz korelacji,
        # a element `[0, 1]` zawiera korelację między pierwszą i drugą tablicą.
        #
        # Wartość `r` może być:
        # - bliska 1   -> silna dodatnia zależność,
        # - bliska 0   -> brak wyraźnej zależności,
        # - bliska -1  -> silna ujemna zależność.
        r = float(np.corrcoef(ilosci, przychody)[0, 1])

        # Wyświetlamy obliczoną wartość korelacji.
        print(f"Korelacja (ilość vs przychód): r = {r:.3f}")


# Ten warunek sprawdza, czy plik został uruchomiony bezpośrednio,
# a nie zaimportowany jako moduł do innego pliku.
# To bardzo częsty i dobry wzorzec w Pythonie.
if __name__ == "__main__":
    # Jeżeli plik uruchomiono bezpośrednio,
    # wywołujemy główną funkcję programu.
    analiza_sprzedazy_zaawansowana()