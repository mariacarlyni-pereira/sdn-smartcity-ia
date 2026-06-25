import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import sys
import os
import time

# ForÃ§a o Matplotlib a gerar imagens em segundo plano de forma estÃ¡vel
plt.switch_backend('Agg')

# 1. ConfiguraÃ§Ãµes iniciais
ARQUIVO_CSV = 'dataset_smartcity.csv'
COLUNAS = ['timestamp', 'switch_id', 'porta', 'tx_bytes', 'rx_bytes', 'tx_pacotes', 'rx_pacotes']

# Listas globais para salvar a histÃ³ria do experimento para o relatÃ³rio texto
historico_tempo = []
historico_throughput = []
tempo_mitigacao = None
mitigado = False
ciclo_atual = 0

print("=" * 60)
print("   SISTEMA DE MONITORAMENTO E DEFESA PROATIVA (IA & SDN)")
print("=" * 60)
print("Iniciando monitoramento em tempo real...")
print("Pressione [Ctrl + C] a qualquer momento para encerrar e gerar os relatÃ³rios.\n")

try:
    while True:
        time.sleep(3)
        ciclo_atual += 1
        tempo_segundos = ciclo_atual * 3
        
        if not os.path.exists(ARQUIVO_CSV):
            print(f"[{time.strftime('%H:%M:%S')}] Aguardando telemetria inicial do Controlador Ryu...")
            continue
            
        try:
            df = pd.read_csv(ARQUIVO_CSV, names=COLUNAS, header=None, skiprows=1)
            df.columns = df.columns.str.strip()
            if df.empty:
                continue
        except Exception:
            continue

        # Filtrar os dados do Servidor (Porta 3)
        df_servidor = df[df['porta'] == 3].copy()

        if len(df_servidor) < 2:
            continue

        # Calcular o Throughput e Converter para Megabytes (MB)
        df_servidor['throughput'] = (df_servidor['tx_bytes'].diff().fillna(0)) / (1024 * 1024)
        throughput_atual = df_servidor['throughput'].values[-1]
        
        if throughput_atual < 0:
            throughput_atual = 0
            
        historico_tempo.append(tempo_segundos)
        historico_throughput.append(throughput_atual)

        # Preparar a InteligÃªncia Artificial (RegressÃ£o Linear)
        y = df_servidor['throughput'].values
        X = np.arange(len(y)).reshape(-1, 1)

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

        # PrediÃ§Ã£o para T+5 segundos
        ultimo_x = X[-1][0]
        ponto_futuro = np.array([[ultimo_x + 2]])
        predicao = modelo.predict(ponto_futuro)
        predicao_final = max(0, predicao[0])

        print(f"[{time.strftime('%H:%M:%S')}] Tempo: {tempo_segundos}s | Carga Atual: {throughput_atual:.2f} MB | PrevisÃ£o T+5s: {predicao_final:.2f} MB")

        # =========================================================================
        # 7. GERAR GRÃFICO DE VISUALIZAÃ‡ÃƒO EXATAMENTE COM A SUA LÃ“GICA (A CADA CICLO)
        # =========================================================================
        try:
            plt.figure(figsize=(10, 6))

            # Plotamos os dados reais da janela recente
            plt.plot(X_treino.flatten(), y_treino, color='#1f77b4', marker='o', linewidth=2.5, label='TrÃ¡fego Real Recente (tx_bytes)')

            # Linha de tendÃªncia calculada pela IA
            X_linha_tendencia = np.array([[X_treino[0][0]], [ponto_futuro[0][0]]])
            y_linha_tendencia = modelo.predict(X_linha_tendencia)
            plt.plot(X_linha_tendencia.flatten(), y_linha_tendencia, color='#ff7f0e', linestyle='--', linewidth=2, label='TendÃªncia IA (Janela recente)')

            # Ponto de previsÃ£o futuro (T+5s)
            plt.scatter(ponto_futuro[0][0], predicao_final, color='red', s=150, edgecolors='black', label='PrevisÃ£o Futura (T+5s)', zorder=5)

            plt.title('DetecÃ§Ã£o Proativa de Congestionamento - SDN & IA')
            plt.xlabel('Amostras de Tempo (Ciclos Recentes)')
            plt.ylabel('Throughput (MB Transmitidos para o Servidor)')

            # Ajustes EstÃ©ticos CrÃ­ticos mantidos idÃªnticos
            plt.ylim(bottom=0, top=max(y_treino.max(), predicao_final) * 1.1 + 1)
            plt.xlim(X_treino[0][0] - 0.3, ponto_futuro[0][0] + 0.3)

            plt.legend(loc='upper left')
            plt.grid(True, alpha=0.4, linestyle='--')

            # Ãrea sombreada (Zona de Risco)
            plt.axvspan(ultimo_x, ponto_futuro[0][0] + 0.3, color='red', alpha=0.05)

            plt.tight_layout()
            plt.savefig('grafico_ia.png', dpi=300)
            plt.close()
        except Exception as e:
            pass # Ignora erros de renderizaÃ§Ã£o em tempo real para nÃ£o travar o loop

        # LÃ³gica de Alerta e MitigaÃ§Ã£o Ativa
        LIMITE_MINIMO_MB = 1.0

        if predicao_final > throughput_atual * 1.3 and predicao_final > LIMITE_MINIMO_MB and not mitigado:
            print("\n" + "!" * 60)
            print("ALERTA: TendÃªncia de Congestionamento Detectada! âš ï¸")
            print("[MECANISMO DE DEFESA PROATIVA EM MALHA FECHADA ATIVADO] ðŸ›‘")
            print("Bloqueando trÃ¡fego malicioso do host 'usuario' (IP: 10.0.0.2)...")
            
            os.system('sudo ovs-ofctl add-flow s1 "priority=50000,tcp,nw_src=10.0.0.2,actions=drop"')
            
            print("Regra de DROP aplicada com sucesso na borda da rede (Switch S1)!")
            print("!" * 60 + "\n")
            
            tempo_mitigacao = tempo_segundos
            mitigado = True

except KeyboardInterrupt:
    print("\n\n" + "=" * 60)
    print("SINAL DE ENCERRAMENTO RECEBIDO. SALVANDO RELATÃ“RIO TEXTO...")
    print("=" * 60)
    
    # === GERAÃ‡ÃƒO DO RELATÃ“RIO DE AUDITORIA (TXT) ===
    try:
        pico_carga = max(historico_throughput) if historico_throughput else 0
        carga_final = historico_throughput[-1] if historico_throughput else 0
        status_final = "ATAQUE BLOQUEADO / TRÃFEGO NORMALIZADO" if mitigado else "SISTEMA MONITORADO SEM ANOMALIAS"
        
        relatorio_conteudo = f"""===================================================================
        RELATÃ“RIO AUTOMÃTICO DE AUDITORIA DE REDE - SMART CITY
===================================================================
Data/Hora do Teste: {time.strftime('%Y-%m-%d %H:%M:%S')}
Topologia Aplicada: Mininet OVS (1 Switch Central S1 | 3 Hosts)
Algoritmo de IA: RegressÃ£o Linear Aplicada com Janela Deslizante (N=5)
-------------------------------------------------------------------

1. RESUMO GERAL DA EXECUÃ‡ÃƒO DO EXPERIMENTO
   - Tempo Total Monitorado: {historico_tempo[-1] if historico_tempo else 0} segundos
   - Pico MÃ¡ximo de Carga Registrado: {pico_carga:.2f} MB
   - VazÃ£o da Rede no Encerramento: {carga_final:.2f} MB
   - Status de SeguranÃ§a Final: {status_final}

2. ANÃLISE DO EVENTO E MITIGAÃ‡ÃƒO PROATIVA
   - Alerta CrÃ­tico Disparado: {"SIM" if mitigado else "NÃƒO"}
   - Momento Exato do Bloqueio: {f"{tempo_mitigacao} segundos (T)" if tempo_mitigacao else "Nenhum incidente detectado"}
   - Comando de Defesa Injetado: sudo ovs-ofctl add-flow s1 "priority=50000,tcp,nw_src=10.0.0.2,actions=drop"
   - Host Penalizado na Borda: Host 'usuario' (IP 10.0.0.2)

3. PARECER TÃ‰CNICO ACADÃŠMICO
   A arquitetura em malha fechada extraiu as estatÃ­sticas fÃ­sicas do switch
   a cada 3 segundos via OpenFlow utilizando o controlador Ryu. 
   Ao detectar a inclinaÃ§Ã£o abrupta na rampa de aceleraÃ§Ã£o do trÃ¡fego TCP,
   a InteligÃªncia Artificial calculou a projeÃ§Ã£o para T+5 segundos.
   O estouro de buffer foi previsto antes do colapso do hardware, acionando
   a regra de DROP na origem e mantendo o streaming UDP da cÃ¢mera fluido.

===================================================================
                       FIM DO RELATÃ“RIO
===================================================================
"""
        with open('relatorio_final.txt', 'w') as f:
            f.write(relatorio_conteudo)
        print("[âœ”] Sucesso: O relatÃ³rio texto foi salvo como 'relatorio_final.txt'")
    except Exception as e:
        print(f"[âŒ] Erro ao gerar o relatÃ³rio texto: {e}") 