from flask import flash, redirect, render_template, url_for, request, make_response
from app.models import Usuario, Endereco, TiposUsuario
from app.daos.UsuarioDAO import usuario_dao
from werkzeug.security import check_password_hash, generate_password_hash

#static_folder='static', static_url_path='assets')

from . import auth

# @auth.before_app_request
# def before_anything():
#     print('beforeeeeee anything')
#     pass

@auth.route('/login', methods=["GET", "POST"])
def autenticar():
        print('request.method')
        print(request.method)
        if request.method == 'GET':
            return render_template('login.html')

        if request.method == 'POST':
            email = request.form['email']
            senha = request.form['senha']
            print('email')
            print(email)
            print('senha')
            print(senha)

            if email == "" or senha == "":
                print('erro 1')
                return render_template('login.html', erro='Credenciais inválidas')

            usuario = usuario_dao.get_by_email(email)

            if not usuario or not check_password_hash(usuario.senha, senha):
                print('erro 2')
                return render_template('login.html', erro='Credenciais inválidas')

            print('erro 3')
            resposta = make_response(redirect("/"))

            # Armazena o login realizado com sucesso em cookies (autenticação).
            resposta.set_cookie("login", email, samesite = "Strict")
            resposta.set_cookie("senha", senha, samesite = "Strict")
            return resposta

        # return render_template('login.html')


@auth.route('/cadastro', methods=["GET", "POST"])
def cadastrar():
    print('get')
    if request.method == 'GET':
        return render_template('form_cadastro.html', usuario='novo')

    if request.method == 'POST':
        print('cadastro')
        print(request.form['nome'])
        print(request.form)
        usuario = Usuario()
        usuario.nome = request.form['nome']
        usuario.email = request.form['email']
        usuario.senha = generate_password_hash(request.form['senha'])
        usuario.tipoUsuario = 1

        endereco = Endereco()
        endereco.logradouro = request.form['logradouro']
        endereco.bairro = request.form['bairro']
        endereco.numero = request.form['numero']
        endereco.complemento = request.form['complemento']
        endereco.pontoDeReferencia = request.form['pontoDeReferencia']
        endereco.longitude = request.form['longitude']
        endereco.latitude = request.form['latitude']
        usuario.endereco = endereco

        usuario_dao.register(usuario)
        return redirect("/login")
    


@auth.route("/logout")
def logout():
    # Monta a resposta.
    resposta = make_response(render_template("login.html", mensagem = "Até breve!"))

    # Limpa os cookies com os dados de login (autenticação).
    resposta.set_cookie("login", "", samesite = "Strict")
    resposta.set_cookie("senha", "", samesite = "Strict")
    return resposta