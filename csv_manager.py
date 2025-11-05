import csv, os

def salvar_csv(ofertas, filename):
    if os.path.exists(filename):
        os.remove(filename)

    with open(filename, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "Data da Consulta",
            "Companhia Aérea",
            "Ida - Partida",
            "Ida - Chegada",
            "Volta - Partida",
            "Volta - Chegada",
            "Preço (R$)"
        ], delimiter=";")
        writer.writeheader()
        writer.writerows(ofertas)
