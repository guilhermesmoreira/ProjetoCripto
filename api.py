from pickle import GET
from flask import Flask, jsonify, request
from flask_cors import CORS
from monitor_cripto import obter_preco #Importando a função já existente para obter o preço da Criptomoeda

app = Flask(__name__)
CORS(app) #Esse comando permite ao React fazer requisições.

@app.route('/preco', methods=[GET])
def consultar_preco():
    cripto = request.args.get('cripto', 'bitcoin')
    moeda = request.args.get('moeda', 'brl')
    preco = obter_preco(cripto, moeda)
    return jsonify({"preco": preco})

if __name__ == '__main__':
        app.run(debug=True)
