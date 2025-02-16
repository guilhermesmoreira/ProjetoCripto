# Código para testar como é a interface do Python

import tkinter as tk
from tkinter import messagebox
from monitor_cripto import obter_preco 
from alertas import monitorar_preco 
from historico_cripto import obter_historico_preco 
from plyer import notification
import time


def consultar_preco():
    cripto = cripto_entry.get().lower()
    moeda = moeda_entry.get().lower()
    preco_atual = obter_preco(cripto, moeda) #Chama função de obter preço
    preco_label.config(text=f"Preço atual: {preco_atual}")

def definir_alerta():
    cripto = cripto_entry.get().lower()
    moeda = moeda_entry.get().lower()
    try:
        preco_alvo = float(preco_alvo_entry.get())
        monitorar_preco(cripto, moeda, preco_alvo) # Chama a função de monitoramento de preco
    except ValueError:
        messagebox.showerror("Erro", "Preço alvo deve ser um número válido.")

#Criar a janela principal
root = tk.Tk()
root.title("Monitor de Preços de Criptomoedas")

#criar os widgets
cripto_label = tk.Label(root, text="Criptomoeda (Ex: Bitcoin, ethereum, dogecoin):")
cripto_label.pack()
cripto_entry = tk.Entry(root)
cripto_entry.pack()

moeda_label = tk.Label(root, text="Moeda (ex: brl, usd, eur):")
moeda_label.pack()
moeda_entry = tk.Entry(root)
moeda_entry.pack()

preco_alvo_label = tk.Label(root, text="Preço-alvo:")
preco_alvo_label.pack()
preco_alvo_entry = tk.Entry(root)
preco_alvo_entry.pack()

consultar_button = tk.Button(root, text="Consultar Preço", command=consultar_preco)
consultar_button.pack()

alerta_button = tk.Button(root, text="Definir Alerta", command=definir_alerta)
alerta_button.pack()

preco_label = tk.Label(root, text="Preço atual: Nenhum")
preco_label.pack()

# Iniciar o loop principal da interface
root.mainloop()