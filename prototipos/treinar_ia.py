import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import sys
import os  # Adicionado para executar comandos do Open vSwitch

# 1. Configurações iniciais
ARQUIVO_CSV = 'dataset_smartcity.csv'
COLUNAS = ['timestamp', 'switch_id', 'porta', 'tx_bytes', 'rx_bytes', 'tx_pacotes', 'rx_pacotes']

# 2. Carregar os dados
try:
    df = pd.read_csv(ARQUIVO_CSV, names=COLUNAS, header=None, skiprows=1)
    df.columns = df.columns.str.strip()

    if df.empty:
        print("Erro: O arquivo CSV está vazio. Gere tráfego no Mininet primeiro!")
        sys.exit()

except Exception as e:
    print(f"Erro ao carregar o arquivo: {e}")
    sys.exit()

# 3. Filtrar os dados do Servidor (Porta 3)
df_servidor = df[df['porta'] == 3].copy()

if len(df_servidor) < 2:
    print("Erro: Dados insuficientes para a Porta 3. Rode o iperf no Mininet por mais tempo.")
    sys.exit()

# 4. Calcular o Throughput e Converter para Megabytes (MB)
df_servidor['throughput'] = (df_servidor['tx_bytes'].diff().fillna(0)) / (1024 * 1024)

# 5. Preparar a Inteligência Artificial (Regressão Linear)
X = np.arange(len(df_servidor)).reshape(-1, 1)
y = df_servidor['throughput'].values

# --- JANELA DESLIZANTE ---
TAMANHO_JANELA = 5
if len(X) >= TAMANHO_JANELA:
    X_treino = X[-TAMANHO_JANELA:]
    y_treino = y[-TAMANHO_JANELA:]
else:
    X_treino = X
    y_treino = y

# Criar e treinar o modelo
modelo = LinearRegression()
modelo.fit(X_treino, y_treino)

# 6. Predição para T+5 segundos
ultimo_x = X[-1][0]
ponto_futuro = np.array([[ultimo_x + 2]])
predicao = modelo.predict(ponto_futuro)

# Garantir que a predição não seja negativa
predicao_final = max(0, predicao[0])

print("-" * 45)
print(f"RELATÓRIO PREDITIVO - SMART CITY")
print(f"Última carga registrada: {y[-1]:.2f} MB")
print(f"Previsão da IA para T+5s: {predicao_final:.2f} MB")

# Lógica de Alerta e Mitigação Ativa
LIMITE_MINIMO_MB = 1.0

if predicao_final > y[-1] * 1.3 and predicao_final > LIMITE_MINIMO_MB:
    print("ALERTA: Tendência de Congestionamento Detectada! ⚠️")
    print("\n[MECANISMO DE DEFESA ATIVADO] 🛑")
    print("Bloqueando tráfego malicioso do host 'usuario' (IP: 10.0.0.2)...")
    
    # Injeta uma regra de fluxo prioritária no Open vSwitch para dropar pacotes UDP do atacante
    # Nota: Caso o nome do seu switch seja diferente de s1, altere o parâmetro abaixo.
    os.system('sudo ovs-ofctl add-flow s1 "priority=50000,udp,nw_src=10.0.0.2,actions=drop"')
    
    print("Regra de DROP aplicada com sucesso no switch de borda!")
else:
    print("STATUS: Rede Estável. ✅")
print("-" * 45)

# =========================================================================
# 7. Gerar Gráfico de Visualização FOCADO e CORRIGIDO (Sem valores negativos)
# =========================================================================
plt.figure(figsize=(10, 6))

# Plotamos os dados reais da janela recente
plt.plot(X_treino, y_treino, color='#1f77b4', marker='o', linewidth=2.5, label='Tráfego Real Recente (tx_bytes)')

# Linha de tendência calculada pela IA
X_linha_tendencia = np.array([[X_treino[0][0]], [ponto_futuro[0][0]]])
y_linha_tendencia = modelo.predict(X_linha_tendencia)
plt.plot(X_linha_tendencia, y_linha_tendencia, color='#ff7f0e', linestyle='--', linewidth=2, label='Tendência IA (Janela recente)')

# Ponto de previsão futuro (T+5s)
plt.scatter(ponto_futuro, predicao_final, color='red', s=150, edgecolors='black', label='Previsão Futura (T+5s)', zorder=5)

plt.title('Detecção Proativa de Congestionamento - SDN & IA')
plt.xlabel('Amostras de Tempo (Ciclos Recentes)')
plt.ylabel('Throughput (MB Transmitidos para o Servidor)')

# --- AJUSTES ESTÉTICOS CRÍTICOS ---
plt.ylim(bottom=0, top=max(y_treino.max(), predicao_final) + 1)
plt.xlim(X_treino[0][0] - 0.3, ponto_futuro[0][0] + 0.3)

plt.legend(loc='upper left')
plt.grid(True, alpha=0.4, linestyle='--')

# Área sombreada que destaca o avanço preditivo no tempo
plt.axvspan(ultimo_x, ponto_futuro[0][0] + 0.3, color='red', alpha=0.05, label='Zona de Risco')

plt.tight_layout()
plt.savefig('grafico_ia.png', dpi=300)
print("\n*** Sucesso: O gráfico 'grafico_ia.png' foi corrigido e salvo!")
