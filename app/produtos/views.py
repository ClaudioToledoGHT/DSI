from app.daos.DAO import DAO
from flask import flash, redirect, render_template, url_for, request, jsonify
from app.models import Produto, Pagamentos
from app.daos.ProdutoDAO import produto_dao
from app.daos.UsuarioDAO import usuario_dao
from app.daos.EnderecoDAO import endereco_dao
from app.daos.PagamentosDAO import pagamentos_dao
from . import produto
from app.auth.views import esta_autenticado
from app.helper.location import geolocation
from app.helper.payments import paypal




@produto.route('/produtos')
def listar_produtos():
    usuario = esta_autenticado()
    produtos = produto_dao.get_all()

    lista = []
    for produto in produtos:
        produto.valorInicial = '{:.2f}'.format(produto.valorInicial)
        produto.peso = '{:.1f}'.format(produto.peso)
        lista.append(produto)

    return render_template('list.html', produtos=produtos, tipoUsr = usuario.tipoUsuario)

@produto.route("/produtos/cadastrar", methods=["GET", "POST"])
def adicionar_produto():
    msg = ''
    if request.method == 'POST':
        produto = Produto()
        produto.nome = request.form['nome']
        produto.descricao = request.form['descricao']
        produto.valorInicial = request.form['valorInicial']
        produto.peso = request.form['peso']
        produto.desabilitado = 'S'
        produto.usuario_id = 1 # ajustar

        produto_dao.register(produto)
        msg = 'Item cadastrado com sucesso!'

    return render_template("form_produto.html", sabores=[], produto='novo', mensagem=msg)

@produto.route("/produtos/detalhes/<int:id>", methods=["GET", "POST"])
def detalhes_produto(id):
    produto = produto_dao.get_one(id)
    usuario = esta_autenticado()
    endereco_usuario = endereco_dao.get_address_by_user_id(usuario.id)
    endereco_vendedor = endereco_dao.get_address_by_user_id(produto.usuario_id)
    vendedor = usuario_dao.get_by_id(produto.usuario_id)

    transporte = vendedor.forma_entrega
    if not transporte:
        transporte = 'motorcycle'

    if produto:
        produto.valorInicial = '{:.2f}'.format(produto.valorInicial)
        produto.peso = '{:.1f}'.format(produto.peso)

        distance = geolocation.calcular_distancia(endereco_usuario.latitude, endereco_usuario.longitude, endereco_vendedor.latitude, endereco_vendedor.longitude, transporte)
        
        if distance != False:
            produto.tempoEntrega = distance["tempoEmMinutos"]
            produto.distanciaEmKm = distance["distanciaEmKm"]

    return render_template('detalhe_produto.html', produto=produto, tipoUsr = usuario.tipoUsuario)


@produto.route("/produtos/editar/<int:id>", methods=["GET", "POST"])
def editar_produto(id):
    produto = produto_dao.get_one(id)
    if request.method == 'POST':

        produto.nome = request.form['nome']
        produto.descricao = request.form['descricao']
        produto.valorInicial = request.form['valorInicial']
        produto.peso = request.form['peso']
        produto.desabilitado = 'N'

        produto_dao.alter(produto)

        msg = 'Item alterado com sucesso!'

        return render_template('edit_produto.html', produtos=produto, produto = 'velho', tipoUsr = esta_autenticado().tipoUsuario, mensagem = msg)

    return render_template('edit_produto.html', produtos=produto, produto = 'velho', tipoUsr = esta_autenticado().tipoUsuario)


@produto.route("/produtos/desabilitar/<int:id>", methods=["GET", "POST"])
def desabilitar_produto(id):
    produto = produto_dao.get_one(id)

    if produto.desabilitado == 'S':

        produto.desabilitado = 'N'

        produto_dao.alter(produto)

        msg = "{} Habilitado.".format(produto.nome)

    else:

        produto.desabilitado = 'S'

        produto_dao.alter(produto)

        msg = "{} Desabilitado.".format(produto.nome)

    return redirect(url_for("produtos.listar_produtos"))

@produto.route("/paypal/payment", methods=["POST"])
def paypal_payment():

    id = request.form['produtoId']
    nome = request.form['produtoNome']
    preco = request.form['produtoPreco']

    payment = paypal.createPayment(id,nome,preco)

    return jsonify({'paymentID' : payment.id})

@produto.route("/paypal/execute", methods=["POST"])
def paypal_execute():

    paymentID = request.form['paymentID']
    payerID = request.form['payerID']

    success = paypal.executePayment(paymentID,payerID)

    return jsonify({'success' : success})