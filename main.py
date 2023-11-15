from genetic_alg import genetic_algorithm


def onemax(x):
    return -sum(x)


def main():
    n_iter = 100
    n_bits = 20
    n_pop = 100
    r_cross = 0.9
    r_mut = 1.0 / float(n_bits)
    best, score = genetic_algorithm(onemax, n_bits, n_iter, n_pop, r_cross, r_mut)
    print('Done!')
    print('f(%s) = %f' % (best, score))


if __name__ == '__main__':
    main()
