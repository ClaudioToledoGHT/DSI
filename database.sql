CREATE TABLE usuarios (
ID INTEGER PRIMARY KEY IDENTITY(1,1),
NOME VARCHAR(255) NOT NULL,
EMAIL VARCHAR(50) NOT NULL,
SENHA VARCHAR(255) NOT NULL,
TIPOUSUARIO INT NOT NULL)

CREATE TABLE enderecos (
ID INTEGER PRIMARY KEY IDENTITY(1,1),
LOGRADOURO VARCHAR(120) NOT NULL,
BAIRRO VARCHAR(80) NOT NULL,
NUMERO VARCHAR(10) NOT NULL,
COMPLEMENTO VARCHAR(20) NOT NULL,
PONTODEREFERENCIA VARCHAR(40) NOT NULL,
LATITUDE FLOAT NOT NULL,
LONGITUDE FLOAT NOT NULL,
USUARIO_ID INTEGER NOT NULL,
FOREIGN KEY (USUARIO_ID) REFERENCES USUARIOS(ID))

CREATE TABLE produtos (
ID INTEGER PRIMARY KEY IDENTITY(1,1),
NOME VARCHAR(20) NOT NULL,
DESCRICAO VARCHAR(100) NOT NULL,
VALORINICIAL FLOAT NOT NULL,
PESO FLOAT NOT NULL,
USUARIO_ID INTEGER NOT NULL,
FOREIGN KEY (USUARIO_ID) REFERENCES USUARIOS(ID))