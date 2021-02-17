

import time
import json
from nuuJoyLib.Pythonista.touchpad import MousePad
from nuuJoyLib.Socket.tcpipv4 import client_socket


__version__ = (2021,2,17,'beta')


server_address = ('172.20.10.9',13666)


class socketjsonput():
    class fake_client():
        def send_msgs(self,*args,**kwargs):
            pass
    def __init__(self,client=None):
        self.client = self.fake_client() if client is None else client
    def send_event(self,action,state):
        msgstext = json.dumps({**{'action':action},**state})
        self.client.send_msgs(msgstext.encode())
        

if __name__ == '__main__':

    scktjson = socketjsonput()
    mousepad = MousePad()

    mousepad.override_extfunc('right_bttn','touchbegan_extfunc',scktjson.send_event)
    mousepad.override_extfunc('right_bttn','touchended_extfunc',scktjson.send_event)
    mousepad.override_extfunc('drag_bttn','toggle_on_extfunc',scktjson.send_event)
    mousepad.override_extfunc('drag_bttn','toggle_off_extfunc',scktjson.send_event)
    mousepad.override_extfunc('left_bttn','touchbegan_extfunc',scktjson.send_event)
    mousepad.override_extfunc('left_bttn','touchended_extfunc',scktjson.send_event)
    mousepad.override_extfunc('rectpad','touchbegan_extfunc',scktjson.send_event)
    mousepad.override_extfunc('rectpad','touchmoved_extfunc',scktjson.send_event)
    mousepad.override_extfunc('rectpad','touchended_extfunc',scktjson.send_event)

    mousepad.run()


    while not(mousepad.stop_event.is_set()):
        print('connecting to server ...')
        try:
            with client_socket(*server_address) as client:
                scktjson.client = client
                while client.conn_status() and not(mousepad.stop_event.is_set()):
                    time.sleep(1.0)
                scktjson.client = socketjsonput.fake_client()
        except Exception as err:
            print('Exception: ',err)
            scktjson.client = socketjsonput.fake_client()
        time.sleep(1.0)
            
    print('terminate.')

