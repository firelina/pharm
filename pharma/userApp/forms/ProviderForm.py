from flask_wtf import FlaskForm
from wtforms import TimeField, SubmitField, SelectField, IntegerField, FloatField, StringField
from wtforms.validators import DataRequired


# форма для добавления поставщика
class ProviderForm(FlaskForm):
    # transport = SelectField('Транспорт', validators=[DataRequired()], validate_choice=False)
    name = StringField('Название поставщика', validators=[DataRequired()])
    adress = StringField('Адрес поставщика', validators=[DataRequired()])
    telethon = StringField('Телефон', validators=[DataRequired()])
    submit = SubmitField('Отправить')