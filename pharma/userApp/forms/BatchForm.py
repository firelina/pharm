from flask_wtf import FlaskForm
from wtforms import TimeField, SubmitField, SelectField, IntegerField, FloatField, StringField, DateField
from wtforms.validators import DataRequired


# форма для добавления партии
class BatchForm(FlaskForm):
    goods_number = IntegerField('Количество товаров', validators=[DataRequired()])
    batch_date = DateField('Дата поставки', validators=[DataRequired()])
    id_provider = SelectField('Поставщик', validators=[DataRequired()], validate_choice=False)
    id_drug = SelectField('Леарство', validators=[DataRequired()], validate_choice=False)
    submit = SubmitField('Отправить')