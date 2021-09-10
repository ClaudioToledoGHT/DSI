from flask import flash, redirect, render_template, url_for, request, make_response
from app.models import Usuario, Endereco
from app.daos.UsuarioDAO import usuario_dao
from werkzeug.security import check_password_hash, generate_password_hash
from . import auth
from geopy.geocoders import Nominatim

def caminhoPrincipal():
    return '/produtos'

# Valida se o usuário está autenticado antes de toda requisição
@auth.before_app_request
def before_anything():
    if str(request.url_rule) != '/login' and str(request.url_rule) != '/cadastro' and str(request.url_rule) != '/' and not esta_autenticado():
        return redirect("/login")


@auth.route('/cadastro', methods=["GET", "POST"])
def cadastrar():
    print('method', request.method)
    if request.method == 'GET':
        return render_template('form_cadastro.html', usuario='novo')

    if request.method == 'POST':
        usuario = Usuario()
        usuario.nome = request.form['nome']
        usuario.email = request.form['email']
        usuario.senha = generate_password_hash(request.form['senha'])
        usuario.tipoUsuario = request.form['tipoUsuario']

        endereco = Endereco()
        endereco.logradouro = request.form['logradouro']
        endereco.cidade = request.form['cidade']
        endereco.cep = request.form['cep']
        endereco.uf = request.form['uf']
        endereco.bairro = request.form['bairro']
        endereco.numero = request.form['numero']
        endereco.complemento = request.form['complemento']
        endereco.pontoDeReferencia = request.form['pontoDeReferencia']
        geolocator = Nominatim(user_agent="DSI_GHT_2021")
        location = geolocator.geocode(endereco.logradouro + ", " + endereco.numero + ", " + endereco.cidade + " - " + endereco.bairro)

        print('locatioooon')
        print(location)
        latitude = 0
        longitude = 0
        if location:
            latitude = location.latitude
            longitude = location.latitude
            
        endereco.longitude = longitude
        endereco.latitude = latitude
        usuario.endereco = endereco

        usuario_dao.register(usuario)
        
        return redirect("/login")

@auth.route("/")
@auth.route('/login', methods=["GET", "POST"])
def autenticar():
        print('request.method')
        print(request.method)
        if request.method == 'GET':
            return render_template('login.html')

        if request.method == 'POST':
            email = request.form['email']
            senha = request.form['senha']

            if email == "" or senha == "":
                return render_template('login.html', erro='Informe as credenciais')

            autenticado = validar_autenticacao(email, senha)

            if not autenticado:
                return render_template('login.html', erro='Credenciais inválidas')
            else:
                print('autenticado com sucesso')
                resposta = redirect(caminhoPrincipal())
                # Armazena o login realizado com sucesso em cookies (autenticação).
                resposta.set_cookie("login", email, samesite = "Strict")
                resposta.set_cookie("senha", senha, samesite = "Strict")
                # resposta.set_cookie("tipo_usuario", autenticado.tipoUsuario, samesite = "Strict")
                return resposta

        return render_template('login.html')


@auth.route("/logout")
def logout():
    # Monta a resposta.
    resposta = make_response(render_template("login.html", mensagem = "Até breve!"))

    # Limpa os cookies com os dados de login (autenticação).
    resposta.set_cookie("login", "", samesite = "Strict")
    resposta.set_cookie("senha", "", samesite = "Strict")
    return resposta

@auth.errorhandler(404)
def not_found(e):
    print(e)
    return render_template('404.html')


@auth.errorhandler(Exception)
def general_exception(e):
    print(e)
    return render_template('error.html')

# Helpers
def esta_autenticado():
    email = request.cookies.get("login", "")
    senha = request.cookies.get("senha", "")
    return validar_autenticacao(email, senha)

def validar_autenticacao(email, senha):

    usuario = usuario_dao.get_by_email(email)

    if not usuario or not check_password_hash(usuario.senha, senha):
        return False
    return usuario