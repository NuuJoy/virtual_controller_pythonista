

import time
import json
from nuuJoyLib.Pythonista.touchpad import touchGamePad
from nuuJoyLib.Pythonista.sensor import motion_sensor
from nuuJoyLib.Socket.tcpipv4 import client_socket
from nuuJoyLib.HWCtrl.acquisition import constantRateAcquisition


__version__ = (2021,2,9,'beta')


#server_address = ('172.20.10.9',13666)
server_address = ('192.168.254.118',13666)
enable_imu_sensor = True


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

    ds4pad = touchGamePad('ds4')

    ds4pad.override_extfunc('dpad_y_up','touchbegan_extfunc',scktjson.send_event)
    ds4pad.override_extfunc('dpad_y_up','touchended_extfunc',scktjson.send_event)
    ds4pad.override_extfunc('dpad_y_down','touchbegan_extfunc',scktjson.send_event)
    ds4pad.override_extfunc('dpad_y_down','touchended_extfunc',scktjson.send_event)
    ds4pad.override_extfunc('dpad_x_left','touchbegan_extfunc',scktjson.send_event)
    ds4pad.override_extfunc('dpad_x_left','touchended_extfunc',scktjson.send_event)
    ds4pad.override_extfunc('dpad_x_right','touchbegan_extfunc',scktjson.send_event)
    ds4pad.override_extfunc('dpad_x_right','touchended_extfunc',scktjson.send_event)
    ds4pad.override_extfunc('button_cross','touchbegan_extfunc',scktjson.send_event)
    ds4pad.override_extfunc('button_cross','touchended_extfunc',scktjson.send_event)
    ds4pad.override_extfunc('button_circle','touchbegan_extfunc',scktjson.send_event)
    ds4pad.override_extfunc('button_circle','touchended_extfunc',scktjson.send_event)
    ds4pad.override_extfunc('button_square','touchbegan_extfunc',scktjson.send_event)
    ds4pad.override_extfunc('button_square','touchended_extfunc',scktjson.send_event)
    ds4pad.override_extfunc('button_triangle','touchbegan_extfunc',scktjson.send_event)
    ds4pad.override_extfunc('button_triangle','touchended_extfunc',scktjson.send_event)
    ds4pad.override_extfunc('button_l1','touchbegan_extfunc',scktjson.send_event)
    ds4pad.override_extfunc('button_l1','touchended_extfunc',scktjson.send_event)
    ds4pad.override_extfunc('button_l2','touchbegan_extfunc',scktjson.send_event)
    ds4pad.override_extfunc('button_l2','touchended_extfunc',scktjson.send_event)
    ds4pad.override_extfunc('button_r1','touchbegan_extfunc',scktjson.send_event)
    ds4pad.override_extfunc('button_r1','touchended_extfunc',scktjson.send_event)
    ds4pad.override_extfunc('button_r2','touchbegan_extfunc',scktjson.send_event)
    ds4pad.override_extfunc('button_r2','touchended_extfunc',scktjson.send_event)
    ds4pad.override_extfunc('button_option','touchbegan_extfunc',scktjson.send_event)
    ds4pad.override_extfunc('button_option','touchended_extfunc',scktjson.send_event)
    ds4pad.override_extfunc('button_ps','touchbegan_extfunc',scktjson.send_event)
    ds4pad.override_extfunc('button_ps','touchended_extfunc',scktjson.send_event)
    ds4pad.override_extfunc('button_share','touchbegan_extfunc',scktjson.send_event)
    ds4pad.override_extfunc('button_share','touchended_extfunc',scktjson.send_event)
    ds4pad.override_extfunc('left_analog','touchbegan_extfunc',scktjson.send_event)
    ds4pad.override_extfunc('left_analog','touchmoved_extfunc',scktjson.send_event)
    ds4pad.override_extfunc('left_analog','touchended_extfunc',scktjson.send_event)
    ds4pad.override_extfunc('right_analog','touchbegan_extfunc',scktjson.send_event)
    ds4pad.override_extfunc('right_analog','touchmoved_extfunc',scktjson.send_event)
    ds4pad.override_extfunc('right_analog','touchended_extfunc',scktjson.send_event)

    ds4pad.run()


    while not(ds4pad.stop_event.is_set()):
        print('connecting to server ...')
        try:
            with client_socket(*server_address) as client:
                scktjson.client = client
                while client.conn_status() and not(ds4pad.stop_event.is_set()):
                    if enable_imu_sensor:
                        with motion_sensor() as sensor:
                            def emit_attitude():
                                scktjson.send_event('attitude',{'name':'imu_sensor','roll':sensor.attitude['roll'],
                                                                                    'pitch':sensor.attitude['pitch'],
                                                                                    'yaw':sensor.attitude['yaw']})
                            dataAcqs = constantRateAcquisition(func_list=(emit_attitude,),output_list=(None,),
                                                            rate_limit=50,stop_event=ds4pad.stop_event)
                            dataAcqs.start_acquiring()
                    time.sleep(1.0)
                scktjson.client = socketjsonput.fake_client()
        except Exception as err:
            print('Exception: ',err)
            scktjson.client = socketjsonput.fake_client()
        time.sleep(1.0)
            
    print('terminate.')

