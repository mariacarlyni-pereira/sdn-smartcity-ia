import csv
import time
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub
from ryu.app import simple_switch_13

class ColetorDados(simple_switch_13.SimpleSwitch13):
    def __init__(self, *args, **kwargs):
        super(ColetorDados, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self._monitor)
        
        # Criando/Limpando o arquivo CSV e colocando o cabeçalho
        with open('dataset_smartcity.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'switch_id', 'porta', 'tx_bytes', 'rx_bytes', 'tx_pacotes', 'rx_pacotes'])

    @set_ev_cls(ofp_event.EventOFPStateChange, [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                self.logger.info('*** Switch conectado: %016x', datapath.id)
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.info('*** Switch desconectado: %016x', datapath.id)
                del self.datapaths[datapath.id]

    def _monitor(self):
        while True:
            for dp in self.datapaths.values():
                self._request_stats(dp)
            hub.sleep(3) # A cada 3 segundos ele extrai os dados

    def _request_stats(self, datapath):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        # Pedindo estatísticas das portas
        req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
        datapath.send_msg(req)

    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    def _port_stats_reply_handler(self, ev):
        body = ev.msg.body
        agora = time.strftime('%Y-%m-%d %H:%M:%S')
        
        with open('dataset_smartcity.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            for stat in sorted(body, key=lambda stat: stat.port_no):
                # Ignorando a porta 'local' do switch para não sujar os dados
                if stat.port_no != ev.msg.datapath.ofproto.OFPP_LOCAL:
                    writer.writerow([agora, ev.msg.datapath.id, stat.port_no,
                                     stat.tx_bytes, stat.rx_bytes,
                                     stat.tx_packets, stat.rx_packets])
