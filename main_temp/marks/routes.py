from flask import request, render_template, session, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from main_temp import db, bcrypt
from main_temp.users.forms import RegistrationTeacherForm, RegistrationStudentForm, LoginForm
from main_temp.models import Teachers, Subject, Students, Marks, Classes, Subject_classes
from main_temp.main.forms import Students_form, Add_date_form

marks = Blueprint('marks', __name__)

@marks.route("/table")
@login_required
def table():
    if session['account_type'] == 'Students':
        subject = []
        subjects = Subject_classes.query.filter_by(class_id=current_user.class_id)
        for i in subjects:
            subject.append(i.subject_id)
        subjects = []
        for i in subject:
            temps = Subject.query.filter_by(id=i).first()
            subjects.append(temps.name)
        return render_template('layout.html', title='Table', subjects=subjects)
    elif session['account_type'] == 'Teachers':
        teacher = Teachers.query.filter_by(id=current_user.id).first()
        teacher = teacher.teacher_subject
        subjects = []
        for i in teacher:
            temps = i.subject_class
            subjects.append(temps)
        classes_and_subjects = {}
        final_classes_and_subjects = {}
        unique_classes_ids = []
        for i in subjects:
            for j in i:
                if j.class_id not in unique_classes_ids:
                    unique_classes_ids.append(j.class_id)
        for i in unique_classes_ids:
            temps = Subject_classes.query.filter_by(class_id=i)
            classes_and_subjects[i] = []
            for j in temps:
                classes_and_subjects[i].append(j.subject_id)
        for i in classes_and_subjects:
            class_name = Classes.query.filter_by(id=i).first().name
            final_classes_and_subjects[class_name] = []
            for j in classes_and_subjects[i]:
                subject_name = Subject.query.filter_by(id=j).first().name
                final_classes_and_subjects[class_name].append(subject_name)
        return render_template('layout.html', title='Table',
                               classes_and_subjects=final_classes_and_subjects)

@marks.route("/table/")
@marks.route("/table/<subject_name>/<class_name>")
@marks.route("/table/<subject_name>/<class_name>/<student_name>", methods=['GET', 'POST'])
@login_required
def table_with_variables(subject_name, class_name, student_name='show'):
    if session['account_type'] == 'Students':
        subject = []
        subjects = Subject_classes.query.filter_by(class_id=current_user.class_id)
        for i in subjects:
            subject.append(i.subject_id)
        subjects = []
        for i in subject:
            temps = Subject.query.filter_by(id=i).first()
            subjects.append(temps.name)

        temp = Subject.query.filter_by(name=subject_name).first()
        current_subject = Marks.query.filter_by(class_id=current_user.class_id,
                                                student_id=current_user.id,
                                                subject_id=temp.id)
        return render_template('table.html', title='Table', marks_=current_subject, subjects=subjects)
    if session['account_type'] == 'Teachers':
        adding_bool = False
        students_form = Students_form()
        if request.method == "POST":
            if request.form["submit_button"] == "Load Student":
                student_name = students_form.students.data
            if request.form["submit_button"] == "Add new date":
                adding_bool = True
                adding_form = Add_date_form()
                if adding_form.validate():
                    print("valid")
                print(adding_form.errors)
                if adding_form.validate_on_submit():
                    date = adding_form.date.data
                    type = adding_form.type.data
                    class_id = Classes.query.filter_by(name=class_name).first().id
                    student_id = Students.query.filter_by(fullname=student_name, class_id=class_id).first().id
                    subject_id = Subject.query.filter_by(name=subject_name).first().id
                    new_mark = Marks(subject_id=subject_id, student_id=student_id,
                                     teacher_id=current_user.id, class_id=class_id,
                                     date=date, type=type)
                    db.session.add(new_mark)
                    db.session.commit()
        if class_name and class_name is not None and student_name and student_name is not None:
            class_id = Classes.query.filter_by(name=class_name).first().id
            if student_name == 'show':
                student_name = Students.query.filter_by(class_id=class_id).first().fullname
            student_id = Students.query.filter_by(fullname=student_name, class_id=class_id).first().id
            subject_id = Subject.query.filter_by(name=subject_name).first().id
            current_subject = Marks.query.filter_by(subject_id=subject_id,
                                                    teacher_id=current_user.id,
                                                    class_id=class_id,
                                                    student_id=student_id)
        teacher = Teachers.query.filter_by(id=current_user.id).first()
        teacher = teacher.teacher_subject
        subjects = []
        for i in teacher:
            temps = i.subject_class
            subjects.append(temps)
        current_subject_students = Classes.query.filter_by(id=class_id).first().class_students
        for i in current_subject_students:
            student = i.fullname
            if student not in students_form.students.choices:
                students_form.students.choices.append(student)
        classes_and_subjects = {}
        final_classes_and_subjects = {}
        unique_classes_ids = []
        for i in subjects:
            for j in i:
                if j.class_id not in unique_classes_ids:
                    unique_classes_ids.append(j.class_id)
        for i in unique_classes_ids:
            temps = Subject_classes.query.filter_by(class_id=i)
            classes_and_subjects[i] = []
            for j in temps:
                classes_and_subjects[i].append(j.subject_id)
        for i in classes_and_subjects:
            class_name_ = Classes.query.filter_by(id=i).first().name
            final_classes_and_subjects[class_name_] = []
            for j in classes_and_subjects[i]:
                subject_name_ = Subject.query.filter_by(id=j).first().name
                final_classes_and_subjects[class_name_].append(subject_name_)
        if adding_bool:
            return render_template('table_for_teacher.html', title='Table', marks_=current_subject,
                               classes_and_subjects=final_classes_and_subjects, student_name=student_name,
                               form=students_form, adding_form=adding_form)
        else:
            return render_template('table_for_teacher.html', title='Table', marks_=current_subject,
                                   classes_and_subjects=final_classes_and_subjects, student_name=student_name,
                                   form=students_form)
