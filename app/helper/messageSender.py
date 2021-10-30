import os
from twilio.rest import Client

class NotificationSender():
  def send_message(self, destinatario, mensagem):
    
    try:
      account_sid = os.environ['TWILIO_ACCOUNT_SID']
      auth_token = os.environ['TWILIO_AUTH_TOKEN']
      sender_number = os.environ['TWILIO_PHONE_NUMBER']

      print('endereco')
      print(account_sid)
      print(auth_token)
      print(sender_number)

      client = Client(account_sid, auth_token)
      client.messages.create(from_=sender_number, to=destinatario, body=mensagem)
      return True
    except:
      return False

notification_sender = NotificationSender()