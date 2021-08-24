from flask import Blueprint

produto = Blueprint("produtos", __name__, template_folder='templates',url_prefix="/produtos")

from . import views