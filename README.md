# CoralReefMonitoring

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)

## Monitoramento e Conservação de Recifes de Coral

Este projeto tem como objetivo desenvolver um webapp com Machine Learning embarcado para monitoramento e conservação de recifes de coral. A aplicação permite a visualização da saúde dos recifes, identificação de espécies ameaçadas e detecção de padrões de degradação ambiental, promovendo a sustentabilidade da Economia Azul.

## Índice

- [Descrição do Projeto](#descrição-do-projeto)
- [Motivação do Projeto](#motivação-do-projeto)
- [Objetivo](#objetivo)
- [Resultados Esperados](#resultados-esperados)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Uso](#uso)

## Descrição do Projeto

Este projeto é parte da disciplina de Front End & Mobile Development da turma 2TIAR e tem como prazo de entrega o dia 07/06/2024.

## Motivação do Projeto

Os recifes de coral são ecossistemas vitais que suportam uma vasta diversidade de vida marinha. No entanto, estão ameaçados por várias atividades humanas e mudanças climáticas. Monitorar a saúde dos recifes é crucial para implementar ações de conservação eficazes.

## Objetivo

Desenvolver uma aplicação web interativa que permita monitorar a saúde dos recifes de coral, identificar espécies ameaçadas e detectar padrões de degradação ambiental.

## Resultados Esperados

- Previsão da severidade do branqueamento dos corais.
- Probabilidades associadas às previsões.
- Visualização das variáveis mais importantes no modelo.

## Estrutura do Projeto

1. **Notebook .ipynb**
   - Carregamento e limpeza dos dados
   - Análise Exploratória dos Dados (EDA)
   - Modelagem (Machine Learning)

2. **Desenvolvimento do Webapp**
   - Utilização do framework Streamlit

## Instalação

Siga os passos abaixo para configurar o ambiente localmente:

1. Clone o repositório:
   ```sh
   git clone https://github.com/SEU_USUARIO/CoralReefMonitoring.git
   cd CoralReefMonitoring

2. Crie um ambiente virtual e ative-o:
   ```sh
   python -m venv venv
   source venv/bin/activate  # No Windows use `venv\Scripts\activate`

3. Instale as dependências:
   ```sh
   pip install -r requirements.txt`

## Uso

Siga os passos abaixo para configurar o ambiente localmente:

1. Execute a aplicação Streamlit:
   ```sh
   streamlit run app.py`

2. Acesse a aplicação em http://localhost:8501 no seu navegador.

## Funcionalidades do Webapp

- Carregar CSV: Permite carregar um arquivo CSV com dados dos recifes.
- Inserir Manualmente: Permite inserir dados manualmente para prever a severidade do branqueamento.
- Visualização de Dados: Exibe as previsões e probabilidades, além da importância das variáveis.
