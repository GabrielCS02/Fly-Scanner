# 🛫 Fly-Scanner  
[![Status do Workflow](https://github.com/GabrielCS02/Fly-Scanner/actions/workflows/monitor_voos.yml/badge.svg)](https://github.com/GabrielCS02/Fly-Scanner/actions/workflows/monitor_voos.yml)  
![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg?logo=python&logoColor=white)

**Fly-Scanner** é um sistema automatizado de monitoramento de passagens aéreas desenvolvido em **Python**, que consulta a **API Amadeus** e envia **alertas diários via Telegram** quando encontra ofertas abaixo de um preço limite.  

> ⚙️ O projeto roda automaticamente na nuvem, via **GitHub Actions**, sem necessidade de manter o computador ligado.

---

## 📦 Funcionalidades principais
- 🔍 Consulta automática de voos nacionais e internacionais  
- 📊 Geração do arquivo `voos.csv` com as 20 melhores ofertas diárias  
- 🔔 Notificações no **Telegram** com detalhes e link direto para o **Google Flights**  
- ☁️ Execução diária automática (GitHub Actions)  
- 🔒 Uso seguro de credenciais com **GitHub Secrets**

---

## ⚙️ Tecnologias utilizadas

| Tecnologia | Função |
|-------------|--------|
| 🐍 **Python 3.11+** | Linguagem principal |
| 🌍 **Amadeus API** | Fonte de dados de voos |
| 🤖 **Telegram Bot API** | Sistema de alertas |
| 📬 **Requests** | Comunicação com APIs |
| 🧶 **CSV Manager** | Geração e salvamento de relatórios |
| ☁️ **GitHub Actions** | Automação e agendamento diário |

---

## 🚀 Como funciona

1. O script `main.py` consulta voos de acordo com os parâmetros definidos em `config.py`.  
2. As ofertas são classificadas do **menor para o maior preço** e exportadas para `voos.csv`.  
3. Se algum valor estiver **abaixo de R$ 2 100**, é enviado um **alerta automático no Telegram**.  
4. Caso contrário, o sistema notifica o **menor preço do dia**.  
5. Todo o processo é executado automaticamente **uma vez ao dia** via **GitHub Actions**.

---

## ⚙️ Configuração local (opcional)

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/GabrielCS02/Fly-Scanner.git
   cd Fly-Scanner
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate     # Windows
   source .venv/bin/activate  # Linux / Mac
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Crie um arquivo `.env`** (não envie para o GitHub):
   ```env
   AMADEUS_CLIENT_ID=seu_id
   AMADEUS_CLIENT_SECRET=sua_chave
   TELEGRAM_BOT_TOKEN=seu_token
   TELEGRAM_CHAT_ID=seu_chat_id
   ```

5. **Execute:**
   ```bash
   python main.py
   ```

---

## ☁️ Execução automática (GitHub Actions)

O agendamento é definido em  
`.github/workflows/monitor_voos.yml`:

```yaml
schedule:
  - cron: '0 13 * * *'  # Executa todos os dias às 10h (horário de Brasília)
```

Os secrets devem ser configurados em  
**Settings → Secrets → Actions**:

- `AMADEUS_CLIENT_ID`  
- `AMADEUS_CLIENT_SECRET`  
- `TELEGRAM_BOT_TOKEN`  
- `TELEGRAM_CHAT_ID`

---

## 📊 Exemplo de notificação no Telegram

> 🔔 **Oferta encontrada abaixo de R$ 2 100,00!**  
> ✈️ Companhia: G3  
> 💰 Preço: R$ 1 978,45  
> 🛨️ Ida: 13/02/2026 07:15 → 09:35  
> 🛪️ Volta: 17/02/2026 17:45 → 20:05  
> 🌐 [Ver no Google Flights](https://www.google.com/flights)

---

## 🧐 Estrutura do projeto

```
Fly-Scanner/
│
├── main.py                 # Script principal
├── alerta_telegram.py      # Sistema de alertas e mensagens
├── amadeus_client.py       # Comunicação com a API Amadeus
├── csv_manager.py          # Geração do arquivo CSV
├── config.py               # Configurações de voo
├── requirements.txt        # Dependências do projeto
├── .github/workflows/      # Automação CI/CD
│   └── monitor_voos.yml
└── .gitignore              # Arquivos ignorados pelo Git
```

---

## 🔒 Boas práticas de segurança
- 🚫 **Nunca** suba o arquivo `.env` para o repositório.  
- 🔐 Use sempre **GitHub Secrets** para credenciais.  
- 🧹 Adicione `.venv/`, `chromedriver.exe` e `voos.csv` ao `.gitignore`.  
- 💾 O arquivo `voos.csv` é gerado automaticamente e não deve ser versionado.  

---

## 👨‍💻 Autor

**Gabriel Costa**  
Desenvolvedor Python | Automação | APIs | GitHub Actions  
📧 [linkedin.com/in/gabrielcs02](https://www.linkedin.com/in/gabrielcs02)

---

## 📜 Licença

Distribuído sob a licença **MIT**.  
Sinta-se livre para usar e aprimorar este projeto, dando os devidos créditos.  

---

## 💡 Dica extra
Adicione um **print da mensagem do Telegram** (exemplo real de alerta) logo abaixo da seção “📊 Exemplo de notificação” para deixar o README ma