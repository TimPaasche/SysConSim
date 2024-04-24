from sympy import pretty, sympify

# Example usage
formal_expression = "1/2 * (3*x + 4*y**2)"
expr = sympify(formal_expression, evaluate=False)
human_readable_expression = pretty(expr,  use_unicode=True)
print(human_readable_expression)
