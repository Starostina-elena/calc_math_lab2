from flask_wtf import FlaskForm
from wtforms import RadioField, FloatField, SubmitField
from wtforms.validators import DataRequired, InputRequired, NumberRange


class EquationSystemForm(FlaskForm):
    equation = RadioField('Выберите систему уравнений', choices=[
        'x^2 + y^2 = 4 && y = 3x^2',
        'y = sin(x) && y = cos(x)',
    ], validators=[DataRequired()])

    x0 = FloatField('Введите начальное приближение для x', validators=[InputRequired()])
    y0 = FloatField('Введите начальное приближение для y', validators=[InputRequired()])
    eps = FloatField('Введите значение eps', validators=[DataRequired(), NumberRange(0.0000001, 5)])

    submit = SubmitField('Решить')
