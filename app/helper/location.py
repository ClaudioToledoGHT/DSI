import os
import json
import requests
import datetime

class Geolocation():

  def calcular_distancia(self, latitude1, longitude1, latitude2, longitude2, transporte):
    try:
      tomtomKey = os.environ['TOMTOM_KEY']
      url = "https://api.tomtom.com"
      coordenadas = f"{latitude1}%2C{longitude1}%3A{latitude2}%2C{longitude2}"
      response =requests.get(url + "/routing/1/calculateRoute/" + coordenadas + "/json?routeType=fastest&avoid=unpavedRoads&travelMode=" + transporte + "&key=" + tomtomKey)
      response_dict = json.loads(response.text)
      
      result = response_dict['routes'][0]['summary']
      minutos = result['travelTimeInSeconds'] / 60
      distancia = result['lengthInMeters']

      if distancia:
        distancia = float(distancia) /1000
      
      if minutos < 60:
        tempo = f'{round(minutos)} minutos'
      else:
        horas = minutos // 60
        minutos = minutos % 60
        horasTexto = ''
        if horas == 1:
          horasTexto += ' hora'
        else:
          horasTexto += ' horas'
        tempo = f'{round(horas)} {horasTexto} e {round(minutos)} minutos'

      return { "tempoEmMinutos": tempo, "distanciaEmKm": distancia }
    except:
      return False

geolocation = Geolocation()