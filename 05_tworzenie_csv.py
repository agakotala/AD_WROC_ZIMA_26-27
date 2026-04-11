# Importujemy bibliotekę `pandas` i nadajemy jej skróconą nazwę `pd`.
# `pandas` służy do pracy z danymi tabelarycznymi,
# czyli na przykład do tworzenia tabel, wczytywania plików CSV
# oraz zapisywania danych do plików.
import pandas as pd

# Importujemy bibliotekę `numpy` i nadajemy jej skróconą nazwę `np`.
# `numpy` jest często używane do pracy z liczbami, tablicami
# oraz do losowania danych.
import numpy as np

# Ustawiamy tzw. ziarno losowania na wartość 42.
# Dzięki temu przy każdym uruchomieniu programu
# losowane dane będą takie same.
# Jest to bardzo przydatne podczas testowania,
# bo wyniki są powtarzalne.
np.random.seed(42)

# Tworzymy listę imion, z której program będzie później losował wartości.
# Lista zawiera napisy reprezentujące różne imiona klientów.
imiona = ['Anna', 'Jan', 'Marta', 'Piotr', 'Kasia', 'Tomek', 'Ewa', 'Michał', 'Julia', 'Alicja', 'Radosław', 'Magdalena', 'Aleksandra']

# Tworzymy listę miast, z której również będą losowane dane.
# Każdy klient otrzyma jedno z tych miast jako miejsce zamieszkania.
miasta = ['Warszawa', 'Wrocław', 'Gdańsk', 'Laskowa', 'Kraków', 'Limanowa', 'Bobrowniki', 'Pcim Dolny', 'Kobyla Góra', 'Bralin', 'Adamczycha']

# Tworzymy nowy DataFrame o nazwie `df_klienci`.
# DataFrame to tabela składająca się z kolumn i wierszy.
# W nawiasach klamrowych `{}` podajemy nazwy kolumn
# oraz dane, które mają się w nich znaleźć.
df_klienci = pd.DataFrame({
    # Tworzymy kolumnę `klient_id`.
    # `range(1, 1001)` generuje liczby od 1 do 1000.
    # Każdy klient otrzyma unikalny identyfikator.
    'klient_id': range(1, 1001),

    # Tworzymy kolumnę `imię`.
    # `np.random.choice(imiona, 1000)` losuje 1000 wartości z listy `imiona`.
    # Oznacza to, że dla każdego klienta zostanie przypisane losowe imię.
    # Imiona mogą się powtarzać, ponieważ losowanie odbywa się wielokrotnie.
    'imię': np.random.choice(imiona, 1000),

    # Tworzymy kolumnę `miasto`.
    # `np.random.choice(miasta, 1000)` losuje 1000 wartości z listy `miasta`.
    # Dzięki temu każdy klient dostaje losowo przypisane miasto.
    # Tak samo jak w przypadku imion, miasta mogą się powtarzać.
    'miasto': np.random.choice(miasta, 1000)
})

# Zapisujemy utworzony DataFrame do pliku CSV o nazwie `klienci.csv`.
# `index=False` oznacza, że nie zapisujemy dodatkowej kolumny z numerami wierszy.
# `encoding='utf-8-sig'` ustawia kodowanie znaków tak,
# aby polskie znaki były poprawnie odczytywane np. w Excelu.
df_klienci.to_csv('klienci.csv', index=False, encoding='utf-8-sig')