

import pyautogui
import json
import evdev
from nuuJoyLib.Socket.tcpipv4 import server_socket


__version__ = (2021,2,17,'beta')


mouse_events =  {
                evdev.ecodes.EV_REL:[
                                    evdev.ecodes.REL_X,
                                    evdev.ecodes.REL_Y,
                                    evdev.ecodes.REL_WHEEL,
                                    ],
                evdev.ecodes.EV_KEY:[
                                    evdev.ecodes.BTN_LEFT,
                                    evdev.ecodes.BTN_RIGHT,
                                    ],
                }


if __name__ == '__main__':

    sensitivity = 5.0

    last_posx = 0.0
    last_posy = 0.0

    with evdev.UInput(events=mouse_events,
                      name='myCustomMouse',
                      devnode='/dev/uinput',
                      phys='py-evdev-uinput',
                      input_props=None) as vMouse:

        with server_socket() as server:
            
            while True:
                client_conn = server.client_accept()
                with client_conn as conn:
                    msgsData = True
                    while msgsData:
                        try:
                            msgsData = server.recv_msgsstrm(conn=conn,timeout=30.0,buff=1024)
                            cmnddict = json.loads(msgsData.data)
                            print(cmnddict)
                            if cmnddict['name'] == 'rectpad':
                                if cmnddict['action'] == 'touch_began':
                                    last_posx = cmnddict['x']
                                    last_posy = cmnddict['y']
                                elif cmnddict['action'] == 'touch_moved':
                                    vMouse.write(evdev.ecodes.EV_REL, evdev.ecodes.REL_X,int(sensitivity*(cmnddict['x']-last_posx)))
                                    vMouse.write(evdev.ecodes.EV_REL, evdev.ecodes.REL_Y,int(-sensitivity*(cmnddict['y']-last_posy)))
                                    last_posx = cmnddict['x']
                                    last_posy = cmnddict['y']
                            elif cmnddict['name'] == 'left_bttn':
                                if cmnddict['action'] == 'touch_began':
                                    vMouse.write(evdev.ecodes.EV_KEY, evdev.ecodes.BTN_LEFT,1)
                                if cmnddict['action'] == 'touch_ended':
                                    vMouse.write(evdev.ecodes.EV_KEY, evdev.ecodes.BTN_LEFT,0)
                            elif cmnddict['name'] == 'drag_bttn':
                                if cmnddict['action'] == 'toggle_on':
                                    vMouse.write(evdev.ecodes.EV_KEY, evdev.ecodes.BTN_LEFT,1)
                                if cmnddict['action'] == 'toggle_off':
                                    vMouse.write(evdev.ecodes.EV_KEY, evdev.ecodes.BTN_LEFT,0)
                            elif cmnddict['name'] == 'right_bttn':
                                if cmnddict['action'] == 'touch_began':
                                    vMouse.write(evdev.ecodes.EV_KEY, evdev.ecodes.BTN_RIGHT,1)
                                if cmnddict['action'] == 'touch_ended':
                                    vMouse.write(evdev.ecodes.EV_KEY, evdev.ecodes.BTN_RIGHT,0)
                            vMouse.syn()
                        except Exception as err:
                            break

