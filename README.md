# SDN Smart City com IA Preditiva
Este projeto utiliza o controlador **Ryu** e o simulador **Mininet** para monitorar o tráfego de uma rede de Smart City.
Utilizamos **Regressão Linear (Scikit-Learn)** para prever congestionamentos com 5 segundos de antecedência.

## Como rodar
1. Inicie a topologia: `sudo python3 topologia_smartcity.py`
2. Inicie o controlador: `ryu-manager coletor_dados.py`
3. Execute a IA: `python3 treinar_ia.py`
