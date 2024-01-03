from create_zorgette_catalogue import Tuple
#!/usr/bin/env python3

import argparse
import json
import fractions
import sympy
import padic

parser = argparse.ArgumentParser()
parser.add_argument("--prime", type=int, default=409,
                    help="What prime was used with create_zorgette_catalogue.py")
parser.add_argument("--input-file", default="zorgette-catalog.json",
                    help="File generated by create_zorgette_catalogue.py. Should be a list of 3-element lists")
args = parser.parse_args()

data = json.load(open(args.input_file))

# Something funny about this... there's only one division. That
# doesn't seem right. Unless A is really big?
def cross_product(v1: Tuple[float, float, float], v2: Tuple[float, float, float]) -> Tuple[float, float, float]:
    return (
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0]
    )

def dot_product(v1: Tuple[float, float, float], v2: Tuple[float, float, float]) -> float:
    return sum(x * y for x, y in zip(v1, v2))


class PlaceValued:
    def __init__(self, prime: int, prime_symbol: str, number: int) -> None:
        if number == 0:
            return 0
        signum = 1
        if number < 0:
            signum = -1
            number = -number
        # number is now positive
        expression = 0
        power = 0
        while number > 0:
            remainder = number % prime
            expression += remainder * (prime_symbol ** power)
            power += 1
            number = number - remainder
            number = number // prime
        return signum * expression

class PlaneEquation:
    def __init__(self, A: float, B: float, C: float, D: float) -> None:
        self.A = A
        self.B = B
        self.C = C
        self.D = D

    def fractional_expression(self) -> Tuple[sympy.Expr, sympy.Expr]:
        x, y, z = sympy.symbols('x y z')
        self.fractional_lhs_expression = x
        self.fractional_rhs_expression = (
            - fractions.Fraction(self.B,self.A) * y
            - fractions.Fraction(self.C,self.A) * z
            - fractions.Fraction(self.D,self.A)
        )
        return (self.fractional_lhs_expression, self.fractional_rhs_expression)

    def fractional_expression_string(self) -> str:
        l,r = self.fractional_expression()
        return str(l) + " = " + str(r)

    def integer_expression(self) -> Tuple[sympy.Expr, sympy.Expr]:
        x, y, z = sympy.symbols('x y z')
        self.integral_lhs_expression = self.A * x
        self.integral_rhs_expression = - self.B * y - self.C * z - self.D
        return (self.integral_lhs_expression, self.integral_rhs_expression)

    def integer_expression_string(self) -> str:
        l,r = self.fractional_expression()
        return str(l) + " = " + str(r)

    def __str__(self):
        return self.integer_expression_string()

def find_plane_equation(p1, p2, p3):
    v1 = [p2[i] - p1[i] for i in range(3)]
    v2 = [p3[i] - p1[i] for i in range(3)]
    normal = cross_product(v1, v2)
    A, B, C = normal
    D = -dot_product(normal, p1)
    return PlaneEquation(A, B, C, D)

def solve_for_x(equation, y, z):
    if equation.A == 0:
        raise ValueError("A cannot be zero for this equation.")
    return (-equation.B*y - equation.C*z - equation.D) // equation.A  # Use integer division for integers and fractions


best_triple = None
score = None
best_equation = None

for i, p1 in enumerate(data):
    for j, p2 in enumerate(data):
        if j <= i:
            continue
        for k, p3 in enumerate(data):
            if k <= i or k <= j:
                continue
            equation = find_plane_equation(p1, p2, p3)
            # Now, we go through each point in our data set and
            # see what the residual is.
            sum_of_residuals = 0.0
            for p4 in data:
                p4_hat = solve_for_x(equation, p4[1], p4[2])
                residual = padic.distance(args.prime, p4[0], p4_hat)
                sum_of_residuals += residual
            if score is None or sum_of_residuals < score:
                score = sum_of_residuals
                best_triple = (p1,p2,p3)
                best_equation = equation
                print(f"{best_equation}  -> {score}")

print()
print(best_equation)
