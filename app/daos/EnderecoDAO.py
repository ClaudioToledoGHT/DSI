from app.models import Endereco
from app.daos.DAO import DAO

class EnderecoDAO(DAO):
    def __init__(self, model):
        self.model = model
        super().__init__()

    def get_address_by_user_id(self, id):
        with self.engine.connect() as connection:
            with self.session(bind=connection) as session:
                return session.query(self.model).filter_by(usuario_id=id).first()

endereco_dao = EnderecoDAO(Endereco)
