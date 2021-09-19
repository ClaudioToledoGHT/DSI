from app import db
import urllib
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

class DAO:
    def __init__(self):

        # dbstr = (os.getenv("DRIVER")+ os.getenv("SERVER")+os.getenv("DATABASE")+
        #     os.getenv("UID")+ os.getenv("PWD"))
        
        # engine = os.getenv("CONNECT")

        # params = urllib.parse.quote_plus(dbstr) 
        # self.engine = db.create_engine("{}{}".format(engine,params), {})
        # self.session = sessionmaker(self.engine)

        params = urllib.parse.quote_plus("DRIVER={SQL Server Native Client 11.0};"
                                    "SERVER=dsi-si-impacta.database.windows.net;"
                                    "DATABASE=dsi;"
                                    "UID=GHTadm;"
                                    "PWD=DB_SI@GHT2021")
        self.engine = db.create_engine("mssql+pyodbc:///?odbc_connect={}".format(params), {})
        self.session = sessionmaker(self.engine)

    def get_engine(self):
        return self.engine

    def get_session(self):
        return self.session