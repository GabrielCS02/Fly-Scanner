# alerta_telegram.py
import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlencode

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
LIMITE_PRECO = 2100.0  # novo limite definido

def _enviar_mensagem(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensagem, "parse_mode": "Markdown", "disable_web_page_preview": True}
    try:
        resp = requests.post(url, json=payload)
        if resp.status_code == 200:
            print("✅ Mensagem enviada ao Telegram com sucesso.")
        else:
            print(f"❌ Falha ao enviar mensagem: {resp.text}")
    except Exception as ex:
        print(f"❌ Erro ao enviar alerta Telegram: {ex}")

def _gerar_url_google_flights(origem, destino, data_ida, data_volta):
    base_url = "https://www.google.com/flights?"
    params = {
        "hl": "pt-BR",
        "gl": "br",
        "flt": f"{origem}.{destino}.{data_ida}*{destino}.{origem}.{data_volta}"
    }
    return base_url + urlencode(params)

def enviar_alerta(preco, companhia, ida_partida, ida_chegada, volta_partida, volta_chegada, origem, destino, data_ida, data_volta):
    """Envia alerta quando há oferta abaixo do limite."""
    link = _gerar_url_google_flights(origem, destino, data_ida, data_volta)
    mensagem = (
        f"🔔 *Oferta encontrada abaixo de R$ {LIMITE_PRECO:.2f}!*\n\n"
        f"✈️ Companhia: {companhia}\n"
        f"💰 Preço: R$ {preco:.2f}\n\n"
        f"🛫 Ida: {ida_partida} → {ida_chegada}\n"
        f"🛬 Volta: {volta_partida} → {volta_chegada}\n\n"
        f"🌐 [Ver no Google Flights]({link})"
    )
    _enviar_mensagem(mensagem)

def enviar_alerta_sem_ofertas(menor_preco):
    """Envia alerta informando ausência de ofertas abaixo do limite."""
    if menor_preco:
        mensagem = (
            f"⚙️ Nenhuma oferta abaixo de R$ {LIMITE_PRECO:.2f} encontrada hoje.\n"
            f"Menor preço atual: *R$ {menor_preco:.2f}*."
        )
    else:
        mensagem = (
            f"⚙️ Nenhuma oferta disponível hoje para as datas consultadas.\n"
            f"Limite definido: R$ {LIMITE_PRECO:.2f}."
        )
    _enviar_mensagem(mensagem)
