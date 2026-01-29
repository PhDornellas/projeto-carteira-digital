# 💰 Crypto Wallet Manager & Exchange

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-009688?style=flat-square&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat-square&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)

Backend de alta performance para gestão de criptoativos, focado em **integridade transacional** e **ingestão de dados**. O sistema consome a API da Coinbase em tempo real para realizar conversões monetárias e gerencia saldos em banco de dados relacional.

## 🚀 Funcionalidades

- **Gestão de Carteiras:** Criação de carteiras com geração de chaves (Pública/Privada).
- **Integração Externa:** Consulta de taxas de câmbio em tempo real via **Coinbase API**.
- **Câmbio (Swap):** Conversão dinâmica entre moedas (USD, BTC, ETH, SOL).
- **Ambiente Dockerizado:** Orquestração completa via Docker Compose.

## 🛠️ Tecnologias

- **Linguagem:** Python (FastAPI)
- **Banco de Dados:** PostgreSQL
- **Infraestrutura:** Docker & Docker Compose
- **Integração:** Requests (API Rest)

