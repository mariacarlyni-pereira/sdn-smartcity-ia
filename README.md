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
2. Iniciar o Controlador (Plano de Controle)
Bash
ryu-manager coletor_dados.py
3. Executar o Cérebro da IA (Análise Preditiva)
Bash
python3 treinar_ia.py
📊 Resultados
O sistema gera um gráfico chamado grafico_ia.png que demonstra a curva de tráfego real versus a linha de tendência projetada pela IA. Quando uma subida agressiva é detectada, o terminal exibe um alerta de Congestionamento Iminente.

Desenvolvido por: [Seu Nome ou Link do GitHub] 🚀


---

### Por que ficou melhor?
1.  **Badges:** Aqueles selinhos no topo (Python, Ryu, Mininet) dão um ar de projeto profissional e bem acabado.
2.  **Emojis:** Facilitam a leitura rápida e deixam o visual menos cansativo.
3.  **Estrutura em Tópicos:** Quem olha o repositório entende o que é, o que usa e como roda em menos de 10 segundos.
4.  **Blocos de Código:** Destaca os comandos, facilitando para outra pessoa (ou seu professor) testar o projeto.

**Dica extra:** Depois de colar, não esqueça de subir o seu arquivo `grafico_ia.png` para a pasta principal do GitHub também. Assim, você pode até adicionar uma linha no README como `![Gráfico do Projeto](grafico_ia.png)` para a imagem aparecer direto na página inicial!

Ficou bem mais "profissa", né? Quer que eu mude mais alguma coisa?
