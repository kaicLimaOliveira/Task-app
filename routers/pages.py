from flask import Blueprint, request
from controllers.PagesController import Pages

pages = Blueprint('pages', __name__, template_folder='templates', url_prefix='/')


@pages.route('', methods=['GET'])
def index():
    return Pages().index(request)

@pages.route('import', methods=['GET', 'POST'])
def imports():
    return Pages().new_imports(request)

@pages.route('errors_report', methods=['GET'])
def errors_report():
    return Pages().errors_report(request)

@pages.route('user/<link>', methods=['GET'])
def user(link):
    return Pages().user(request, link)
