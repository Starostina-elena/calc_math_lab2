def newton_method(a, b, f, f_, f__, eps):
    if f(a) * f__(a) > 0:
        x0 = a
    elif f(b) * f__(b) > 0:
        x0 = b
    else:
        raise ValueError('Метод неприменим')
    x = x0 - f(x0) / f_(x0)
    while abs(x - x0) > eps:
        x0 = x
        x = x0 - f(x0) / f_(x0)
    return x
