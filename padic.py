import fractions
# Calculate padic measure
def measure(prime, q):
    if q == 0:
        return None
    if type(q) == fractions.Fraction:
        return measure(prime, q.numerator) - measure(prime, q.denominator)
    if type(q) == int:
        if q % prime != 0:
            return 1.0
        return 1.0 + measure(prime, q // prime)
    raise ValueError(q)

# Calculate padic distance between r and s
def distance(prime, r, s):
    q = r - s
    m = measure(prime, q)
    if m is None:
        answer = 0.0
    else:
        answer = prime ** (- m)
    return answer
