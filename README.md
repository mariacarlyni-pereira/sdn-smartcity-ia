🏙️ Roteamento Preventivo em Smart Cities com SDN e Inteligência Artificial
Este projeto propõe uma arquitetura de roteamento preventivo para ambientes de Cidades Inteligentes (Smart Cities), utilizando Redes Definidas por Software (SDN) e Inteligência Artificial (Machine Learning).

O objetivo é prever tendências de congestionamento e agir proativamente para proteger tráfegos críticos (como streaming de câmeras de vigilância via UDP) contra tráfegos agressivos (como downloads massivos via TCP).

Projeto desenvolvido para a disciplina de Avaliação de Desempenho no Instituto Federal da Paraíba (IFPB).

🏗️ Arquitetura e Topologia
O ambiente foi virtualizado dividindo os planos de controle e de dados:

Plano de Controle: Controlador Ryu (gerencia o switch, coleta métricas dinâmicas e aplica regras OpenFlow).

Plano de Dados: Emulador Mininet com um Switch Open vSwitch (OVS).

Hosts da Topologia:

H1 (Câmera): Gera tráfego de vídeo crítico (UDP, limitado a 5 Mbps).

H2 (Usuário Agressor): Gera tráfego massivo e concorrente (TCP).

H3 (Servidor): Destino de todo o tráfego (Sumidouro / iperf server).

⚙️ Tecnologias Utilizadas
Python 3

Mininet (Emulação de Redes)

Ryu SDN Framework (Controlador SDN)

Scikit-Learn (Regressão Linear para predição)

Matplotlib (Geração de gráficos em tempo real)

Iperf (Geração e medição de tráfego)

🚀 Como Executar o Experimento
Para reproduzir este cenário, você precisará de 3 terminais abertos na raiz do projeto.

1. Iniciar a Coleta de Dados (Terminal 1)
Inicie o controlador Ryu com o script de monitoramento para extrair a vazão do switch a cada segundo:

Bash
./ryu_env/bin/ryu-manager coletor_dados.py
2. Subir a Topologia e Gerar Tráfego (Terminal 2)
Inicie o Mininet:

Bash
sudo python3 topologia_smartcity.py
No prompt do Mininet (mininet>), inicie os servidores e o tráfego comportado da Câmera:

Bash
# Liga o servidor TCP e UDP
servidor iperf -s &
servidor iperf -s -u &

# Liga a Câmera (5 Mbps UDP por 60s)
camera iperf -c 10.0.0.3 -u -b 5M -t 60 &
Aguarde cerca de 10 a 15 segundos para gerar uma base de dados limpa. Em seguida, dispare o ataque do usuário:

Bash
# Liga o Usuário Agressor (TCP massivo por 60s)
usuario iperf -c 10.0.0.3 -t 60 &
3. Executar a Inteligência Artificial (Terminal 3)
Cerca de 3 a 5 segundos após iniciar o tráfego do usuário agressor, execute o script preditivo da IA:

Bash
./ryu_env/bin/python treinar_ia.py
📊 Resultados e Status do Projeto
O modelo de Regressão Linear consome o dataset_smartcity.csv gerado em tempo real e calcula a tendência do tráfego. Ao detectar um crescimento abrupto (início do ataque TCP), a IA projeta a carga da rede para T + 5 segundos.

Se a projeção indicar saturação, o sistema emite um alerta de mitigação preventiva e gera um gráfico (grafico_ia.png) ilustrando o momento exato da predição.

Status atual (Entrega Parcial):

[x] Ambiente de emulação configurado.

[x] Coleta de métricas (Throughput) em tempo real.

[x] Predição de IA funcional com alertas e gráficos.

[ ] Atuação autônoma (Regra de Drop OpenFlow) - Trabalho Futuro.

[ ] Extração de Perda de Pacotes e Tempo de Resposta - Trabalho Futuro.
