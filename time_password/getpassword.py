import string
import random
import timeit
import numpy as np
import itertools

allchar = string.ascii_lowercase + ' '
userdatabase = {'yuanz': 'gzh pypi r and python'}


def check_password(user, guess_pd):
    actual_pd = userdatabase[user]

    if len(actual_pd) != len(guess_pd):
        return False

    for i in range(len(guess_pd)):
        if guess_pd[i] != actual_pd[i]:
            return False

    return True


def random_str(size):
    return ''.join(random.choices(allchar, k=size))


def guess_length(user, max_length=32, verbose=False) -> int:
    trials = 10000

    times = np.zeros(shape=max_length)

    for i in range(max_length):
        i_time = timeit.repeat(stmt="""check_password(user, x)""",
                               setup=f"user={user!r}; x=random_str({i!r})",
                               globals=globals(),
                               number=trials,
                               repeat=10)
        times[i] = min(i_time)

    if verbose:
        most_likely_n = np.argsort(times)[::-1][:5]
        print(most_likely_n, times[most_likely_n] / times[most_likely_n[0]])

    most_likely = int(np.argmax(times))

    return most_likely


def guess_str(user, length, verbose=False):
    guess = random_str(size=length)
    trials = 1000
    counter = itertools.count()

    while True:
        i = next(counter) % length
        for c in allchar:
            alt = guess[:i] + c + guess[(i + 1):]

            alt_time = timeit.repeat(stmt="""check_password(user, x)""",
                                     setup=f"user={user!r}; x={alt!r}",
                                     globals=globals(),
                                     number=trials,
                                     repeat=10)

            guess_time = timeit.repeat(stmt="""check_password(user, x)""",
                                       setup=f"user={user!r}; x={guess!r}",
                                       globals=globals(),
                                       number=trials,
                                       repeat=10)

            if check_password(user=user, guess_pd=alt):
                print(alt)
                return alt

            if min(alt_time) > min(guess_time):
                guess = alt
                if verbose:
                    print(guess)


def main():
    pd_length = guess_length(user='yuanz', verbose=True)
    print(pd_length)

    password = guess_str(user="yuanz", length=pd_length, verbose=True)
    print(f"password: {password!r}")


if __name__ == '__main__':
    main()
