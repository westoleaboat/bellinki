from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
from ..models import Permission, User, Follow, Role, Post, Comment
from flask_migrate import upgrade



@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)

 # migrate database to latest revision
# upgrade()

# # create or update user roles
# Role.insert_roles()

# # ensure all users are following themselves
# User.add_self_follows()