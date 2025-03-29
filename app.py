import io
from math import cos, sin
from flask import Flask, render_template, request, redirect, url_for, make_response, send_file
from forms.one_equation_form import OneEquationForm
from forms.equation_system_form import EquationSystemForm

from utils.math_methods.one_equation.chord import chord_method
from utils.math_methods.one_equation.newton import newton_method
from utils.math_methods.one_equation.simple_iteration import simple_iteration_method
from utils.math_methods.equation_system.newton import newton_system_method

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ukDSvjgGDjy678i3hrb^&B*&Bgjhfn'


@app.route('/download_report', methods=['POST'])
def download_report():
    equation = request.form['equation']
    method = request.form['method']
    a = request.form['a']
    b = request.form['b']
    eps = request.form['eps']
    result = request.form['result']
    report_content = f"Equation: {equation}\nMethod: {method}\nInterval: [{a}, {b}]\nEpsilon: {eps}\nResult: {result}\n"
    report = io.StringIO(report_content)
    return send_file(io.BytesIO(report.getvalue().encode('utf-8')),
                     mimetype='text/plain',
                     as_attachment=True,
                     download_name='report.txt')


@app.route('/download_report_system', methods=['POST'])
def download_report_system():
    equation = request.form['equation']
    method = request.form['method']
    eps = request.form['eps']
    result = request.form['result']
    report_content = f"Equation: {equation}\nMethod: {method}\nEpsilon: {eps}\nResult: {result}\n"
    report = io.StringIO(report_content)
    return send_file(io.BytesIO(report.getvalue().encode('utf-8')),
                     mimetype='text/plain',
                     as_attachment=True,
                     download_name='report.txt')


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
            if f(a) * f(b) > 0:
                 raise ValueError('Некорректный отрезок: корня нет или корней больше одного')
            if f_(a) * f_(b) < 0:
                 raise ValueError('Некорректный отрезок: больше одного корня (производная не сохраняет знак)')
            if method == 'chord_method':
                result = chord_method(a, b, f, eps)
            elif method == 'newton_method':
                result = newton_method(a, b, f, f_, f__, eps)
            else:
                result = simple_iteration_method(a, b, f, f_, f__, eps)
            y = f(result)
        except (ValueError, ZeroDivisionError) as e:
            return render_template('one-equation.html', form=form, result=e, y=None)
        return render_template('one-equation.html', form=form, result=result, y=y)
    if request.method == 'POST':
        return render_template('one-equation.html', form=form, y=None, result='Введите корректные данные')
    return render_template('one-equation.html', form=form, result=None, y=None)


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
            return render_template('equation-system.html', form=form, x=e, y=None)
        return render_template('equation-system.html', form=form, y=y1, x=x1, result=f"x = {x1}, y={y1}, ответ получен за {cnt} итераций. Погрешность x: {delta_x}, погрешность y: {delta_y}")
    if request.method == 'POST':
        return render_template('equation-system.html', form=form, y=None, x=None, result='Введите корректные данные')
    return render_template('equation-system.html', form=form, y=None, x=None)


if __name__ == '__main__':
    app.run()
