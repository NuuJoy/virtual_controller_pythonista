

import json
import evdev
from nuuJoyLib.Socket.tcpipv4 import server_socket


__version__ = (2021,2,17,'beta')


ds4_events =    {
                evdev.ecodes.EV_ABS:[
                                    (evdev.ecodes.ABS_X,evdev.AbsInfo(value=0,min=-32767,max=32767,fuzz=0,flat=0,resolution=0)),
                                    (evdev.ecodes.ABS_Y,evdev.AbsInfo(value=0,min=-32767,max=32767,fuzz=0,flat=0,resolution=0)),
                                    (evdev.ecodes.ABS_Z,evdev.AbsInfo(value=-32767,min=-32767,max=32767,fuzz=0,flat=0,resolution=0)),
                                    (evdev.ecodes.ABS_RX,evdev.AbsInfo(value=0,min=-32767,max=32767,fuzz=0,flat=0,resolution=0)),
                                    (evdev.ecodes.ABS_RY,evdev.AbsInfo(value=0,min=-32767,max=32767,fuzz=0,flat=0,resolution=0)),
                                    (evdev.ecodes.ABS_RZ,evdev.AbsInfo(value=-32767,min=-32767,max=32767,fuzz=0,flat=0,resolution=0)),
                                    (evdev.ecodes.ABS_HAT0X,evdev.AbsInfo(value=0,min=-32767,max=32767,fuzz=0,flat=0,resolution=0)),
                                    (evdev.ecodes.ABS_HAT0Y,evdev.AbsInfo(value=0,min=-32767,max=32767,fuzz=0,flat=0,resolution=0)),
                                    ],
                evdev.ecodes.EV_KEY:[
                                    evdev.ecodes.BTN_TR2,
                                    evdev.ecodes.BTN_MODE,
                                    evdev.ecodes.BTN_TL2,
                                    evdev.ecodes.BTN_B,
                                    evdev.ecodes.BTN_C,
                                    evdev.ecodes.BTN_A,
                                    evdev.ecodes.BTN_X,
                                    evdev.ecodes.BTN_Y,
                                    evdev.ecodes.BTN_Z,
                                    evdev.ecodes.BTN_TL,
                                    evdev.ecodes.BTN_TR,
                                    evdev.ecodes.BTN_SELECT,
                                    evdev.ecodes.BTN_START,
                                    evdev.ecodes.BTN_THUMBL,
                                    ],
                evdev.ecodes.EV_MSC:[
                                    evdev.ecodes.MSC_SCAN,
                                    ],
                evdev.ecodes.EV_FF:[
                                    evdev.ecodes.FF_RUMBLE,
                                    evdev.ecodes.FF_PERIODIC,
                                    evdev.ecodes.FF_SQUARE,
                                    evdev.ecodes.FF_TRIANGLE,
                                    evdev.ecodes.FF_SINE,
                                    evdev.ecodes.FF_GAIN,
                                    ],
                }


if __name__ == '__main__':
        
    with evdev.UInput(events=ds4_events,
                    name='Sony Computer Entertainment Wireless Controller',
                    vendor=0x54c,
                    product=0x5c4,
                    version=0x111,
                    bustype=0x3,
                    devnode='/dev/uinput',
                    phys='py-evdev-uinput',
                    input_props=None) as vPad:

        with server_socket() as server:
            
            while True:
                client_conn = server.client_accept()
                with client_conn as conn:
                    msgsData = True
                    while msgsData:
                        try:
                            msgsData = server.recv_msgsstrm(conn=conn,timeout=30.0,buff=1024)
                            cmnddict = json.loads(msgsData.data)
                            if cmnddict['name'] == 'left_analog':
                                vPad.write(evdev.ecodes.EV_ABS, evdev.ecodes.ABS_X,round(32767*cmnddict['x']))
                                vPad.write(evdev.ecodes.EV_ABS, evdev.ecodes.ABS_Y,round(-32767*cmnddict['y']))
                            elif cmnddict['name'] == 'right_analog':
                                vPad.write(evdev.ecodes.EV_ABS, evdev.ecodes.ABS_Z,round(32767*cmnddict['x']))
                                vPad.write(evdev.ecodes.EV_ABS, evdev.ecodes.ABS_RZ,round(-32767*cmnddict['y']))
                            elif cmnddict['name'] == 'dpad_x_left':
                                vPad.write(evdev.ecodes.EV_ABS, evdev.ecodes.ABS_HAT0X,-32767*int(cmnddict['press']))
                            elif cmnddict['name'] == 'dpad_x_right':
                                vPad.write(evdev.ecodes.EV_ABS, evdev.ecodes.ABS_HAT0X,32767*int(cmnddict['press']))
                            elif cmnddict['name'] == 'dpad_y_up':
                                vPad.write(evdev.ecodes.EV_ABS, evdev.ecodes.ABS_HAT0Y,-32767*int(cmnddict['press']))
                            elif cmnddict['name'] == 'dpad_y_down':
                                vPad.write(evdev.ecodes.EV_ABS, evdev.ecodes.ABS_HAT0Y,32767*int(cmnddict['press']))
                            elif cmnddict['name'] == 'button_cross':
                                vPad.write(evdev.ecodes.EV_KEY, evdev.ecodes.BTN_SOUTH,int(cmnddict['press']))
                            elif cmnddict['name'] == 'button_circle':
                                vPad.write(evdev.ecodes.EV_KEY, evdev.ecodes.BTN_EAST,int(cmnddict['press']))
                            elif cmnddict['name'] == 'button_square':
                                vPad.write(evdev.ecodes.EV_KEY, evdev.ecodes.BTN_WEST,int(cmnddict['press']))
                            elif cmnddict['name'] == 'button_triangle':
                                vPad.write(evdev.ecodes.EV_KEY, evdev.ecodes.BTN_NORTH,int(cmnddict['press']))
                            elif cmnddict['name'] == 'button_l1':
                                vPad.write(evdev.ecodes.EV_KEY, evdev.ecodes.BTN_TL,int(cmnddict['press']))
                            elif cmnddict['name'] == 'button_r1':
                                vPad.write(evdev.ecodes.EV_KEY, evdev.ecodes.BTN_TR,int(cmnddict['press']))
                            elif cmnddict['name'] == 'button_l2':
                                vPad.write(evdev.ecodes.EV_KEY, evdev.ecodes.BTN_TL2,int(cmnddict['press']))
                            elif cmnddict['name'] == 'button_r2':
                                vPad.write(evdev.ecodes.EV_KEY, evdev.ecodes.BTN_TR2,int(cmnddict['press']))
                            elif cmnddict['name'] == 'button_l3':
                                vPad.write(evdev.ecodes.EV_KEY, evdev.ecodes.BTN_SELECT,int(cmnddict['press']))
                            elif cmnddict['name'] == 'button_r3':
                                vPad.write(evdev.ecodes.EV_KEY, evdev.ecodes.BTN_START,int(cmnddict['press']))
                            elif cmnddict['name'] == 'button_trackpad':
                                vPad.write(evdev.ecodes.EV_KEY, evdev.ecodes.BTN_THUMBL,int(cmnddict['press']))
                            elif cmnddict['name'] == 'button_option':
                                vPad.write(evdev.ecodes.EV_KEY, evdev.ecodes.BTN_C,int(cmnddict['press']))
                            elif cmnddict['name'] == 'button_ps':
                                vPad.write(evdev.ecodes.EV_KEY, evdev.ecodes.BTN_MODE,int(cmnddict['press']))
                            elif cmnddict['name'] == 'button_share':
                                vPad.write(evdev.ecodes.EV_KEY, evdev.ecodes.BTN_Z,int(cmnddict['press']))
                            vPad.syn()
                        except Exception as err:
                            break

