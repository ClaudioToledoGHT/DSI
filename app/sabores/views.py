from app.daos.DAO import DAO
from flask import flash, redirect, render_template, url_for, request
from app.models import Sabores
from app.daos.SaboresDAO import sabores_dao
from app.daos.UsuarioDAO import usuario_dao
from . import sabores
from app.auth.views import esta_autenticado

@sabores.route('/sabores')
def listar_sabores():
    esta_autenticado()
    sabores = sabores_dao.get_all()
    usuario = esta_autenticado()
    return render_template('listSabores.html', sabores=sabores, tipoUsr = usuario.tipoUsuario, usuario_id=usuario.id)

@sabores.route("/sabores/cadastrar", methods=["GET", "POST"])
def adicionar_sabor():
    msg = ''
    if request.method == 'POST':
        sabor = Sabores()
        sabor.sabor = request.form['sabor']
        sabor.desabilitado = 'S'


        sabores_dao.register(sabor)
        msg = 'Item cadastrado com sucesso!'

    return render_template("add_sabor.html", sabores=[], sabor='novo', mensagem=msg)

@sabores.route('/cadastro/vendedor/<int:id>', methods=["GET", "POST"])
def editar_transporte(id):
    vendedor = usuario_dao.get_by_id(id)
    vendedor.forma_entrega = request.form["transporte"]
    usuario_dao.edit_transportation(vendedor)
    return redirect(url_for("sabores.listar_sabores"))

@sabores.route("/sabores/details/<int:id>", methods=["GET", "POST"])
def detalhes_sabor(id):
    print('detalhes')

'''
@sabor.route("/sabores/editar/<int:id>", methods=["GET", "POST"])
def editar_sabor(id):
    sabor = sabor_dao.get_one(id)
    if request.method == 'POST':

        sabor.nome = request.form['nome']
        sabor.descricao = request.form['descricao']
        sabor.valorInicial = request.form['valorInicial']
        sabor.peso = request.form['peso']
        sabor.desabilitado = 'N'

        sabor_dao.alter(sabor)

        msg = 'Item alterado com sucesso!'

        return render_template('edit_sabor.html', sabores=sabor, sabor = 'velho', tipoUsr = esta_autenticado().tipoUsuario, mensagem = msg)

    return render_template('edit_sabor.html', sabores=sabor, sabor = 'velho', tipoUsr = esta_autenticado().tipoUsuario)
'''

@sabores.route("/sabores/desabilitar/<int:id>", methods=["GET", "POST"])
def desabilitar_sabor(id):
    sabor = sabores_dao.get_one(id)

    if sabor.desabilitado == 'S':

        sabor.desabilitado = 'N'

        sabores_dao.alter(sabor)

        msg = "{} Habilitado.".format(sabor.sabor)

    else:

        sabor.desabilitado = 'S'

        sabores_dao.alter(sabor)

        msg = "{} Desabilitado.".format(sabor.sabor)

    return redirect(url_for("sabores.listar_sabores"))
