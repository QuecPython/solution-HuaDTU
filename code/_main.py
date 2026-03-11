import sim
import osTimer
from machine import Pin
from usr import network
from usr.dtu import DTU
import dataCall
from misc import Power

class Manager(object):

    def __init__(self, dog_gpio=Pin.GPIO12):
        self.dog_pin = Pin(dog_gpio, Pin.OUT, Pin.PULL_DISABLE, 1)
        self.dog_feed_timer = osTimer()

        self.dtu = DTU('Quectel')
        self.dtu.config.read_from_json('/usr/dtu_config.json')

    def start(self):
        self.dog_feed_timer.start(3000, 1, self.__feed)
        if sim.getStatus() != 1:
            raise ValueError("sim card not ready")
        
        self.__config_apn()

        # 网络就绪
        network.wait_network_ready()
        # dtu应用启动
        self.dtu.run()

    def __feed(self, args):
        if self.dog_pin.read():
            self.dog_pin.write(0)
        else:
            self.dog_pin.write(1)

    def __config_apn(self):

        usr_apn = self.dtu.config.get('apn', '')          # APN名称
        usr_user = self.dtu.config.get('apn_user', '')    # 用户名，可选
        usr_pwd = self.dtu.config.get('apn_password', '') # 密码，可选

        if usr_apn:
            print("检测到用户APN配置，准备设置...")
            profile_id = 1  # 通常使用第一路
            ip_type = 0     # 默认IPv4，可根据需要从配置读取

            pdp_ctx = dataCall.getPDPContext(profile_id)
            if pdp_ctx != -1:
                current_apn = pdp_ctx[1]  # 元组索引1为apn
                if current_apn != usr_apn:
                    ret = dataCall.setPDPContext(
                        profile_id,
                        ip_type,
                        usr_apn,
                        usr_user,
                        usr_pwd,
                        0  # authType，0表示无鉴权
                    )
                    if ret == 0:
                        print("APN配置成功，模组即将重启...")
                        self.dog_feed_timer.stop()
                        Power.powerRestart()
                    else:
                        print("APN配置失败，将使用默认APN尝试拨号")
                else:
                    print("APN已正确配置，无需修改")
            else:
                print("获取PDP Context失败，无法配置APN")
        else:
            print("未检测到用户APN配置，使用默认APN")


if __name__ == "__main__":
    manager = Manager()
    manager.start()
