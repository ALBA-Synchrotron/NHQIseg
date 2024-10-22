
from tango import DevState, AttReqType
from tango.server import Device, attribute, device_property, command
from ..constant import Models, State
from ..controller import NHQPowerSupply
import logging


class NHQIseg(Device):

    model = device_property(dtype=str, doc='NHQ_xxxx model e.g.: NHQ_202M')
    url = device_property(dtype=str, doc='See serialio documentation')
    auto_start = device_property(dtype=bool, doc='Activate the auto start')
    nhq = None
    library_debug = device_property(dtype=bool, default_value=False)

    def init_device(self):
        Device.init_device(self)
        self.info_stream('Connecting to NHQ model: {} '
                         'url: {}'.format(self.model, self.url))
        model = Models.from_str(self.model)
        if self.library_debug:
            logging.basicConfig(level=logging.DEBUG)
        self.nhq = NHQPowerSupply(self.url, model)
        for i in range(1, self.nhq.channels+1):
            ch = {1: 'A', 2: 'B'}[i]
            self.nhq[i].auto_start = self.auto_start
            self.info_stream('Set Channel{} auto_start: '
                             '{}'.format(ch, self.auto_start))

    def always_executed_hook(self):
        status = ''
        states = []
        for i in range(1, self.nhq.channels + 1):
            state = self.nhq[i].state
            ch = {1: 'A', 2: 'B'}[i]
            msg = 'Channel{} state {}.' \
                  '\n'.format(ch, State.means(state))
            status += msg
            states.append(state)
            msg = msg.replace('\n', '')
            self.info_stream(msg)
        self.set_status(status)
        if State.L2H in states or State.H2L in states:
            self.set_state(DevState.RUNNING)
        elif set(states) in [{State.OFF}, {State.MAN}]:
            self.set_state(DevState.FAULT)
        elif State.OFF in states or State.MAN in states \
                or State.ERR in states or State.INH in states \
                or State.QUA in states:
            self.set_state(DevState.ALARM)
        else:
            self.set_state(DevState.ON)

    def read_attribute(self, attr, channel):
        try:
            return self.nhq[channel].__getattribute__(attr)
        except KeyError:
            raise ValueError('Model {} has only channel A'.format(self.model))

    def write_attribute(self, attr, channel, value):
        try:
            setattr(self.nhq[channel], attr, value)
        except KeyError:
            raise ValueError('Model {} has only channel A'.format(self.model))

    def is_write_allow(self, req_type):
        if req_type == AttReqType.READ_REQ:
            return True
        else:
            return self.get_state() != DevState.FAULT

    @attribute(name="currentA", unit="A", dtype=float)
    def current_a(self):
        return self.read_attribute('current', 1)

    @attribute(name="currentB", unit="A", dtype=float)
    def current_b(self):
        return self.read_attribute('current', 2)

    @attribute(name="voltageA", unit="V", dtype=float)
    def voltage_a(self):
        return self.read_attribute('voltage', 1)

    @voltage_a.write
    def voltage_a(self, value):
        return self.write_attribute('set_voltage', 1, value)

    @attribute(name="voltageB", unit="V", dtype=float)
    def voltage_b(self):
        return self.read_attribute('voltage', 2)

    @voltage_b.write
    def voltage_b(self, value):
        return self.write_attribute('set_voltage', 2, value)

    @attribute(name="rampSpeedA", unit="V/s", dtype=int, min_value=2,
               max_value=255, fisallowed='is_write_allow')
    def ramp_speed_a(self):
        return self.read_attribute('ramp_speed', 1)

    @ramp_speed_a.write
    def ramp_speed_a(self, value):
        return self.write_attribute('ramp_speed', 1, value)

    @attribute(name="rampSpeedB", unit="V/s", dtype=int, min_value=2,
               max_value=255, fisallowed='is_write_allow')
    def ramp_speed_b(self):
        return self.read_attribute('ramp_speed', 2)

    @ramp_speed_b.write
    def ramp_speed_b(self, value):
        return self.write_attribute('ramp_speed', 2, value)

    @attribute(name="maxVoltageA", unit="V", dtype=float)
    def voltage_limit_a(self):
        return self.read_attribute('voltage_limit', 1)

    @attribute(name="maxVoltageB", unit="V", dtype=float)
    def voltage_limit_b(self):
        return self.read_attribute('voltage_limit', 2)

    @attribute(name="maxCurrentA", unit="A", dtype=float)
    def current_limit_a(self):
        return self.read_attribute('current_limit', 1)

    @attribute(name="maxCurrentB", unit="A", dtype=float)
    def current_limit_b(self):
        return self.read_attribute('current_limit', 2)

    @command()
    def restore_voltage(self):
        for channel in self.nhq:
            channel.start()


def main():
    NHQIseg.run_server()


if __name__ == "__main__":
    main()
