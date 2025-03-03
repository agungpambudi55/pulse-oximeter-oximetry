'''
Created on Apr 2019

Contributor :
- Agung Pambudi <agung.pambudi5595@gmail.com>
- Azman Latif <azman.latif@mail.ugm.ac.id>
- Imam Syuhada <imam.sy11@gmail.com>
'''

import pygatt

#import logging
#logging.basicConfig()
#logging.getLogger('pygatt').setLevel(logging.DEBUG)

def handleData(handle, value):
    if len(value) == 4:
        spo2 = abs(value[2])
        pr = abs(value[1])
        pi = abs(value[3]) / float(10)
                                            
        if spo2 == 127 and pr == 127 and pi == 0:
            print('Finger out')
        else:
            print('SpO2 {} % , PR {} bpm , PI {} %'.format(spo2,pr,pi))

        
try:
    adapter = pygatt.GATTToolBackend(hci_device='hci0')
    adapter.start()

    for discover in adapter.scan(run_as_root=True, timeout=5):
        if discover['name'] == 'Medical':
            try:
                print('Device found, try to connect with device')
                device = adapter.connect(discover['address'])
                print('Connected with device')

                while True:
                    device.subscribe('0000fee1-0000-1000-8000-00805f9b34fb', callback=handleData)
                    
            except KeyboardInterrupt:
                print('Terminate')
            except:
                print('Failed to connect with device')
            finally:
                device.disconnect()
                
except KeyboardInterrupt:
    print('Terminate')
except:
    print('Something went wrong with adapter')
finally:
    adapter.stop()