# 📊 Desigualdades Raciais no Mercado de Trabalho Brasileiro (2021)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://seu-app-link.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Sobre o Projeto

Dashboard interativo que analisa as desigualdades raciais no mercado de trabalho brasileiro com base nos dados da **PNAD Contínua do IBGE (2021)**.

### Principais análises:
- Taxas de formalização, desocupação e subutilização por raça
- Impacto da escolaridade na redução das desigualdades
- Comparação direta entre população branca e negra
- Estimativa do impacto de políticas públicas na formalização

### Principais descobertas:
- Negros têm **13,6 pontos percentuais** menor taxa de formalização que brancos
- Desocupação entre negros é **44% maior** que entre brancos
- Mesmo com Ensino Superior, persiste **gap de 3,1 pontos percentuais** na formalização

## 🛠️ Tecnologias Utilizadas

- **Python 3.11** - Linguagem principal
- **Streamlit** - Framework para criação do dashboard
- **Pandas** - Manipulação e análise de dados
- **Plotly** - Visualizações interativas
- **GitHub Pages** - Hospedagem do portfólio

## 📁 Estrutura do Projeto
dashboard-desigualdades/
├── app.py # Aplicação principal Streamlit
├── requirements.txt # Dependências do projeto
├── README.md # Documentação
└── .gitignore # Arquivos ignorados


## 🚀 Como executar localmente

1. Clone o repositório:
   ```bash
   git clone https://github.com/luaramaciel/dashboard-desigualdades
   cd dashboard-desigualdades

2. Crie um ambiente virtual:
    ```bash

    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    # ou
    venv\Scripts\activate     # Windows   

3. Instale as dependências:
    pip install -r requirements.txt

4. Execute o app:
    streamlit run app.py


🌐 Acesse online

O dashboard está disponível em: https://dashboard-desigualdades.streamlit.app/
📊 Visualizações

O dashboard inclui:

    Gráficos de barras comparativos entre grupos raciais

    Gráficos de linha mostrando impacto da educação

    Métricas interativas com cálculos automáticos

    Download dos dados em CSV

🔍 Fonte dos Dados

    IBGE - PNAD Contínua 2021

    Link: Desigualdades Sociais por Cor ou Raça (https://www.google.com/url?q=https%3A%2F%2Fwww.ibge.gov.br%2Festatisticas%2Fsociais%2Fpopulacao%2F25844-desigualdades-sociais-por-cor-ou-raca.html)

👩‍💻 Autora

Luara Maciel

    GitHub: @luaramaciel

    [[LinkedIn] (https://www.linkedin.com/in/luara-maciel)]

📝 Licença

Este projeto está sob licença MIT.
