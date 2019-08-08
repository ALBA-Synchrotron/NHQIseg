import weakref
from .constant import State


class NHQChannel:
    """
    NHQ channel, it can be standard or high precision.
    """

    def __init__(self, parent, channel_id):
        self._id = channel_id
        self._parent = weakref.proxy(parent)

    def _tofloat(self, raw_value):
        value_sign = 1
        if raw_value[0] in ['+', '-']:
            if raw_value[0] == '-':
                value_sign = -1
            raw_value = raw_value[1:]
        if '-' in raw_value:
            sign = -1
            mantissa, exp = raw_value.split('-')
        elif '+':
            sign = +1
            mantissa, exp = raw_value.split('+')
        value = value_sign * int(mantissa) * pow(10, sign*int(exp))
        return value

    def read_cmd(self, cmd):
        cmd = '{}{}'.format(cmd, self._id)
        ans = self._parent.send_cmd(cmd)
        raw_value = ans.split('\r\n')[1]
        return raw_value

    def write_cmd(self, cmd, value):
        cmd = '{}{}={}'.format(cmd, self._id, value)
        ans = self._parent.send_cmd(cmd)
        # The HW can answer in two ways:
        #   1) D1=40\r\n\r\n
        #   2) D1\r\n40\r\n
        if '=' in ans:
            raw_value = ans.strip().split('=')[1]
        else:
            raw_value = ans.split('\r\n')[1]
        return raw_value

    def write_int(self, cmd, value):
        value = int(value)
        raw_value = self.write_cmd(cmd, value)
        read_value = int(raw_value)
        if read_value != value:
            msg = 'Value in power supply is not equal to the value ' \
                  'set {} != {}'.format(read_value, value)
            raise RuntimeError(msg)

    def write_float(self, cmd, value):
        str_value = '{:4.2f}'.format(value)
        value = float(str_value)
        raw_value = self.write_cmd(cmd, str_value)
        read_value = float(raw_value)
        if read_value != value:
            msg = 'Value in power supply is not equal to the value ' \
                  'set {} != {}'.format(read_value, value)
            raise RuntimeError(msg)

    @property
    def voltage(self):
        raw_value = self.read_cmd('U')
        if self._parent.is_high_precision():
            value = self._tofloat(raw_value)
        else:
            value = int(raw_value)
        return value

    @property
    def set_voltage(self):
        raw_value = self.read_cmd('D')
        if self._parent.is_high_precision():
            value = self._tofloat(raw_value)
        else:
            value = int(raw_value)
        return value

    @set_voltage.setter
    def set_voltage(self, voltage):
        if voltage > self._parent.max_voltage:
            raise ValueError('Maximum voltage '
                             '{}'.format(self._parent.max_voltage))
        if self._parent.is_high_precision():
            self.write_float('D', voltage)
        else:
            self.write_int('D', voltage)

    @property
    def current(self):
        """
        Return the measured current value in Ampere
        :return:
        """
        raw_value = self.read_cmd('I')
        return self._tofloat(raw_value)

    @property
    def ramp_speed(self):
        """
        Return the ramp speed in V/s.
        :return:
        """
        raw_value = self.read_cmd('V')
        return  int(raw_value)

    @ramp_speed.setter
    def ramp_speed(self, value):
        """
        Set the ramp speed in V/s, it can change from 2 V/s to 255 V/s
        :param value:
        """
        if not 2 <= value <= 255:
            raise ValueError('The value must be between 2 and 255')
        self.write_int('V', value)

    @property
    def auto_start(self):
        """
        Read auto start state
        :return:
        """
        raw_value = self.read_cmd('A')
        value = int(raw_value)
        if value == 0:
            return False
        elif value == 8:
            return True
        else:
            raise RuntimeError('Unknown value {}'.format(raw_value))

    @auto_start.setter
    def auto_start(self, value):
        """
        Set auto start state
        :param value:
        :return:
        """
        if self.auto_start == value:
            return
        if value is True:
            value = 8
        else:
            value = 0
        self.write_int('A', value)

    @property
    def state(self):
        raw_value = self.read_cmd('S')
        raw_state = raw_value.split('=')[1].strip()
        return State.from_str(raw_state)

    @property
    def current_trip(self):
        raw_value = self.read_cmd('L')
        if self._parent.is_high_precision():
            value = self._tofloat(raw_value)
        else:
            value = int(raw_value)
        return value

    @current_trip.setter
    def current_trip(self, value):
        self.write_int('L', value)

    @property
    def voltage_limit(self):
        """
        Return the voltage limit in V.
        :return:
        """
        raw_value = self.read_cmd('M')
        value = int(raw_value) * self._parent.max_voltage / 100
        return value

    @property
    def current_limit(self):
        """
        Return the current limit in A.
        :return:
        """
        raw_value = self.read_cmd('N')
        value = int(raw_value) * self._parent.max_current / 100
        return value

    def start(self):
        raw_value = self._parent.send_cmd('G{}'.format(self._id))
        raw_state = raw_value.split('=')[1].strip()
        return State.from_str(raw_state)
