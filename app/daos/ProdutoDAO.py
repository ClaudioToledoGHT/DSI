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

    def get_one(self,id):
        with self.engine.connect() as connection:
            with self.session(bind=connection) as session:
                return session.query(self.model).filter_by(id=id).first()
   
    def alter(self, model):
        with self.engine.connect() as connection:
            with self.session(bind=connection) as session:
                session.execute("""UPDATE PRODUTOS SET
                                 NOME = '{}', DESCRICAO = '{}',
                                 VALORINICIAL = {}, PESO = {},
                                 DESABILITADO = '{}'
                                WHERE id = {}""".format(model.nome,model.descricao,model.valorInicial,
                                model.peso,model.desabilitado, model.id))
                session.commit()

produto_dao = ProdutoDAO(Produto)
