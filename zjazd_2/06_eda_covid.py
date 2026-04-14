# ============================================================
# IMPORTY BIBLIOTEK
# ============================================================

import sys
# sys daje dostęp m.in. do sys.stdout, czyli standardowego wyjścia.
# Dzięki temu możemy przechwytywać printy i jednocześnie pokazywać je
# w konsoli oraz zapisywać do bufora tekstowego.

import html
# html będzie użyte przy budowaniu raportu HTML.
# Funkcja html.escape(...) zabezpiecza tekst przed potraktowaniem go
# jako kod HTML. To ważne np. wtedy, gdy raport tekstowy zawiera znaki
# typu <, >, &, które w HTML mają specjalne znaczenie.

import pandas as pd
# pandas to główna biblioteka do pracy z danymi tabelarycznymi.
# Używamy jej do:
# - wczytania pliku CSV,
# - czyszczenia danych,
# - grupowania,
# - sumowania,
# - liczenia braków,
# - agregacji po datach, wieku, płci, województwach itd.

import numpy as np
# numpy daje narzędzia numeryczne.
# Tutaj używamy go głównie do:
# - pracy z NaN,
# - generowania równych przedziałów kolorów (np.linspace),
# - wygodnej współpracy z matplotlib.

import matplotlib.pyplot as plt
# matplotlib.pyplot służy do rysowania wykresów.
# Korzystamy z niego do:
# - tworzenia figur i osi,
# - rysowania linii, słupków, histogramów, boxplotów i wykresów kołowych,
# - ustawiania tytułów, etykiet i legend.

import matplotlib.dates as mdates
# mdates zawiera narzędzia do czytelnego formatowania osi dat.
# Używamy go przy wykresach dziennych i miesięcznych,
# aby etykiety dat na osi X były automatycznie dopasowane.

from pathlib import Path
# Path pozwala wygodnie pracować ze ścieżkami do plików i folderów.
# Jest bardziej nowoczesny i czytelny niż operowanie na zwykłych stringach.
# Dzięki temu łatwiej:
# - wskazać plik wejściowy,
# - tworzyć folder wyjściowy,
# - zapisywać raport HTML.

from datetime import datetime
# datetime będzie użyte do zapisania momentu wykonania analizy.
# Ten czas jest potem używany:
# - w nagłówku raportu,
# - w nazwie pliku HTML.

from textwrap import fill
# fill służy do łamania długiego tekstu na kilka linii.
# Użyjemy tego przy etykietach legendy, np. na wykresach kołowych,
# aby długie nazwy kategorii nie były zbyt szerokie.

from io import StringIO, BytesIO
# StringIO to bufor tekstowy w pamięci RAM:
# - przechwytujemy tam printy,
# - potem wstawiamy je do sekcji tekstowej HTML.
#
# BytesIO to bufor bajtowy w pamięci:
# - zapisujemy tam wykres PNG,
# - potem kodujemy go do base64,
# - dzięki temu można osadzić obraz bezpośrednio w HTML
#   bez zapisywania osobnych plików .png.

import base64
# base64 służy do zakodowania obrazów jako tekst.
# W praktyce:
# - wykres zapisujemy do BytesIO jako PNG,
# - zamieniamy go na base64,
# - wstawiamy do HTML jako:
#   <img src="data:image/png;base64,...">
# To daje jeden samowystarczalny plik HTML.

from contextlib import redirect_stdout
# redirect_stdout pozwala przekierować standardowe wyjście print()
# do własnego obiektu/strumienia.
# Dzięki temu raport tekstowy:
# - widać w konsoli,
# - jednocześnie zapisuje się do bufora StringIO.


# ============================================================
# KONFIGURACJA GŁÓWNA
# ============================================================

INPUT_PATH = Path("/ewp_dsh_zakazenia_po_szczepieniu_202203020921.csv")
# INPUT_PATH wskazuje pełną ścieżkę do wejściowego pliku CSV.
# To jest źródło danych dla całej analizy.
#
# Warto trzymać tę ścieżkę na samej górze skryptu, bo dzięki temu:
# - łatwo zmienić plik bez szukania po całym kodzie,
# - konfiguracja jest od razu widoczna,
# - kod jest bardziej czytelny.

OUTPUT_DIR = Path("eda_output")
# OUTPUT_DIR to folder, do którego zostanie zapisany raport HTML.
# Używamy osobnego katalogu wyjściowego, aby:
# - nie mieszać raportów z plikami źródłowymi,
# - zachować porządek w projekcie,
# - łatwo znaleźć wygenerowane wyniki.

OUTPUT_DIR.mkdir(exist_ok=True)
# mkdir(exist_ok=True) tworzy folder, jeśli jeszcze nie istnieje.
# Parametr exist_ok=True oznacza:
# - jeśli katalog już istnieje, nie zgłaszaj błędu.
# Dzięki temu skrypt można uruchamiać wiele razy.

ANALYSIS_TIME = datetime.now()
# ANALYSIS_TIME zapisuje dokładny moment uruchomienia skryptu.
# Będzie użyty:
# - w nagłówku raportu,
# - w nazwie pliku,
# - w metadanych HTML.

STAMP = ANALYSIS_TIME.strftime("%Y-%m-%d_%H-%M-%S")
# STAMP to tekstowa, bezpieczna wersja daty/czasu,
# odpowiednia do użycia w nazwie pliku.
#
# Format:
# - %Y -> rok 4-cyfrowy
# - %m -> miesiąc 2-cyfrowy
# - %d -> dzień 2-cyfrowy
# - %H -> godzina
# - %M -> minuta
# - %S -> sekunda
#
# Przykład:
# 2026-04-11_16-43-59

REPORT_HTML = OUTPUT_DIR / f"EDA_report_{STAMP}.html"
# REPORT_HTML to pełna ścieżka docelowego raportu HTML.
# Operator / w pathlib łączy katalog z nazwą pliku.
#
# Dzięki unikalnemu znacznikowi czasu:
# - każdy raport ma własną nazwę,
# - stare raporty nie są nadpisywane,
# - łatwo porównać wyniki z różnych uruchomień.

W = "liczba_zaraportowanych_zakazonych"
# W to nazwa kolumny, która pełni rolę "wagi" / liczby przypadków.
# To kluczowy element analizy.
#
# Dlaczego to ważne?
# W tym zbiorze pojedynczy wiersz nie musi oznaczać 1 przypadku.
# Dlatego wyniki liczymy jako sumę tej kolumny, a nie jako liczbę rekordów.
#
# Trzymanie nazwy kolumny w osobnej zmiennej upraszcza kod:
# - można ją łatwo zmienić,
# - nie trzeba powtarzać nazwy w wielu miejscach,
# - kod jest bardziej spójny.

plt.style.use("seaborn-v0_8-whitegrid")
# Ustawiamy domyślny styl wykresów.
# "seaborn-v0_8-whitegrid" daje:
# - jasne tło,
# - delikatną siatkę,
# - estetyczny wygląd.
#
# Taki styl zwykle poprawia czytelność wykresów w raporcie.

PASTEL = plt.cm.Pastel1(np.linspace(0, 1, 9))
# PASTEL to paleta pastelowych kolorów pobrana z matplotlib.
# np.linspace(0, 1, 9) generuje 9 równomiernie rozmieszczonych punktów
# w przedziale od 0 do 1, co pozwala pobrać 9 kolorów z mapy barw.
#
# Używamy tych kolorów do spokojniejszych, "miękkich" wykresów.

BRIGHT = plt.cm.tab10(np.linspace(0, 1, 10))
# BRIGHT to mocniejsza, bardziej kontrastowa paleta 10 kolorów.
# Jest dobra np. do wielu linii na jednym wykresie,
# bo kolejne serie łatwiej odróżnić.


# ============================================================
# FUNKCJE I KLASY POMOCNICZE
# ============================================================

class Tee:
    """
    Klasa Tee działa jak "rozdzielacz" strumienia wyjścia.

    Chodzi o to, że standardowo print() wysyła tekst do jednego miejsca,
    zwykle do konsoli (sys.stdout).

    Tutaj chcemy osiągnąć dwa cele naraz:
    1) widzieć raport tekstowy na żywo w konsoli,
    2) jednocześnie zapisać ten sam tekst do bufora StringIO,
       aby potem wkleić go do raportu HTML.

    Dlatego obiekt Tee przyjmuje kilka strumieni i każdą wiadomość
    wysyła do wszystkich z nich.
    """

    def __init__(self, *streams):
        # *streams oznacza dowolną liczbę przekazanych strumieni.
        # Przykładowo:
        # Tee(sys.stdout, text_buffer)
        #
        # wtedy self.streams będzie krotką zawierającą:
        # - standardową konsolę,
        # - bufor tekstowy StringIO.
        self.streams = streams

    def write(self, data):
        # Metoda write jest wywoływana przez print() podczas zapisu tekstu.
        # Parametr data to fragment tekstu, który ma zostać wypisany.
        #
        # Iterujemy po wszystkich strumieniach i zapisujemy ten sam tekst
        # do każdego z nich.
        for s in self.streams:
            s.write(data)

    def flush(self):
        # flush wymusza opróżnienie bufora strumienia.
        # To ważne, bo niektóre środowiska wyjściowe buforują tekst.
        #
        # Dzięki flush:
        # - tekst szybciej pojawia się w konsoli,
        # - zapis jest bardziej przewidywalny.
        for s in self.streams:
            s.flush()


def shorten_labels(labels, maxlen=26):
    """
    Skraca zbyt długie etykiety tekstowe.

    Parametry:
    - labels: lista / indeks / iterowalna kolekcja etykiet
    - maxlen: maksymalna długość pojedynczej etykiety

    Po co to robimy?
    Na wykresach, zwłaszcza poziomych słupkach, bardzo długie nazwy:
    - wychodzą poza obszar rysunku,
    - psują układ wykresu,
    - utrudniają czytanie.

    Strategia:
    - jeśli etykieta mieści się w limicie -> zostaje bez zmian,
    - jeśli jest za długa -> przycinamy ją i dopisujemy "...".
    """
    out = []
    # out będzie nową listą skróconych etykiet.

    for x in labels:
        # Iterujemy po wszystkich etykietach wejściowych.

        s = str(x)
        # Zamieniamy każdą etykietę na tekst.
        # To zabezpiecza nas na wypadek, gdyby etykieta była np. liczbą,
        # wartością typu pandas, obiektem itp.

        if len(s) <= maxlen:
            # Jeśli długość etykiety nie przekracza limitu,
            # zachowujemy ją bez zmian.
            out.append(s)
        else:
            # Jeśli etykieta jest zbyt długa:
            # bierzemy jej początek i dodajemy "...".
            #
            # Używamy maxlen - 3, bo trzy znaki zajmie wielokropek.
            out.append(s[:maxlen - 3] + "...")

    return out
    # Zwracamy gotową listę etykiet.


def wrap_labels(labels, width=18):
    """
    Łamie etykiety na kilka linii.

    Parametry:
    - labels: lista etykiet
    - width: maksymalna szerokość jednej linii tekstu

    Po co?
    Niektóre etykiety są długie, ale nie chcemy ich agresywnie ucinać.
    Zamiast tego możemy zawinąć tekst do kilku linii.
    To przydaje się np. w legendzie wykresu kołowego.

    Funkcja fill(...) z textwrap dzieli tekst na linie tak,
    aby każda miała około 'width' znaków.
    """
    return [fill(str(x), width=width) for x in labels]
    # Dla każdej etykiety:
    # - zamieniamy ją na tekst,
    # - zawijamy do zadanej szerokości,
    # - zwracamy listę wyników.


def format_date_axis(ax):
    """
    Formatuje oś X wykresu tak, aby daty były czytelne.

    Parametr:
    - ax: obiekt osi matplotlib (Axes)

    Dlaczego to jest potrzebne?
    Domyślne etykiety dat na osi czasu często:
    - są zbyt gęste,
    - nachodzą na siebie,
    - mają mało czytelny format.

    AutoDateLocator dobiera sensowną liczbę znaczników (ticków),
    a ConciseDateFormatter skraca zapis dat w zależności od skali czasu.
    """
    locator = mdates.AutoDateLocator(minticks=6, maxticks=10)
    # AutoDateLocator automatycznie dobiera pozycje etykiet dat.
    # minticks=6 -> staramy się mieć co najmniej ok. 6 etykiet
    # maxticks=10 -> ale nie więcej niż ok. 10
    #
    # To pomaga zachować czytelność.

    ax.xaxis.set_major_locator(locator)
    # Ustawiamy ten lokalizator jako główny mechanizm rozmieszczania ticków.

    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
    # Ustawiamy zwięzły formatter dat.
    # Dzięki temu np. zamiast pełnej daty przy każdym ticku
    # matplotlib potrafi skrócić zapis do miesięcy / lat / dni,
    # zależnie od kontekstu.


def fig_to_base64(fig):
    """
    Zamienia obiekt wykresu matplotlib (Figure) na tekst base64.

    Parametr:
    - fig: obiekt Figure

    Zwraca:
    - string base64 reprezentujący obraz PNG

    Dlaczego to robimy?
    Chcemy wygenerować jeden samowystarczalny plik HTML,
    bez osobnych obrazów zapisanych na dysku.
    Dlatego:
    1) zapisujemy wykres do pamięci jako PNG,
    2) kodujemy go do base64,
    3) osadzamy bezpośrednio w tagu <img>.
    """
    buf = BytesIO()
    # Tworzymy bajtowy bufor w pamięci.
    # To taki "wirtualny plik", ale bez zapisu na dysk.

    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    # Zapisujemy figurę do bufora:
    # - format="png" -> obraz PNG
    # - dpi=150 -> sensowna jakość do raportu
    # - bbox_inches="tight" -> przycięcie zbędnych marginesów
    #
    # Dzięki temu obraz jest:
    # - czytelny,
    # - zwarty,
    # - dobrze wygląda w HTML.

    plt.close(fig)
    # Zamykamy figurę po zapisaniu.
    # To ważne przy wielu wykresach, bo:
    # - zwalnia pamięć,
    # - zapobiega kumulowaniu "otwartych" figur,
    # - zmniejsza ryzyko warningów matplotlib.

    return base64.b64encode(buf.getvalue()).decode("utf-8")
    # buf.getvalue() pobiera surowe bajty PNG z pamięci.
    # base64.b64encode(...) koduje te bajty do base64.
    # decode("utf-8") zamienia wynik na zwykły tekst (string),
    # który można wkleić do HTML.


def barh_top(series, n=15, title="", xlabel="", color=None):
    """
    Tworzy poziomy wykres słupkowy dla TOP n wartości.

    Parametry:
    - series: pandas Series, gdzie:
      * indeks = nazwy kategorii,
      * wartości = liczby do pokazania
    - n: ile kategorii pokazać
    - title: tytuł wykresu
    - xlabel: opis osi X
    - color: kolor słupków

    Zwraca:
    - obiekt Figure albo None, jeśli brak danych

    Dlaczego wykres poziomy (barh)?
    Dla kategorii tekstowych jest zwykle czytelniejszy niż pionowy,
    szczególnie gdy nazwy są długie.
    """
    s = series.dropna().sort_values(ascending=False).head(n).sort_values()
    # Krok po kroku:
    # 1) dropna() -> usuwa brakujące wartości
    # 2) sort_values(ascending=False) -> sortuje malejąco,
    #    czyli największe wartości na początku
    # 3) head(n) -> bierze TOP n kategorii
    # 4) sort_values() -> ponownie sortuje rosnąco,
    #    żeby na barh największy słupek był "na górze końcowej części"
    #    i wykres wyglądał estetycznie

    if len(s) == 0:
        # Jeśli po odrzuceniu braków i przycięciu nie ma żadnych danych,
        # nie próbujemy rysować pustego wykresu.
        return None

    labels = shorten_labels(s.index, 30)
    # Skracamy etykiety kategorii, żeby nie były zbyt długie na osi Y.

    fig_h = max(4, 0.35 * len(s) + 1)
    # Dynamicznie dobieramy wysokość wykresu.
    # Im więcej słupków, tym większa wysokość, aby się nie zlewały.
    # Minimalna wysokość to 4 cale.

    fig, ax = plt.subplots(figsize=(10, fig_h))
    # Tworzymy figurę i jedną oś.
    # Szerokość = 10, wysokość zależna od liczby kategorii.

    ax.barh(labels, s.values, color=color)
    # Rysujemy poziome słupki:
    # - labels -> etykiety na osi Y
    # - s.values -> wartości słupków
    # - color -> kolor

    ax.set_title(title)
    # Ustawiamy tytuł wykresu.

    ax.set_xlabel(xlabel)
    # Ustawiamy podpis osi X.

    fig.tight_layout()
    # Automatycznie dopasowujemy marginesy,
    # żeby tekst i osie się nie ucinały.

    return fig
    # Zwracamy figurę do dalszego użycia
    # (konwersja do base64 i osadzenie w HTML).


def pie_with_legend(series, top_n=6, title="", donut=True, colors=None):
    """
    Tworzy wykres kołowy z legendą, opcjonalnie w formie donut.

    Parametry:
    - series: pandas Series (indeks = kategorie, wartości = liczby)
    - top_n: ile największych kategorii pokazać osobno
    - title: tytuł wykresu
    - donut: jeśli True, rysujemy środek jako białe koło
    - colors: lista kolorów

    Zwraca:
    - obiekt Figure albo None

    Dlaczego ograniczamy do top_n?
    Wykresy kołowe źle wyglądają przy zbyt dużej liczbie kategorii.
    Dlatego:
    - pokazujemy największe kategorie osobno,
    - resztę łączymy do kategorii "Inne".
    """
    s = series.dropna().sort_values(ascending=False)
    # Czyścimy dane:
    # - usuwamy braki,
    # - sortujemy malejąco, aby największe kategorie były pierwsze.

    if len(s) == 0:
        # Jeśli nie ma danych, nie rysujemy wykresu.
        return None

    head = s.head(top_n).copy()
    # Bierzemy top_n największych kategorii.
    # copy() tworzy niezależną kopię,
    # żeby można było bezpiecznie modyfikować wynik.

    rest = s.iloc[top_n:].sum()
    # Sumujemy wszystkie pozostałe kategorie poza top_n.

    if rest > 0:
        # Jeśli istnieją jakieś dodatkowe kategorie poza top_n,
        # dodajemy je jako jeden wspólny segment "Inne".
        head.loc["Inne"] = rest

    labels = wrap_labels(shorten_labels(head.index, 22), width=18)
    # Etykiety przygotowujemy dwuetapowo:
    # 1) shorten_labels -> przycięcie bardzo długich nazw,
    # 2) wrap_labels -> zawinięcie tekstu do kilku linii.
    #
    # Dzięki temu legenda jest czytelniejsza.

    fig, ax = plt.subplots(figsize=(9, 6))
    # Tworzymy figurę i jedną oś dla wykresu kołowego.

    wedges, _, _ = ax.pie(
        head.values,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors
    )
    # ax.pie(...) rysuje wykres kołowy.
    #
    # head.values -> wartości segmentów
    # autopct="%1.1f%%" -> na wykresie pokaż procent z 1 miejscem po przecinku
    # startangle=90 -> zaczynamy od góry, co zwykle wygląda estetyczniej
    # colors=colors -> przypisujemy kolory segmentom
    #
    # Zwracane są:
    # - wedges -> obiekty segmentów koła
    # - drugi i trzeci element ignorujemy (_,_)

    ax.legend(
        wedges,
        labels,
        loc="center left",
        bbox_to_anchor=(1.0, 0.5),
        frameon=False
    )
    # Dodajemy legendę:
    # - wedges -> elementy odpowiadające kolorom
    # - labels -> tekstowe opisy kategorii
    # - loc="center left" -> punkt zaczepienia legendy
    # - bbox_to_anchor=(1.0, 0.5) -> przesunięcie legendy na prawo od wykresu
    # - frameon=False -> bez ramki

    if donut:
        ax.add_artist(plt.Circle((0, 0), 0.62, fc="white"))
        # Jeśli donut=True, rysujemy białe koło w środku.
        # To daje efekt "pierścienia" zamiast pełnego wykresu kołowego.
        #
        # Parametry:
        # - środek (0,0)
        # - promień 0.62
        # - fc="white" -> wypełnienie białe

    ax.set_title(title)
    # Ustawiamy tytuł wykresu.

    fig.tight_layout()
    # Dopasowanie układu, aby nic się nie ucinało.

    return fig
    # Zwracamy figurę.


# ============================================================
# GŁÓWNA FUNKCJA EDA
# ============================================================

def run_eda():
    """
    Główna funkcja wykonująca analizę eksploracyjną danych (EDA).

    Zwraca:
    - text_buffer.getvalue() -> cały raport tekstowy jako jeden string
    - images -> listę par (tytuł_wykresu, obraz_base64)

    Schemat działania funkcji:
    1) tworzy bufor na tekst raportu,
    2) tworzy listę na wykresy,
    3) wczytuje dane,
    4) przygotowuje i czyści kolumny,
    5) liczy podstawowe statystyki i agregaty,
    6) tworzy wykresy,
    7) zwraca gotowy materiał do wstawienia do HTML.
    """
    text_buffer = StringIO()
    # StringIO będzie przechowywać wszystkie printy.
    # Dzięki temu raport tekstowy możemy później wkleić do HTML jako <pre>...</pre>.

    images = []
    # Lista na wykresy.
    # Każdy element będzie miał formę:
    # ("Tytuł wykresu", "ciąg_base64_obrazu")

    with redirect_stdout(Tee(sys.stdout, text_buffer)):
        # Ten blok powoduje, że każdy print:
        # - pokaże się w konsoli (sys.stdout),
        # - jednocześnie zapisze do text_buffer.
        #
        # To kluczowy mechanizm, dzięki któremu:
        # - widzisz raport "na żywo",
        # - i jednocześnie masz go w raporcie HTML.

        print("=" * 80)
        # Dekoracyjna linia oddzielająca nagłówek raportu.

        print("RAPORT EDA - COVID: ZAKAŻENIA PO SZCZEPIENIU")
        # Główny tytuł raportu tekstowego.

        print("Plik wejściowy:", INPUT_PATH.resolve())
        # resolve() zwraca pełną, absolutną ścieżkę do pliku.
        # To przydatne, bo w raporcie od razu widać,
        # z którego dokładnie pliku pochodzi analiza.

        print("Data i godzina analizy:", ANALYSIS_TIME.strftime("%Y-%m-%d_%H-%M-%S"))
        # Wypisujemy moment wykonania analizy.
        # To przydaje się np. gdy raportów jest kilka.

        print("=" * 80)
        # Zamknięcie sekcji nagłówkowej.


        # ------------------------------------------------------------
        # WCZYTANIE DANYCH
        # ------------------------------------------------------------
        try:
            df = pd.read_csv(INPUT_PATH, encoding="cp1250", low_memory=False)
            # Próbujemy wczytać CSV z kodowaniem cp1250.
            # To częste kodowanie dla polskich plików CSV tworzonych np. w Excelu
            # lub systemach działających w środowisku Windows.
            #
            # low_memory=False:
            # pandas domyślnie potrafi czytać plik partiami i zgadywać typy,
            # co czasem prowadzi do ostrzeżeń lub niespójnych typów.
            # Ustawienie False każe mu przeczytać spójniej cały plik.

            used_encoding = "cp1250"
            # Zapamiętujemy informację, jakie kodowanie zadziałało.

        except UnicodeDecodeError:
            # Jeśli odczyt cp1250 się nie powiedzie, próbujemy utf-8.
            # To częsty fallback dla współczesnych plików tekstowych.

            df = pd.read_csv(INPUT_PATH, encoding="utf-8", low_memory=False)
            used_encoding = "utf-8"

        print("\n=== WCZYTANIE ===")
        # Nagłówek sekcji opisującej wczytanie danych.

        print("Użyte kodowanie", used_encoding)
        # Pokazujemy, które kodowanie zadziałało.

        print("Rozmiar (wiersz, kolumny):", df.shape)
        # df.shape zwraca krotkę:
        # (liczba_wierszy, liczba_kolumn)

        print("Kolumny:", df.columns.tolist())
        # Wypisujemy listę nazw kolumn.
        # To ważna kontrola struktury danych.

        print("\nPierwsze 5 wierszy:\n", df.head())
        # Pokazujemy pierwsze 5 rekordów.
        # To szybki podgląd danych:
        # - czy kolumny wyglądają sensownie,
        # - czy wartości są poprawnie wczytane,
        # - czy nie ma dziwnych przesunięć lub błędów separatorów.


        # ------------------------------------------------------------
        # PRZYGOTOWANIE DANYCH
        # ------------------------------------------------------------
        if "data_rap_zakazenia" in df.columns:
            # Sprawdzamy, czy kolumna z datą istnieje.
            # Dzięki temu kod jest odporny:
            # jeśli kolumny zabraknie, skrypt nie wywali błędu.

            df["data_rap_zakazenia"] = pd.to_datetime(df["data_rap_zakazenia"], errors="coerce")
            # Zamieniamy tekstową kolumnę dat na typ datetime.
            # errors="coerce" oznacza:
            # - jeśli jakaś wartość nie da się zinterpretować jako data,
            #   zostanie zamieniona na NaT (odpowiednik brakującej daty).
            #
            # To bezpieczniejsze niż errors="raise", bo pojedynczy zły wpis
            # nie zatrzyma całej analizy.

            df["miesiac"] = df["data_rap_zakazenia"].dt.to_period("M").dt.to_timestamp()
            # Tworzymy dodatkową kolumnę "miesiac", która reprezentuje miesiąc raportowania.
            #
            # Krok po kroku:
            # - .dt.to_period("M") -> zamienia datę na okres miesięczny, np. 2022-01
            # - .dt.to_timestamp() -> zamienia ten okres z powrotem na timestamp,
            #   zwykle pierwszy dzień danego miesiąca
            #
            # Dzięki temu łatwo grupować dane po miesiącach.

        if W in df.columns:
            # Sprawdzamy, czy istnieje kolumna wag/liczby przypadków.

            df[W] = pd.to_numeric(df[W], errors="coerce").fillna(0)
            # Zamieniamy kolumnę na typ liczbowy.
            # errors="coerce" -> błędne wpisy zamienią się na NaN.
            # fillna(0) -> braki w tej kolumnie zastępujemy zerem.
            #
            # To istotne, bo potem sumujemy tę kolumnę.
            # Braki traktujemy tu jako 0, aby nie psuły agregacji.

            total_cases = float(df[W].sum())
            # Łączna liczba zakażeń to suma kolumny W.
            # Rzutujemy na float, aby mieć pewność spójnego typu liczbowego.

        else:
            # Jeśli kolumny W nie ma, stosujemy plan awaryjny:
            # traktujemy liczbę wierszy jako liczbę obserwacji.
            #
            # To mniej poprawne merytorycznie dla tego zbioru,
            # ale pozwala skryptowi działać dalej.
            total_cases = float(len(df))

        if "producent" in df.columns:
            df["producent2"] = df["producent"].fillna("brak informacji")
            # Tworzymy pomocniczą kolumnę producent2.
            # Zamiast pozostawiać NaN, wpisujemy tekst "brak informacji".
            #
            # Dlaczego nowa kolumna zamiast nadpisania starej?
            # - zachowujemy oryginalne dane,
            # - możemy równolegle mieć wersję "surową" i "raportową".

        if "dawka_ost" in df.columns:
            df["dawka2"] = df["dawka_ost"].fillna("brak informacji")
            # Analogicznie przygotowujemy kolumnę dawka2,
            # aby braki nie znikały z agregacji.

        if "plec" in df.columns:
            df["plec2"] = df["plec"].fillna("nieznana")
            # To samo dla płci.
            # Dzięki temu osoby z brakującą płcią są nadal uwzględnione
            # jako osobna kategoria "nieznana".

        woj_map = {
            2: "dolnośląskie",
            4: "kujawsko-pomorskie",
            6: "lubelskie",
            8: "lubuskie",
            10: "łódzkie",
            12: "małopolskie",
            14: "mazowieckie",
            16: "opolskie",
            18: "podkarpackie",
            20: "podlaskie",
            22: "pomorskie",
            24: "śląskie",
            26: "świętokrzyskie",
            28: "warmińsko-mazurskie",
            30: "wielkopolskie",
            32: "zachodniopomorskie"
        }
        # Słownik mapujący kody województw TERYT na pełne nazwy.
        #
        # W danych często występują kody liczbowe, ale do raportu
        # lepiej nadają się nazwy tekstowe.

        if "teryt_woj" in df.columns:
            df["woj"] = pd.to_numeric(df["teryt_woj"], errors="coerce").astype("Int64")
            # Zamieniamy kody województw na typ liczbowy.
            # errors="coerce" -> błędne wartości staną się NaN.
            # astype("Int64") -> używamy pandasowego typu całkowitego z obsługą braków.
            #
            # To ważne, bo zwykły int nie obsługuje NaN.

            df["woj_nazwa"] = df["woj"].map(woj_map)
            # Na podstawie kodu województwa tworzymy nazwę województwa.
            # Jeśli kod nie istnieje w mapie albo jest pusty,
            # wynik będzie NaN.


        # ------------------------------------------------------------
        # PODSTAWOWE INFO
        # ------------------------------------------------------------
        print("\n=== PODSTAWOWE INFO ===")
        # Nagłówek podstawowej sekcji opisowej.

        print("Łączna liczba zakażeń (suma wag):", int(total_cases))
        # Wypisujemy sumę wag jako całkowitą liczbę przypadków.

        if "data_rap_zakazenia" in df.columns:
            print("Zakres dat:", df["data_rap_zakazenia"].min(), " -> ", df["data_rap_zakazenia"].max())
            # Pokazujemy minimalną i maksymalną datę w danych.
            # To informacja, jaki okres obejmuje analiza.


        # ------------------------------------------------------------
        # ANALIZA BRAKÓW DANYCH
        # ------------------------------------------------------------
        missing = df.isna().sum()
        # df.isna() tworzy tabelę True/False dla braków.
        # .sum() po kolumnach liczy, ile braków jest w każdej kolumnie.

        missing_pct = (missing / len(df) * 100).round(2)
        # Obliczamy procent braków:
        # liczba_braków / liczba_wierszy * 100
        # .round(2) -> zaokrąglamy do 2 miejsc po przecinku.

        missing_table = (
            pd.DataFrame({"braki": missing, "braki_%": missing_pct})
            .sort_values("braki", ascending=False)
        )
        # Tworzymy tabelę z dwiema kolumnami:
        # - liczba braków
        # - procent braków
        # Następnie sortujemy malejąco po liczbie braków,
        # aby najważniejsze problemy były na górze.

        print("\n=== BRAKI DANYCH (TOP 20) ===")
        print(missing_table.head(20))
        # Wypisujemy 20 kolumn z największą liczbą braków.

        top = missing_table.head(20).iloc[::-1]
        # Bierzemy TOP 20, ale odwracamy kolejność.
        # Dzięki temu na wykresie poziomym barh największe wartości
        # będą na "górze listy" w naturalnym porządku wizualnym.

        fig, ax = plt.subplots(figsize=(10, 6))
        # Tworzymy wykres braków danych.

        ax.barh(shorten_labels(top.index, 32), top["braki_%"].values, color=PASTEL[0])
        # Rysujemy poziome słupki:
        # - etykiety = nazwy kolumn
        # - wartości = procent braków
        # - kolor = pastelowy

        ax.set_title("TOP 20 kolumn wg % braków")
        ax.set_xlabel("% braków")
        # Opisujemy wykres.

        fig.tight_layout()
        # Dopasowanie marginesów.

        images.append(("TOP 20 kolumn wg % braków", fig_to_base64(fig)))
        # Konwertujemy figurę do base64 i zapisujemy do listy obrazów
        # wraz z tytułem sekcji.


        # ------------------------------------------------------------
        # TREND DZIENNY
        # ------------------------------------------------------------
        if "data_rap_zakazenia" in df.columns and W in df.columns:
            # Sekcję wykonujemy tylko wtedy, gdy mamy:
            # - datę,
            # - kolumnę wag/liczby przypadków.

            daily = df.groupby("data_rap_zakazenia")[W].sum().sort_index()
            # Grupujemy dane po dacie i sumujemy liczbę zakażeń dla każdego dnia.
            # sort_index() zapewnia porządek chronologiczny.

            roll7 = daily.rolling(7).mean()
            # Liczymy 7-dniową średnią kroczącą.
            #
            # Po co?
            # Dzienne dane mają zwykle duży szum raportowania:
            # - weekendy,
            # - opóźnienia,
            # - nieregularności administracyjne.
            #
            # Średnia 7D wygładza ten szum i pokazuje trend.

            print("\n=== SZCZYT DZIENNY ===")
            print("Data szczytu:", daily.idxmax(), "| Liczba:", int(daily.max()))
            # daily.idxmax() -> data z największą wartością
            # daily.max() -> największa liczba przypadków dziennych

            fig, ax = plt.subplots(figsize=(12, 5))
            # Tworzymy figurę dla wykresu trendu dziennego.

            ax.plot(daily.index, daily.values, linewidth=1.0, color=BRIGHT[3], label="Dziennie")
            # Cieńsza linia dla surowych danych dziennych.

            ax.plot(roll7.index, roll7.values, linewidth=2.5, color=BRIGHT[0], label="Średnia 7D")
            # Grubsza linia dla wygładzonego trendu.

            format_date_axis(ax)
            # Formatujemy oś dat.

            ax.set_title("Zakażenia dzienne + 7-dniowa średnia")
            ax.set_xlabel("Data")
            ax.set_ylabel("Liczba zakażeń")
            # Ustawiamy opisy.

            ax.legend(frameon=False)
            # Pokazujemy legendę bez ramki.

            fig.tight_layout()
            images.append(("Zakażenia dzienne + 7-dniowa średnia", fig_to_base64(fig)))
            # Dodajemy wykres do raportu.


        # ------------------------------------------------------------
        # TREND MIESIĘCZNY
        # ------------------------------------------------------------
        if "miesiac" in df.columns and W in df.columns:
            # Sekcja miesięczna wymaga kolumny pomocniczej "miesiac"
            # oraz kolumny z wagą/liczbą przypadków.

            monthly = df.groupby("miesiac")[W].sum().sort_index()
            # Grupujemy przypadki po miesiącu i sumujemy wartości.
            # sort_index() zapewnia chronologiczną kolejność miesięcy.

            print("\n=== MIESIĘCZNE SUMY (TOP 10) ===")
            print(monthly.sort_values(ascending=False).head(10))
            # Wypisujemy 10 miesięcy z największą liczbą przypadków.

            fig, ax = plt.subplots(figsize=(12, 5))
            ax.plot(monthly.index, monthly.values, linewidth=3.0, color=PASTEL[1])
            # Rysujemy liniowy przebieg miesięczny.

            format_date_axis(ax)
            # Formatujemy daty na osi X.

            ax.set_title("Zakażenia miesięczne")
            ax.set_ylabel("Liczba zakażeń")
            ax.set_xlabel("Miesiąc")
            # Opisy wykresu.

            fig.tight_layout()
            images.append(("Zakażenia miesięczne", fig_to_base64(fig)))
            # Dodajemy wykres do HTML.


        # ------------------------------------------------------------
        # PŁEĆ
        # ------------------------------------------------------------
        if "plec2" in df.columns and W in df.columns:
            # Analiza płci wymaga:
            # - przygotowanej kolumny plec2,
            # - kolumny wag.

            sex = df.groupby("plec2")[W].sum().sort_values(ascending=False)
            # Sumujemy zakażenia wg płci i sortujemy malejąco.

            print("\n=== PŁEĆ (udział % ) ===")
            print((sex / total_cases * 100).round(2).rename("procent_%"))
            # Przeliczamy udziały procentowe:
            # udział = liczba przypadków danej płci / liczba wszystkich przypadków * 100

            fig = pie_with_legend(
                sex,
                top_n=5,
                title="Zakażenia wg płci (donut)",
                donut=True,
                colors=BRIGHT[:7]
            )
            # Tworzymy wykres kołowy typu donut.

            if fig is not None:
                images.append(("Zakażenia wg płci (donut)", fig_to_base64(fig)))
                # Jeśli wykres powstał, dodajemy go do raportu.


        # ------------------------------------------------------------
        # KATEGORIE WIEKU
        # ------------------------------------------------------------
        if "kat_wiek" in df.columns and W in df.columns:
            # Sekcja analizująca z góry przygotowane kategorie wieku.

            age_cat = df.groupby("kat_wiek")[W].sum().sort_values(ascending=False)
            # Sumujemy przypadki w każdej kategorii wieku.

            print("\n=== KATEGORIA WIEKU (TOP 10) ===")
            print(age_cat.head(10).astype(int))
            # Wypisujemy 10 największych kategorii wiekowych.

            fig = barh_top(
                age_cat,
                n=15,
                title="Zakażenia wg kategorii wieku (TOP 15)",
                xlabel="Liczba zakażeń",
                color=PASTEL[2]
            )
            # Tworzymy wykres poziomy dla 15 największych kategorii.

            if fig is not None:
                images.append(("Zakażenia wg kategorii wieku (TOP 15)", fig_to_base64(fig)))


        # ------------------------------------------------------------
        # WIEK LICZBOWY
        # ------------------------------------------------------------
        if "wiek" in df.columns:
            # Ta sekcja dotyczy surowego wieku liczbowego.

            age_num = pd.to_numeric(df["wiek"], errors="coerce").dropna()
            # Zamieniamy kolumnę wiek na wartości liczbowe.
            # Niepoprawne wpisy -> NaN.
            # dropna() usuwa braki.
            #
            # W efekcie age_num zawiera tylko poprawne wartości liczbowe.

            print("\n=== WIEK (statystyki) ===")

            if len(age_num) > 0:
                # Jeśli są jakiekolwiek poprawne dane wieku, liczymy statystyki.

                print(age_num.describe())
                # describe() zwraca podstawowe statystyki:
                # - count
                # - mean
                # - std
                # - min
                # - 25%
                # - 50% (mediana)
                # - 75%
                # - max

                print("Ile <0 lub >110:", int(((age_num < 0) | (age_num > 110)).sum()))
                # Dodatkowa kontrola jakości:
                # liczymy wartości podejrzane, np. poniżej 0 lub powyżej 110 lat.

                fig, ax = plt.subplots(figsize=(10, 5))
                ax.hist(age_num, bins=40, edgecolor="black", alpha=0.9, color=PASTEL[3])
                # Histogram rozkładu wieku:
                # - bins=40 -> liczba koszyków histogramu
                # - edgecolor="black" -> czarne obramowania słupków
                # - alpha=0.9 -> lekka przezroczystość
                # - color -> kolor pastelowy

                ax.set_title("Histogram wieku")
                ax.set_xlabel("Wiek")
                ax.set_ylabel("Liczba rekordów")
                fig.tight_layout()
                images.append(("Histogram wieku", fig_to_base64(fig)))
                # Dodajemy histogram do raportu.

                fig, ax = plt.subplots(figsize=(6, 4))
                bp = ax.boxplot(age_num.values, vert=True, patch_artist=True)
                # Tworzymy boxplot wieku.
                #
                # age_num.values -> surowe wartości liczbowe
                # vert=True -> pionowy boxplot
                # patch_artist=True -> pozwala wypełnić pudełko kolorem

                for box in bp["boxes"]:
                    box.set_facecolor(PASTEL[4])
                    # Kolorujemy pudełko boxplota,
                    # aby wykres był spójny wizualnie.

                ax.set_title("Boxplot wieku")
                ax.set_ylabel("Wiek")
                fig.tight_layout()
                images.append(("Boxplot wieku", fig_to_base64(fig)))
                # Dodajemy boxplot do raportu.

            else:
                print("[POMINIĘTO] brak danych w 'wiek'")
                # Jeśli po czyszczeniu nie ma żadnych poprawnych wartości,
                # informujemy o pominięciu sekcji.


        # ------------------------------------------------------------
        # PRODUCENT SZCZEPIONKI
        # ------------------------------------------------------------
        if "producent2" in df.columns and W in df.columns:
            # Analiza producenta wymaga kolumny producent2 i wagi.

            prod = df.groupby("producent2")[W].sum().sort_values(ascending=False)
            # Sumujemy zakażenia wg producenta.

            prod_known = prod.drop(index=["brak informacji"], errors="ignore")
            # Tworzymy wersję bez kategorii "brak informacji".
            # errors="ignore" oznacza, że jeśli takiej kategorii nie ma,
            # pandas nie zgłosi błędu.

            print("\n=== PRODUCENT (ZNANI) TOP 10 ===")
            print(prod_known.head(10))
            # Wypisujemy 10 największych kategorii producenta
            # po usunięciu braków.

            fig = barh_top(
                prod_known,
                n=10,
                title="Zakażenia wg producenta (bez brak informacji)",
                xlabel="Liczba zakażeń",
                color=PASTEL[2]
            )
            # Wykres poziomy TOP 10 producentów.

            if fig is not None:
                images.append(("Zakażenia wg producenta (bez brak informacji)", fig_to_base64(fig)))


        # ------------------------------------------------------------
        # RODZAJ DAWKI
        # ------------------------------------------------------------
        if "dawka2" in df.columns and W in df.columns:
            # Analiza dawki wymaga kolumny dawka2 i kolumny wagi.

            dose = df.groupby("dawka2")[W].sum().sort_values(ascending=False)
            # Sumujemy przypadki wg rodzaju dawki / statusu dawki.

            print("\n=== DAWKA (udział %) ===")
            print((dose / total_cases * 100).round(2).rename("procent_%"))
            # Wypisujemy udział procentowy każdej kategorii dawki.

            fig = pie_with_legend(
                dose,
                top_n=6,
                title="Zakażenia wg dawki (donut)",
                donut=True,
                colors=BRIGHT[:7]
            )
            # Tworzymy wykres kołowy typu donut.

            if fig is not None:
                images.append(("Zakażenia wg dawki (donut)", fig_to_base64(fig)))


        # ------------------------------------------------------------
        # WOJEWÓDZTWA
        # ------------------------------------------------------------
        if "woj_nazwa" in df.columns and W in df.columns:
            # Analiza geograficzna wg województw.

            woj = df.groupby("woj_nazwa")[W].sum().sort_values(ascending=False)
            # Sumujemy przypadki wg nazw województw.

            print("\n=== WOJEWÓDZTWA TOP 10 ===")
            print(woj.head(10))
            # Wypisujemy TOP 10 województw.

            fig = barh_top(
                woj,
                n=10,
                title="Top 10 województw wg zakażeń",
                xlabel="Liczba zakażeń",
                color=PASTEL[2]
            )
            # Rysujemy poziomy wykres TOP 10 województw.

            if fig is not None:
                images.append(("Top 10 województw", fig_to_base64(fig)))


        # ------------------------------------------------------------
        # TOP 5 WOJEWÓDZTW - TREND MIESIĘCZNY
        # ------------------------------------------------------------
        if "woj_nazwa" in df.columns and "miesiac" in df.columns and W in df.columns:
            # Ta sekcja wymaga:
            # - nazwy województwa,
            # - miesiąca,
            # - wagi przypadków.

            woj_total = df.groupby("woj_nazwa")[W].sum().sort_values(ascending=False)
            # Liczymy całkowitą liczbę przypadków w każdym województwie.

            top5 = woj_total.head(5).index.tolist()
            # Pobieramy nazwy 5 województw z największą liczbą przypadków.

            pivot = (
                df[df["woj_nazwa"].isin(top5)]
                .groupby(["miesiac", "woj_nazwa"])[W]
                .sum()
                .unstack(fill_value=0)
                .sort_index()
            )
            # Tworzymy tabelę przestawną (pivot) z układem:
            # - wiersze: miesiące
            # - kolumny: województwa
            # - wartości: suma przypadków
            #
            # Krok po kroku:
            # 1) df[df["woj_nazwa"].isin(top5)] -> zostawiamy tylko TOP 5 województw
            # 2) groupby(["miesiac", "woj_nazwa"])[W].sum() -> agregujemy po miesiącu i województwie
            # 3) unstack(fill_value=0) -> zamieniamy jeden poziom indeksu na kolumny
            #    i brakujące kombinacje uzupełniamy zerem
            # 4) sort_index() -> porządek chronologiczny po miesiącach

            fig, ax = plt.subplots(figsize=(12, 6))
            # Tworzymy figurę dla wieloliniowego wykresu trendu.

            for i, col in enumerate(pivot.columns):
                # Iterujemy po kolejnych województwach (kolumnach tabeli pivot).
                ax.plot(
                    pivot.index,
                    pivot[col].values,
                    linewidth=2.5,
                    label=str(col),
                    color=BRIGHT[i % len(BRIGHT)]
                )
                # Rysujemy linię dla każdego województwa:
                # - X = miesiące
                # - Y = liczba zakażeń
                # - label = nazwa województwa
                # - color = kolejny kolor z palety
                #
                # i % len(BRIGHT) zabezpiecza nas, gdyby serii było więcej niż kolorów.

            format_date_axis(ax)
            # Formatujemy oś dat.

            ax.legend(loc="upper left", frameon=False)
            # Dodajemy legendę.

            ax.set_title("Top 5 województw - trend miesięczny")
            ax.set_xlabel("Miesiąc")
            ax.set_ylabel("Liczba zakażeń")
            # Opisujemy osie i tytuł.

            fig.tight_layout()
            images.append(("Top 5 województw - trend miesięczny", fig_to_base64(fig)))
            # Dodajemy wykres do raportu.


        # ------------------------------------------------------------
        # PODSUMOWANIE TEKSTOWE
        # ------------------------------------------------------------
        print("\n" + "=" * 80)
        print("PODSUMOWANIE KLUCZOWYCH ELEMENTÓW")
        # Sekcja końcowego podsumowania raportu tekstowego.

        print("1) Waga danych:", W, "-> wyniki liczymy jako sumę tej kolumny, nie liczbę wierszy")
        # Przypomnienie najważniejszej zasady interpretacji.

        print("2) Największe ograniczenie: braki danych w niektórych kolumnach (sprawdź tabelę braków)")
        # Informacja o głównym ograniczeniu jakości danych.

        print("3) Trend dzienny + 7-dniowa średnia pokazuje fale i redukuje szum raportowania")
        # Krótkie wyjaśnienie, po co był liczony wykres trendu.

        print("4) Rozkłady: płeć, wiek, dawki, geografia")
        # Krótkie przypomnienie głównych przekrojów analizy.

        print("\n" + "=" * 80)
        # Zamyka część tekstową.

    return text_buffer.getvalue(), images
    # Po wyjściu z bloku redirect_stdout:
    # - text_buffer zawiera cały raport tekstowy,
    # - images zawiera wszystkie wygenerowane wykresy w base64.
    #
    # Zwracamy oba elementy do dalszego składania raportu HTML.


# ============================================================
# GENEROWANIE RAPORTU HTML
# ============================================================

text, images = run_eda()
# Uruchamiamy całą analizę.
#
# Wynikiem są:
# - text   -> raport tekstowy jako string
# - images -> lista wykresów w postaci base64

html_parts = []
# Tworzymy listę fragmentów HTML.
# Zamiast budować jeden bardzo długi string od razu,
# wygodniej dokładać kolejne części do listy,
# a na końcu połączyć je "\n".join(...).

html_parts.append("<html>")
# Otwieramy dokument HTML.

html_parts.append("<head>")
# Otwieramy sekcję <head>, w której umieszczamy metadane i styl.

html_parts.append("<meta charset='utf-8'>")
# Ustawiamy kodowanie UTF-8.
# To bardzo ważne przy polskich znakach.

html_parts.append("<title>EDA report</title>")
# Tytuł strony widoczny np. na karcie przeglądarki.

html_parts.append("""
<style>
body {
    font-family: Arial, sans-serif;
    margin: 30px;
    line-height: 1.45;
}
pre {
    white-space: pre-wrap;
    font-family: Consolas, monospace;
    background: #f7f7f7;
    border: 1px solid #ddd;
    padding: 14px;
    border-radius: 8px;
}
img {
    max-width: 100%;
    height: auto;
    border: 1px solid #ddd;
    margin-bottom: 24px;
}
h1, h2, h3 {
    color: #222;
}
hr {
    margin: 28px 0;
}
</style>
""")
# Wstawiamy prosty CSS bezpośrednio do pliku HTML.
#
# Co robi styl?
# - body:
#   * Arial -> czytelna czcionka
#   * margin: 30px -> odstęp od krawędzi strony
#   * line-height: 1.45 -> większa czytelność tekstu
#
# - pre:
#   * white-space: pre-wrap -> zachowuje układ tekstu, ale pozwala zawijać linie
#   * Consolas -> czcionka monospace dla raportu tekstowego
#   * tło, ramka, padding, zaokrąglenia -> estetyczne pudełko
#
# - img:
#   * max-width: 100% -> obraz nie wyjdzie poza szerokość strony
#   * height: auto -> zachowuje proporcje
#   * border -> delikatna ramka
#   * margin-bottom -> odstęp między wykresami
#
# - h1, h2, h3:
#   * lekko ciemniejszy kolor nagłówków
#
# - hr:
#   * większe odstępy pionowe

html_parts.append("</head>")
# Zamykamy sekcję <head>.

html_parts.append("<body>")
# Otwieramy treść raportu HTML.

html_parts.append("<h1>EDA report</h1>")
# Główny nagłówek strony.

html_parts.append(f"<p><b>Data i godzina:</b> {ANALYSIS_TIME.strftime('%Y-%m-%d %H:%M:%S')}</p>")
# Pokazujemy czas wykonania analizy.
# Używamy formatu bardziej "czytelnego dla człowieka" niż w nazwie pliku.

html_parts.append(f"<p><b>Plik:</b> {html.escape(str(INPUT_PATH.resolve()))}</p>")
# Pokazujemy pełną ścieżkę wejściowego pliku.
# html.escape(...) zabezpiecza tę ścieżkę, gdyby zawierała znaki specjalne.

html_parts.append("<hr>")
# Linia oddzielająca metadane od właściwego raportu.

html_parts.append("<h2>Wyniki tekstowe</h2>")
# Nagłówek sekcji z raportem tekstowym.

html_parts.append("<pre>")
# Otwieramy blok <pre>, który zachowuje układ tekstu i spacje.

html_parts.append(html.escape(text))
# Wstawiamy cały raport tekstowy do HTML.
# Używamy html.escape(...), aby np. znaki < i > nie zostały
# zinterpretowane jako znaczniki HTML.

html_parts.append("</pre>")
# Zamykamy blok pre.

html_parts.append("<hr>")
# Linia oddzielająca sekcję tekstową od wykresów.

html_parts.append("<h2>Wykresy</h2>")
# Nagłówek sekcji wykresów.

for title, b64 in images:
    # Iterujemy po wszystkich wykresach zapisanych wcześniej w liście images.
    # Każdy element to:
    # - title -> tytuł sekcji/wykresu
    # - b64 -> obraz zakodowany w base64

    html_parts.append(f"<h3>{html.escape(title)}</h3>")
    # Dodajemy tytuł wykresu jako nagłówek niższego poziomu.
    # html.escape(...) zabezpiecza tekst.

    html_parts.append(
        f"<img src='data:image/png;base64,{b64}' alt='{html.escape(title)}'>"
    )
    # Dodajemy sam obraz.
    #
    # src='data:image/png;base64,...'
    # oznacza, że obraz jest zapisany bezpośrednio w treści HTML.
    #
    # alt=... dodaje opis alternatywny:
    # - przydatny dla dostępności,
    # - widoczny np. gdy obraz się nie załaduje.

html_parts.append("</body></html>")
# Zamykamy dokument HTML.

REPORT_HTML.write_text("\n".join(html_parts), encoding="utf-8")
# Sklejamy wszystkie fragmenty HTML w jeden tekst
# i zapisujemy do pliku.
#
# "\n".join(html_parts) dodaje przejścia do nowej linii,
# co poprawia czytelność wygenerowanego źródła HTML.
#
# encoding="utf-8" zapewnia poprawny zapis polskich znaków.

print(f"\nGotowe - plik z ANALIZĄ EDA COVID zapisany: {REPORT_HTML.resolve()}")
# Końcowa informacja dla użytkownika:
# - raport został wygenerowany,
# - pokazujemy jego pełną ścieżkę.

