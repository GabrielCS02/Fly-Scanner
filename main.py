from datetime import datetime
from amadeus_client import buscar_ofertas
from csv_manager import salvar_csv
from alerta_telegram import enviar_alerta, enviar_alerta_sem_ofertas, LIMITE_PRECO
import config

def consultar_voos():
    print(f"\n🕐 Iniciando consulta em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}...\n")

    ofertas_raw = buscar_ofertas(config.ORIGEM, config.DESTINO, config.DATA_IDA, config.DATA_VOLTA, config.ADULTOS)
    ofertas = []

    for offer in ofertas_raw:
        companhia = offer["validatingAirlineCodes"][0]
        preco = float(offer["price"]["total"])
        data_consulta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # --- Trecho de ida ---
        ida = offer["itineraries"][0]
        ida_partida = ida["segments"][0]["departure"]["at"]
        ida_chegada = ida["segments"][-1]["arrival"]["at"]

        # --- Trecho de volta (caso exista) ---
        volta = offer["itineraries"][1] if len(offer["itineraries"]) > 1 else None
        volta_partida = volta["segments"][0]["departure"]["at"] if volta else ""
        volta_chegada = volta["segments"][-1]["arrival"]["at"] if volta else ""

        def fmt(dt):
            return datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S").strftime("%d/%m/%Y %H:%M") if dt else ""

        ofertas.append({
            "Data da Consulta": data_consulta,
            "Companhia Aérea": companhia,
            "Ida - Partida": fmt(ida_partida),
            "Ida - Chegada": fmt(ida_chegada),
            "Volta - Partida": fmt(volta_partida),
            "Volta - Chegada": fmt(volta_chegada),
            "Preço (R$)": preco
        })

    if not ofertas:
        print("⚠️ Nenhuma oferta encontrada.")
        enviar_alerta_sem_ofertas(None)
        return

    ofertas_ordenadas = sorted(ofertas, key=lambda x: x["Preço (R$)"])[:20]
    salvar_csv(ofertas_ordenadas, config.FILENAME)

    print(f"💾 Resultados atualizados e salvos em '{config.FILENAME}' com sucesso!\n")

    menor_preco = ofertas_ordenadas[0]["Preço (R$)"]

    if menor_preco < LIMITE_PRECO:
        voo = ofertas_ordenadas[0]
        enviar_alerta(
            voo["Preço (R$)"],
            voo["Companhia Aérea"],
            voo["Ida - Partida"],
            voo["Ida - Chegada"],
            voo["Volta - Partida"],
            voo["Volta - Chegada"],
            config.ORIGEM,
            config.DESTINO,
            config.DATA_IDA,
            config.DATA_VOLTA
        )
    else:
        print(f"⚙️ Nenhum alerta de preço — menor valor é R$ {menor_preco:.2f}, acima de R$ {LIMITE_PRECO:.2f}.")
        enviar_alerta_sem_ofertas(menor_preco)

    print("✅ Execução concluída.\n")

if __name__ == "__main__":
    consultar_voos()
