import enum
from app import db
from flask_login import UserMixin

class TiposUsuario(enum.Enum):
    cliente = 1
    fornecedor = 2,
    admin = 3

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255))
    provedor_id = db.Column(db.String(255))
    provedor = db.Column(db.String(10))
    email = db.Column(db.String(50))
    senha = db.Column(db.String(255))
    telefone = db.Column(db.String(20))
    tipoUsuario = db.Column(db.Integer)
    # uselist = false representa relação one-to-one
    endereco = db.relationship("Endereco", backref="usuario", uselist=False)
    _id = db.relationship('Produto', backref='usuario', lazy=True)



class Endereco(db.Model):
    __tablename__ = "enderecos"
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cep = db.Column(db.String(20))
    uf = db.Column(db.String(2))
    cidade = db.Column(db.String(30))
    logradouro = db.Column(db.String(120))
    bairro = db.Column(db.String(80))
    numero = db.Column(db.String(10))
    complemento = db.Column(db.String(20))
    pontoDeReferencia = db.Column(db.String(40))
    longitude = db.Column(db.Float())
    latitude = db.Column(db.Float())

class Produto(db.Model):
    __tablename__ = "produtos"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(30), nullable=False)
    descricao = db.Column(db.String(50), nullable=False)
    valorInicial = db.Column(db.Integer)
    peso = db.Column(db.Integer)
    desabilitado = db.Column(db.String(1))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

class Pedido(db.Model):
    __tablename__ = "pedidos"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


class Sabores(db.Model):
    __tablename__ = "SABORES"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sabor = db.Column(db.String(40), nullable=False)
    desabilitado = db.Column(db.String(1))

    #embalagem
