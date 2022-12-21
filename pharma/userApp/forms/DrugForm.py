from flask_wtf import FlaskForm
from wtforms import TimeField, SubmitField, SelectField, BooleanField, FloatField, StringField, DateField
from wtforms.validators import DataRequired


# форма для добавления партии
class DrugForm(FlaskForm):
    # transport = SelectField('Транспорт', validators=[DataRequired()], validate_choice=False)
    name = StringField('Название лекарства', validators=[DataRequired()])
    price = FloatField('Цена лекарства', validators=[DataRequired()])
    release_date = DateField('Дата производства', validators=[DataRequired()])
    id_provider = SelectField('Поставщик', validators=[DataRequired()], validate_choice=False)
    consist = StringField('Состав лекарства', validators=[DataRequired()])
    suitability = BooleanField('Годно ли лекарство')
    # people = FloatField('Скорость пребывания людей на станцию', validators=[DataRequired()])
    # length = IntegerField('Длина маршрута', validators=[DataRequired()])
    # time = IntegerField('Время тестирования в минутах', validators=[DataRequired()])
    submit = SubmitField('Отправить')