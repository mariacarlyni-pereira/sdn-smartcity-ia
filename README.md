# Detecção Proativa de Congestionamento em Redes SDN via Inteligência Artificial para Smart Cities

> **Projeto acadêmico da disciplina de Avaliação de Desempenho**
> 
> Uma abordagem preditiva utilizando Redes Definidas por Software (SDN) e Regressão Linear para proteger infraestruturas críticas contra saturação de banda.

## 📋 Sobre o Projeto

O avanço das Cidades Inteligentes (Smart Cities) gera um volume massivo de dados que convergem para a mesma infraestrutura física de rede. Neste cenário, fluxos de missão crítica, como videomonitoramento de segurança, competem diretamente por recursos com o tráfego gerado por usuários comuns ou dispositivos infectados por *malware*.

Redes tradicionais operam sob um paradigma **reativo**, intervindo apenas após o transbordo das filas (*buffer overflow*) e a perda de pacotes, o que inviabiliza transmissões em tempo real. 

Este projeto propõe uma arquitetura **proativa**: utilizando o controlador **Ryu (SDN)** para coleta ágil de estatísticas e um modelo de **Inteligência Artificial (Regressão Linear)** para prever a saturação do enlace com 5 segundos de antecedência, emitindo alertas antes que a degradação da Qualidade de Serviço (QoS) ocorra.

## 🏗️ Topologia da Rede

A infraestrutura foi emulada utilizando o **Mininet** e é composta pelos seguintes elementos:

* **H1 (Câmera - Tráfego Crítico):** Gera um fluxo de vídeo simulado via protocolo UDP (5 Mbps). Exige baixa latência e não tolera atrasos.
* **H2 (Origem de Sobrecarga):** Representa a saturação por tráfego TCP massivo. Pode simular atividades legítimas de alta demanda ou dispositivos comprometidos por *malware* (botnets).
* **H3 (Servidor):** Destino central que recebe o tráfego de H1 e H2, funcionando como o ponto de medição.
* **S1 (Switch OpenFlow):** Elemento de encaminhamento (Open vSwitch) controlado pelo SDN.
* **Ryu Controller:** O "cérebro" da rede, responsável por monitorar o tráfego a cada segundo e exportar os dados para o modelo preditivo.

## ⚙️ Como Funciona (Fluxo de Execução)

1. **Estado Normal:** A câmera (H1) transmite vídeo (UDP) para o servidor (H3) fluidamente. O Ryu monitora os *bytes* passantes no switch (S1) a cada 1 segundo e gera um *dataset* (CSV).
2. **A Perturbação:** O host agressor (H2) inicia um fluxo TCP massivo, competindo pela mesma largura de banda em direção ao servidor.
3. **Coleta Ágil:** O controlador Ryu detecta imediatamente a subida rápida no volume de tráfego.
4. **Predição Matemática:** O script de Inteligência Artificial lê o CSV em tempo real e aplica **Regressão Linear**, avaliando a inclinação da reta de crescimento.
5. **Alerta Proativo:** A IA identifica que o enlace atingirá 100% de saturação no instante *T+5s* e emite um alerta de "Congestionamento Iminente".
6. **Mitigação (Tr
