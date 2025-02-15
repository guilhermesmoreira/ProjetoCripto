import requests

# def é a variável para criar uma função.
def obter_preco(cripto="bitcoin", moeda="brl"):
    """
    Obtém o preço atual de uma criptomoeda em uma moeda específica.
    :param cripto: Nome da criptomoeda (ex: "bitcoin", "ethereum").
    :param moeda: Moeda para conversão (ex: "brl", "usd").
    :return: Preço da criptomoeda na moeda escolhida.

    """
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={cripto}&vs_currencies={moeda}"

    try:
        #Faz uma requisição para a API da CoinGecko.
        resposta = requests.get(url)
        #Converte a resposta para um dicionário Python.
        dados = resposta.json()

        if cripto in dados:
            preco = dados[cripto][moeda]
            return preco
            #f"O preço do {cripto.capitalize()} é {preco} {moeda.upper()}"
        else:
            return None
            #"Erro: Criptomoeda não encontrada."
        
    except  Exception as e:
        return None
        # f"Erro ao obter dados: {e}"
    
#Teste da função

if __name__ == "__main__":
    cripto = input("Digite a criptomoeda (ex: Bitcoin, ethereum, dogecoin): ").lower()
    moeda = input("Digite a moeda (ex: brl, usd, eur)").lower()

    print(obter_preco(cripto, moeda))