# Importujemy moduł `random`, który pozwala losować różne wartości.
# W tym programie będzie on potrzebny do wylosowania tajnej liczby,
# którą użytkownik ma odgadnąć.
import random

# Funkcja `random.randint(1,100)` losuje liczbę całkowitą
# z przedziału od 1 do 100 włącznie.
# Oznacza to, że wylosowana liczba może być równa 1, 100
# albo dowolnej liczbie pomiędzy nimi.
# Wylosowaną wartość zapisujemy do zmiennej `tajna`.
tajna = random.randint(1,100)

# Pętla `while True` tworzy pętlę nieskończoną,
# czyli taki fragment programu, który będzie wykonywał się cały czas,
# dopóki nie zostanie przerwany instrukcją `break`.
# Dzięki temu użytkownik może zgadywać tyle razy, ile potrzebuje.
while True:
    # Funkcja `input("Zgadnij liczbę od 1 do 100: ")`
    # wyświetla komunikat i czeka, aż użytkownik wpisze wartość z klawiatury.
    # To, co wpisze użytkownik, jest początkowo tekstem.
    # Funkcja `int(...)` zamienia ten tekst na liczbę całkowitą.
    # Ostatecznie wpisana liczba zostaje zapisana do zmiennej `proba`.
    proba = int(input("Zgadnij liczbę od 1 do 100: "))

    # Sprawdzamy, czy liczba podana przez użytkownika (`proba`)
    # jest mniejsza od liczby wylosowanej przez komputer (`tajna`).
    if proba < tajna:
        # Jeśli tak, oznacza to, że użytkownik podał za małą liczbę.
        # Program wyświetla wskazówkę, że trzeba spróbować z większą wartością.
        print("Za mała! Spróbuj jeszcze raz.")

    # Jeśli poprzedni warunek nie został spełniony,
    # sprawdzamy, czy liczba podana przez użytkownika jest większa od tajnej liczby.
    elif proba > tajna:
        # Jeśli ten warunek jest prawdziwy, użytkownik podał za dużą liczbę.
        # Program informuje, że trzeba spróbować ponownie z mniejszą wartością.
        print("Za duża! Spróbuj jeszcze raz.")

    # Blok `else` wykona się wtedy, gdy oba wcześniejsze warunki są fałszywe.
    # To oznacza, że `proba` nie jest ani mniejsza, ani większa od `tajna`,
    # więc musi być dokładnie równa tej liczbie.
    else:
        # Program wyświetla komunikat gratulacyjny,
        # ponieważ użytkownik poprawnie odgadł liczbę.
        print("Brawo! Zgadłeś")

        # Instrukcja `break` przerywa działanie pętli `while`.
        # Dzięki temu program kończy się w momencie odgadnięcia liczby.
        break