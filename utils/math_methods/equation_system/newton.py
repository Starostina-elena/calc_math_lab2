def newton_system_method(f_x, f_y, g_x, g_y, f, g,  x0, y0, eps):
    dy = (-g(x0, y0) + g_x(x0, y0) * f(x0, y0)) / (g_y(x0, y0) - f_y(x0, y0) * g_x(x0, y0))
    dx = -f(x0, y0) - f_y(x0, y0) * dy

    x1 = x0 + dx
    y1 = y0 + dy

    cnt = 1

    while abs(x1 - x0) > eps or abs(y1 - y0) > eps:
        x0 = x1
        y0 = y1
        dy = (-g(x0, y0) + g_x(x0, y0) * f(x0, y0)) / (g_y(x0, y0) - f_y(x0, y0) * g_x(x0, y0))
        dx = -f(x0, y0) - f_y(x0, y0) * dy

        x1 = x0 + dx
        y1 = y0 + dy

        cnt += 1

    return x1, y1, cnt, x1 - x0, y1 - y0
