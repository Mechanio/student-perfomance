from main_temp import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_teacher(teacher_id):
    return Teachers.query.get(int(teacher_id))


@login_manager.user_loader
def load_student(student_id):
    return Students.query.get(int(student_id))


class Teachers(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    teacher_subject = db.relationship('Subject', backref='subjects')


class Classes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    class_students = db.relationship('Students', backref='members')


class Students(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    subject_class = db.relationship('Subject_classes')


class Marks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer)
    student_id = db.Column(db.Integer)
    teacher_id = db.Column(db.Integer)
    class_id = db.Column(db.Integer)
    date = db.Column(db.Text)
    mark = db.Column(db.Integer)
    type = db.Column(db.String(120))


class Subject_classes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    class_id = db.Column(db.Integer)
