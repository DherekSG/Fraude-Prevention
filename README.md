
# 💸 Sistema de Prevenção de Fraude com Ciência de Dados

Projeto colaborativo que visa criar um sistema completo de detecção de fraudes em transações financeiras, usando dados sintéticos, aprendizado de máquina e visualização interativa.

---

## 🚀 Visão Geral

Desenvolver uma solução capaz de:
- Gerar transações simuladas (reais e fraudulentas)
- Treinar um modelo de machine learning
- Classificar transações via API
- Armazenar e visualizar os resultados em tempo real

---

## 🧰 Tecnologias Utilizadas

### Linguagem:
- Python 3.10+

### Bibliotecas:
- **Pandas** – manipulação de dados
- **Scikit-learn** – classificação e treinamento
- **Faker** – simulação de dados sintéticos
- **FastAPI** – criação da API REST
- **Streamlit** ou **Dash** – dashboard de visualização
- **Joblib** – serialização do modelo
- **SQLite** (dev) / **PostgreSQL** (prod) – banco de dados

### DevOps:
- **Docker** – containerização
- **GitLab CI/CD** – integração e entrega contínua

---

## 🧱 Estrutura do Projeto

```
fraude-prevention/
├── api/                 ← API REST (FastAPI)
├── dashboard/           ← Interface gráfica (Streamlit/Dash)
├── data/                ← Dados gerados e processados
│   ├── raw/
│   └── processed/
├── model/               ← Treinamento e modelo ML
├── simulator/           ← Geração de dados sintéticos
├── docker/              ← Configurações Docker
├── tests/               ← Testes unitários
├── .gitlab-ci.yml       ← Pipeline CI/CD
├── requirements.txt     ← Dependências do projeto
├── README.md
└── .gitignore
```

---

## 🔁 Fluxo de Funcionamento

1. **Gerar dados** com o simulador (`simulator/generate.py`)
2. **Treinar modelo** com `model/train.py`
3. **Salvar modelo** como `model/model.pkl`
4. **Executar API** FastAPI para classificar transações
5. **Visualizar dados** e métricas no dashboard
6. **Banco de dados** armazena histórico e respostas

---

## ⚙️ Etapas do Projeto

| Etapa | Descrição |
|-------|-----------|
| ✅ 1 | Estruturação inicial e arquitetura |
| ✅ 2 | Simulação de dados com Faker |
| ⏳ 3 | Treinamento do modelo (Scikit-learn) |
| ⏳ 4 | Criação da API REST com FastAPI |
| ⏳ 5 | Integração com banco de dados |
| ⏳ 6 | Dashboard interativo |
| ⏳ 7 | Dockerização dos serviços |
| ⏳ 8 | CI/CD com GitLab |

---

## 🧑‍🤝‍🧑 Colaboração

Este projeto está sendo construído em equipe:

- Cada membro desenvolve em sua branch (`nome/feature`)
- Integração via Pull Requests para a branch `dev`
- Histórico de commits preservado com autores individuais

---

## 📁 Como Rodar Localmente

```bash
# Clone o repositório
git clone https://github.com/DherekSG/fraude-prevention.git
cd fraude-prevention

# Crie o ambiente virtual e instale dependências
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt

# Gerar dados simulados
python simulator/generate.py

# Iniciar dashboard interativo
streamlit run dashboard/app.py
```

Por padrão, o dashboard lê os dados do arquivo `data/raw/transacoes_sinteticas.csv`.
Para utilizar uma API ou outro banco, defina a variável `DATA_SOURCE` com a URL ou caminho desejado.

---

## 🧪 Testes

O projeto utiliza `pytest` para rodar os testes unitários e de integração.

```bash
pytest
```

---

## 📌 Status Atual

- ✅ Estrutura do projeto criada
- ✅ Simulador de dados funcionando
- ⏳ Treinamento e API em desenvolvimento

---

## 👥 Contribuidores

- [Dherek S.](https://github.com/DherekSG)
- [Juan](https://github.com/juanmh10)

---

## 📜 Licença

Projeto de aprendizado com fins educacionais. Licença livre.

---

## 📬 Contato

Para dúvidas ou contribuições, abra uma issue ou envie um pull request.
