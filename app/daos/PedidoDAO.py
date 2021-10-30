from app.models import Pedido
from app.daos.DAO import DAO

class PedidoDAO(DAO):
    def __init__(self, model):
        self.model = model
        super().__init__()



pedido_dao = PedidoDAO(Pedido)
