# 🌆 SDN Smart City: Monitoramento Preditivo com IA

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Ryu](https://img.shields.io/badge/SDN-Controller-green.svg)](https://ryu-sdn.org/)
[![Mininet](https://img.shields.io/badge/Network-Simulator-orange.svg)](http://mininet.org/)

Este projeto simula uma infraestrutura de rede para uma **Smart City** utilizando **SDN (Software Defined Networking)**. O sistema utiliza o controlador **Ryu** para coletar métricas de tráfego em tempo real e um modelo de **Machine Learning** para prever congestionamentos antes que eles ocorram.

---

## 🚀 Funcionalidades
- **Topologia Smart City:** Simulação de sensores (câmera), usuários e servidor central.
- **Coleta de Dados Automática:** Extração de estatísticas de fluxo via OpenFlow.
- **Inteligência Artificial:** Algoritmo de Regressão Linear que prevê a carga da rede com **5 segundos de antecedência**.
- **Visualização:** Geração automática de gráficos de tendência de tráfego.

## 🛠️ Tecnologias Utilizadas
* **Mininet:** Emulação de rede.
* **Ryu Controller:** Plano de controle SDN.
* **Scikit-Learn:** Inteligência Artificial (Regressão Linear).
* **Pandas & Matplotlib:** Manipulação de dados e visualização gráfica.

---

## 💻 Como Executar

Siga a ordem dos terminais abaixo dentro do ambiente virtual `ryu_env`:

### 1. Iniciar a Rede (Plano de Dados)
```bash
sudo python3 topologia_smartcity.py
