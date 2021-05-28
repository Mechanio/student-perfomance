from flask import render_template, url_for,session, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from main_temp import db, bcrypt, login_manager, app
from main_temp.users.forms import RegistrationTeacherForm, RegistrationStudentForm, LoginForm
from  main_temp.models import Teachers, Subject, Students, Marks, Classes, Subject_classes


users = Blueprint('users', __name__)
main_user = Blueprint("main_user", __name__)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        teacher = Teachers.query.filter_by(email=form.email.data).first()
        student = Students.query.filter_by(email=form.email.data).first()
        if teacher and bcrypt.check_password_hash(teacher.password, form.password.data):
            login_user(teacher, remember=form.remember.data)
            next_page = request.args.get('next')
            session['account_type'] = 'Teachers'
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        elif student and bcrypt.check_password_hash(student.password, form.password.data):
            login_user(student, remember=form.remember.data)
            next_page = request.args.get('next')
            session['account_type'] = 'Students'
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/register_teacher", methods=['GET', 'POST'])
def register_teacher():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationTeacherForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        teacher = Teachers(fullname=form.fullname.data, email=form.email.data, password=hashed_password)
        db.session.add(teacher)
        db.session.commit()
        flash(f'Account created for {form.fullname.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register_teacher.html', title='Register', form=form)


@users.route("/register_student", methods=['GET', 'POST'])
def register_student():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationStudentForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        temp = Classes.query.filter_by(name=form.class_.data).first()
        student = Students(fullname=form.fullname.data, email=form.email.data, members=temp, password=hashed_password)
        db.session.add(student)
        db.session.commit()
        flash(f'Account created for {form.fullname.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register_student.html', title='Register', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')


@login_manager.user_loader
def load_user(user_id):
    if session['account_type'] == 'Students':
        return Students.query.get(int(user_id))
    elif session['account_type'] == 'Teachers':
        return Teachers.query.get(int(user_id))


    # if app.config['APPLICATION_ROOT'] == '/teacher':
    #     print('abcs')
    #     return Teachers.query.get(int(user_id))
    # elif app.config['APPLICATION_ROOT'] == '/student':
    #     print('abcasfs')
    #     return Students.query.get(int(user_id))
    # else:
    #     print("sadaf")





