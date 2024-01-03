# Calculate padic measure
def measure(prime, q):
    if q == 0:
        return 0.0
    if q % prime != 0:
        return 1.0
    return 1.0 + measure(prime, q // prime)

# Calculate padic distance between r and s
def distance(prime, r, s):
    q = r - s
    answer = prime ** (- measure(prime, q))
    return answer
