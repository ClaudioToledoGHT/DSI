from flask import flash, redirect, render_template, url_for, request
from app.models import Produto
from app.daos.ProdutoDAO import produto_dao
from . import produto
from app.auth.views import esta_autenticado

@produto.route('/produtos')
def listar_produtos():
    esta_autenticado()
    produtos = produto_dao.get_all()
    print('produtos')
    print(produtos)
    return render_template('list.html', produtos=produtos, tipoUsr = esta_autenticado().tipoUsuario)

@produto.route("/produtos/cadastrar", methods=["GET", "POST"])
def adicionar_produto():
    msg = ''
    if request.method == 'POST':
        produto = Produto()
        produto.nome = request.form['nome']
        produto.descricao = request.form['descricao']
        produto.valorInicial = request.form['valorInicial']
        produto.peso = request.form['peso']
        produto.usuario_id = 1 # ajustar

        produto_dao.register(produto)
        msg = 'Sorvete cadastrado com sucesso!'

    return render_template("form_produto.html", sabores=[], produto='novo', mensagem=msg)

@produto.route("/produtos/details/<int:id>", methods=["GET", "POST"])
def detalhes_produto(id):
    print('detalhes')