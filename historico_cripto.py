import requests
import matplotlib.pyplot as plt 
from datetime import datetime

def obter_historico_preco(cripto="bitcoin", moeda="brl", dias=30):
    """
    Obtém o histórico de preços de uma criptomoeda em uma moeda específica.
    
    :param cripto: Nome da criptomoeda (ex: "bitcoin").
    :param moeda: Moeda para conversão (ex: "brl").
    :param dias: Número de dias para buscar o histórico (ex: últimos 30 dias).
    :return: Lista de datas e preços históricos.
    """
    url = f"https://api.coingecko.com/api/v3/coins/{cripto}/market_chart"
    params = {
        'vs_currency': moeda,
        'days': dias,
        'interval': 'daily'  # Intervalo diário
    }
    
    try:
        resposta = requests.get(url, params=params)
        dados = resposta.json()
        
        if 'prices' in dados:
            return dados['prices']  # Retorna a lista de preços (timestamp e valor)
        else:
            print("Erro ao obter dados históricos.")
            return []
    except Exception as e:
        print(f"Erro ao obter dados: {e}")
        return []

def exibir_grafico_historico(prices):
    """
    Exibe um gráfico com os preços históricos de uma criptomoeda.
    
    :param prices: Lista de preços (timestamp e valor).
    """
    # Extrair datas e preços
    datas = [datetime.fromtimestamp(item[0] / 1000) for item in prices]  # Convertendo de milissegundos para datetime
    valores = [item[1] for item in prices]

    # Plotando o gráfico
    plt.figure(figsize=(10, 5))
    plt.plot(datas, valores, label='Preço', color='blue', marker='o')
    plt.title("Histórico de Preços de Criptomoeda")
    plt.xlabel("Data")
    plt.ylabel("Preço")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    # Exibe o gráfico
    plt.show()

if __name__ == "__main__":
    cripto = input("Digite a criptomoeda (ex: bitcoin, ethereum): ").lower()
    moeda = input("Digite a moeda (ex: brl, usd, eur): ").lower()
    
    # Pergunta ao usuário quantos dias de histórico ele quer
    dias = input("Quantos dias de histórico você quer visualizar? (ex: 30, 90, 180): ")
    try:
        dias = int(dias)
        prices = obter_historico_preco(cripto, moeda, dias)
        
        if prices:
            exibir_grafico_historico(prices)  # Exibe o gráfico
        else:
            print("Erro ao obter dados históricos.")
    
    except ValueError:
        print("Erro: O valor dos dias deve ser um número válido.")
