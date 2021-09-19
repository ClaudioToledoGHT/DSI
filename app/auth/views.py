from flask import flash, redirect, session, render_template, url_for, request, make_response
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
        usuario_obj['nome'] = request.cookies.get("nome", "")
        usuario_obj['email'] = request.cookies.get("email", "")
        usuario_obj['provedor_id'] = request.cookies.get("provedor_id", "")
        usuario_obj['provedor'] = request.cookies.get("provedor", "")
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

        print('location')
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


@auth.route('/google/login', methods=["GET", "POST"])
def autenticar_google():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@auth.route("/")
@auth.route('/login', methods=["GET", "POST"])
def autenticar():
        if request.method == 'POST':
            email = request.form['email']
            senha = request.form['senha']

            if email == "" or senha == "":
                print('empty data')
                return render_template('login.html', erro='Informe as credenciais')

            autenticado = validar_autenticacao(email, senha, None)

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
    resposta.set_cookie("senha", "", samesite = "Strict")
    resposta.set_cookie("nome", "", samesite = "Strict")
    resposta.set_cookie("email", "", samesite = "Strict")
    resposta.set_cookie("provedor", "", samesite = "Strict")
    resposta.set_cookie("provedor_id", "", samesite = "Strict")
    return resposta


@auth.errorhandler(404)
def not_found(e):
    print(e)
    return render_template('404.html')


@auth.errorhandler(Exception)
def general_exception(e):
    print(e)
    return render_template('error.html')


@auth.route("/callback")
def google_auth_callback():
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

    session["google_id"] = id_info.get("sub")

    google_id = id_info.get("sub")
    email = id_info.get("email")
    nome = id_info.get("name")

    # verificando se o e-mail já está cadastrado
    usuario = validar_autenticacao(email, '', GOOGLE_PROVIDER)
    print('verify user')
    print(usuario)

    if not usuario:
        resposta = redirect('/cadastro')
        resposta.set_cookie("nome", nome, samesite = "Strict")
        resposta.set_cookie("email", email, samesite = "Strict")

    else:
        print('carregar produtos')
        resposta = redirect(caminhoPrincipal())
        resposta.set_cookie("login", email, samesite = "Strict")
        # resposta.set_cookie("senha", google_id, samesite = "Strict")
        resposta.set_cookie("nome", nome, samesite = "Strict")

    resposta.set_cookie("provedor_id", google_id, samesite = "Strict")
    resposta.set_cookie("provedor", GOOGLE_PROVIDER, samesite = "Strict")
    return resposta

# Helpers
def esta_autenticado():
    email = request.cookies.get("login", "")
    senha = request.cookies.get("senha", "")
    # if not senha:
    #     senha = request.cookies.get("provedor_id", "")
    tipo_auth = request.cookies.get("provedor", "")

    return validar_autenticacao(email, senha, tipo_auth)


def validar_autenticacao(email, senha, tipo_de_autenticacao):
    usuario = usuario_dao.get_by_email(email)
    print(usuario)
    if not usuario:
        print('not user')
        return False
    
    if tipo_de_autenticacao == GOOGLE_PROVIDER:
        print('auth google')
        # if usuario.provedor_id != senha:
        #     return False
    elif not check_password_hash(usuario.senha, senha):
        print('auth original: ' + usuario.senha)
        return False
    print('fim')
    return usuario
