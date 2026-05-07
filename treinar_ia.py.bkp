import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import sys

# 1. Configurações iniciais
ARQUIVO_CSV = 'dataset_smartcity.csv'
COLUNAS = ['timestamp', 'switch_id', 'porta', 'tx_bytes', 'rx_bytes', 'tx_pacotes', 'rx_pacotes']

# 2. Carregar os dados
try:
    # Lemos o CSV forçando os nomes das colunas e tratando possíveis problemas de formatação
    df = pd.read_csv(ARQUIVO_CSV, names=COLUNAS, header=None, skiprows=1)
    
    # Limpeza de espaços nos nomes (por segurança)
    df.columns = df.columns.str.strip()
    
    if df.empty:
        print("Erro: O arquivo CSV está vazio. Gere tráfego no Mininet primeiro!")
        sys.exit()
        
    print(f"*** Dataset carregado! Analisando {len(df)} linhas de dados.")

except Exception as e:
    print(f"Erro ao carregar o arquivo: {e}")
    sys.exit()

# 3. Filtrar os dados do Servidor (Porta 3)
# No Mininet, o servidor ficou na porta 3 do switch central
df_servidor = df[df['porta'] == 3].copy()

if len(df_servidor) < 2:
    print("Erro: Dados insuficientes para a Porta 3. Rode o iperf no Mininet por mais tempo.")
    sys.exit()

# 4. Calcular o Throughput (Variação de bytes recebidos)
# Como o Ryu salva o acumulado, o diff() nos dá o tráfego real do intervalo
df_servidor['throughput'] = df_servidor['rx_bytes'].diff().fillna(0)

# 5. Preparar a Inteligência Artificial (Regressão Linear)
# X = Eixo do Tempo (0, 1, 2...)
# y = Volume de dados (Throughput)
X = np.arange(len(df_servidor)).reshape(-1, 1)
y = df_servidor['throughput'].values

# Criar e treinar o modelo com o Scikit-Learn
modelo = LinearRegression()
modelo.fit(X, y)

# 6. Predição para T+5 segundos
# O próximo ponto no tempo (amostra atual + 2 ciclos de 3s)
ponto_futuro = np.array([[len(X) + 2]])
predicao = modelo.predict(ponto_futuro)

# Garantir que a predição não seja negativa (matematicamente possível, fisicamente não)
predicao_final = max(0, predicao[0])

print("-" * 45)
print(f"RELATÓRIO PREDITIVO - SMART CITY")
print(f"Última carga registrada: {y[-1]:.2f} bytes")
print(f"Previsão da IA para T+5s: {predicao_final:.2f} bytes")

# Lógica de Alerta
if predicao_final > y[-1] * 1.3:
    print("ALERTA: Tendência de Congestionamento Detectada! ⚠️")
else:
    print("STATUS: Rede Estável. ✅")
print("-" * 45)

# 7. Gerar Gráfico de Visualização
plt.figure(figsize=(10, 6))
plt.plot(X, y, color='#1f77b4', marker='o', label='Tráfego Real (Histórico)')
plt.plot(X, modelo.predict(X), color='#ff7f0e', linestyle='--', label='Linha de Tendência IA')
plt.scatter(ponto_futuro, predicao_final, color='red', s=150, edgecolors='black', label='Previsão T+5s', zorder=5)

plt.title('Monitoramento de Rede SDN - Predição via Regressão Linear')
plt.xlabel('Amostras de Tempo (Intervalos de 3s)')
plt.ylabel('Bytes Recebidos (Throughput)')
plt.legend()
plt.grid(True, alpha=0.3)

# Salvar o gráfico
plt.savefig('grafico_ia.png')
print("\n*** Sucesso: O gráfico 'grafico_ia.png' foi gerado!")
