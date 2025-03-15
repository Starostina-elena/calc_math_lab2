def simple_iteration_method(a, b, f, f_, f__, eps):
    lambda_ = 1 / max(abs(f_(a)), abs(f_(b)))
    if f_(a) > 0:
        lambda_ *= -1
    if 1 + lambda_ * f_(a) > 1 or 1 + lambda_ * f_(b) > 1:
        raise ValueError('Уравнение не сходится')

    if f(a) > 0 and f__(a) > 0 or f(a) < 0 and f__(a) < 0:
        x0 = a
    else:
        x0 = b

    x1 = x0 + lambda_ * f(x0)

    cnt = 0
    while abs(x1 - x0) > eps:
        cnt += 1
        x0 = x1
        x1 = x0 + lambda_ * f(x0)
        if cnt > 1000:
            raise ValueError('Превышено количество итераций')

    return x1
