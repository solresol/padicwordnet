import fractions
from typing import Optional, Union
# Calculate padic measure
def measure(prime: int, q: Union[int, fractions.Fraction]) -> Optional[float]:
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
def distance(prime: int, r: Union[int, fractions.Fraction], s: Union[int, fractions.Fraction]) -> float:
    q = r - s
    m = measure(prime, q)
    if m is None:
        answer = 0.0
    else:
        answer = prime ** (- m)
    return answer
