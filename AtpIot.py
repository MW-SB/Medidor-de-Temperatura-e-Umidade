import dht
import machine
import time
from wifi_lib import conecta
import urequests

d = dht.DHT11(machine.Pin(4))
r = machine.Pin(4, machine.Pin.OUT)

while True:
    d.measure()
    dt = d.temperature()
    dh = d.humidity()
    if(dt > 31 or dh < 70):
        print('Temperatura: {}°'.format(dt))
        print('Umidade: {}%'.format(dh))
        print('Estabelecendo conexão com a internet, aguarde um momento.')
        station = conecta('Pedreira02', 'Pedreira02')
        if not station.isconnected():
            print('Desculpe, houve uma falha na conexão.')
            print('As informações de temperatura e humidade não serão transmitidas ao servidor')
        else:
            response = urequests.get("http://api.thingspeak.com/update?api_key=5UL30VA6BII1CXPI&field1={}&field2={}".format(dt, dh))
            print('As informações foram enviadas com sucesso.')
    else:
        print('As condições do ambiente não permitirão que sejam feitas a leitura de temperatura e humidade.')
        r.value(0)