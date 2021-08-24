from app import db
import urllib
from sqlalchemy.orm import sessionmaker

class DAO:
    def __init__(self):
        params = urllib.parse.quote_plus("DRIVER={SQL Server Native Client 11.0};"
                                    "SERVER=dsi-si-impacta.database.windows.net;"
                                    "DATABASE=dsi;"
                                    "UID=GHTadm;"
                                    "PWD=GHT@SI2021")
        self.engine = db.create_engine("mssql+pyodbc:///?odbc_connect={}".format(params), {})
        self.session = sessionmaker(self.engine)

    def get_engine(self):
        return self.engine

    def get_session(self):
        return self.session