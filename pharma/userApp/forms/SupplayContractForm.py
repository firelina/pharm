from flask_wtf import FlaskForm
from wtforms import TimeField, SubmitField, SelectField, IntegerField, FloatField, StringField, DateField
from wtforms.validators import DataRequired


# форма для добавления поставщика
class SupplayContractForm(FlaskForm):
    # transport = SelectField('Транспорт', validators=[DataRequired()], validate_choice=False)
    id_batch = SelectField('Партия', validators=[DataRequired()])
    id_drugstore = SelectField('Аптека', validators=[DataRequired()])
    contract_date = DateField('Дата заключения контракта', validators=[DataRequired()])
    id_employee = SelectField('Работник', validators=[DataRequired()])
    notes = StringField('Заметки', validators=[DataRequired()])
    submit = SubmitField('Отправить')