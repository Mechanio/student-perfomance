from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from main_temp.models import Teachers, Students, Subject, Marks, Classes
from main_temp import db

class RegistrationTeacherForm(FlaskForm):
    fullname = StringField('Fullname',
                           validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_fullname(self, fullname):
        teacher = Teachers.query.filter_by(fullname=fullname.data).first()
        if teacher:
            raise ValidationError('Name is already taken')

    def validate_email(self, email):
        teacher = Teachers.query.filter_by(email=email.data).first()
        if teacher:
            raise ValidationError('Email is already taken')


class RegistrationStudentForm(FlaskForm):
    fullname = StringField('Fullname',
                           validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    class_ = StringField('Class', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_fullname(self, fullname):
        teacher = Teachers.query.filter_by(fullname=fullname.data).first()
        if teacher:
            raise ValidationError('Name is already taken')

    def validate_email(self, email):
        teacher = Teachers.query.filter_by(email=email.data).first()
        if teacher:
            raise ValidationError('Email is already taken')

    def validate_class_(self, class_):
        temp = Classes.query.filter_by(name=class_.data).first()
        if not temp:
            new_class = Classes(name=class_.data)
            db.session.add(new_class)
            db.session.commit()

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')