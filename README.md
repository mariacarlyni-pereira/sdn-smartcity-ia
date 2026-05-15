# Detecção Proativa de Congestionamento em Redes SDN via Inteligência Artificial para Smart Cities

> **Projeto acadêmico da disciplina de Avaliação de Desempenho**
>
> Uma abordagem preditiva utilizando Redes Definidas por Software (SDN) e Regressão Linear para proteger infraestruturas críticas contra saturação de largura de banda.

---

## 📋 Sobre o Projeto

O avanço das Cidades Inteligentes (*Smart Cities*) gera um volume massivo de dados que convergem para a mesma infraestrutura física de rede. Neste cenário, fluxos de missão crítica, como videomonitoramento de segurança, competem diretamente por recursos com o tráfego gerado por usuários comuns ou dispositivos infectados por *malware*.

Redes tradicionais operam sob um paradigma **reativo**, intervindo apenas após o transbordo das filas (*buffer overflow*) e a perda de pacotes, o que inviabiliza transmissões em tempo real.

Este projeto propõe uma arquitetura **proativa**: utilizando o controlador **Ryu (SDN)** para coleta ágil de estatísticas e um modelo de **Inteligência Artificial (Regressão Linear)** para prever a saturação do enlace com 5 segundos de antecedência, emitindo alertas antes que a degradação da Qualidade de Serviço (QoS) ocorra.

---

# 🏗️ Topologia da Rede

A infraestrutura foi emulada utilizando o **Mininet** e é composta pelos seguintes elementos:

- **H1 (Câmera - Tráfego Crítico):**  
  Gera um fluxo de vídeo simulado via protocolo UDP (5 Mbps). Exige baixa latência e não tolera atrasos.

- **H2 (Origem de Sobrecarga):**  
  Representa a saturação da largura de banda por tráfego TCP massivo. Simula desde atividades legítimas de alta demanda até ações de usuários mal-intencionados ou dispositivos infectados por *malware* que sobrecarregam a infraestrutura e sufocam os serviços críticos.

- **H3 (Servidor):**  
  Destino central que recebe o tráfego de H1 e H2, funcionando como o ponto de medição de desempenho.

- **S1 (Switch OpenFlow):**  
  Elemento de encaminhamento (*Open vSwitch*) controlado pelo SDN.

- **Ryu Controller:**  
  O “cérebro” da rede, responsável por monitorar o tráfego a cada segundo e exportar os dados para o modelo preditivo.

---

# ⚙️ Detalhamento Técnico: Fluxo do Projeto

O funcionamento da solução pode ser compreendido em 6 etapas fundamentais:

---

## Passo 1: O Estado Normal (A Paz na Smart City)

Quando a topologia é iniciada no Mininet, a infraestrutura física virtual é criada.

### O que acontece:
A câmera (**H1**) começa a transmitir seu vídeo de segurança para o servidor (**H3**) usando o protocolo UDP a 5 Mbps.

### O papel do Switch:
O Switch OpenFlow (**S1**) é como um guarda de trânsito “cego”. Ele não pensa, apenas encaminha os pacotes da câmera para o servidor.

### O papel do Controlador:
O **Ryu** (*Plano de Controle*) fica monitorando a rede. A cada 1 segundo, ele envia uma mensagem para o Switch perguntando:

> “Quantos bytes passaram por você agora?”

O Switch responde e o Ryu registra essas informações em um arquivo CSV que servirá como base para o modelo de IA.

---

## Passo 2: A Perturbação (O Início do Problema)

De repente, o Host 2 (**H2**) entra em ação.

### O que acontece:
O H2 utiliza o protocolo TCP, que tenta ocupar toda a banda disponível da rede.

### O Gargalo:
Os fluxos de H1 (câmera) e H2 (tráfego massivo) convergem para o mesmo enlace em direção ao servidor (**H3**), criando um ponto de congestionamento físico.

---

## Passo 3: A Coleta Ágil (A Mágica do SDN)

Redes tradicionais só perceberiam o problema após perda de pacotes.

### O que acontece:
Como o controlador SDN monitora continuamente os fluxos, ele detecta rapidamente o aumento abrupto no volume de tráfego.

O dataset CSV começa então a registrar uma subida acentuada no consumo de banda.

---

## Passo 4: O Cérebro Entra em Ação (A Matemática)

Aqui entra o modelo de Inteligência Artificial.

### O que acontece:
O script Python lê continuamente o CSV gerado pelo Ryu.

A IA utiliza os últimos valores coletados para ajustar uma reta utilizando **Regressão Linear**.

### A Sacada:
O sistema não observa apenas o estado atual da rede, mas principalmente a **inclinação da reta**, permitindo prever o comportamento futuro do tráfego.

Se a taxa de crescimento continuar elevada, a IA projeta matematicamente onde o tráfego estará nos próximos 5 segundos.

---

## Passo 5: A Predição e o Alerta (A Proatividade)

### O que acontece:
A IA identifica que o enlace atingirá 100% da capacidade em aproximadamente 5 segundos.

### A Ação:
Antes que ocorram perdas de pacotes ou degradação do vídeo, o sistema emite:

- Um alerta de congestionamento iminente no terminal;
- Um gráfico de projeção de saturação;
- Um aviso preventivo para o administrador da rede.

---

## Passo 6: O Trabalho Futuro (O Fechamento do Ciclo)

Esta etapa representa a evolução futura do projeto.

### O que vai acontecer:
Após detectar o congestionamento, o sistema enviará automaticamente instruções para o controlador Ryu.

O controlador aplicará novas regras OpenFlow diretamente no Switch.

### O Resultado:
O sistema poderá:

- Aplicar *Traffic Shaping*;
- Limitar dinamicamente a banda de H2;
- Bloquear fluxos maliciosos;
- Priorizar o tráfego crítico da câmera.

Assim, o vídeo de monitoramento continuará funcionando sem interrupções, mesmo sob condições extremas de tráfego.

---

# 🛠️ Tecnologias Utilizadas

- **Mininet** — Emulação da infraestrutura de rede;
- **Ryu SDN Framework** — Controlador SDN;
- **Open vSwitch (OVS)** — Switch virtual compatível com OpenFlow;
- **Python 3** — Scripts de automação e IA;
- **Pandas / Scikit-learn** — Manipulação de dados e Regressão Linear;
- **Iperf** — Geração de tráfego TCP/UDP.

---

# 🚀 Como Executar

## Pré-requisitos

Certifique-se de possuir os seguintes componentes instalados em um ambiente Linux (preferencialmente Ubuntu):

- Python 3
- Mininet
- Ryu Controller
- Open vSwitch
- Iperf

---

## Passos para Execução

### 1. Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
cd NOME_DO_REPOSITORIO
```

### 2. Inicie o controlador Ryu

```bash
ryu-manager ryu_monitor.py
```

### 3. Inicie a topologia Mininet

```bash
sudo python3 topologia.py
```

### 4. Gere o tráfego nos hosts

Utilize o **Iperf** para gerar:

- Tráfego UDP no H1;
- Tráfego TCP massivo no H2.

---

### 5. Execute o motor de IA

```bash
python3 ia_predicao.py
```

---

# 📈 Próximos Passos (Trabalhos Futuros)

- [ ] Implementar regras automáticas de *Drop* para fluxos maliciosos;

---

# 👨‍💻 Autores

- Maria Carlyni Pereira de Oliviera
