from thinkgear import *

import ouimeaux
from ouimeaux.environment import Environment

def configWemo():
    env = Environment()
    env.start()
    env.discover(3)
    global light
    light = env.get_switch(env.list_switches()[1])
    global onFlag
    onFlag = False
    print(light)

def switchLight():
    light.toggle()
    print 'Light switched'

def main():
    global packet_log
    packet_log = []
    logging.basicConfig(level=logging.WARNING)

    configWemo()

    for pkt in ThinkGearProtocol('/dev/tty.MindWaveMobile-SerialPo').get_packets():
        packet_log.append(pkt)
        for d in pkt:
            if isinstance(d, ThinkGearAttentionData) and d.value > 0:
                print "Attention: %s" % d.value
                global onFlag
                if onFlag == False and d.value > 70:
                    switchLight()
                    onFlag = True
                    print onFlag
                    break
                elif onFlag == True and d.value < 30:
                    switchLight()
                    onFlag = False
                    print onFlag
                    break

if __name__ == '__main__':
    main()
