from app.models import Usuario
from app.daos.DAO import DAO

class UsuarioDAO(DAO):
    def __init__(self, model):
        self.model = model
        super().__init__()

    def get_by_email(self, email):
        with self.engine.connect() as connection:
            with self.session(bind=connection) as session:
                return session.query(self.model).filter_by(email=email).first()

    def get_clientes(self, id):
            with self.engine.connect() as connection:
                with self.session(bind=connection) as session:
                    # return session.query(self.model).filter_by(tipoUsuario=1)
                    return session.query(self.model).all()

    def get_usuario_by_id(self, id):
        with self.engine.connect() as connection:
            with self.session(bind=connection) as session:
                return session.query(self.model).filter_by(id=id).first()

    def register(self, model):
        with self.engine.connect() as connection:
            with self.session(bind=connection) as session:
                session.add(model)
                session.commit()


usuario_dao = UsuarioDAO(Usuario)
