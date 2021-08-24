from app.models import Produto
from app.daos.DAO import DAO

class ProdutoDAO(DAO):
    def __init__(self, model):
        self.model = model
        super().__init__()

    def get_all(self):
        with self.engine.connect() as connection:
            with self.session(bind=connection) as session:
                return session.query(self.model).all()

    def register(self, model):
        with self.engine.connect() as connection:
            with self.session(bind=connection) as session:
                session.add(model)
                session.commit()


produto_dao = ProdutoDAO(Produto)
