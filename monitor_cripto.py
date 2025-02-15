import requests


COINGECKO_API_URL = "https://api.coingecko.com/api/v3"
# def é a variável para criar uma função.
def obter_preco(cripto="bitcoin", moeda="brl"):
    """
    Obtém o preço atual de uma criptomoeda em uma moeda específica.
    :param cripto: Nome da criptomoeda (ex: "bitcoin", "ethereum").
    :param moeda: Moeda para conversão (ex: "brl", "usd").
    :return: Preço da criptomoeda na moeda escolhida.

    """
    url = f"{COINGECKO_API_URL}/simple/price"

    parametros = {
        "ids": cripto.lower(), # Nome da criptomoeda
        "vs_currencies": moeda.lower() # Moeda de conversão
    }
    
    try:
        #Faz uma requisição para a API da CoinGecko.
        resposta = requests.get(url, params=parametros)
        #Converte a resposta para um dicionário Python.
        dados = resposta.json()

        return dados.get(cripto.lower(), {}).get(moeda.lower(), None)
    except Exception as e:
        return None
    
#Teste da função

if __name__ == "__main__":
    cripto = input("Digite a criptomoeda (ex: Bitcoin, ethereum, dogecoin): ").lower()
    moeda = input("Digite a moeda (ex: brl, usd, eur)").lower()

    print(obter_preco(cripto, moeda))