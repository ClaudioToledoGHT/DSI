import enum
from app import db
from flask_login import UserMixin

class TiposUsuario(enum.Enum):
    cliente = 1
    fornecedor = 2

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255))
    email = db.Column(db.String(50))
    senha = db.Column(db.String(255))
    tipoUsuario = db.Column(db.Integer)
    # uselist = false representa relação one-to-one
    endereco = db.relationship("Endereco", backref="usuario", uselist=False)

class Endereco(db.Model):
    __tablename__ = "enderecos"
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    logradouro = db.Column(db.String(120))
    bairro = db.Column(db.String(80))
    numero = db.Column(db.String(10))
    complemento = db.Column(db.String(20))
    pontoDeReferencia = db.Column(db.String(40))
    longitude = db.Column(db.Float())
    latitude = db.Column(db.Float())

class Produto():
    __tablename__ = "produtos"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(30), nullable=False)
    descricao = db.Column(db.String(50), nullable=False)
    peso = db.Column(db.BigInteger)
    valor = db.Column(db.BigInteger)
    valor = db.Column(db.BigInteger)