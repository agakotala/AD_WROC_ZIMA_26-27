# Tworzymy zmienną `x` i przypisujemy jej wartość 10.
# Oznacza to, że od tej liczby program zacznie odliczanie.
x = 10

# Pętla `while` będzie wykonywać się tak długo,
# jak długo warunek `x > 0` będzie prawdziwy.
# Innymi słowy: program będzie działał, dopóki `x` jest większe od zera.
while x > 0:
    # W każdej iteracji pętli wyświetlamy aktualną wartość zmiennej `x`.
    # Dzięki temu na ekranie pojawią się kolejne liczby:
    # 10, 9, 8, 7, 6, 5, 4, 3, 2, 1
    print(x)

    # Zapis `x -= 1` oznacza:
    # "zmniejsz wartość zmiennej `x` o 1".
    # Jest to skrócona forma zapisu:
    # x = x - 1
    # Dzięki temu po każdym obiegu pętli liczba będzie o 1 mniejsza.
    x -= 1