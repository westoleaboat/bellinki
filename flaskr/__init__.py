import os

from flask import Flask, render_template, session, redirect, url_for

from flask_bootstrap import Bootstrap

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_moment import Moment
from flask_mail import Mail

from flask_jwt_extended import JWTManager


from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade

from flask_login import LoginManager

from datetime import datetime
from dotenv import load_dotenv
from flask_pagedown import PageDown





bootstrap = Bootstrap()
moment = Moment()
mail = Mail()
db = SQLAlchemy()
migrate = Migrate()
pagedown = PageDown()
jwt = JWTManager()


login_manager = LoginManager()
login_manager.login_view = 'auth.login'

basedir = os.path.abspath(os.path.dirname(__file__))
def create_app():
    # create and configure the app
    app = Flask(__name__)
    load_dotenv()
    app.config['SECRET_KEY'] = 'hard to guess string'
    app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASKY_ADMIN'] = 'chacotasprod@admin.com'
    app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[PSI]'
    app.config['FLASKY_MAIL_SENDER'] = 'Admin <admin@example.com>'


    app.config['MAIL_SERVER']=os.environ.get('MAIL_SERVER')
    app.config['MAIL_PORT'] = (os.environ.get('MAIL_PORT'))
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    app.config['MAIL_USERNAME']= os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    
    app.config['FLASKY_POSTS_PER_PAGE'] = 20
    app.config['FLASKY_FOLLOWERS_PER_PAGE'] = 50
    app.config['FLASKY_COMMENTS_PER_PAGE'] = 30
    app.config['FLASKY_SLOW_DB_QUERY_TIME'] = 0.5

    @staticmethod
    def init_app(app):
        pass

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    jwt.init_app(app)

    login_manager.init_app(app)
    pagedown.init_app(app)

    @app.shell_context_processor
    def make_shell_context():
        # from .models import Permission
        return dict(db=db, User=User, Role=Role, Permission=Permission, Post=Post, Comment=Comment)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')


    @app.cli.command()
    def test():
        """Run the unit tests."""
        import unittest
        tests = unittest.TestLoader().discover('tests')
        unittest.TextTestRunner(verbosity=2).run(tests)


    with app.app_context():
            from .models import Role, User

            db.create_all()
            upgrade()  # Assuming you want to upgrade the database as well
            Role.insert_roles()
            print('roles inserted!')
            User.add_self_follows()
            
            

    return app
