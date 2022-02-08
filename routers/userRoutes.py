from flask import Blueprint, request
from controllers.UserController import User

user = Blueprint('user', __name__, template_folder='templates', url_prefix='/user')

@user.route('/<link>', methods=['GET'])
def index(link):
    return User().index(request, link)

