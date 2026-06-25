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
|
 Métrica / Comportamento Observado 
|
 Cenário 1 (Rede Tradicional Reativa) 
|
 Cenário 2 (Rede Preditiva Proativa) 
|
|
:---
|
:---
|
:---
|
|
**
Carga Nominal Injetada
**
|
 Ampla Inundação TCP Concorrente 
|
 Ampla Inundação TCP Concorrente 
|
|
**
Throughput Útil Alcançado
**
|
 Saturação Crítica do Enlace 
|
 Fluxo Interrompido na Borda 
|
|
**
Volume de Datagramas Perdidos
**
|
 🔴 Alto descarte de pacotes 
|
 🟢 0 pacotes (Pós-Mitigação) 
|
|
**
Estabilidade da Rede (Jitter)
**
|
 Elevado / Instável 
|
 Residual (< 0,5 ms) 
|
|
**
Status do Streaming de Vídeo
**
|
 ❌ Congelamento / Queda de Quadros 
|
 ✅ Fluido, Estável e Contínuo 
|
|
**
Ação do Plano de Gerenciamento
**
|
 Nenhuma (Rede Inerte/Conivente) 
|
 Injeção Dinâmica de Fluxo (DROP) 
|
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

## 🛠️ Tecnologias Utilizadas

* **Mininet** — Emulação da infraestrutura de rede virtual;
* **Ryu SDN Framework** — Desenvolvimento do plano de controle programável;
* **Open vSwitch (OVS)** — Comutador virtual compatível com o protocolo OpenFlow 1.3;
* **Python 3** — Scripting, automação de comandos de infraestrutura e processamento analítico;
* **Pandas & Scikit-learn** — Manipulação de séries temporais e modelagem de Regressão Linear;
* **Iperf** — Geração controlada de tráfego UDP e de matrizes de estresse volumétrico;
* **FFmpeg** — Ferramenta de processamento e transmissão de fluxos de vídeo em tempo real.

---

## 🚀 Guia de Instalação e Execução da Infraestrutura

Para implantar este projeto do zero, siga o passo a passo detalhado abaixo para configurar o ambiente de rede (Mininet, Open vSwitch) e de desenvolvimento (Python, Ryu Controller, Machine Learning).

### 🖥️ 1. Requisitos do Sistema
* **SO Recomendado:** Ubuntu 22.04 LTS (ou 20.04 LTS) rodando em máquina nativa ou virtual (VirtualBox/VMware) com suporte a rede e recursos de virtualização habilitados.
* **Recursos Mínimos:** 2 vCPUs, 4 GB de RAM.

---

### 📦 2. Instalação dos Pacotes do Sistema (Infraestrutura)
Atualize os repositórios e instale o emulador Mininet, o switch virtual Open vSwitch, geradores de tráfego, pacotes de compilação C/Python e dependências de rede necessárias:

```bash
sudo apt-get update
sudo apt-get install -y mininet openvswitch-switch iperf ffmpeg python3-pip python3-venv python3-dev gcc libxml2-dev libxslt1-dev zlib1g-dev
```

Certifique-se de que o serviço do Open vSwitch está em execução:
```bash
sudo systemctl start openvswitch-switch
sudo systemctl enable openvswitch-switch
```

---

### 🐍 3. Configuração do Ambiente Virtual Python (`ryu_env`)
Como o Ryu Controller possui requisitos estritos de bibliotecas mais antigas (como `eventlet` e `greenlet`) que podem conflitar com dependências do sistema moderno, é altamente recomendado utilizar um ambiente virtual isolado.

1. **Crie o ambiente virtual:**
   ```bash
   python3 -m venv ryu_env
   ```

2. **Ative o ambiente virtual:**
   ```bash
   source ryu_env/bin/activate
   ```

3. **Atualize as ferramentas de empacotamento base:**
   ```bash
   pip install --upgrade pip setuptools wheel
   ```

---

### 🎮 4. Instalação do Ryu Controller e Correções de Compatibilidade
1. **Instale o Ryu Controller:**
   O Ryu possui algumas incompatibilidades com versões recentes do Python (como Python 3.10+). Instale a versão estável compatível do `eventlet` primeiro, e depois instale o Ryu:
   ```bash
   pip install eventlet==0.30.2
   pip install ryu
   ```

2. **Resolução de Problemas Comuns (Eventlet/Selector Loop):**
   Se ao iniciar o Ryu você encontrar um erro como `ValueError: Selector loop helper...` ou erros DNS, defina a seguinte variável de ambiente em seu terminal (ou adicione-a ao seu `~/.bashrc`):
   ```bash
   export EVENTLET_NO_GREENDNS=yes
   ```

---

### 📊 5. Instalação das Bibliotecas de Inteligência Artificial e Ciência de Dados
No mesmo ambiente virtual (`ryu_env` ativo), instale as bibliotecas necessárias para rodar o motor analítico e preditivo:

```bash
pip install pandas scikit-learn matplotlib numpy
```

---

### 🏃‍♂️ 6. Roteiro Passo a Passo de Execução

Para rodar a demonstração prática, você precisará de **3 terminais** abertos na máquina Linux com a pasta do projeto clonada.

#### 📁 Preparação Inicial (Clone)
```bash
git clone https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
cd NOME_DO_REPOSITORIO
```

---

#### 📌 Terminal 1: O Controlador Ryu (Plano de Controle)
Este terminal iniciará a aplicação controladora Ryu que escuta conexões do switch e realiza telemetria contínua, gravando as estatísticas no arquivo CSV.

1. **Ative o ambiente Python:**
   ```bash
   source ryu_env/bin/activate
   ```
2. **Execute o gerenciador Ryu com o coletor de dados:**
   ```bash
   ryu-manager coletor_dados.py
   ```
   *O terminal ficará ativo aguardando conexões na porta padrão 6653.*

---

#### 📌 Terminal 2: O Plano de Dados (Mininet & Clientes)
Este terminal rodará a topologia e gerará os fluxos de dados reais.

1. **Limpe conexões residuais de execuções anteriores:**
   ```bash
   sudo mn -c
   ```
2. **Inicie a topologia customizada (abre o console do Mininet):**
   ```bash
   sudo python3 topologia_smartcity.py
   ```
3. **No prompt do Mininet (`mininet>`), configure o Servidor (H3) para escutar conexões UDP e Iperf:**
   ```bash
   mininet> servidor nc -u -l -p 1234 > /dev/null &
   mininet> servidor iperf -s -u &
   ```
4. **No prompt do Mininet (`mininet>`), inicie o streaming de vídeo legítimo da Câmera (H1) para o Servidor (H3):**
   ```bash
   mininet> camera ffmpeg -re -i video_amostra.mp4 -f mpegts udp://10.0.0.3:1234 &
   ```

---

#### 📌 Terminal 3: Motor Analítico de IA (Predição e Mitigação)
Este terminal executará o script de Machine Learning que avalia o tráfego em tempo real e insere regras de firewall no switch se detectar congestionamento iminente.

1. **Ative o ambiente Python:**
   ```bash
   source ryu_env/bin/activate
   ```

---

### 🧪 7. Testando os Cenários de Validação

#### 🔴 Cenário 1: Rede Tradicional (Sem IA - Colapso por Degradação)
Neste cenário, simulamos o estouro do enlace sem nenhuma defesa preditiva.
1. No **Terminal 2 (Mininet)**, dispare uma inundação volumétrica de tráfego UDP do host `usuario` (H2) para o servidor (H3):
   ```bash
   mininet> usuario iperf -u -c 10.0.0.3 -b 1000M -t 30
   ```
2. **Resultado Observado:** O fluxo legítimo de vídeo congelará ou apresentará perda severa de quadros. No relatório do Iperf no servidor, você notará uma perda massiva de pacotes (cerca de 4.1% a mais de descarte físico e alto jitter de ~11ms).

#### 🟢 Cenário 2: Rede Preditiva (Com IA - Mitigação Proativa em Ciclo Fechado)
Neste cenário, executamos o motor de Inteligência Artificial para barrar o agressor antes do transbordo do buffer.
1. Se necessário, pare o iperf anterior e limpe a rede (`sudo mn -c`), reiniciando o Terminal 1 e o Terminal 2 nos mesmos passos.
2. Inicie novamente a inundação volumétrica de tráfego do `usuario` (H2) no **Terminal 2**:
   ```bash
   mininet> usuario iperf -u -c 10.0.0.3 -b 1000M -t 30
   ```
3. Imediatamente no **Terminal 3 (IA)**, execute o script de predição:
   ```bash
   python3 treinar_ia.py
   ```
4. **Resultado Observado:**
   * O script lerá a janela deslizante de throughput e detectará a aceleração acentuada do tráfego direcionado à porta do servidor (Porta 3).
   * O motor de IA fará a projeção para $T+5$s e acusará estouro do limiar de segurança (30% de rampa acima do último throughput).
   * Um alerta será emitido e o comando `ovs-ofctl` será invocado automaticamente pelo script Python, adicionando a regra de descarte (`DROP`) para o IP `10.0.0.2` no switch `s1`.
   * No **Terminal 2**, você verá o tráfego do usuário ser bloqueado na borda (`did not receive ack`). O streaming de vídeo da câmera permanecerá fluido, sem nenhum congelamento ou perda.
   * Um gráfico atualizado mostrando a curva de tendência e a projeção futura calculada pela IA será salvo em `grafico_ia.png`.

---

## 🔮 Próximos Passos (Trabalhos Futuros)

* **Tratamento de Platôs pós-saturação:** Evolução do algoritmo para integrar gatilhos de limites absolutos (thresholds estáticos) combinados à inclinação da reta.
* **Modelos Não-Lineares de Aprendizado:** Substituição da Regressão Linear por redes neurais recorrentes do tipo LSTM (Long Short-Term Memory) para identificação e predição de padrões sazonais e complexos de tráfego urbano de longo período.
* **Mecanismos de Mitigação Alternativos:** Substituir o bloqueio completo (`DROP`) por mecanismos de QoS dinâmico (Traffic Shaping / Rate Limiting) para tráfegos concorrentes de prioridade média ou redirecionamento de fluxos via múltiplos caminhos (Multigraph Routing).

---

## 👨‍💻 Autora

* **Maria Carlyni Pereira de Oliveira** — maria.carlyni@academico.ifpb.edu.br
* Curso Superior de Tecnologia em Redes de Computadores — Instituto Federal da Paraíba (IFPB).

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
A infraestrutura foi emulada utilizando o **Mininet** em uma topologia em estrela estruturada pelos seguintes elementos:
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
|
 Métrica / Comportamento Observado 
|
 Cenário 1 (Rede Tradicional Reativa) 
|
 Cenário 2 (Rede Preditiva Proativa) 
|
|
:---
|
:---
|
:---
|
|
**
Carga Nominal Injetada
**
|
 Ampla Inundação TCP Concorrente 
|
 Ampla Inundação TCP Concorrente 
|
|
**
Throughput Útil Alcançado
**
|
 Saturação Crítica do Enlace 
|
 Fluxo Interrompido na Borda 
|
|
**
Volume de Datagramas Perdidos
**
|
 🔴 Alto descarte de pacotes 
|
 🟢 0 pacotes (Pós-Mitigação) 
|
|
**
Estabilidade da Rede (Jitter)
**
|
 Elevado / Instável 
|
 Residual (< 0,5 ms) 
|
|
**
Status do Streaming de Vídeo
**
|
 ❌ Congelamento / Queda de Quadros 
|
 ✅ Fluido, Estável e Contínuo 
|
|
**
Ação do Plano de Gerenciamento
**
|
 Nenhuma (Rede Inerte/Conivente) 
|
 Injeção Dinâmica de Fluxo (DROP) 
|
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
