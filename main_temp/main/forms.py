from flask_wtf import FlaskForm
from wtforms import SelectField, StringField


class Students_form(FlaskForm):
    students = SelectField('students', choices=[])


class Add_date_form(FlaskForm):
    date = StringField('Date')
    type = StringField('Type of Lesson')