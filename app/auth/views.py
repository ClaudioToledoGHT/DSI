from flask import flash, redirect, session, abort, render_template, url_for, request, make_response
from app.models import Usuario, Endereco
from app.daos.UsuarioDAO import usuario_dao
from werkzeug.security import check_password_hash, generate_password_hash
from . import auth
from geopy.geocoders import Nominatim
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
import os
import requests
import pathlib
import time

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
GOOGLE_CLIENT_ID = "933766707378-urgg0ad2k7s0e6p0s0kji327j8vae7sn.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)

GOOGLE_PROVIDER = 'GOOGLE'

def caminhoPrincipal():
    return '/produtos'

# Valida se o usuário está autenticado antes de toda requisição
@auth.before_app_request
def before_anything():
    if str(request.url_rule) != '/login' and str(request.url_rule) != '/logout' and str(request.url_rule) != '/callback' and str(request.url_rule) != '/cadastro' and str(request.url_rule) != '/google/login' and str(request.url_rule) != '/':
        if not esta_autenticado():
                return redirect("/login")

@auth.route('/cadastro', methods=["GET", "POST"])
def cadastrar():
    if request.method == 'GET':
        usuario_obj = {}
        nome = request.cookies.get("nome", "")
        email = request.cookies.get("email", "")
        provedor_id = request.cookies.get("provedor_id", "")
        provedor = request.cookies.get("provedor", "")
        
        time.sleep(5)

        if not nome and not email and session:
            if 'email' in session:
                email = session["email"]
            if 'nome' in session:
                nome = session["nome"]
            if 'provedor' in session:
                provedor = session["provedor"]
            if 'provedor_id' in session:
                provedor_id = session["provedor_id"]
            usuario_obj['senha'] = ''

        usuario_obj['email'] = email
        usuario_obj['nome'] = nome
        usuario_obj['provedor_id'] = provedor_id
        usuario_obj['provedor'] = provedor
        usuario_obj['cadastro'] = True

        return render_template('form_cadastro.html', usuario=usuario_obj)

    if request.method == 'POST':
        provedor = request.form['provedor']
        provedor_id = request.form['provedor_id']
        senha = None

        if provedor == '':
            provedor = None

        if provedor_id == '':
            provedor_id = None
        else:
            senha = generate_password_hash(request.form['senha'])

        usuario = Usuario()
        usuario.nome = request.form['nome']
        usuario.email = request.form['email']
        usuario.provedor = provedor
        usuario.provedor_id = provedor_id
        usuario.senha = senha
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
        if request.method == 'POST':
            email = request.form['email']
            senha = request.form['senha']

            if email == "" or senha == "":
                return render_template('login.html', erro='Informe as credenciais')

            autenticado = validar_autenticacao(email, senha, None)
            if not autenticado:
                return render_template('login.html', erro='Credenciais inválidas')
            else:
                resposta = redirect(caminhoPrincipal())
                # Armazena o login realizado com sucesso em cookies (autenticação).
                resposta.set_cookie("login", email, samesite = "Strict")
                resposta.set_cookie("senha", senha, samesite = "Strict")
                # resposta.set_cookie("tipo_usuario", autenticado.tipoUsuario, samesite = "Strict")
                return resposta
        else:
            if not esta_autenticado():
                return render_template('login.html')
            else:
                return redirect(caminhoPrincipal())


@auth.route("/logout")
def logout():
    # Monta a resposta.
    resposta = make_response(render_template("login.html", mensagem = "Até breve!"))

    # Limpa os cookies com os dados de login (autenticação).
    resposta.set_cookie("login", "", samesite = "Strict")
    resposta.set_cookie("state", "", samesite = "Strict")
    resposta.set_cookie("senha", "", samesite = "Strict")
    resposta.set_cookie("nome", "", samesite = "Strict")
    resposta.set_cookie("email", "", samesite = "Strict")
    resposta.set_cookie("provedor", "", samesite = "Strict")
    resposta.set_cookie("provedor_id", "", samesite = "Strict")
    session["email"] = None
    session["nome"] = None
    session["state"] = None
    session["provedor"] = None
    session["provedor_id"] = None
    return resposta


@auth.errorhandler(404)
def not_found(e):
    return render_template('404.html')


@auth.errorhandler(Exception)
def general_exception(e):
    print('500')
    print(e)
    return render_template('error.html')

@auth.route('/google/login', methods=["GET", "POST"])
def autenticar_google():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    resposta = redirect(authorization_url)
    resposta.set_cookie("state", state, samesite = "Strict")
    return resposta

@auth.route("/callback")
def google_auth_callback():
    try:
        flow.fetch_token(authorization_response=request.url)

        if not session["state"] == request.args["state"]:
            abort(500)  # State does not match!

        credentials = flow.credentials
        request_session = requests.session()
        cached_session = cachecontrol.CacheControl(request_session)
        token_request = google.auth.transport.requests.Request(session=cached_session)

        id_info = id_token.verify_oauth2_token(
            id_token=credentials._id_token,
            request=token_request,
            audience=GOOGLE_CLIENT_ID
        )

        google_id = id_info.get("sub")
        email = id_info.get("email")
        nome = id_info.get("name")

        # verificando se o e-mail já está cadastrado
        usuario = validar_autenticacao(email, '', GOOGLE_PROVIDER)

        if not usuario:
            resposta = redirect('/cadastro')
            resposta.set_cookie("nome", nome, samesite = "Strict")
            resposta.set_cookie("email", email, samesite = "Strict")

        else:
            resposta = redirect("/produtos")
            resposta.set_cookie("login", email, samesite = "Strict")
            # resposta.set_cookie("senha", google_id, samesite = "Strict")
            resposta.set_cookie("nome", nome, samesite = "Strict")
            session["email"] = email
            session["provedor_id"] = google_id
            session["provedor"] = GOOGLE_PROVIDER
            session["nome"] = nome

        resposta.set_cookie("provedor_id", google_id, samesite = "Strict")
        resposta.set_cookie("provedor", GOOGLE_PROVIDER, samesite = "Strict")
        return resposta
    except Exception as e:
        print(e)
        return redirect("/login")


# Helpers
def esta_autenticado():
    # session["email"] = "teste"
    email = request.cookies.get("login", "")
    senha = request.cookies.get("senha", "")

    tipo_auth = request.cookies.get("provedor", "")
    if not email:
        if session:
            if 'email' in session:
                email = session["email"]
            if 'provedor' in session:
                tipo_auth = session["provedor"]
        else:
            return False
    # if not senha:
    #     senha = request.cookies.get("provedor_id", "")

    return validar_autenticacao(email, senha, tipo_auth)


def validar_autenticacao(email, senha, tipo_de_autenticacao):
    usuario = usuario_dao.get_by_email(email)
    if not usuario:
        return False
    
    if tipo_de_autenticacao == GOOGLE_PROVIDER:
        print('auth google')
        # if usuario.provedor_id != senha:
        #     return False
    elif not check_password_hash(usuario.senha, senha):
        return False
    return usuario
