# 🏙️ Roteamento Preventivo em Smart Cities com SDN e Inteligência Artificial

Este projeto propõe uma arquitetura de roteamento preventivo para ambientes de Cidades Inteligentes (Smart Cities), utilizando **Redes Definidas por Software (SDN)** e **Inteligência Artificial (Machine Learning)**. 

O objetivo é prever tendências de congestionamento e agir proativamente para proteger tráfegos críticos (como streaming de câmeras de vigilância via UDP) contra tráfegos agressivos (como downloads massivos via TCP).

Projeto desenvolvido para a disciplina de **Avaliação de Desempenho** no Instituto Federal da Paraíba (IFPB).

---

## 🏗️ Arquitetura e Topologia

O ambiente foi virtualizado dividindo os planos de controle e de dados:
* **Plano de Controle:** Controlador **Ryu** (gerencia o switch, coleta métricas dinâmicas e aplica regras OpenFlow).
* **Plano de Dados:** Emulador **Mininet** com um Switch Open vSwitch (OVS).

**Hosts da Topologia:**
* **H1 (Câmera):** Gera tráfego de vídeo crítico (UDP, limitado a 5 Mbps).
* **H2 (Usuário Agressor):** Gera tráfego massivo e concorrente (TCP).
* **H3 (Servidor):** Destino de todo o tráfego (Sumidouro / iperf server).

---

## ⚙️ Tecnologias Utilizadas
* **Python 3**
* **Mininet** (Emulação de Redes)
* **Ryu SDN Framework** (Controlador SDN)
* **Scikit-Learn** (Regressão Linear para predição)
* **Matplotlib** (Geração de gráficos em tempo real)
* **Iperf** (Geração e medição de tráfego)

---

## 🚀 Como Executar o Experimento

Para reproduzir este cenário, você precisará de 3 terminais abertos na raiz do projeto.

### 1. Iniciar a Coleta de Dados (Terminal 1)
Inicie o controlador Ryu com o script de monitoramento para extrair a vazão do switch a cada segundo:
```bash
./ryu_env/bin/ryu-manager coletor_dados.py
