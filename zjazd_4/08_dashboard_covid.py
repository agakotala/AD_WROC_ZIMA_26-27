from typing import Any  # Importujemy typ Any, który oznacza dowolny typ danych; używany jest tutaj w adnotacji typu funkcji.
import pandas as pd  # Importujemy bibliotekę pandas jako pd; służy do pracy z danymi tabelarycznymi, np. DataFrame i CSV.
import numpy as np  # Importujemy bibliotekę numpy jako np; służy m.in. do obliczeń numerycznych i obsługi wartości NaN.
import streamlit as st  # Importujemy bibliotekę Streamlit jako st; służy do tworzenia interaktywnych aplikacji webowych w Pythonie.
import plotly.express as px  # Importujemy Plotly Express jako px; służy do tworzenia interaktywnych wykresów.
from pathlib import Path  # Importujemy Path, który ułatwia pracę ze ścieżkami do plików.
from io import BytesIO  # Importujemy BytesIO, aby móc traktować dane bajtowe jak plik w pamięci.

st.set_page_config(page_title='EDA COVID Dashboard', page_icon='🦠', layout='wide', initial_sidebar_state='expanded')  # Ustawiamy konfigurację strony Streamlit: tytuł, ikonę, szeroki układ oraz rozwinięty panel boczny.

DOMYSLNY_PLIK = 'ewp_dsh_zakazenia_po_szczepieniu_202203020921.csv'  # Definiujemy nazwę domyślnego pliku CSV, który aplikacja spróbuje wczytać, jeśli użytkownik nie wgra pliku ręcznie.
KOLUMNA_WAGI = 'liczba_zaraportowanych_zakazonych'  # Definiujemy nazwę kolumny z liczbą zaraportowanych zakażonych, która będzie używana jako waga/liczba przypadków.
KOLUMNA_DATY = 'data_rap_zakazenia'  # Definiujemy nazwę kolumny zawierającej datę raportowania zakażenia.

WOJ_MAP = {  # Tworzymy słownik mapujący kody TERYT województw na ich nazwy.
    2: 'dolnośląskie',  # Kod 2 oznacza województwo dolnośląskie.
    4: 'kujawsko-pomorskie',  # Kod 4 oznacza województwo kujawsko-pomorskie.
    6: 'lubelskie',  # Kod 6 oznacza województwo lubelskie.
    8: 'lubuskie',  # Kod 8 oznacza województwo lubuskie.
    10: 'łódzkie',  # Kod 10 oznacza województwo łódzkie.
    12: 'małopolskie',  # Kod 12 oznacza województwo małopolskie.
    14: 'mazowieckie',  # Kod 14 oznacza województwo mazowieckie.
    16: 'opolskie',  # Kod 16 oznacza województwo opolskie.
    18: 'podkarpackie',  # Kod 18 oznacza województwo podkarpackie.
    20: 'podlaskie',  # Kod 20 oznacza województwo podlaskie.
    22: 'pomorskie',  # Kod 22 oznacza województwo pomorskie.
    24: 'śląskie',  # Kod 24 oznacza województwo śląskie.
    26: 'świętokrzyskie',  # Kod 26 oznacza województwo świętokrzyskie.
    28: 'warmińsko-mazurskie',  # Kod 28 oznacza województwo warmińsko-mazurskie.
    30: 'wielkopolskie',  # Kod 30 oznacza województwo wielkopolskie.
    32: 'zachodniopomorskie'  # Kod 32 oznacza województwo zachodniopomorskie.
}  # Kończymy definicję słownika województw.

def czytaj_csv_auto(zrodlo):  # Definiujemy funkcję, która automatycznie próbuje wczytać plik CSV różnymi kodowaniami i separatorami.
    if hasattr(zrodlo, 'getvalue'):  # Sprawdzamy, czy źródło ma metodę getvalue, czyli czy pochodzi np. z pliku wgranego przez Streamlit.
        dane = zrodlo.getvalue()  # Jeśli plik został wgrany przez użytkownika, pobieramy jego zawartość jako bajty.
    else:  # Wykonujemy tę część, jeśli źródło nie jest plikiem wgranym, tylko np. ścieżką do pliku.
        dane = Path(zrodlo).read_bytes()  # Odczytujemy zawartość pliku ze ścieżki jako bajty.
    kodowania = ['cp1250', 'utf-8', 'utf-8-sig']  # Tworzymy listę kodowań, które będą testowane przy wczytywaniu CSV.
    separatory = [',', ';']  # Tworzymy listę separatorów CSV, które będą testowane: przecinek oraz średnik.
    ostatni_blad = None  # Tworzymy zmienną do zapamiętania ostatniego błędu, jeśli próby wczytania się nie powiodą.
    for encoding in kodowania:  # Rozpoczynamy pętlę po możliwych kodowaniach.
        for sep in separatory:  # Dla każdego kodowania testujemy każdy możliwy separator.
            try:  # Rozpoczynamy blok try, ponieważ wczytywanie pliku może zakończyć się błędem.
                df = pd.read_csv(BytesIO(dane), encoding=encoding, sep=sep, low_memory=False)  # Próbujemy wczytać dane CSV z pamięci, używając danego kodowania i separatora.
                if df.shape[1] > 1:  # Sprawdzamy, czy po wczytaniu powstała więcej niż jedna kolumna, co sugeruje poprawny separator.
                    return (df, encoding, sep)  # Jeśli dane wyglądają poprawnie, zwracamy DataFrame oraz użyte kodowanie i separator.
            except Exception as e:  # Jeśli wystąpi błąd podczas wczytywania, przechwytujemy go jako zmienną e.
                ostatni_blad = e  # Zapisujemy ostatni napotkany błąd, aby móc go później wyświetlić.
    raise ValueError(f'Nie udało się wczytać pliku CSV. Ostatni błąd: {ostatni_blad}')  # Jeśli żadna kombinacja nie zadziałała, zgłaszamy błąd z informacją o ostatnim problemie.

def przygotuj_dane(df: object) -> tuple[Any, str]:  # Definiujemy funkcję przygotowującą dane do analizy; zwraca DataFrame oraz nazwę kolumny z wagą.
    df = df.copy()  # Tworzymy kopię danych, aby nie modyfikować oryginalnego DataFrame.
    df.columns = pd.Index(df.columns).astype(str).str.replace('\ufeff', '', regex=False).str.strip()  # Czyścimy nazwy kolumn: zamieniamy je na tekst, usuwamy znak BOM i zbędne spacje.
    if KOLUMNA_DATY in df.columns:  # Sprawdzamy, czy w danych istnieje kolumna z datą raportowania zakażenia.
        df[KOLUMNA_DATY] = pd.to_datetime(df[KOLUMNA_DATY], errors='coerce')  # Zamieniamy kolumnę daty na typ datetime; błędne daty zostaną zamienione na NaT.
        df['miesiac'] = df[KOLUMNA_DATY].dt.to_period('M').dt.to_timestamp()  # Tworzymy kolumnę z miesiącem, zaokrąglając datę do początku miesiąca.
    if KOLUMNA_WAGI in df.columns:  # Sprawdzamy, czy istnieje kolumna z liczbą zaraportowanych zakażonych.
        df[KOLUMNA_WAGI] = pd.to_numeric(df[KOLUMNA_WAGI], errors='coerce').fillna(0)  # Zamieniamy kolumnę wagi na liczby, a braki lub błędy zastępujemy zerem.
        kolumna_wagi = KOLUMNA_WAGI  # Ustawiamy, że kolumną wagi będzie oryginalna kolumna z liczbą zakażonych.
    else:  # Wykonujemy tę część, jeśli kolumna z liczbą zakażonych nie istnieje.
        df['_liczba_rekordow'] = 1  # Tworzymy pomocniczą kolumnę, w której każdy wiersz ma wartość 1.
        kolumna_wagi = '_liczba_rekordow'  # Ustawiamy, że wagą będzie liczba rekordów, czyli każdy wiersz będzie liczony jako jeden przypadek.
    if 'producent' in df.columns:  # Sprawdzamy, czy w danych istnieje kolumna z producentem szczepionki.
        df['producent2'] = df['producent'].fillna('brak informacji').astype(str)  # Tworzymy oczyszczoną kolumnę producenta, zastępując braki tekstem „brak informacji”.
    if 'dawka_ost' in df.columns:  # Sprawdzamy, czy istnieje kolumna z informacją o ostatniej dawce.
        df['dawka2'] = df['dawka_ost'].fillna('brak informacji').astype(str)  # Tworzymy oczyszczoną kolumnę dawki, zamieniając braki na „brak informacji”.
    if 'plec' in df.columns:  # Sprawdzamy, czy istnieje kolumna z płcią.
        df['plec2'] = df['plec'].fillna('nieznana').astype(str)  # Tworzymy oczyszczoną kolumnę płci, zamieniając braki na „nieznana”.
    if 'teryt_woj' in df.columns:  # Sprawdzamy, czy istnieje kolumna z kodem TERYT województwa.
        df['woj'] = pd.to_numeric(df['teryt_woj'], errors='coerce').astype('Int64')  # Zamieniamy kod województwa na liczbę całkowitą z obsługą braków.
        df['woj_nazwa'] = df['woj'].map(WOJ_MAP).fillna('brak informacji')  # Mapujemy kod województwa na nazwę województwa, a braki opisujemy jako „brak informacji”.
    if 'wiek' in df.columns:  # Sprawdzamy, czy istnieje kolumna z wiekiem.
        df['wiek_num'] = pd.to_numeric(df['wiek'], errors='coerce')  # Zamieniamy wiek na wartość liczbową; błędne wartości zostaną zamienione na NaN.
    return (df, kolumna_wagi)  # Zwracamy przygotowany DataFrame oraz nazwę kolumny używanej jako liczba przypadków.

def agreguj_top(df, kolumna, kolumna_wagi, n=10):  # Definiujemy funkcję agregującą dane i wybierającą TOP n kategorii według liczby przypadków.
    if kolumna not in df.columns:  # Sprawdzamy, czy wskazana kolumna istnieje w danych.
        return pd.DataFrame(columns=[kolumna, 'liczba'])  # Jeśli kolumny nie ma, zwracamy pusty DataFrame z oczekiwanymi nazwami kolumn.
    wynik = df.groupby(kolumna, dropna=False)[kolumna_wagi].sum().sort_values(ascending=False).head(n).reset_index().rename(columns={kolumna_wagi: 'liczba'})  # Grupujemy dane według kategorii, sumujemy przypadki, sortujemy malejąco, wybieramy TOP n i zmieniamy nazwę kolumny na „liczba”.
    return wynik  # Zwracamy przygotowaną tabelę z najczęstszymi kategoriami.

def ustaw_layout(fig, wysokosc=450):  # Definiujemy funkcję ustawiającą wspólny wygląd wykresów Plotly.
    fig.update_layout(template='plotly_dark', height=wysokosc, margin=dict(l=20, r=20, t=60, b=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(size=13), title_font=dict(size=20), legend_title_text='')  # Ustawiamy ciemny motyw, wysokość, marginesy, przezroczyste tło, rozmiar czcionki i pusty tytuł legendy.
    return fig  # Zwracamy wykres z zastosowanymi ustawieniami wyglądu.

st.title('🦠 EDA COVID — interaktywny dashboard')  # Wyświetlamy główny tytuł aplikacji Streamlit.
st.caption('Dashboard do analizy zakażeń po szczepieniu: trendy, struktura, wiek, płeć, dawki, województwa i producenci.')  # Wyświetlamy krótki opis dashboardu pod tytułem.

with st.sidebar:  # Rozpoczynamy blok elementów umieszczanych w panelu bocznym aplikacji.
    st.header('⚙️ Ustawienia')  # Dodajemy nagłówek sekcji ustawień w panelu bocznym.
    uploaded_file = st.file_uploader('Wgraj plik CSV', type=['csv'])  # Dodajemy pole do wgrywania pliku CSV przez użytkownika.
    st.info('Możesz wgrać plik ręcznie albo trzymać CSV w tym samym folderze co dashboard.')  # Wyświetlamy informację o dwóch sposobach dostarczenia pliku danych.

try:  # Rozpoczynamy blok try odpowiedzialny za bezpieczne wczytywanie danych.
    if uploaded_file is not None:  # Sprawdzamy, czy użytkownik wgrał plik przez panel boczny.
        df_raw, used_encoding, used_sep = czytaj_csv_auto(uploaded_file)  # Wczytujemy wgrany plik CSV automatycznie wykrywając kodowanie i separator.
        nazwa_pliku = uploaded_file.name  # Zapisujemy nazwę wgranego pliku.
    else:  # Wykonujemy tę część, jeśli użytkownik nie wgrał pliku.
        if not Path(DOMYSLNY_PLIK).exists():  # Sprawdzamy, czy domyślny plik CSV istnieje w folderze aplikacji.
            st.error(f'Nie znaleziono pliku `{DOMYSLNY_PLIK}`. Wgraj CSV przez panel po lewej albo umieść plik w folderze dashboardu.')  # Wyświetlamy błąd, jeśli plik domyślny nie istnieje.
            st.stop()  # Zatrzymujemy dalsze wykonywanie aplikacji, ponieważ nie ma danych do analizy.
        df_raw, used_encoding, used_sep = czytaj_csv_auto(DOMYSLNY_PLIK)  # Wczytujemy domyślny plik CSV z folderu aplikacji.
        nazwa_pliku = DOMYSLNY_PLIK  # Zapisujemy nazwę użytego pliku jako nazwę pliku domyślnego.
except Exception as e:  # Jeśli podczas wczytywania danych wystąpi błąd, przechwytujemy go jako e.
    st.error(f'Błąd wczytywania danych: {e}')  # Wyświetlamy komunikat błędu w aplikacji Streamlit.
    st.stop()  # Zatrzymujemy działanie aplikacji, ponieważ bez danych nie można tworzyć dashboardu.

df, kolumna_wagi = przygotuj_dane(df_raw)  # Przygotowujemy dane do analizy i pobieramy nazwę kolumny używanej jako liczba przypadków.

with st.sidebar:  # Ponownie dodajemy elementy do panelu bocznego.
    st.header('🔎 Filtry')  # Dodajemy nagłówek sekcji filtrów.
    st.write(f'**Plik:** `{nazwa_pliku}`')  # Wyświetlamy nazwę aktualnie używanego pliku.
    st.write(f'**Kodowanie:** `{used_encoding}`')  # Wyświetlamy wykryte kodowanie pliku.
    st.write(f'**Separator:** `{used_sep}`')  # Wyświetlamy wykryty separator CSV.
    df_filt = df.copy()  # Tworzymy kopię danych, która będzie filtrowana bez zmiany oryginalnego DataFrame.
    if KOLUMNA_DATY in df_filt.columns:  # Sprawdzamy, czy dostępna jest kolumna daty.
        min_date = df_filt[KOLUMNA_DATY].min()  # Wyznaczamy najwcześniejszą datę w danych.
        max_date = df_filt[KOLUMNA_DATY].max()  # Wyznaczamy najpóźniejszą datę w danych.
        if pd.notna(min_date) and pd.notna(max_date):  # Sprawdzamy, czy minimalna i maksymalna data nie są brakami danych.
            zakres_dat = st.date_input('Zakres dat', value=(min_date.date(), max_date.date()), min_value=min_date.date(), max_value=max_date.date())  # Tworzymy wybór zakresu dat w panelu bocznym.
            if isinstance(zakres_dat, tuple) and len(zakres_dat) == 2:  # Sprawdzamy, czy użytkownik wybrał poprawny zakres dwóch dat.
                start_date, end_date = zakres_dat  # Rozpakowujemy początkową i końcową datę zakresu.
                df_filt = df_filt[(df_filt[KOLUMNA_DATY] >= pd.to_datetime(start_date)) & (df_filt[KOLUMNA_DATY] <= pd.to_datetime(end_date))]  # Filtrujemy dane tak, aby pozostały tylko rekordy z wybranego zakresu dat.
    if 'woj_nazwa' in df_filt.columns:  # Sprawdzamy, czy dostępna jest kolumna z nazwą województwa.
        woj_options = sorted(df_filt['woj_nazwa'].dropna().unique())  # Tworzymy posortowaną listę dostępnych województw bez braków danych.
        woj_selected = st.multiselect('Województwa', options=woj_options, default=woj_options)  # Dodajemy filtr wielokrotnego wyboru województw.
        df_filt = df_filt[df_filt['woj_nazwa'].isin(woj_selected)]  # Zostawiamy tylko rekordy z wybranych województw.
    if 'producent2' in df_filt.columns:  # Sprawdzamy, czy dostępna jest oczyszczona kolumna producenta.
        prod_options = sorted(df_filt['producent2'].dropna().unique())  # Tworzymy posortowaną listę producentów bez braków danych.
        prod_selected = st.multiselect('Producenci', options=prod_options, default=prod_options)  # Dodajemy filtr wielokrotnego wyboru producentów.
        df_filt = df_filt[df_filt['producent2'].isin(prod_selected)]  # Zostawiamy tylko rekordy dotyczące wybranych producentów.
    if 'plec2' in df_filt.columns:  # Sprawdzamy, czy dostępna jest oczyszczona kolumna płci.
        plec_options = sorted(df_filt['plec2'].dropna().unique())  # Tworzymy posortowaną listę dostępnych wartości płci.
        plec_selected = st.multiselect('Płeć', options=plec_options, default=plec_options)  # Dodajemy filtr wielokrotnego wyboru płci.
        df_filt = df_filt[df_filt['plec2'].isin(plec_selected)]  # Zostawiamy tylko rekordy pasujące do wybranych wartości płci.

suma_przypadkow = int(df_filt[kolumna_wagi].sum())  # Obliczamy łączną liczbę przypadków po zastosowaniu filtrów.
liczba_wierszy = len(df_filt)  # Obliczamy liczbę rekordów po zastosowaniu filtrów.
if 'wiek_num' in df_filt.columns:  # Sprawdzamy, czy dostępna jest liczbowo przetworzona kolumna wieku.
    sredni_wiek = df_filt['wiek_num'].mean()  # Obliczamy średni wiek dla przefiltrowanych danych.
else:  # Wykonujemy tę część, jeśli nie ma kolumny wieku.
    sredni_wiek = np.nan  # Ustawiamy średni wiek jako NaN, czyli brak możliwej do obliczenia wartości.
if KOLUMNA_DATY in df_filt.columns:  # Sprawdzamy, czy dostępna jest kolumna daty.
    data_min = df_filt[KOLUMNA_DATY].min()  # Obliczamy najwcześniejszą datę po filtrach.
    data_max = df_filt[KOLUMNA_DATY].max()  # Obliczamy najpóźniejszą datę po filtrach.
else:  # Wykonujemy tę część, jeśli nie ma kolumny daty.
    data_min = None  # Ustawiamy minimalną datę jako None.
    data_max = None  # Ustawiamy maksymalną datę jako None.

kpi1, kpi2, kpi3, kpi4 = st.columns(4)  # Tworzymy cztery kolumny w układzie strony, które posłużą do pokazania wskaźników KPI.
kpi1.metric('🧮 Liczba przypadków', f'{suma_przypadkow:,}'.replace(',', ' '))  # W pierwszej kolumnie pokazujemy łączną liczbę przypadków z separatorem tysięcy jako spacja.
kpi2.metric('📄 Liczba rekordów', f'{liczba_wierszy:,}'.replace(',', ' '))  # W drugiej kolumnie pokazujemy liczbę rekordów po filtrowaniu.
if pd.notna(sredni_wiek):  # Sprawdzamy, czy średni wiek jest poprawną wartością, a nie brakiem danych.
    kpi3.metric('👤 Średni wiek', f'{sredni_wiek:.1f}')  # Jeśli średni wiek istnieje, pokazujemy go z jednym miejscem po przecinku.
else:  # Wykonujemy tę część, jeśli średni wiek nie może zostać obliczony.
    kpi3.metric('👤 Średni wiek', 'brak danych')  # Pokazujemy informację, że brak danych o średnim wieku.
if data_min is not None and pd.notna(data_min):  # Sprawdzamy, czy zakres dat jest dostępny.
    kpi4.metric('📅 Zakres', f'{data_min.date()} → {data_max.date()}')  # Pokazujemy zakres dat od najwcześniejszej do najpóźniejszej.
else:  # Wykonujemy tę część, jeśli nie ma informacji o datach.
    kpi4.metric('📅 Zakres', 'brak dat')  # Pokazujemy informację, że brakuje dat.

st.divider()  # Dodajemy poziomą linię oddzielającą wskaźniki KPI od dalszej części dashboardu.

if KOLUMNA_DATY in df_filt.columns:  # Sprawdzamy, czy można tworzyć wykres trendu w czasie.
    st.subheader('📈 Trend zakażeń w czasie')  # Dodajemy podtytuł sekcji trendu zakażeń.
    dziennie = df_filt.dropna(subset=[KOLUMNA_DATY]).groupby(KOLUMNA_DATY)[kolumna_wagi].sum().sort_index().reset_index().rename(columns={kolumna_wagi: 'Dziennie'})  # Usuwamy rekordy bez daty, grupujemy dane dziennie, sumujemy przypadki i zmieniamy nazwę kolumny na „Dziennie”.
    if len(dziennie) > 0:  # Sprawdzamy, czy po agregacji istnieją dane do wykresu.
        dziennie['Średnia 7D'] = dziennie['Dziennie'].rolling(7).mean()  # Obliczamy 7-dniową średnią kroczącą liczby przypadków.
        fig = px.line(dziennie, x=KOLUMNA_DATY, y=['Dziennie', 'Średnia 7D'], markers=False, title='Zakażenia dzienne + 7-dniowa średnia krocząca')  # Tworzymy wykres liniowy dziennych zakażeń oraz średniej 7-dniowej.
        fig.update_traces(line=dict(width=3))  # Ustawiamy grubość linii na wykresie.
        fig = ustaw_layout(fig, wysokosc=520)  # Stosujemy wspólny styl wykresu i ustawiamy jego wysokość.
        st.plotly_chart(fig, use_container_width=True)  # Wyświetlamy wykres Plotly w aplikacji na pełną szerokość kontenera.
    else:  # Wykonujemy tę część, jeśli nie ma danych do trendu dziennego.
        st.warning('Brak danych do wykresu dziennego.')  # Wyświetlamy ostrzeżenie, że nie można narysować wykresu.

left, right = st.columns(2)  # Tworzymy dwie kolumny układu strony: lewą i prawą.
with left:  # Wchodzimy do lewej kolumny.
    if 'woj_nazwa' in df_filt.columns:  # Sprawdzamy, czy dostępna jest kolumna województwa.
        st.subheader('🗺️ TOP województwa')  # Dodajemy podtytuł sekcji z top województwami.
        top_woj = agreguj_top(df_filt, 'woj_nazwa', kolumna_wagi, n=10)  # Agregujemy dane i wybieramy 10 województw z największą liczbą przypadków.
        fig = px.bar(top_woj, x='liczba', y='woj_nazwa', orientation='h', title='Top 10 województw wg liczby przypadków', text='liczba', color='liczba', color_continuous_scale='Reds')  # Tworzymy poziomy wykres słupkowy TOP 10 województw.
        fig.update_layout(yaxis=dict(autorange='reversed'))  # Odwracamy kolejność osi Y, aby największa wartość była na górze.
        fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')  # Formatujemy etykiety słupków jako liczby całkowite i ustawiamy je na zewnątrz słupków.
        fig = ustaw_layout(fig, wysokosc=520)  # Stosujemy wspólny wygląd wykresu i ustawiamy wysokość.
        st.plotly_chart(fig, use_container_width=True)  # Wyświetlamy wykres w lewej kolumnie.

with right:  # Wchodzimy do prawej kolumny.
    if 'producent2' in df_filt.columns:  # Sprawdzamy, czy dostępna jest kolumna producenta.
        st.subheader('💉 Producenci szczepionek')  # Dodajemy podtytuł sekcji producentów szczepionek.
        top_prod = agreguj_top(df_filt, 'producent2', kolumna_wagi, n=10)  # Agregujemy dane i wybieramy 10 producentów z największą liczbą przypadków.
        fig = px.bar(top_prod, x='liczba', y='producent2', orientation='h', title='Top 10 producentów wg liczby przypadków', text='liczba', color='liczba', color_continuous_scale='Blues')  # Tworzymy poziomy wykres słupkowy TOP 10 producentów.
        fig.update_layout(yaxis=dict(autorange='reversed'))  # Odwracamy kolejność osi Y, aby największa wartość była na górze.
        fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')  # Ustawiamy format i pozycję etykiet liczbowych na słupkach.
        fig = ustaw_layout(fig, wysokosc=520)  # Stosujemy wspólny styl wykresu.
        st.plotly_chart(fig, use_container_width=True)  # Wyświetlamy wykres w prawej kolumnie.

left, right = st.columns(2)  # Tworzymy kolejne dwie kolumny układu strony.
with left:  # Wchodzimy do lewej kolumny.
    if 'plec2' in df_filt.columns:  # Sprawdzamy, czy dostępna jest oczyszczona kolumna płci.
        st.subheader('⚧️ Struktura wg płci')  # Dodajemy podtytuł sekcji struktury według płci.
        plec = df_filt.groupby('plec2')[kolumna_wagi].sum().reset_index().rename(columns={kolumna_wagi: 'liczba'})  # Grupujemy dane według płci i sumujemy liczbę przypadków.
        fig = px.pie(plec, names='plec2', values='liczba', hole=0.58, title='Udział przypadków wg płci')  # Tworzymy wykres kołowy typu donut pokazujący udział przypadków według płci.
        fig.update_traces(textposition='inside', textinfo='percent+label')  # Ustawiamy, aby etykiety i procenty były widoczne wewnątrz wykresu.
        fig = ustaw_layout(fig, wysokosc=460)  # Ustawiamy wspólny wygląd i wysokość wykresu.
        st.plotly_chart(fig, use_container_width=True)  # Wyświetlamy wykres w lewej kolumnie.

with right:  # Wchodzimy do prawej kolumny.
    if 'dawka2' in df_filt.columns:  # Sprawdzamy, czy dostępna jest oczyszczona kolumna dawki.
        st.subheader('💊 Struktura wg dawki')  # Dodajemy podtytuł sekcji struktury według dawki.
        dawka = df_filt.groupby('dawka2')[kolumna_wagi].sum().reset_index().rename(columns={kolumna_wagi: 'liczba'})  # Grupujemy dane według dawki i sumujemy liczbę przypadków.
        fig = px.pie(dawka, names='dawka2', values='liczba', hole=0.58, title='Udział przypadków wg dawki')  # Tworzymy wykres kołowy typu donut pokazujący udział przypadków według dawki.
        fig.update_traces(textposition='inside', textinfo='percent+label')  # Wyświetlamy etykiety i wartości procentowe wewnątrz wykresu.
        fig = ustaw_layout(fig, wysokosc=460)  # Stosujemy wspólny wygląd wykresu i wysokość.
        st.plotly_chart(fig, use_container_width=True)  # Wyświetlamy wykres w prawej kolumnie.

if 'kat_wiek' in df_filt.columns and 'dawka2' in df_filt.columns:  # Sprawdzamy, czy dostępne są jednocześnie kolumna kategorii wieku oraz kolumna dawki.
    st.subheader('🔥 Heatmapa: kategoria wieku × dawka')  # Dodajemy podtytuł sekcji heatmapy.
    heat = df_filt.groupby(['kat_wiek', 'dawka2'])[kolumna_wagi].sum().reset_index()  # Grupujemy dane według kategorii wieku i dawki, a następnie sumujemy przypadki.
    pivot = heat.pivot_table(index='kat_wiek', columns='dawka2', values=kolumna_wagi, aggfunc='sum', fill_value=0)  # Tworzymy tabelę przestawną, gdzie wiersze to kategorie wieku, kolumny to dawki, a wartości to liczba przypadków.
    fig = px.imshow(pivot, text_auto=True, aspect='auto', color_continuous_scale='Turbo', title='Liczba przypadków według kategorii wieku i dawki')  # Tworzymy heatmapę z automatycznymi etykietami wartości.
    fig = ustaw_layout(fig, wysokosc=600)  # Stosujemy wspólny wygląd wykresu i ustawiamy większą wysokość.
    st.plotly_chart(fig, use_container_width=True)  # Wyświetlamy heatmapę na pełną szerokość kontenera.

mozliwe_kolumny_treemap = [col for col in ['woj_nazwa', 'producent2', 'dawka2'] if col in df_filt.columns]  # Tworzymy listę kolumn dostępnych do wykresu treemap, wybierając tylko te, które istnieją w danych.
if len(mozliwe_kolumny_treemap) >= 2:  # Sprawdzamy, czy mamy co najmniej dwie kolumny, aby sensownie utworzyć strukturę hierarchiczną.
    st.subheader('🌳 Treemap: struktura przypadków')  # Dodajemy podtytuł sekcji treemap.
    treemap_df = df_filt.groupby(mozliwe_kolumny_treemap)[kolumna_wagi].sum().reset_index().rename(columns={kolumna_wagi: 'liczba'})  # Grupujemy dane według dostępnych kolumn hierarchii i sumujemy przypadki.
    fig = px.treemap(treemap_df, path=mozliwe_kolumny_treemap, values='liczba', color='liczba', color_continuous_scale='Viridis', title='Hierarchiczna struktura przypadków')  # Tworzymy wykres treemap pokazujący hierarchiczną strukturę przypadków.
    fig = ustaw_layout(fig, wysokosc=650)  # Ustawiamy wspólny wygląd wykresu i większą wysokość.
    st.plotly_chart(fig, use_container_width=True)  # Wyświetlamy treemap w aplikacji.

with st.expander('📋 Podgląd danych po filtrach'):  # Tworzymy rozwijaną sekcję z podglądem danych po zastosowanych filtrach.
    st.dataframe(df_filt.head(500), use_container_width=True)  # Wyświetlamy pierwsze 500 wierszy przefiltrowanych danych w interaktywnej tabeli.

with st.expander('📊 Podstawowe informacje o kolumnach'):  # Tworzymy rozwijaną sekcję z informacjami o kolumnach.
    opis = pd.DataFrame({  # Tworzymy DataFrame zawierający opis kolumn.
        'kolumna': df_filt.columns,  # Dodajemy nazwy kolumn.
        'typ': [str(t) for t in df_filt.dtypes],  # Dodajemy typ danych każdej kolumny jako tekst.
        'braki': df_filt.isna().sum().values,  # Dodajemy liczbę brakujących wartości w każdej kolumnie.
        'braki_%': (df_filt.isna().sum().values / max(len(df_filt), 1) * 100).round(2)  # Obliczamy procent braków danych, zabezpieczając się przed dzieleniem przez zero.
    })  # Kończymy tworzenie DataFrame z opisem kolumn.
    st.dataframe(opis, use_container_width=True)  # Wyświetlamy opis kolumn w interaktywnej tabeli Streamlit.