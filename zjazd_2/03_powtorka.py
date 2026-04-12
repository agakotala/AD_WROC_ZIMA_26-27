# Importujemy moduł `random`, który pozwala losować różne wartości.
# Dzięki niemu program może wybrać przypadkową liczbę,
# którą użytkownik będzie próbował odgadnąć.
import random

# Funkcja `random.randint(1,10)` losuje liczbę całkowitą
# z przedziału od 1 do 10 włącznie.
# Wylosowana liczba zostaje zapisana do zmiennej `tajna`.
# To właśnie tę liczbę użytkownik ma odgadnąć.
tajna = random.randint(1,10)

# Pętla `while True` tworzy pętlę nieskończoną,
# czyli taki fragment programu, który będzie wykonywał się w kółko,
# dopóki nie przerwiemy go instrukcją `break`.
# Tutaj jest to użyte po to, aby użytkownik mógł zgadywać tyle razy,
# ile będzie potrzebował, aż poda poprawną liczbę.
while True:
    # Funkcja `input("Zgadnij liczbę od 1 do 10: ")` wyświetla komunikat
    # i czeka, aż użytkownik wpisze swoją odpowiedź z klawiatury.
    # Wpisana wartość jest początkowo tekstem.
    # Funkcja `int(...)` zamienia ten tekst na liczbę całkowitą.
    # Ostatecznie liczba podana przez użytkownika zostaje zapisana w zmiennej `proba`.
    proba = int(input("Zgadnij liczbę od 1 do 10: "))

    # Instrukcja `if` sprawdza, czy liczba podana przez użytkownika (`proba`)
    # jest taka sama jak wylosowana wcześniej tajna liczba (`tajna`).
    if proba == tajna:

        # Jeśli warunek jest prawdziwy, oznacza to,
        # że użytkownik odgadł poprawną liczbę.
        # Program wyświetla komunikat gratulacyjny.
        print("Brawo! Zgadłeś")

        # Instrukcja `break` natychmiast przerywa działanie pętli `while`.
        # Dzięki temu program kończy zgadywanie,
        # ponieważ użytkownik podał już dobrą odpowiedź.
        break
    else:
        # Blok `else` wykona się wtedy,
        # gdy liczba podana przez użytkownika nie jest poprawna.
        # Program wyświetli wtedy komunikat zachęcający do kolejnej próby.
        print("Spróbuj jeszcze raz!")