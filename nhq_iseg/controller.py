from .communication import NHQComm
from .channel import NHQChannel
from .constant import Specs


class NHQPowerSupply:
    """
    Class controller of the power supply it can have one or two channels.
    It is based on serial communication.
    """

    def __init__(self, port, model):
        self.model = model
        wait_time = 0
        if Specs.is_high_precision(model):
            wait_time = 200
        self.com = NHQComm(port, wait_time)
        self._channels = {}
        for i in range(1, self.channels+1):
            self._channels[i] = NHQChannel(self, i)

    def __getitem__(self, item):
        if item not in self._channels:
            raise ValueError('Bad channel value')
        return self._channels[item]

    def send_cmd(self, cmd):
        return self.com.send_cmd(cmd)

    @property
    def max_voltage(self):
        return Specs.max_voltage(self.model)

    @property
    def max_current(self):
        return Specs.max_current(self.model)

    @property
    def channels(self):
        return Specs.channels(self.model)

    def is_high_precision(self):
        return Specs.is_high_precision(self.model)
