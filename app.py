from math import cos, sin
from flask import Flask, render_template, request, redirect, url_for
from forms.one_equation_form import OneEquationForm
from forms.equation_system_form import EquationSystemForm

from utils.math_methods.one_equation.chord import chord_method
from utils.math_methods.one_equation.newton import newton_method
from utils.math_methods.one_equation.simple_iteration import simple_iteration_method
from utils.math_methods.equation_system.newton import newton_system_method

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ukDSvjgGDjy678i3hrb^&B*&Bgjhfn'

# методы хорд, Ньютона, простой итерации для одного уравнения
# метод Ньютона для системы
@app.route('/')
def start_page():
    return render_template('start.html')

@app.route('/one-equation', methods=['GET', 'POST'])
def one_equation():
    form = OneEquationForm()
    if form.validate_on_submit():
        equation = form.equation.data
        method = form.method.data
        a = form.a.data
        b = form.b.data
        eps = form.eps.data
        if equation == 'x^3 - x + 4':
            f = lambda x: x ** 3 - x + 4
            f_ = lambda x: 3 * x ** 2 - 1
            f__ = lambda x: 6 * x
        elif equation == 'x^2 - 4':
            f = lambda x: x ** 2 - 4
            f_ = lambda x: 2 * x
            f__ = lambda x: 2
        else:
            f = lambda x: sin(x) - 0.5
            f_ = lambda x: cos(x)
            f__ = lambda x: -sin(x)
        try:
            if f(a) * f(b) > 0 or f__(a) * f__(b) < 0:
            # if f_(a) * f_(b) > 0:
                 raise ValueError('Некорректный отрезок')
            if method == 'chord_method':
                result = chord_method(a, b, f, eps)
            elif method == 'newton_method':
                result = newton_method(a, b, f, f_, f__, eps)
            else:
                result = simple_iteration_method(a, b, f, f_, f__, eps)
        except ValueError as e:
            return render_template('one-equation.html', form=form, result=e)
        return render_template('one-equation.html', form=form, result=result)
    return render_template('one-equation.html', form=form)


@app.route('/equation-system', methods=['GET', 'POST'])
def equation_system():
    form = EquationSystemForm()
    if form.validate_on_submit():
        equation = form.equation.data
        x0 = form.x0.data
        y0 = form.y0.data
        eps = form.eps.data
        if equation == 'x^2 + y^2 = 4 && y = 3x^2':
            f = lambda x, y: x ** 2 + y ** 2 - 4
            g = lambda x, y: y - 3 * x ** 2
            f_x = lambda x, y: 2 * x
            f_y = lambda x, y: 2 * y
            g_x = lambda x, y: -6 * x
            g_y = lambda x, y: 1
        else:
            f = lambda x, y: y - sin(x)
            g = lambda x, y: y - cos(x)
            f_x = lambda x, y: -cos(x)
            f_y = lambda x, y: 1
            g_x = lambda x, y: sin(x)
            g_y = lambda x, y: 1
        try:
            x1, y1, cnt, delta_x, delta_y = newton_system_method(f_x, f_y, g_x, g_y, f, g, x0, y0, eps)
        except ValueError as e:
            return render_template('equation-system.html', form=form, result=e)
        return render_template('equation-system.html', form=form, result=f"x = {x1}, y={y1}, ответ получен за {cnt} итераций. Погрешность x: {delta_x}, погрешность y: {delta_y}")
    return render_template('equation-system.html', form=form)


if __name__ == '__main__':
    app.run()
