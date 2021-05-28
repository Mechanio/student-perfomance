from flask import Blueprint, render_template, url_for
# from main_temp import subjects

main = Blueprint('main', __name__)


@main.route('/home')
def home():
    return render_template('home.html', title='SPJ')#,subjects=subjects)


@main.route('/about')
def about():
    return render_template('about.html', title='About')
