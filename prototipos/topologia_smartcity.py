from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel

def topologia_smartcity():
    setLogLevel('info')

    # Criando a rede ligada ao nosso Ryu
    net = Mininet(controller=RemoteController, switch=OVSKernelSwitch)

    print("*** Adicionando Controlador Ryu")
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653)

    print("*** Adicionando Switch Central (S1)")
    s1 = net.addSwitch('s1')

    print("*** Adicionando Hosts (Conforme Diagrama)")
    # h1 vira câmera (Tráfego Legítimo UDP)
    camera = net.addHost('camera', ip='10.0.0.1') 
    
    # h2 vira usuário (Tráfego Agressivo TCP)
    usuario = net.addHost('usuario', ip='10.0.0.2') 
    
    # h3 vira o servidor de destino (Onde chega o vídeo e o ataque)
    servidor = net.addHost('servidor', ip='10.0.0.3') 

    print("*** Criando Links (Cabos)")
    net.addLink(camera, s1)
    net.addLink(usuario, s1)
    net.addLink(servidor, s1)

    print("*** Iniciando a Rede")
    net.build()
    c0.start()
    s1.start([c0])

    print("*** Abrindo Terminal do Mininet")
    CLI(net)

    print("*** Encerrando a Rede")
    net.stop()

if __name__ == '__main__':
    topologia_smartcity()
