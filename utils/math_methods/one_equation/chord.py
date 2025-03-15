def chord_method(a, b, f, eps):
    x0 = a - (b- a) / (f(b) - f(a)) * f(a)
    if a * x0 < 0:
        b = x0
    else:
        a = x0
    x = a - (b - a) / (f(b) - f(a)) * f(a)
    while abs(x - x0) > eps:
        x0 = x
        if a * x0 < 0:
            b = x0
        else:
            a = x0
        x = a - (b - a) / (f(b) - f(a)) * f(a)
    return x
