from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, DateField
# from wtforms.fields.html5 import EmailField
from wtforms.fields import DateField, EmailField, TelField, SelectField
from wtforms.validators import DataRequired


# форма для регистрации
class RegisterForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    id_employee = SelectField('Администратор', validators=[DataRequired()], validate_choice=False)
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')
