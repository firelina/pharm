from flask_wtf import FlaskForm
from wtforms import TimeField, SubmitField, SelectField, IntegerField, FloatField, StringField
from wtforms.validators import DataRequired


# форма для добавления аптекаи
class DrugstoreForm(FlaskForm):
    # transport = SelectField('Транспорт', validators=[DataRequired()], validate_choice=False)
    name = StringField('Название аптеки', validators=[DataRequired()])
    adress = StringField('Адрес аптеки', validators=[DataRequired()])
    telethon = StringField('Телефон', validators=[DataRequired()])
    submit = SubmitField('Отправить')