from genetic_alg import genetic_algorithm

#фуекція максимізації
def onemax(x):
    return -sum(x)


def main():
    #кількість ітерацій алгоритму (поколінь).
    n_iter = 100
    # кількість бітів у бінарних рядкових послідовностях (розмір геному).
    n_bits = 20
    # кількість особин у популяції.
    n_pop = 100
    #ймовірність рекомбінації (кроссовера) між батьками.
    r_cross = 0.9
    #ймовірність мутації для кожного біта.
    r_mut = 1.0 / float(n_bits)

    best, score = genetic_algorithm(onemax, n_bits, n_iter, n_pop, r_cross, r_mut)
    print('Done!')
    print('f(%s) = %f' % (best, score))


if __name__ == '__main__':
    main()
