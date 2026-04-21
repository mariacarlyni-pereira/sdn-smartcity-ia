🌆 SDN Smart City: Monitoramento Preditivo com IA
Este projeto simula uma infraestrutura de rede para uma Smart City utilizando SDN (Software Defined Networking). O sistema utiliza o controlador Ryu para coletar métricas de tráfego em tempo real e um modelo de Machine Learning para prever congestionamentos antes que eles ocorram.

🚀 Funcionalidades
Topologia Smart City: Simulação de sensores (câmera), usuários e servidor central.

Coleta de Dados Automática: Extração de estatísticas de fluxo via OpenFlow diretamente do Switch.

Inteligência Artificial: Algoritmo de Regressão Linear que prevê a carga da rede com 5 segundos de antecedência.

Visualização: Geração automática de gráficos de tendência de tráfego (grafico_ia.png).

🛠️ Tecnologias Utilizadas
Mininet: Emulação de rede OpenFlow.

Ryu Controller: Plano de controle SDN em Python.

Scikit-Learn: Framework de Machine Learning para a Regressão Linear.

Pandas & Matplotlib: Processamento de dados e geração de gráficos.

💻 Como Executar
Siga a ordem dos terminais abaixo (certifique-se de estar com o ambiente ryu_env ativo):

1. Iniciar a Rede (Plano de Dados)
Bash
sudo python3 topologia_smartcity.py
2. Iniciar o Controlador (Plano de Controle)
Bash
ryu-manager coletor_dados.py
3. Executar o Cérebro da IA (Análise Preditiva)
Bash
python3 treinar_ia.py
📊 Resultados e Análise
O sistema analisa o histórico de bytes recebidos na porta do Servidor. Ao identificar uma tendência de alta (positiva), o modelo de IA projeta o volume de dados para o próximo intervalo. Se a predição ultrapassar o limite de segurança, o sistema emite um Alerta de Congestionamento Iminente.

Desenvolvido como projeto de Redes Definidas por Software e Inteligência Artificial.
