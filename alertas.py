import time
import requests
from plyer import notification
from monitor_cripto import obter_preco 

def monitorar_preco(cripto, moeda, preco_alvo, intervalo=60):
    """
    Monitora o preço da criptomoeda e envia um alerta quando atingir o valor desejado.
    
    :param cripto: Nome da criptomoeda (ex: "bitcoin").
    :param moeda: Moeda para conversão (ex: "brl").
    :param preco_alvo: Valor para ativar o alerta.
    :param intervalo: Tempo entre as verificações (em segundos).
    """
    print(f"Monitorando {cripto}... Alvo: {preco_alvo} {moeda.upper()}")

    while True:
        preco_atual = obter_preco(cripto, moeda)

        if preco_atual is not None:
            print(f"Preço atual do {cripto.capitalize()}: {preco_atual} {moeda.upper()}")

            if preco_atual >= preco_alvo:
                mensagem = f"O {cripto.capitalize()} atingiu {preco_atual} {moeda.upper()}!"
                print(mensagem)

                # Enviar notificação
                notification.notify(
                    title="Alerta de Preço de Criptomoeda",
                    message=mensagem,
                    timeout=10  # Tempo da notificação na tela
                )
                break  # Para o loop após o alerta
        else:
            print("Erro ao buscar o preço. Tentando novamente...")

        time.sleep(intervalo)  # Aguarda antes de verificar novamente

if __name__ == "__main__":
    cripto = input("Digite a criptomoeda (ex: bitcoin, ethereum): ").lower()
    moeda = input("Digite a moeda (ex: brl, usd, eur): ").lower()
    
    try:
        preco_alvo = float(input(f"Digite o preço-alvo em {moeda.upper()}: "))
        monitorar_preco(cripto, moeda, preco_alvo)
    except ValueError:
        print("Erro: O valor do preço-alvo deve ser um número válido.")
