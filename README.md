# Detecção e Mitigação Proativa de Congestionamento em Redes SDN via Inteligência Artificial para Smart Cities

Projeto acadêmico final desenvolvido para a disciplina de **Avaliação de Desempenho** do Curso Superior de Tecnologia em Redes de Computadores no **Instituto Federal da Paraíba (IFPB)**.

Uma abordagem preditiva e de ciclo fechado utilizando Redes Definidas por Software (SDN) e Regressão Linear com Janela Deslizante para proteger infraestruturas urbanas críticas contra saturação de largura de banda e ataques volumétricos em tempo real.

---

## 📋 Sobre o Projeto

O avanço das Cidades Inteligentes (*Smart Cities*) gera um volume massivo de dados heterogêneos que convergem para a mesma infraestrutura física de rede. Neste cenário, fluxos de missão crítica, como o videomonitoramento de segurança urbana, competem diretamente por recursos com o tráfego gerado por acessos comuns ou picos provocados por nós maliciosos (ataques DDoS).

As redes tradicionais operam sob um paradigma puramente reativo, intervindo apenas após o transbordo das filas físicas (*buffer overflow*) e a consequente perda de dados.

Este projeto quebra esse paradigma ao consolidar uma arquitetura proativa de ciclo fechado:
1. O controlador **Ryu (SDN)** realiza telemetria ágil das portas via OpenFlow.
2. Um motor de **Inteligência Artificial (Regressão Linear)** consome esses dados via janela deslizante e prevê a saturação do enlace com antecedência de tempo estipulada ($T+5$).
3. Ao detectar uma rampa de aceleração abrupta que ameace a estabilidade da rede, o sistema executa uma mitigação ativa e automatizada, injetando regras no **Open vSwitch** para bloquear o agressor na borda antes que ocorra degradação da Qualidade de Serviço (QoS).

---

## 🏗️ Topologia da Rede

A infraestrutura foi emulada utilizando o **Mininet** em uma topologia em estrela estruturada pelos seguintes elements:

* **Host 1 (`camera` - IP 10.0.0.1):** Nó gerador de tráfego constante e benigno. Transmite um streaming de vídeo contínuo em tempo real via protocolo UDP (usando FFmpeg ou simulação Iperf UDP) em direção à central operacional. Exige entrega contínua.
* **Host 2 (`usuario` - IP 10.0.0.2):** Vetor de anomalia volumétrica. Utiliza conexões paralelas da ferramenta Iperf para injetar fluxos massivos de estresse TCP, simulando a saturação repentina da infraestrutura ou uma negação de serviço.
* **Host 3 (`servidor` - IP 10.0.0.3):** O *sink* (sorvedouro) central de dados da topologia. Recebe simultaneamente o fluxo de vídeo legítimo e a carga de estresse, configurando-se como o gargalo físico e alvo de proteção do sistema.
* **Switch OpenFlow (`s1`):** Elemento central do plano de dados (Open vSwitch). Encaminha pacotes baseando-se estritamente na tabela de fluxos dinâmica gerenciada pelo controlador.
* **Controlador Ryu + Motor de IA:** O plano de controle inteligente. Uma aplicação Python trabalhando em conjunto com um agente preditivo isolado que executa varreduras periódicas (*polling*) a cada 3 segundos para a extração de telemetria das portas e aplicação do algoritmo de aprendizado de máquina supervisionado.

---

## ⚙️ Detalhamento Técnico: Fluxo de Execução do Sistema

O funcionamento completo da solução integrada é dividido em 6 etapas fundamentais:

### Passo 1: O Estado Normal (A Paz na Smart City)
Com a topologia iniciada, o host `camera` transmite seu fluxo de vídeo para o `servidor`. O Switch OpenFlow (`s1`) faz o encaminhamento padronizado dos pacotes. O controlador Ryu monitora a rede enviando requisições a cada 3 segundos e salvando as métricas brutas no arquivo `dataset_smartcity.csv`.

### Passo 2: A Perturbação (Injeção de Carga)
O host `usuario` inicia uma inundação de tráfego volumétrico concorrente através de múltiplas sessões TCP paralelas direcionadas ao servidor. Ambos os fluxos competem pelo mesmo enlace físico na porta do servidor, iniciando uma rampa ascendente abrupta de utilização de banda.

### Passo 3: Isolamento e Diferenciação Discreta
Como os contadores internos do OpenFlow são estritamente acumuladores incrementais, o script de IA lê o arquivo CSV em tempo real e realiza uma diferença discreta (`.diff()`) para isolar a taxa real de transferência instantânea por ciclo, convertendo o volume bruto para Megabytes (MB):

$$\text{Throughput (MB)} = \frac{\Delta\text{Bytes}}{1024 \times 1024}$$

### Passo 4: Predição baseada em Janela Deslizante (Sliding Window)
Para eliminar o viés gerado por longos períodos históricos de repouso na rede, o modelo de Regressão Linear é treinado utilizando uma janela dinâmica de tamanho fixo $N=5$ (focando apenas nas últimas 5 amostras / ~15 segundos recentes). A IA calcula a reta de tendência com base na inclinação atual da aceleração e projeta matematicamente a carga futura para o instante do ponto futuro.

### Passo 5: A Tomada de Decisão
Se a seção futura calculada pela IA superar um limiar de tolerância de 30% em relação à carga do último ciclo registrado (e apresentar valor absoluto substancial acima do limite mínimo), o ecossistema entra em estado de emergência.

### Passo 6: Mitigação Ativa em Tempo Real (Fechamento do Laço)
Diferente de abordagens puramente consultivas, o script invoca comandos automáticos de sistema e interage direto com o switch de borda via utilitário `ovs-ofctl`. Uma regra OpenFlow prioritária de descarte é injetada dinamicamente:

```bash
sudo ovs-ofctl add-flow s1 "priority=50000,tcp,nw_src=10.0.0.2,actions=drop"
```

O tráfego agressor do IP 10.0.0.2 é cortado na entrada do switch, contendo a anomalia e permitindo que o tráfego estável da câmera restabeleça sua transmissão contínua sem degradação.

---

## 📈 Resultados Experimentais e Análise Comparativa

A eficiência do ecossistema inteligente foi avaliada confrontando o comportamento da infraestrutura sob dois cenários operacionais distintos:

| Métrica / Comportamento Observado | Cenário 1 (Rede Tradicional Reativa) | Cenário 2 (Rede Preditiva Proativa) |
| :--- | :--- | :--- |
| **Carga Nominal Injetada** | Ampla Inundação TCP Concorrente | Ampla Inundação TCP Concorrente |
| **Throughput Útil Alcançado** | Saturação Crítica do Enlace | Fluxo Interrompido na Borda |
| **Volume de Datagramas Perdidos** | 🔴 Alto descarte de pacotes | 🟢 0 pacotes (Pós-Mitigação) |
| **Estabilidade da Rede (Jitter)** | Elevado / Instável | Residual (< 0,5 ms) |
| **Status do Streaming de Vídeo** | ❌ Congelamento / Queda de Quadros | ✅ Fluido, Estável e Contínuo |
| **Ação do Plano de Gerenciamento** | Nenhuma (Rede Inerte/Conivente) | Injeção Dinâmica de Fluxo (DROP) |

**Nota de Desempenho:** No Cenário 1, a rede entrou em colapso devido à exaustão física. No Cenário 2, a IA capturou a aceleração abrupta na rampa de subida da janela recente (saltando instantaneamente os patamares de MB), projetou o estouro iminente e executou o bloqueio. O tráfego do agressor foi contido na borda e o streaming da câmera permaneceu fluido e ativo.

---

## 🛠️ Tecnologias Utilizadas

* **Mininet** — Emulação da infraestrutura de rede virtual;
* **Ryu SDN Framework** — Desenvolvimento do plano de controle programável;
* **Open vSwitch (OVS)** — Comutador virtual compatível com o protocolo OpenFlow 1.3;
* **Python 3** — Scripting, tratamento de sinais do sistema e processamento analítico;
* **Pandas & Scikit-learn** — Manipulação de séries temporais e modelagem de Regressão Linear;
* **Matplotlib** — Renderização gráfica dinâmica em segundo plano (Agg backend);
* **Iperf / FFmpeg** — Geração controlada de tráfego de vídeo e inundações volumétricas estruturadas.

---

## 🚀 Como Executar

### Pré-requisitos
Certifique-se de possuir os seguintes componentes instalados em seu ambiente Linux (preferencialmente Ubuntu LTS com suporte a Python 3 e ambientes virtuais):

```bash
sudo apt-get install mininet openvswitch-switch iperf ffmpeg python3-pip
```

### Passos para Execução

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
   cd NOME_DO_REPOSITORIO
   ```

2. **Inicie o coletor de dados do controlador Ryu (Terminal 1):**
   ```bash
   ryu-manager coletor_dados.py
   ```

3. **Em outro terminal, levante a topologia customizada no Mininet (Terminal 2):**
   ```bash
   sudo python3 topologia_smartcity.py
   ```

4. **Inicie o motor analítico de IA utilizando o interpretador do ambiente virtual (Terminal 3):**
   ```bash
   ./ryu_env/bin/python treinar_ia_final.py
   ```

5. **Dispare os fluxos dentro da CLI do Mininet (`mininet>` no Terminal 2):**
   * Ative a escuta do servidor:
     ```bash
     mininet> servidor iperf -s &
     ```
   * Inicie a transmissão contínua da câmera (Ex: via streaming UDP infinito ou iperf de longa duração):
     ```bash
     mininet> camera iperf -c 10.0.0.3 -u -b 5M -t 180 &
     ```
   * Dispare a inundação volumétrica do usuário malicioso:
     ```bash
     mininet> usuario iperf -c 10.0.0.3 -P 25 -t 20
     ```

### Encerramento Seguro e Relatórios
Após a IA aplicar a regra de mitigação ativa e o tráfego retornar à normalidade, vá até o Terminal 3 (IA) e pressione `Ctrl + C`.
O script capturará o sinal de interrupção com segurança e salvará de forma consolidada os seguintes arquivos na pasta do projeto:
* `relatorio_final.txt`: Relatório científico automatizado com parecer técnico acadêmico do experimento.
* `grafico_ia.png`: Gráfico dinâmico contendo as amostras da janela recente, a reta de tendência e o ponto futuro de predição.

---

## 🔮 Próximos Passos (Trabalhos Futuros)

* **Tratamento de Platôs pós-saturação:** Evolução do algoritmo para integrar gatilhos de limites absolutos (thresholds estáticos) combinados à inclinação da reta.
* **Modelos Não-Lineares de Aprendizado:** Substituição da Regressão Linear por redes neurais recorrentes do tipo LSTM (Long Short-Term Memory) para identificação e predição de padrões sazonais e complexos de tráfego urbano de longo período.

---

## 👨‍💻 Autora

* **Maria Carlyni Pereira de Oliveira** — [maria.carlyni@academico.ifpb.edu.br](mailto:maria.carlyni@academico.ifpb.edu.br)
* Curso Superior de Tecnologia em Redes de Computadores — Instituto Federal da Paraíba (IFPB).
