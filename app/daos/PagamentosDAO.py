from app.models import Pagamentos
from app.daos.DAO import DAO

class PagamentosDAO(DAO):
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

    def get_one(self,paymentID):
        with self.engine.connect() as connection:
            with self.session(bind=connection) as session:
                return session.query(self.model).filter_by(paymentID=paymentID).first()

    def alter(self, model):
        with self.engine.connect() as connection:
            with self.session(bind=connection) as session:
                session.execute("""UPDATE pagamentos SET
                                 paymentUpdate = '{}',
                                 STATUS = '{}'
                                WHERE paymentID = '{}'""".format(model.paymentUpdate,model.status, model.paymentID))
                session.commit()

pagamentos_dao = PagamentosDAO(Pagamentos)
