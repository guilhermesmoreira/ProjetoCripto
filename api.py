from pickle import GET
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import time
from datetime import datetime, timedelta
from monitor_cripto import obter_preco #Importando a função já existente para obter o preço da Criptomoeda

app = Flask(__name__)
CORS(app) #Esse comando permite ao React fazer requisições.

COINGECKO_API_URL = "https://api.coingecko.com/api/v3"

#Função para buscar as 10 criptomoedas mais valiosas

cache = {
    "dados": None,
    "valido_ate": None
}

def obter_top_criptos():
    global cache

    # Verifica se os dados em cache ainda são válidos
    if cache["dados"] and cache["valido_ate"] > datetime.now():
        print("Retornando dados do cache.")  # Log para depuração
        return cache["dados"]
    
    url = f"{COINGECKO_API_URL}/coins/markets"
    parametros = {
        "vs_currency": "brl",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": False
    }

    try:
        print("Fazendo requisição à API CoinGecko...")  # Log para depuração
        resposta = requests.get(url, params=parametros)
        resposta.raise_for_status()  # Lança uma exceção se a requisição falhar
        dados = resposta.json()
        print("Dados recebidos da CoinGecko:", dados)  # Log para depuração

        # Atualiza o cache
        cache["dados"] = [{"nome": cripto["name"], "preco": cripto["current_price"]} for cripto in dados]
        cache["valido_ate"] = datetime.now() + timedelta(minutes=5)  # Cache válido por 5 minutos

        return cache["dados"]
    except requests.exceptions.HTTPError as e:
        print(f"Erro HTTP ao buscar criptomoedas: {e}")  # Log para depuração
        return []
    except Exception as e:
        print(f"Erro ao buscar criptomoedas: {e}")  # Log para depuração
        return []
    
    #Criação da rota para retornar as 10 principais criptos
@app.route('/top-criptos', methods=["GET"])
def top_criptos():
    criptos = obter_top_criptos()
    if criptos:
        return jsonify(criptos)  # Retorna os dados no formato JSON
    else:
        return jsonify({"erro": "Erro ao buscar criptomoedas"}), 500
        
@app.route("/preco/<cripto>/<moeda>", methods=["GET"])
def preco_cripto(cripto, moeda):
    preco = obter_preco(cripto, moeda)
    return jsonify({"cripto": cripto, "moeda": moeda, "preco": preco}) if preco else jsonify({"erro": "Criptomoeda não encontrada"}), 404
    
if __name__ == "__main__":
    app.run(debug=True)