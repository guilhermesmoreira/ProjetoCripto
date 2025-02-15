from pickle import GET
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from monitor_cripto import obter_preco #Importando a função já existente para obter o preço da Criptomoeda

app = Flask(__name__)
CORS(app) #Esse comando permite ao React fazer requisições.

COINGECKO_API_URL = "https://api.coingecko.com/api/v3"

#Função para buscar as 10 criptomoedas mais valiosas

def obter_top_criptos():
    url = f"{COINGECKO_API_URL}/coins/markets"
    parametros = {
        "vs_currency": "brl", #Moeda de referência (Real)
        "order": "market_cap_desc", # Ordena por valor de maior para menor seguindo o valor de mercado
        "per_page": 10, # Implementa um limite de 10 moedas
        "page": 1, # Pega somente da página inicial
        "sparkline": False # Não leva em conta os gráficos de tendência
    }

    try:
        resposta = requests.get(url, params=parametros)
        dados = resposta.json()

        # Retornar os dados com nomes e preços que é o que nos interessa
        return [{"nome": cripto["name"], "preco": cripto["current_price"]} for cripto in dados]
    except Exception as e:
        return None
    
    #Criação da rota para retornar as 10 principais criptos
@app.route('/top-criptos', methods=["GET"])
def top_criptos():
    criptos = obter_top_criptos()
    return jsonify(criptos) if criptos else jsonify({"erro": "Erro ao buscar criptos"}), 500
        
@app.route("/preco/<cripto>/<moeda>", methods=["GET"])
def preco_cripto(cripto, moeda):
    preco = obter_preco(cripto, moeda)
    return jsonify({"cripto": cripto, "moeda": moeda, "preco": preco}) if preco else jsonify({"erro": "Criptomoeda não encontrada"}), 404
    
if __name__ == "__main__":
    app.run(debug=True)