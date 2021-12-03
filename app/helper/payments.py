from app.daos.DAO import DAO
from app.models import Pagamentos
from app.daos.PagamentosDAO import pagamentos_dao
import paypalrestsdk
import os

paypalrestsdk.configure({
        "mode": "sandbox", # sandbox or live
        "client_id": os.environ['CLIENT_ID'],
        "client_secret": os.environ['CLIENT_SECRET'] })

class Paypal():

    def createPayment(self,id,nome,preco, usuarioId, vendedorId):

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"},
            "redirect_urls": {
                "return_url": "http://127.0.0.1:5000/produtos",
                "cancel_url": "http://127.0.0.1:5000/produtos"},
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": nome,
                        "sku": id,
                        "price": preco,
                        "currency": "BRL",
                        "quantity": 1}]},
                "amount": {
                    "total": preco,
                    "currency": "BRL"},
                "description": "This is the payment transaction description."}]})

        if payment.create():
            pagamento = Pagamentos()
            pagamento.paymentID = payment.id
            pagamento.paymentCreate = payment.create_time
            pagamento.paymentUpdate = payment.update_time
            pagamento.status = payment.state
            pagamento.id_usuario = usuarioId
            pagamento.id_vendedor = vendedorId
            pagamentos_dao.register(pagamento)
            print('Payment created')
        else:
            print(payment.error)

        return payment

    def executePayment(self, paymentID, payerID):
        success = False

        payment = paypalrestsdk.Payment.find(paymentID)

        if payment.execute({'payer_id' : payerID}):
            print('Execute success!')
            pagamento = pagamentos_dao.get_one(paymentID)
            payment = paypalrestsdk.Payment.find(paymentID)
            pagamento.status = payment.state
            pagamento.paymentUpdate = payment.update_time
            pagamentos_dao.alter(pagamento)
            success = True
        else:
            print(payment.error)
        
        return success

paypal = Paypal()




    



