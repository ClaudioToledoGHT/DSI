from flask import Blueprint

produto = Blueprint("produtos", __name__, template_folder='templates')

from . import views