# Pętla `for` służy do wielokrotnego wykonywania tego samego fragmentu kodu.
# W tym przypadku zmienna `i` będzie po kolei przyjmowała wartości z zakresu od 1 do 10.
# Funkcja `range(1, 11)` generuje liczby całkowite zaczynając od 1,
# a kończąc na 10, ponieważ górna granica 11 nie jest wliczana.
# Dzięki temu pętla wykona się dokładnie 10 razy.
for i in range(1, 11):
    # W każdej iteracji pętli obliczamy wynik mnożenia liczby 5 przez aktualną wartość zmiennej `i`.
    # Na przykład:
    # gdy `i` = 1, wynik będzie równy 5,
    # gdy `i` = 2, wynik będzie równy 10,
    # gdy `i` = 3, wynik będzie równy 15,
    # i tak dalej aż do `i` = 10.
    # Otrzymana wartość zostaje zapisana w zmiennej `wynik`.
    wynik = 5 * i

    # Funkcja `print()` wyświetla tekst na ekranie.
    # Zapis `f"..."` oznacza tzw. f-string, czyli napis formatowany.
    # Pozwala on wstawiać wartości zmiennych bezpośrednio do tekstu za pomocą klamr `{}`.
    # W tym przypadku:
    # `{i}` zostanie zastąpione aktualną wartością zmiennej `i`,
    # a `{wynik}` zostanie zastąpione obliczonym wynikiem mnożenia.
    # Dzięki temu program wyświetli kolejne działania tabliczki mnożenia liczby 5,
    # np.:
    # 5 x 1 = 5
    # 5 x 2 = 10
    # 5 x 3 = 15
    # ...
    # 5 x 10 = 50
    print(f"5 x {i} = {wynik}")