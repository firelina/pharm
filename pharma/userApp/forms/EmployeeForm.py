from flask_wtf import FlaskForm
from wtforms import TimeField, SubmitField, SelectField, IntegerField, FloatField, StringField, DateField
from wtforms.validators import DataRequired


# форма для добавления аптекаи
class EmployeeForm(FlaskForm):
    # transport = SelectField('Транспорт', validators=[DataRequired()], validate_choice=False)
    name = StringField('Имя работника', validators=[DataRequired()])
    surname = StringField('Фамилия работника', validators=[DataRequired()])
    fathername = StringField('Отчество работника', validators=[DataRequired()])
    gender = StringField('Пол работника', validators=[DataRequired()])
    telethon = StringField('Телефон работника', validators=[DataRequired()])
    birthday = DateField('Дата рождения работника', validators=[DataRequired()])
    hire_date = DateField('Дата найма работника', validators=[DataRequired()])
    id_drugstore = SelectField('Аптека', validators=[DataRequired()], validate_choice=False)
    salary = FloatField('Зарплата работника', validators=[DataRequired()])
    submit = SubmitField('Отправить')