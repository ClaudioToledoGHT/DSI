from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = 'secret'
    app.config["SQLALCHEMY_DATABASE_URI"] = "jdbc:sqlserver://dsi-si-impacta.database.windows.net;databaseName=master;user=GHTadm;password=GHT@SI2021;TRUSTED_CONNECTION=no"
    # app.config["SQLALCHEMY_DATABASE_URI"] = "DRIVER={ODBC Driver 11 for SQL Server};SERVER=//dsi-si-impacta.database.windows.net;DATABASE=DSI;TRUSTED_CONNECTION=yes"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["DEBUG"] = True

    SECRET_KEY = 'dev'
#   SQLALCHEMY_DATABASE_URI = 'DRIVER={ODBC Driver 11 for SQL Server};SERVER=myServer;DATABASE=myDB;TRUSTED_CONNECTION=yes'

    db.init_app(app)
    # db.create_all()

    # engine = db.create_engine("sqlite:///app.db", {})
    # connection = engine.connect()
    # connection.execute("""CREATE TABLE IF NOT EXISTS USUARIOS (
    #                     ID INTEGER PRIMARY KEY AUTOINCREMENT,
    #                     NOME VARCHAR(255) NOT NULL,
    #                     EMAIL VARCHAR(50) NOT NULL,
    #                     SENHA VARCHAR(255) NOT NULL,
    #                     TIPOUSUARIO INT NOT NULL)
    #                 """)
    # connection.execute("""CREATE TABLE IF NOT EXISTS ENDERECOS (
    #                     ID INTEGER PRIMARY KEY AUTOINCREMENT,
    #                     LOGRADOURO VARCHAR(120) NOT NULL,
    #                     BAIRRO VARCHAR(80) NOT NULL,
    #                     NUMERO VARCHAR(10) NOT NULL,
    #                     COMPLEMENTO VARCHAR(20) NOT NULL,
    #                     PONTODEREFERENCIA VARCHAR(40) NOT NULL,
    #                     LATITUDE FLOAT NOT NULL,
    #                     LONGITUDE FLOAT NOT NULL,
    #                     USUARIO_ID INTEGER NOT NULL,
    #                     FOREIGN KEY (USUARIO_ID) REFERENCES USUARIOS(ID))
    #                 """)
    # # connection.execute("""ALTER TABLE ENDERECO ADD CONSTRAINT FK_Endereco_Usuario FOREIGN KEY([usuario_id]) REFERENCES [USUARIO]([ID])s""")
    # connection.close()


    from app import routes
    routes.init_app(app)

    return app