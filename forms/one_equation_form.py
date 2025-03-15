from flask_wtf import FlaskForm
from wtforms import RadioField, FloatField, SubmitField
from wtforms.validators import DataRequired, InputRequired, NumberRange


class OneEquationForm(FlaskForm):
    equation = RadioField('Выберите уравнение', choices=[
        'x^3 - x + 4',
        'x^2 - 4',
        'sin(x) - 0.5'
    ], validators=[DataRequired()])

    method = RadioField('Выберите метод', choices=[
        ('chord_method', 'Метод хорд'),
        ('newton_method', 'Метод Ньютона'),
        ('simple_iteration_method', 'Метод простой итерации')
    ], validators=[DataRequired()])

    a = FloatField('Введите значение a', validators=[InputRequired()])
    b = FloatField('Введите значение b', validators=[InputRequired()])
    eps = FloatField('Введите значение eps', validators=[DataRequired(), NumberRange(0.0000001, 5)])

    submit = SubmitField('Решить')
