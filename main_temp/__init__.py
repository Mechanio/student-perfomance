from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'



from main_temp.users.routes import users
from main_temp.main.routes import main
from main_temp.marks.routes import marks

app.register_blueprint(users)
app.register_blueprint(main)
app.register_blueprint(marks)


