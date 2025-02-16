from threading import Thread
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import time
from datetime import datetime, timedelta
from monitor_cripto import obter_preco #Importando a função já existente para obter o preço da Criptomoeda
from alertas import monitorar_preco

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

@app.route('/historico-cripto', methods=["GET"])
def historico_cripto():
    cripto_id = request.args.get("id")
    moeda = request.args.get("moeda")
    dias = request.args.get("dias", default="30")
    
    try:
       url = f"{COINGECKO_API_URL}/coins/{cripto_id}/market_chart"
       parametros = {
           "vs_currency": moeda,
           "days": dias,
           "interval": "daily"
       } 
       resposta = requests.get(url, params=parametros)
       resposta.raise_for_status()
       dados = resposta.json()
       
       #Formatar os dados para retornar apenas preços e datas
       historico = {
           "precos": dados["prices"], # Lista de [timestamp, preço]
           "dias": dias
       }
       
       return jsonify(historico)
    except Exception as e:
       print(f"Erro ao buscar histórico da criptomoeda: {e}")
       return jsonify({"erro": "Erro ao buscar histórico da criptomoeda"}), 500
   
#Função que chama o monitoramento de preço
@app.route("/monitorar-preco", methods=["POST"])
def monitorar_preco_cripto():
    data = request.get_json()

    cripto = data.get("cripto")
    moeda = data.get("moeda")
    preco_alvo = data.get("preco_alvo")

    if not cripto or not moeda or preco_alvo is None:
        return jsonify({"erro": "Parâmetros inválidos!"}), 400

    def iniciar_monitoramento():
        monitorar_preco(cripto, moeda, preco_alvo)

    # Rodar a função de monitoramento em uma thread separada para não bloquear o servidor
    thread = Thread(target=iniciar_monitoramento)
    thread.start()

    return jsonify({"message": f"Iniciando monitoramento para {cripto} em {moeda} até atingir o preço de {preco_alvo}."})
    
if __name__ == "__main__":
    app.run(debug=True)