from app.models import Pagamentos
from app.daos.DAO import DAO
from sqlalchemy import extract  

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

    def get_by_month_and_year(self, month, year):
        with self.engine.connect() as connection:
            with self.session(bind=connection) as session:
                return session.query(Pagamentos).filter(extract('year', Pagamentos.paymentCreate)==year).filter(extract('month', Pagamentos.paymentCreate)==month).all()

pagamentos_dao = PagamentosDAO(Pagamentos)
