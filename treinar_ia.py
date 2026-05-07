import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import os

try:
    # 1. Carregar os dados
    df = pd.read_csv('dataset_smartcity.csv', names=['Tempo', 'Bytes'])
    
    # --- BLINDAGEM CONTRA TEXTOS (Correção do erro 'tx_pacotes') ---
    df['Tempo'] = pd.to_numeric(df['Tempo'], errors='coerce')
    df['Bytes'] = pd.to_numeric(df['Bytes'], errors='coerce')
    df = df.dropna() # Remove qualquer linha que não seja número puro
    # ---------------------------------------------------------------
    
    print(f"\n*** Dataset carregado! Analisando {len(df)} linhas válidas de dados.")

    # Verifica se há dados suficientes para treinar a IA
    if len(df) < 2:
        print("⚠️ Dados insuficientes no CSV. Deixe o Ryu rodando por mais alguns segundos e tente novamente.")
        exit()

    # 2. Preparar os dados para a Regressão Linear
    X = df[['Tempo']].values
    y = df['Bytes'].values

    # 3. Treinar o modelo
    modelo = LinearRegression()
    modelo.fit(X, y)

    # 4. Fazer a Previsão (Tt + 5s)
    ultimo_tempo = df['Tempo'].max()
    ultima_carga = df['Bytes'].iloc[-1]
    tempo_futuro = [[ultimo_tempo + 5]]
    previsao = modelo.predict(tempo_futuro)[0]

    print("\n--- RELATÓRIO PREDITIVO - SMART CITY ---")
    print(f"Última carga registrada: {ultima_carga:.2f} bytes")
    print(f"Previsão da IA para T+5s: {previsao:.2f} bytes")

    # 5. Lógica de Alerta e Ação Mitigadora (A LINHA LARANJA DO DIAGRAMA)
    # Se a previsão apontar um aumento crítico (ex: 20% maior que o atual)
    if previsao > (ultima_carga * 1.20):
        print("\n⚠️ ALERTA: Tendência de Congestionamento Detectada!")
        print("🛡️  AÇÃO DA IA: Enviando regra OpenFlow para DESCARTAR tráfego do Usuário (H2)...")
        
        # Comando que bloqueia o IP do H2 (10.0.0.2) no switch S1
        comando_openflow = "sudo ovs-ofctl add-flow s1 priority=100,ip,nw_src=10.0.0.2,actions=drop"
        os.system(comando_openflow)
        print("✅ Regra aplicada no Switch S1 com sucesso!")
    else:
        print("\n✅ Tráfego estável. Nenhuma ação necessária.")

    # 6. Gerar o Gráfico
    plt.figure(figsize=(10, 5))
    plt.scatter(X, y, color='blue', label='Tráfego Real')
    plt.plot(X, modelo.predict(X), color='orange', label='Tendência (IA)')
    plt.scatter(tempo_futuro, previsao, color='red', marker='X', s=100, label='Previsão (T+5s)')
    plt.title('Monitoramento e Predição de Congestionamento')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Volume de Dados (Bytes)')
    plt.legend()
    plt.grid(True)
    plt.savefig('grafico_ia.png')
    print("\n*** Sucesso: O gráfico 'grafico_ia.png' foi gerado e salvo na pasta!")

except FileNotFoundError:
    print("❌ Erro: O arquivo 'dataset_smartcity.csv' não foi encontrado.")
except Exception as e:
    print(f"❌ Ocorreu um erro inesperado: {e}")
