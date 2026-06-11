# Detecção e Mitigação Proativa de Congestionamento em Redes SDN via Inteligência Artificial para Smart Cities

Projeto acadêmico final desenvolvido para a disciplina de **Avaliação de Desempenho** do Curso Superior de Tecnologia em Redes de Computadores no **Instituto Federal da Paraíba (IFPB)**.

Uma abordagem preditiva e de ciclo fechado utilizando Redes Definidas por Software (SDN) e Regressão Linear com Janela Deslizante para proteger infraestruturas urbanas críticas contra saturação de largura de banda e ataques volumétricos em tempo real.

---

## 📋 Sobre o Projeto

O avanço das Cidades Inteligentes (*Smart Cities*) gera um volume massivo de dados heterogêneos que convergem para a mesma infraestrutura física de rede. Neste cenário, fluxos de missão crítica, como o videomonitoramento de segurança urbana, competem diretamente por recursos com o tráfego gerado por acessos comuns ou picos provocados por nós maliciosos (ataques DDoS).

As redes tradicionais operam sob um paradigma puramente **reativo**, intervindo apenas após o transbordo das filas físicas (*buffer overflow*) e a consequente perda de dados. 

Este projeto quebra esse paradigma ao consolidar uma **arquitetura proativa de ciclo fechado**:
1. O controlador **Ryu (SDN)** realiza telemetria ágil das portas via OpenFlow.
2. Um motor de **Inteligência Artificial (Regressão Linear)** consome esses dados via janela deslizante e prevê a saturação do enlace com 5 segundos de antecedência ($T+5$).
3. Ao detectar uma rampa de aceleração que ameace a estabilidade da rede, o sistema executa uma **mitigação ativa e automatizada**, injetando regras no **Open vSwitch** para bloquear o agressor na borda antes que ocorra degradação da Qualidade de Serviço (QoS).

---

## 🏗️ Topologia da Rede

A infraestrutura foi emulada utilizando o **Mininet** em uma topologia em estrela estruturada pelos seguintes elementos:

* **Host 1 (`camera` - IP 10.0.0.1):** Nó gerador de tráfego constante e benigno. Transmite um streaming de vídeo contínuo em tempo real via protocolo UDP (usando *FFmpeg*) em direção à central operacional. Exige entrega imediata e não tolera descartes.
* **Host 2 (`usuario` - IP 10.0.0.2):** Vetor de anomalia volumétrica. Utiliza a ferramenta *Iperf* para injetar fluxos massivos de estresse (ataque de 1 Gbps), simulando a saturação repentina da infraestrutura ou uma negação de serviço.
* **Host 3 (`servidor` - IP 10.0.0.3):** O *sink* (sorvedouro) central de dados da topologia. Recebe simultaneamente o fluxo de vídeo legítimo e a carga de estresse, configurando-se como o gargalo físico e alvo de proteção do sistema.
* **Switch OpenFlow (`s1`):** Elemento central do plano de dados (*Open vSwitch*). Encaminha pacotes baseando-se estritamente na tabela de fluxos dinâmica gerenciada pelo controlador.
* **Controlador Ryu + Motor de IA:** O plano de controle inteligente. Uma aplicação Python que executa varreduras periódicas (*polling*) a cada 3 segundos para a extração de telemetria das portas e aplica o algoritmo de aprendizado de máquina supervisionado.

---

## ⚙️ Detalhamento Técnico: Fluxo de Execução do Sistema

O funcionamento completo da solução integrada é dividido em 6 etapas fundamentais:

### Passo 1: O Estado Normal (A Paz na Smart City)
Com a topologia iniciada, o host `camera` (H1) transmite seu fluxo de vídeo para o `servidor` (H3). O Switch OpenFlow (`s1`) faz o encaminhamento padronizado dos pacotes. O controlador Ryu monitora a rede enviando requisições `OFPPortStatsRequest` a cada **3 segundos** e salvando as métricas brutas (`tx_bytes` e `rx_bytes`) no arquivo `dataset_smartcity.csv`.

### Passo 2: A Perturbação (Injeção de Carga)
O host `usuario` (H2) inicia uma inundação de tráfego volumétrico UDP de 1 Gbps em direção ao servidor (H3). Ambos os fluxos competem pelo mesmo enlace físico, iniciando uma rampa ascendente abrupta de utilização de banda.

### Passo 3: Isolamento e Diferenciação Discreta
Como os contadores internos do OpenFlow são estritamente acumuladores incrementais, o script de IA lê o arquivo CSV e realiza uma diferença discreta (`.diff()`) para isolar a taxa real de transferência instantânea por ciclo, convertendo o volume bruto para Megabytes:

$$\text{Throughput (MB)} = \frac{\Delta\text{Bytes}}{1024 \times 1024}$$

### Passo 4: Predição baseada em Janela Deslizante (*Sliding Window*)
Para eliminar o viés gerado por longos períodos históricos de repouso na rede, o modelo de **Regressão Linear** é treinado utilizando uma janela dinâmica de tamanho fixo **$N = 5$** (focando apenas nas últimas 5 amostras / ~15 segundos recentes). A IA calcula a reta de tendência com base na inclinação atual da aceleração e projeta matematicamente a carga futura para o instante **$T + 5$ segundos**.

### Passo 5: A Tomada de Decisão
Se a projeção futura calculada pela IA superar um **limiar de tolerância de 30%** em relação à carga do último ciclo registrado (e apresentar valor absoluto substancial), o ecossistema entra em estado de emergência.

### Passo 6: Mitigação Ativa em Tempo Real (Fechamento do Laço)
Diferente das abordagens puramente consultivas, o script invoca comandos automáticos de sistema e interage diretamente com o switch de borda via utilitário `ovs-ofctl`. Uma regra OpenFlow prioritária de descarte é injetada dinamicamente:

```bash
sudo ovs-ofctl add-flow s1 "priority=50000,udp,nw_src=10.0.0.2,actions=drop"
```

O tráfego agressor do IP 10.0.0.2 é cortado na entrada do switch, antes de atingir ou estourar as filas físicas de buffer do servidor alvo.

---

## 📈 Resultados Experimentais e Análise Comparativa

A eficiência do ecossistema inteligente foi avaliada confrontando o comportamento da infraestrutura sob dois cenários operacionais distintos:

<table>
  <thead>
    <tr>
      <th align="left">Métrica / Comportamento Observado</th>
      <th align="left">Cenário 1 (Rede Tradicional Reativa)</th>
      <th align="left">Cenário 2 (Rede Preditiva Proativa)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Carga Nominal Injetada</b></td>
      <td>1000 Mbps (1 Gbps)</td>
      <td>1000 Mbps (1 Gbps)</td>
    </tr>
    <tr>
      <td><b>Throughput Útil Alcançado</b></td>
      <td>762 Mbps (Gargalo de Hardware)</td>
      <td>Fluxo Interrompido na Borda</td>
    </tr>
    <tr>
      <td><b>Volume de Datagramas Perdidos</b></td>
      <td>🔴 83.828 pacotes</td>
      <td>🟢 0 pacotes (Pós-Mitigação)</td>
    </tr>
    <tr>
      <td><b>Percentual de Descarte Real</b></td>
      <td>4,1%</td>
      <td>0%</td>
    </tr>
    <tr>
      <td><b>Instabilidade da Rede (Jitter)</b></td>
      <td>11,383 ms (Crítico)</td>
      <td>Residual (&lt; 0,5 ms)</td>
    </tr>
    <tr>
      <td><b>Pacotes Fora de Ordem</b></td>
      <td>3.260 datagramas</td>
      <td>0</td>
    </tr>
    <tr>
      <td><b>Status do Streaming de Vídeo</b></td>
      <td>❌ Congelamento Total</td>
      <td>✅ Fluido e Estável</td>
    </tr>
    <tr>
      <td><b>Ação do Plano de Gerenciamento</b></td>
      <td>Nenhuma (Rede Inerte/Conivente)</td>
      <td>Injeção Dinâmica de Fluxo (DROP)</td>
    </tr>
  </tbody>
</table>

**Nota de Desempenho:** No Cenário 1, a rede entrou em colapso devido à exaustão física do buffer. No Cenário 2, a IA capturou a aceleração abrupta (rampa de subida saltando para 386,22 MB), calculou uma previsão futura de 647,54 MB para $T+5$ e executou o bloqueio. O cliente agressor foi contido, emitindo o aviso de timeout no terminal (`WARNING: did not receive ack of last datagram`), mantendo o vídeo da câmera perfeitamente estável.

---

## 🛠️ Tecnologias Utilizadas

* **Mininet** — Emulação da infraestrutura de rede virtual;
* **Ryu SDN Framework** — Desenvolvimento do plano de controle programável;
* **Open vSwitch (OVS)** — Comutador virtual compatível com o protocolo OpenFlow 1.3;
* **Python 3** — Scripting, automação de comandos de infraestrutura e processamento analítico;
* **Pandas & Scikit-learn** — Manipulação de séries temporais e modelagem de Regressão Linear;
* **Iperf** — Geração controlada de tráfego UDP e de matrizes de estresse volumétrico.

---

## 🚀 Como Executar

### Pré-requisitos
Certifique-se de possuir os seguintes componentes instalados em um ambiente Linux (preferencialmente Ubuntu LTS):

```bash
sudo apt-get install mininet openvswitch-switch iperf python3-pip
pip3 install pandas scikit-learn
```

### Passos para Execução

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
   cd NOME_DO_REPOSITORIO
   ```

2. **Inicie o gerenciador e monitor do controlador Ryu:**
   ```bash
   ryu-manager ryu_monitor.py
   ```

3. **Em outro terminal, levante a topologia customizada no Mininet:**
   ```bash
   sudo python3 topologia.py
   ```

4. **Inicie as transmissões nos hosts (via CLI do Mininet ou xterm):**
   * Configurar o receptor no Servidor (H3).
   * Iniciar o streaming benigno na Câmera (H1).
   * Disparar a sobrecarga volumétrica no Usuário (H2) via `iperf -c 10.0.0.3 -u -b 1000M`.

5. **Execute o motor analítico de IA:**
   ```bash
   python3 ia_predicao.py
   ```

---

## 🔮 Próximos Passos (Trabalhos Futuros)

* **Tratamento de Platôs pós-saturação:** Evolução do algoritmo para integrar gatilhos de limites absolutos (thresholds estáticos) combinados à inclinação da reta.
* **Modelos Não-Lineares de Aprendizado:** Substituição da Regressão Linear por redes neurais recorrentes do tipo LSTM (Long Short-Term Memory) para identificação e predição de padrões sazonais e complexos de tráfego urbano de longo período.

---

## 👨‍💻 Autora

* **Maria Carlyni Pereira de Oliveira** — maria.carlyni@academico.ifpb.edu.br
* Curso Superior de Tecnologia em Redes de Computadores — Instituto Federal da Paraíba (IFPB).
