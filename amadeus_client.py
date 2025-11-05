from amadeus import Client, ResponseError
from dotenv import load_dotenv
import os

load_dotenv()

AMADEUS_CLIENT_ID = os.getenv("AMADEUS_CLIENT_ID")
AMADEUS_CLIENT_SECRET = os.getenv("AMADEUS_CLIENT_SECRET")

if not AMADEUS_CLIENT_ID or not AMADEUS_CLIENT_SECRET:
    raise ValueError("❌ Credenciais Amadeus não encontradas. Verifique o arquivo .env.")

def buscar_ofertas(origem, destino, data_ida, data_volta, adultos=1):
    amadeus = Client(client_id=AMADEUS_CLIENT_ID, client_secret=AMADEUS_CLIENT_SECRET)

    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origem,
            destinationLocationCode=destino,
            departureDate=data_ida,
            returnDate=data_volta,
            adults=adultos,
            currencyCode="BRL",
            max=40
        )
        return response.data
    except ResponseError as error:
        print("❌ Erro ao consultar API:", error)
        return []
