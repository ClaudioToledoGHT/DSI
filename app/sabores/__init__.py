from flask import Blueprint

sabores = Blueprint("sabores", __name__, template_folder='templates')#, url_prefix="/sabores"

from . import views