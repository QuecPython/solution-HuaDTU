import sim
import osTimer
from machine import Pin
from usr import network
from usr.dtu import DTU


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
        # 网络就绪
        network.wait_network_ready()
        # dtu应用启动
        self.dtu.run()

    def __feed(self, args):
        if self.dog_pin.read():
            self.dog_pin.write(0)
        else:
            self.dog_pin.write(1)


if __name__ == "__main__":
    manager = Manager()
    manager.start()
