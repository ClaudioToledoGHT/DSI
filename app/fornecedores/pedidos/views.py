from werkzeug.utils import redirect
from app.daos.DAO import DAO
from flask import render_template, url_for, make_response, flash
from app.models import Produto
from app.daos.PedidoDAO import pedido_dao
from app.daos.UsuarioDAO import usuario_dao
from app.daos.PagamentosDAO import pagamentos_dao
from app.helper.messageSender import notification_sender
from . import pedido
from app.auth.views import esta_autenticado
import datetime

@pedido.route('/pedidos')
def listar_pedidos():
    usuario = esta_autenticado()
    pedidos = get_pedidos(usuario.id)
    itens = pagamentos_dao.get_by_month_and_year(datetime.datetime.today().month, datetime.datetime.today().year)
    
    parametros='t:'
    for x in range(31):
      parametros += ''
      filtro = filter(lambda pagamento: pagamento.paymentCreate.strftime("%d") == str(x), itens)
      parametros += (str(len(list(filtro))) +  ',')

    return render_template('lista.html', pedidos=pedidos, tipoUsr = usuario.tipoUsuario, vendas=parametros)

@pedido.route('/entregar/pedido/<int:id>', methods=["POST"])
def iniciar_entrega(id):
    usuario = esta_autenticado()
    cliente = usuario_dao.get_usuario_by_id(id)
  
    if not cliente:
      flash('Não foi possível localizar o cliente')
    elif not cliente.telefone:
      flash("Não foi possível localizar o telefone do cliente para envio da mensagem")
    else:
      print('enviar mensagem')
      # enviando a mensagem
      response = notification_sender.send_message(cliente.telefone, usuario.nome +  ': Seu pedido chegará em minutos')
      print('response')
      print(response)
      if response:
        flash('O cliente acaba de ser avisado que em breve receberá o pedido!')
      else:
        flash('Não foi possível se conectar com o cliente')

    return redirect("/pedidos")

def get_pedidos(fornecedorId):
  usuarios = usuario_dao.get_clientes(fornecedorId)

  pedidos = []
  for usuario in usuarios:
      pedido = {}
      pedido['nome'] = usuario.nome
      pedido['cliente_id'] = usuario.id
      pedido['data'] = '01/10/2021'
      pedido['valor'] = 45.50
      pedido['produto'] = 'Sorvete de flocos'
      pedidos.append(pedido)
  
  return pedidos