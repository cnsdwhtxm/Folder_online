# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: random.py
"""Random variable generators.

    integers
    --------
           uniform within range

    sequences
    ---------
           pick random element
           pick random sample
           pick weighted random sample
           generate random permutation

    distributions on the real line:
    ------------------------------
           uniform
           triangular
           normal (Gaussian)
           lognormal
           negative exponential
           gamma
           beta
           pareto
           Weibull

    distributions on the circle (angles 0 to 2pi)
    ---------------------------------------------
           circular uniform
           von Mises

General notes on the underlying Mersenne Twister core generator:

* The period is 2**19937-1.
* It is one of the most extensively tested generators in existence.
* The random() method is implemented in C, executes in a single Python step,
  and is, therefore, threadsafe.

"""
from warnings import warn as _warn
from types import MethodType as _MethodType, BuiltinMethodType as _BuiltinMethodType
from math import log as _log, exp as _exp, pi as _pi, e as _e, ceil as _ceil
from math import sqrt as _sqrt, acos as _acos, cos as _cos, sin as _sin
from os import urandom as _urandom
from _collections_abc import Set as _Set, Sequence as _Sequence
from hashlib import sha512 as _sha512
import itertools as _itertools, bisect as _bisect
__all__ = [
 'Random', 'seed', 'random', 'uniform', 'randint', 'choice', 'sample',
 'randrange', 'shuffle', 'normalvariate', 'lognormvariate',
 'expovariate', 'vonmisesvariate', 'gammavariate', 'triangular',
 'gauss', 'betavariate', 'paretovariate', 'weibullvariate',
 'getstate', 'setstate', 'getrandbits', 'choices',
 'SystemRandom']
NV_MAGICCONST = 4 * _exp(-0.5) / _sqrt(2.0)
TWOPI = 2.0 * _pi
LOG4 = _log(4.0)
SG_MAGICCONST = 1.0 + _log(4.5)
BPF = 53
RECIP_BPF = 2 ** (-BPF)
import _random

class Random(_random.Random):
    __doc__ = "Random number generator base class used by bound module functions.\n\n    Used to instantiate instances of Random to get generators that don't\n    share state.\n\n    Class Random can also be subclassed if you want to use a different basic\n    generator of your own devising: in that case, override the following\n    methods:  random(), seed(), getstate(), and setstate().\n    Optionally, implement a getrandbits() method so that randrange()\n    can cover arbitrarily large ranges.\n\n    "
    VERSION = 3

    def __init__(self, x=None):
        """Initialize an instance.

        Optional argument x controls seeding, as for Random.seed().
        """
        self.seed(x)
        self.gauss_next = None

    def seed(self, a=None, version=2):
        """Initialize internal state from hashable object.

        None or no argument seeds from current time or from an operating
        system specific randomness source if available.

        If *a* is an int, all bits are used.

        For version 2 (the default), all of the bits are used if *a* is a str,
        bytes, or bytearray.  For version 1 (provided for reproducing random
        sequences from older versions of Python), the algorithm for str and
        bytes generates a narrower range of seeds.

        """
        if version == 1:
            if isinstance(a, (str, bytes)):
                a = a.decode('latin-1') if isinstance(a, bytes) else a
                x = ord(a[0]) << 7 if a else 0
                for c in map(ord, a):
                    x = (1000003 * x ^ c) & 18446744073709551615

                x ^= len(a)
                a = -2 if x == -1 else x
        else:
            if version == 2:
                if isinstance(a, (str, bytes, bytearray)):
                    if isinstance(a, str):
                        a = a.encode()
                    a += _sha512(a).digest()
                    a = int.from_bytes(a, 'big')
        super().seed(a)
        self.gauss_next = None

    def getstate(self):
        return (
         self.VERSION, super().getstate(), self.gauss_next)

    def setstate(self, state):
        version = state[0]
        if version == 3:
            version, internalstate, self.gauss_next = state
            super().setstate(internalstate)
        else:
            if version == 2:
                version, internalstate, self.gauss_next = state
                try:
                    internalstate = tuple(x % 4294967296 for x in internalstate)
                except ValueError as e:
                    raise TypeError from e

                super().setstate(internalstate)
            else:
                raise ValueError('state with version %s passed to Random.setstate() of version %s' % (
                 version, self.VERSION))

    def __getstate__(self):
        return self.getstate()

    def __setstate__(self, state):
        self.setstate(state)

    def __reduce__(self):
        return (
         self.__class__, (), self.getstate())

    def randrange(self, start, stop=None, step=1, _int=int):
        """Choose a random item from range(start, stop[, step]).

        This fixes the problem with randint() which includes the
        endpoint; in Python this is usually not what you want.

        """
        istart = _int(start)
        if istart != start:
            raise ValueError('non-integer arg 1 for randrange()')
        if stop is None:
            if istart > 0:
                return self._randbelow(istart)
            raise ValueError('empty range for randrange()')
        istop = _int(stop)
        if istop != stop:
            raise ValueError('non-integer stop for randrange()')
        width = istop - istart
        if step == 1:
            if width > 0:
                return istart + self._randbelow(width)
        if step == 1:
            raise ValueError('empty range for randrange() (%d,%d, %d)' % (istart, istop, width))
        else:
            istep = _int(step)
            if istep != step:
                raise ValueError('non-integer step for randrange()')
            if istep > 0:
                n = (width + istep - 1) // istep
            else:
                if istep < 0:
                    n = (width + istep + 1) // istep
                else:
                    raise ValueError('zero step for randrange()')
        if n <= 0:
            raise ValueError('empty range for randrange()')
        return istart + istep * self._randbelow(n)

    def randint(self, a, b):
        """Return random integer in range [a, b], including both end points.
        """
        return self.randrange(a, b + 1)

    def _randbelow(self, n, int=int, maxsize=1 << BPF, type=type, Method=_MethodType, BuiltinMethod=_BuiltinMethodType):
        """Return a random int in the range [0,n).  Raises ValueError if n==0."""
        random = self.random
        getrandbits = self.getrandbits
        if type(random) is BuiltinMethod or type(getrandbits) is Method:
            k = n.bit_length()
            r = getrandbits(k)
            while r >= n:
                r = getrandbits(k)

            return r
        if n >= maxsize:
            _warn('Underlying random() generator does not supply \nenough bits to choose from a population range this large.\nTo remove the range limitation, add a getrandbits() method.')
            return int(random() * n)
        else:
            if n == 0:
                raise ValueError('Boundary cannot be zero')
            rem = maxsize % n
            limit = (maxsize - rem) / maxsize
            r = random()
            while r >= limit:
                r = random()

            return int(r * maxsize) % n

    def choice(self, seq):
        """Choose a random element from a non-empty sequence."""
        try:
            i = self._randbelow(len(seq))
        except ValueError:
            raise IndexError('Cannot choose from an empty sequence') from None

        return seq[i]

    def shuffle(self, x, random=None):
        """Shuffle list x in place, and return None.

        Optional argument random is a 0-argument function returning a
        random float in [0.0, 1.0); if it is the default None, the
        standard random.random will be used.

        """
        if random is None:
            randbelow = self._randbelow
            for i in reversed(range(1, len(x))):
                j = randbelow(i + 1)
                x[i], x[j] = x[j], x[i]

        else:
            _int = int
            for i in reversed(range(1, len(x))):
                j = _int(random() * (i + 1))
                x[i], x[j] = x[j], x[i]

    def sample(self, population, k):
        """Chooses k unique random elements from a population sequence or set.

        Returns a new list containing elements from the population while
        leaving the original population unchanged.  The resulting list is
        in selection order so that all sub-slices will also be valid random
        samples.  This allows raffle winners (the sample) to be partitioned
        into grand prize and second place winners (the subslices).

        Members of the population need not be hashable or unique.  If the
        population contains repeats, then each occurrence is a possible
        selection in the sample.

        To choose a sample in a range of integers, use range as an argument.
        This is especially fast and space efficient for sampling from a
        large population:   sample(range(10000000), 60)
        """
        if isinstance(population, _Set):
            population = tuple(population)
        else:
            if not isinstance(population, _Sequence):
                raise TypeError('Population must be a sequence or set.  For dicts, use list(d).')
            else:
                randbelow = self._randbelow
                n = len(population)
                if not 0 <= k <= n:
                    raise ValueError('Sample larger than population or is negative')
                result = [
                 None] * k
                setsize = 21
                if k > 5:
                    setsize += 4 ** _ceil(_log(k * 3, 4))
            if n <= setsize:
                pool = list(population)
                for i in range(k):
                    j = randbelow(n - i)
                    result[i] = pool[j]
                    pool[j] = pool[(n - i - 1)]

            else:
                selected = set()
                selected_add = selected.add
                for i in range(k):
                    j = randbelow(n)
                    while j in selected:
                        j = randbelow(n)

                    selected_add(j)
                    result[i] = population[j]

        return result

    def choices(self, population, weights=None, *, cum_weights=None, k=1):
        """Return a k sized list of population elements chosen with replacement.

        If the relative weights or cumulative weights are not specified,
        the selections are made with equal probability.

        """
        random = self.random
        if cum_weights is None:
            if weights is None:
                _int = int
                total = len(population)
                return [population[_int(random() * total)] for i in range(k)]
            cum_weights = list(_itertools.accumulate(weights))
        else:
            if weights is not None:
                raise TypeError('Cannot specify both weights and cumulative weights')
        if len(cum_weights) != len(population):
            raise ValueError('The number of weights does not match the population')
        bisect = _bisect.bisect
        total = cum_weights[(-1)]
        hi = len(cum_weights) - 1
        return [population[bisect(cum_weights, random() * total, 0, hi)] for i in range(k)]

    def uniform(self, a, b):
        """Get a random number in the range [a, b) or [a, b] depending on rounding."""
        return a + (b - a) * self.random()

    def triangular(self, low=0.0, high=1.0, mode=None):
        """Triangular distribution.

        Continuous distribution bounded by given lower and upper limits,
        and having a given mode value in-between.

        http://en.wikipedia.org/wiki/Triangular_distribution

        """
        u = self.random()
        try:
            c = 0.5 if mode is None else (mode - low) / (high - low)
        except ZeroDivisionError:
            return low
        else:
            if u > c:
                u = 1.0 - u
                c = 1.0 - c
                low, high = high, low
            return low + (high - low) * (u * c) ** 0.5

    def normalvariate(self, mu, sigma):
        """Normal distribution.

        mu is the mean, and sigma is the standard deviation.

        """
        random = self.random
        while 1:
            u1 = random()
            u2 = 1.0 - random()
            z = NV_MAGICCONST * (u1 - 0.5) / u2
            zz = z * z / 4.0
            if zz <= -_log(u2):
                break

        return mu + z * sigma

    def lognormvariate(self, mu, sigma):
        """Log normal distribution.

        If you take the natural logarithm of this distribution, you'll get a
        normal distribution with mean mu and standard deviation sigma.
        mu can have any value, and sigma must be greater than zero.

        """
        return _exp(self.normalvariate(mu, sigma))

    def expovariate(self, lambd):
        """Exponential distribution.

        lambd is 1.0 divided by the desired mean.  It should be
        nonzero.  (The parameter would be called "lambda", but that is
        a reserved word in Python.)  Returned values range from 0 to
        positive infinity if lambd is positive, and from negative
        infinity to 0 if lambd is negative.

        """
        return -_log(1.0 - self.random()) / lambd

    def vonmisesvariate(self, mu, kappa):
        """Circular data distribution.

        mu is the mean angle, expressed in radians between 0 and 2*pi, and
        kappa is the concentration parameter, which must be greater than or
        equal to zero.  If kappa is equal to zero, this distribution reduces
        to a uniform random angle over the range 0 to 2*pi.

        """
        random = self.random
        if kappa <= 1e-06:
            return TWOPI * random()
        else:
            s = 0.5 / kappa
            r = s + _sqrt(1.0 + s * s)
            while 1:
                u1 = random()
                z = _cos(_pi * u1)
                d = z / (r + z)
                u2 = random()
                if u2 < 1.0 - d * d or u2 <= (1.0 - d) * _exp(d):
                    break

            q = 1.0 / r
            f = (q + z) / (1.0 + q * z)
            u3 = random()
            if u3 > 0.5:
                theta = (mu + _acos(f)) % TWOPI
            else:
                theta = (mu - _acos(f)) % TWOPI
            return theta

    def gammavariate(self, alpha, beta):
        """Gamma distribution.  Not the gamma function!

        Conditions on the parameters are alpha > 0 and beta > 0.

        The probability distribution function is:

                    x ** (alpha - 1) * math.exp(-x / beta)
          pdf(x) =  --------------------------------------
                      math.gamma(alpha) * beta ** alpha

        """
        if alpha <= 0.0 or beta <= 0.0:
            raise ValueError('gammavariate: alpha and beta must be > 0.0')
        else:
            random = self.random
            if alpha > 1.0:
                ainv = _sqrt(2.0 * alpha - 1.0)
                bbb = alpha - LOG4
                ccc = alpha + ainv
                while 1:
                    u1 = random()
                    if not 1e-07 < u1 < 0.9999999:
                        continue
                    u2 = 1.0 - random()
                    v = _log(u1 / (1.0 - u1)) / ainv
                    x = alpha * _exp(v)
                    z = u1 * u1 * u2
                    r = bbb + ccc * v - x
                    if r + SG_MAGICCONST - 4.5 * z >= 0.0 or r >= _log(z):
                        return x * beta

            else:
                if alpha == 1.0:
                    u = random()
                    while u <= 1e-07:
                        u = random()

                    return -_log(u) * beta
                else:
                    while 1:
                        u = random()
                        b = (_e + alpha) / _e
                        p = b * u
                        if p <= 1.0:
                            x = p ** (1.0 / alpha)
                        else:
                            x = -_log((b - p) / alpha)
                        u1 = random()
                        if p > 1.0:
                            if u1 <= x ** (alpha - 1.0):
                                break
                            else:
                                if u1 <= _exp(-x):
                                    break

                    return x * beta

    def gauss(self, mu, sigma):
        """Gaussian distribution.

        mu is the mean, and sigma is the standard deviation.  This is
        slightly faster than the normalvariate() function.

        Not thread-safe without a lock around calls.

        """
        random = self.random
        z = self.gauss_next
        self.gauss_next = None
        if z is None:
            x2pi = random() * TWOPI
            g2rad = _sqrt(-2.0 * _log(1.0 - random()))
            z = _cos(x2pi) * g2rad
            self.gauss_next = _sin(x2pi) * g2rad
        return mu + z * sigma

    def betavariate(self, alpha, beta):
        """Beta distribution.

        Conditions on the parameters are alpha > 0 and beta > 0.
        Returned values range between 0 and 1.

        """
        y = self.gammavariate(alpha, 1.0)
        if y == 0:
            return 0.0
        else:
            return y / (y + self.gammavariate(beta, 1.0))

    def paretovariate(self, alpha):
        """Pareto distribution.  alpha is the shape parameter."""
        u = 1.0 - self.random()
        return 1.0 / u ** (1.0 / alpha)

    def weibullvariate(self, alpha, beta):
        """Weibull distribution.

        alpha is the scale parameter and beta is the shape parameter.

        """
        u = 1.0 - self.random()
        return alpha * (-_log(u)) ** (1.0 / beta)


class SystemRandom(Random):
    __doc__ = 'Alternate random number generator using sources provided\n    by the operating system (such as /dev/urandom on Unix or\n    CryptGenRandom on Windows).\n\n     Not available on all systems (see os.urandom() for details).\n    '

    def random(self):
        """Get the next random number in the range [0.0, 1.0)."""
        return (int.from_bytes(_urandom(7), 'big') >> 3) * RECIP_BPF

    def getrandbits(self, k):
        """getrandbits(k) -> x.  Generates an int with k random bits."""
        if k <= 0:
            raise ValueError('number of bits must be greater than zero')
        if k != int(k):
            raise TypeError('number of bits should be an integer')
        numbytes = (k + 7) // 8
        x = int.from_bytes(_urandom(numbytes), 'big')
        return x >> numbytes * 8 - k

    def seed(self, *args, **kwds):
        """Stub method.  Not used for a system random number generator."""
        pass

    def _notimplemented(self, *args, **kwds):
        """Method should not be called for a system random number generator."""
        raise NotImplementedError('System entropy source does not have state.')

    getstate = setstate = _notimplemented


def _test_generator(n, func, args):
    import time
    print(n, 'times', func.__name__)
    total = 0.0
    sqsum = 0.0
    smallest = 10000000000.0
    largest = -10000000000.0
    t0 = time.time()
    for i in range(n):
        x = func(*args)
        total += x
        sqsum = sqsum + x * x
        smallest = min(x, smallest)
        largest = max(x, largest)

    t1 = time.time()
    print((round(t1 - t0, 3)), 'sec,', end=' ')
    avg = total / n
    stddev = _sqrt(sqsum / n - avg * avg)
    print('avg %g, stddev %g, min %g, max %g\n' % (
     avg, stddev, smallest, largest))


def _test(N=2000):
    _test_generator(N, random, ())
    _test_generator(N, normalvariate, (0.0, 1.0))
    _test_generator(N, lognormvariate, (0.0, 1.0))
    _test_generator(N, vonmisesvariate, (0.0, 1.0))
    _test_generator(N, gammavariate, (0.01, 1.0))
    _test_generator(N, gammavariate, (0.1, 1.0))
    _test_generator(N, gammavariate, (0.1, 2.0))
    _test_generator(N, gammavariate, (0.5, 1.0))
    _test_generator(N, gammavariate, (0.9, 1.0))
    _test_generator(N, gammavariate, (1.0, 1.0))
    _test_generator(N, gammavariate, (2.0, 1.0))
    _test_generator(N, gammavariate, (20.0, 1.0))
    _test_generator(N, gammavariate, (200.0, 1.0))
    _test_generator(N, gauss, (0.0, 1.0))
    _test_generator(N, betavariate, (3.0, 3.0))
    _test_generator(N, triangular, (0.0, 1.0, 0.3333333333333333))


_inst = Random()
seed = _inst.seed
random = _inst.random
uniform = _inst.uniform
triangular = _inst.triangular
randint = _inst.randint
choice = _inst.choice
randrange = _inst.randrange
sample = _inst.sample
shuffle = _inst.shuffle
choices = _inst.choices
normalvariate = _inst.normalvariate
lognormvariate = _inst.lognormvariate
expovariate = _inst.expovariate
vonmisesvariate = _inst.vonmisesvariate
gammavariate = _inst.gammavariate
gauss = _inst.gauss
betavariate = _inst.betavariate
paretovariate = _inst.paretovariate
weibullvariate = _inst.weibullvariate
getstate = _inst.getstate
setstate = _inst.setstate
getrandbits = _inst.getrandbits
if __name__ == '__main__':
    _test()