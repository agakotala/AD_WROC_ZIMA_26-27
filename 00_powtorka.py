# Pętla `while True` tworzy pętlę nieskończoną, czyli taki fragment programu,
# który będzie wykonywał się bez końca, dopóki sami go nie przerwiemy instrukcją `break`.
# Tutaj jest to użyte po to, aby pytać użytkownika o wiek tak długo,
# aż poda poprawną wartość.
while True:
    # Funkcja `input("Podaj swój wiek: ")` wyświetla użytkownikowi komunikat
    # "Podaj swój wiek: " i czeka, aż wpisze on coś z klawiatury.
    # To, co wpisze użytkownik, jest domyślnie tekstem (napisem, czyli typem `str`).
    # Funkcja `int(...)` zamienia ten tekst na liczbę całkowitą.
    # Ostatecznie wynik zostaje zapisany do zmiennej `wiek`.
    wiek = int(input("Podaj swój wiek: "))

    # Instrukcja `if wiek < 0:` sprawdza, czy podany wiek jest mniejszy od zera.
    # Taki wiek nie ma sensu w rzeczywistości, więc traktujemy go jako błędne dane.
    if wiek < 0:
        # Jeśli warunek powyżej jest prawdziwy, program wyświetli komunikat
        # informujący użytkownika, że podał niepoprawny wiek,
        # i zachęci go do ponownego wpisania wartości.
        print("Błędny wiek, spróbuj jeszcze raz")
    else:
        # Blok `else` wykona się wtedy, gdy warunek `wiek < 0` jest fałszywy,
        # czyli wtedy, gdy użytkownik podał wiek równy 0 lub większy.
        # Oznacza to, że uznajemy tę wartość za poprawną.
        break

# Po wyjściu z pętli mamy pewność, że zmienna `wiek` zawiera poprawną liczbę
# i możemy na jej podstawie określić kategorię wiekową użytkownika.

# Ten warunek sprawdza, czy wiek jest mniejszy niż 15.
# Jeśli tak, program uzna użytkownika za dziecko.
if wiek < 15:
    # Wyświetlenie komunikatu dla osób, które mają mniej niż 15 lat.
    print("Jesteś dzieckiem")

# `elif` oznacza "else if", czyli "w przeciwnym razie, jeśli...".
# Ten warunek sprawdza, czy wiek jest mniejszy niż 18.
# Ponieważ wcześniejszy warunek (`wiek < 15`) musiał być fałszywy,
# oznacza to, że tutaj w praktyce chodzi o osoby w wieku od 15 do 17 lat.
elif wiek < 18:
    # Wyświetlenie komunikatu dla osób niepełnoletnich w wieku 15–17 lat.
    print("Jesteś niepełnoletni")

# Ten warunek sprawdza, czy użytkownik ma dokładnie 18 lat.
# Jest to osobny przypadek wyróżniony w programie.
elif wiek == 18:
    # Wyświetlenie specjalnego komunikatu dla osoby,
    # która ma dokładnie 18 lat.
    print("Masz dokładnie 18 lat")

# Ten warunek sprawdza, czy wiek jest mniejszy lub równy 60.
# Ponieważ wcześniejsze warunki już odrzuciły liczby mniejsze niż 18
# oraz przypadek dokładnie 18 lat, tutaj w praktyce chodzi o osoby
# od 19 do 60 roku życia włącznie.
elif wiek <= 60:
    # Wyświetlenie komunikatu dla osób pełnoletnich w wieku 19–60 lat.
    print("Jesteś pełnoletni")

# `else` wykona się wtedy, gdy żaden z wcześniejszych warunków nie był prawdziwy.
# Skoro wiek nie jest mniejszy niż 15, nie jest mniejszy niż 18,
# nie jest równy 18 i nie jest mniejszy lub równy 60,
# to musi być większy niż 60.
else:
    # Wyświetlenie komunikatu dla osób starszych niż 60 lat.
    print("Jesteś seniorem")