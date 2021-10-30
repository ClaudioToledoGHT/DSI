from flask import Blueprint

pedido = Blueprint("pedidos", __name__, template_folder='templates')

from . import views