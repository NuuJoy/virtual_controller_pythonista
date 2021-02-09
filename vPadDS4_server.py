

import time
import json
import uinput
from nuuJoyLib.Socket.tcpipv4 import server_socket


__version__ = (2021,2,9,'beta')


# sudo modprobe uinput, or add 'uinput' to /etc/modules
# todo: orientation, motion
# note: not excluded trackpad, l2_analog, r2_analog, button_l3, button_r3 (yet)


axes_res    =  32767
ds4_mapping =  {'left_analog_x':uinput.ABS_X,
                'left_analog_y':uinput.ABS_Y,
                'right_analog_x':uinput.ABS_Z,
                'right_analog_y':uinput.ABS_RZ,
                'l2_analog':uinput.ABS_RX,
                'r2_analog':uinput.ABS_RY,
                'orientation_roll':uinput.ABS_THROTTLE,
                'orientation_pitch':uinput.ABS_RUDDER,
                'orientation_yaw':uinput.ABS_WHEEL,
                'motion_z':uinput.ABS_DISTANCE,
                'motion_x':uinput.ABS_TILT_X,
                'motion_y':uinput.ABS_TILT_Y,
                'dpad_x':uinput.ABS_HAT0X,
                'dpad_y':uinput.ABS_HAT0Y,
                'button_options':uinput.BTN_TR2,
                'button_ps':uinput.BTN_MODE,
                'button_share':uinput.BTN_TL2,
                'button_cross':uinput.BTN_B,
                'button_circle':uinput.BTN_C,
                'button_square':uinput.BTN_A,
                'button_triangle':uinput.BTN_X,
                'button_l1':uinput.BTN_Y,
                'button_r1':uinput.BTN_Z,
                'button_l2':uinput.BTN_TL,
                'button_r2':uinput.BTN_TR,
                'button_l3':uinput.BTN_SELECT,
                'button_r3':uinput.BTN_START,
                'button_trackpad':uinput.BTN_THUMBL,}


if __name__ == '__main__':
    
    events = [val for val in ds4_mapping.values()]
    with uinput.Device(events) as device, server_socket() as server:
        while True:
            client_conn = server.client_accept()
            with client_conn as conn:
                dpadstack = 0
                while True:
                    try:
                        msgsData = server.recv_msgsstrm(conn=conn,timeout=30.0,buff=2048)
                        if msgsData:
                            cmnddict = json.loads(msgsData.data)
                            if cmnddict['name'] == 'left_analog':
                                device.emit(uinput.ABS_X, round(axes_res*cmnddict['x']), syn=False)
                                device.emit(uinput.ABS_Y, round(axes_res*cmnddict['y']))
                            elif cmnddict['name'] == 'right_analog':
                                device.emit(uinput.ABS_Z,  round(axes_res*cmnddict['x']), syn=False)
                                device.emit(uinput.ABS_RZ, round(axes_res*cmnddict['y']))
                            elif cmnddict['name'] == 'button_cross':
                                device.emit(uinput.BTN_B, int(cmnddict['press']))
                            elif cmnddict['name'] == 'button_circle':
                                device.emit(uinput.BTN_C, int(cmnddict['press']))
                            elif cmnddict['name'] == 'button_square':
                                device.emit(uinput.BTN_A, int(cmnddict['press']))
                            elif cmnddict['name'] == 'button_triangle':
                                device.emit(uinput.BTN_X, int(cmnddict['press']))
                            elif cmnddict['name'] == 'dpad_y_up':
                                if cmnddict['press']:
                                    device.emit(uinput.ABS_HAT0Y, axes_res)
                                else:
                                    device.emit(uinput.ABS_HAT0Y, 0)
                            elif cmnddict['name'] == 'dpad_y_down':
                                if cmnddict['press']:
                                    device.emit(uinput.ABS_HAT0Y, -axes_res)
                                else:
                                    device.emit(uinput.ABS_HAT0Y, 0)
                            elif cmnddict['name'] == 'dpad_x_left':
                                if cmnddict['press']:
                                    device.emit(uinput.ABS_HAT0X, -axes_res)
                                else:
                                    device.emit(uinput.ABS_HAT0X, 0)
                            elif cmnddict['name'] == 'dpad_x_right':
                                if cmnddict['press']:
                                    device.emit(uinput.ABS_HAT0X,  axes_res)
                                else:
                                    device.emit(uinput.ABS_HAT0X, 0)
                            elif cmnddict['name'] == 'button_l1':
                                device.emit(uinput.BTN_Y, int(cmnddict['press']))
                            elif cmnddict['name'] == 'button_l2':
                                device.emit(uinput.BTN_TL, int(cmnddict['press']))
                            elif cmnddict['name'] == 'button_r1':
                                device.emit(uinput.BTN_Z, int(cmnddict['press']))
                            elif cmnddict['name'] == 'button_r2':
                                device.emit(uinput.BTN_TR, int(cmnddict['press']))
                            elif cmnddict['name'] == 'button_ps':
                                device.emit(uinput.BTN_MODE, int(cmnddict['press']))
                            elif cmnddict['name'] == 'button_option':
                                device.emit(uinput.BTN_TR2, int(cmnddict['press']))
                            elif cmnddict['name'] == 'button_share':
                                device.emit(uinput.BTN_TL2, int(cmnddict['press']))
                        else:
                            break
                    except Exception as err:
                        break

