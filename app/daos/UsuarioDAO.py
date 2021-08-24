from app.models import Usuario
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import db
import urllib

class UsuarioDAO:
    def __init__(self, model):
        self.model = model
    
    def connect(self):
    #     params = urllib.parse.quote_plus(
    # "DRIVER={SQL Server};SERVER=dsi-si-impacta.database.windows.net;DATABASE=dsi;UID=GHTadmin;PWD=GHT@SI2021")
        # engine = db.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params, {})
        # engine = db.create_engine('mssql+pyodbc://GHTadmin:GHT@SI2021@dsi-si-impacta.database.windows.net/dsi DRIVER={SQL Server}', {})
        params = urllib.parse.quote_plus("DRIVER={SQL Server Native Client 11.0};"
                                 "SERVER=dsi-si-impacta.database.windows.net;"
                                 "DATABASE=dsi;"
                                 "UID=GHTadm;"
                                 "PWD=GHT@SI2021")

        engine = db.create_engine("mssql+pyodbc:///?odbc_connect={}".format(params), {})

        # a sessionmaker(), also in the same scope as the engine
        Session = sessionmaker(engine)
        return Session

    def get_by_email(self, email):
        connection = self.connect()
        with connection.begin() as session:
            return session.query(self.model).filter_by(email=email).first()

    def register(self, model):
        connection = self.connect()
        with connection.begin() as session:
            session.add(model)
            session.commit()
        # db.session.add(model)
        # db.session.commit()

usuario_dao = UsuarioDAO(Usuario)
